#!/usr/bin/env python3

# genre_experiment.py

# USAGE syntax:

# python3 main_experiment.py *command*

import sys, os, csv, random
import numpy as np
import pandas as pd
import versatiletrainer2
import metaselector

import matplotlib.pyplot as plt

from scipy import stats

def add2dict(category, key, value):
    if key not in category:
        category[key] = []
    category[key].append(value)

def foldintodict(d1, d2):
    for k, v in d1.items():
        add2dict(d2, k, v)

def reliable_genre_comparisons():

    '''
    This function was used in the current version of the article.

    It addresses weaknesses in earlier versions of genre comparison
    by comparing only models *with no shared instances*.

    [Edit Jan 1: To be even more careful about leakage, make that
    *no shared authors.*]

    Doing that required a ----load of complexity I'm afraid. I have to first
    split each genre into disjoint sets, then create self-comparisons between
    those disjoint sets, as well as cross-comparisons between genres, and then
    finally compare the self-comparisons to the cross-comparisons.
    '''

    outmodels = '../results/reliable_models.tsv'
    outcomparisons = '../results/reliable_comparisons.tsv'
    columns = ['testype', 'name1', 'name2', 'ceiling', 'floor', 'meandate1', 'meandate2', 'acc1', 'acc2', 'alienacc1', 'alienacc2', 'spearman', 'spear1on2', 'spear2on1', 'loss', 'loss1on2', 'loss2on1']

    if not os.path.isfile(outcomparisons):
        with open(outcomparisons, mode = 'a', encoding = 'utf-8') as f:
            scribe = csv.DictWriter(f, delimiter = '\t', fieldnames = columns)
            scribe.writeheader()

    if not os.path.isfile(outmodels):
        with open(outmodels, mode = 'a', encoding = 'utf-8') as f:
            outline = 'name\tsize\tfloor\tceiling\tmeandate\taccuracy\tfeatures\tregularization\ti\n'
            f.write(outline)

    sourcefolder = '../data/'
    sizecap = 72

    c_range = [.00001, .0001, .001, .01, 0.1, 1, 10, 100]
    featurestart = 1500
    featureend = 6500
    featurestep = 300
    modelparams = 'logistic', 15, featurestart, featureend, featurestep, c_range

    master = pd.read_csv('../metadata/mastermetadata.csv', index_col = 'docid')
    periods = [(1800, 1909), (1880, 1924), (1900, 1949), (1910, 1959), (1930, 1969), (1950, 1979), (1970, 1989), (1980, 1999), (1990, 2010)]
    forbiddenwords = {'fantasy', 'fiction', 'science', 'horror'}

    # endpoints both inclusive

    for i in range(15):
        for floor, ceiling in periods:

            split_metadata(master, floor, ceiling, sizecap)

            # That function just above does the real work of preventing leakage,
            # by splitting the genre into two disjoint sets. This allows self-
            # comparisons that avoid shared authors, and are thus strictly
            # comparable to cross-comparisons.

            metaoptions = ['sf1', 'sf2', 'fant1', 'fant2']

            for m in metaoptions:
                metadatapath = '../temp/' + m + '.csv'
                vocabpath = '../lexica/' + m + '.txt'
                name = 'temp_' + m + str(ceiling) + '_' + str(i)

                if m == 'sf1' or m == 'sf2':
                    tags4positive = {'sf_loc', 'sf_oclc', 'sf_bailey'}
                else:
                    tags4positive = {'fantasy_loc', 'fantasy_oclc', 'supernat'}

                tags4negative = {'random', 'randomB'}

                metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist = versatiletrainer2.get_simple_data(sourcefolder, metadatapath, vocabpath, tags4positive, tags4negative, sizecap, excludebelow = floor, excludeabove = ceiling, forbid4positive = {'juv'}, forbid4negative = {'juv'}, force_even_distribution = False, numfeatures = 6500, forbiddenwords = forbiddenwords)

                matrix, maxaccuracy, metadata, coefficientuples, features4max, best_regularization_coef = versatiletrainer2.tune_a_model(metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist, tags4positive, tags4negative, modelparams, name, '../modeloutput/' + name + '.csv')

                meandate = int(round(np.sum(metadata.firstpub) / len(metadata.firstpub)))

                with open(outmodels, mode = 'a', encoding = 'utf-8') as f:
                    outline = name + '\t' + str(sizecap) + '\t' + str(floor) + '\t' + str(ceiling) + '\t' + str(meandate) + '\t' + str(maxaccuracy) + '\t' + str(features4max) + '\t' + str(best_regularization_coef) + '\t' + str(i) + '\n'
                    f.write(outline)

                os.remove(vocabpath)

            r = dict()
            r['testype'] = 'sfself'
            r['ceiling'] = ceiling
            r['floor'] = floor
            r['name1'] = 'temp_sf1' + str(ceiling) + '_' + str(i)
            r['name2'] = 'temp_sf2' + str(ceiling) + '_' + str(i)
            r['spearman'], r['loss'], r['spear1on2'], r['spear2on1'], r['loss1on2'], r['loss2on1'], r['acc1'], r['acc2'], r['alienacc1'], r['alienacc2'], r['meandate1'], r['meandate2'] = get_divergence(r['name1'], r['name2'])
            write_a_row(r, outcomparisons, columns)

            r = dict()
            r['testype'] = 'fantasyself'
            r['ceiling'] = ceiling
            r['floor'] = floor
            r['name1'] = 'temp_fant1' + str(ceiling) + '_' + str(i)
            r['name2'] = 'temp_fant2' + str(ceiling) + '_' + str(i)
            r['spearman'], r['loss'], r['spear1on2'], r['spear2on1'], r['loss1on2'], r['loss2on1'], r['acc1'], r['acc2'], r['alienacc1'], r['alienacc2'], r['meandate1'], r['meandate2'] = get_divergence(r['name1'], r['name2'])
            write_a_row(r, outcomparisons, columns)

            r = dict()
            r['testype'] = 'cross'
            r['ceiling'] = ceiling
            r['floor'] = floor
            r['name1'] = 'temp_sf1' + str(ceiling) + '_' + str(i)
            r['name2'] = 'temp_fant2' + str(ceiling) + '_' + str(i)
            r['spearman'], r['loss'], r['spear1on2'], r['spear2on1'], r['loss1on2'], r['loss2on1'], r['acc1'], r['acc2'], r['alienacc1'], r['alienacc2'], r['meandate1'], r['meandate2'] = get_divergence(r['name1'], r['name2'])
            write_a_row(r, outcomparisons, columns)

            r = dict()
            r['testype'] = 'cross'
            r['ceiling'] = ceiling
            r['floor'] = floor
            r['name1'] = 'temp_sf2' + str(ceiling) + '_' + str(i)
            r['name2'] = 'temp_fant1' + str(ceiling) + '_' + str(i)
            r['spearman'], r['loss'], r['spear1on2'], r['spear2on1'], r['loss1on2'], r['loss2on1'], r['acc1'], r['acc2'], r['alienacc1'], r['alienacc2'], r['meandate1'], r['meandate2'] = get_divergence(r['name1'], r['name2'])
            write_a_row(r, outcomparisons, columns)


def compare_cross_models():
    '''
    Function used in the genredistance project.
    The function assumes that you've already trained the crossmodels,
    and now just need to compare them.
    '''

    files = [x for x in os.listdir('../models') if x.endswith('.pkl')]
    allgenres = list(set([x.split('_')[0] for x in files]))
    print(allgenres)
    outcomparisons = '../results/crosscomparisons.tsv'

    alreadydone = set()
    with open(outcomparisons, encoding = 'utf-8') as f:
        reader = csv.DictReader(f, delimiter = '\t')
        for row in reader:
            g1 = row['name1'].split('_')[0]
            g2 = row['name2'].split('_')[0]
            alreadydone.add((g1, g2))
            alreadydone.add((g2, g1))

    columns = ['testype', 'name1', 'name2', 'ceiling1', 'floor1', 'ceiling2', 'floor2', 'meandate1', 'meandate2', 'acc1', 'acc2', 'alienacc1', 'alienacc2', 'spearman', 'spear1on2', 'spear2on1', 'loss', 'loss1on2', 'loss2on1']

    if not os.path.isfile(outcomparisons):
        with open(outcomparisons, mode = 'a', encoding = 'utf-8') as f:
            scribe = csv.DictWriter(f, delimiter = '\t', fieldnames = columns)
            scribe.writeheader()

    ranA = '_randomA'
    ranB = '_randomB'

    for idx, g1 in enumerate(allgenres):
        for g2 in allgenres[idx + 1: ]:
            if g1 == g2:
                continue
            elif g1.startswith('random') or g2.startswith('random'):
                continue
            elif (g1, g2) in alreadydone:
                print((g1, g2))
                continue
            else:

                r = dict()
                name1 = g1 + ranA
                name2 = g2 + ranB
                r['name1'] = name1
                r['name2'] = name2
                r['testype'] = 'crossAB'
                r['spearman'], r['loss'], r['spear1on2'], r['spear2on1'], r['loss1on2'], r['loss2on1'], r['acc1'], r['acc2'], r['alienacc1'], r['alienacc2'], r['meandate1'], r['meandate2'] = get_divergence(r['name1'], r['name2'])

                write_a_row(r, outcomparisons, columns)

                r = dict()
                name1 = g1 + ranA
                name2 = g1 + ranB
                r['name1'] = name1
                r['name2'] = name2
                r['testype'] = 'self1'
                r['spearman'], r['loss'], r['spear1on2'], r['spear2on1'], r['loss1on2'], r['loss2on1'], r['acc1'], r['acc2'], r['alienacc1'], r['alienacc2'], r['meandate1'], r['meandate2'] = get_divergence(r['name1'], r['name2'])

                write_a_row(r, outcomparisons, columns)

                r = dict()
                name1 = g1 + ranB
                name2 = g2 + ranA
                r['name1'] = name1
                r['name2'] = name2
                r['testype'] = 'crossBA'
                r['spearman'], r['loss'], r['spear1on2'], r['spear2on1'], r['loss1on2'], r['loss2on1'], r['acc1'], r['acc2'], r['alienacc1'], r['alienacc2'], r['meandate1'], r['meandate2'] = get_divergence(r['name1'], r['name2'])

                write_a_row(r, outcomparisons, columns)

                r = dict()
                name1 = g2 + ranA
                name2 = g2 + ranB
                r['name1'] = name1
                r['name2'] = name2
                r['testype'] = 'self2'
                r['spearman'], r['loss'], r['spear1on2'], r['spear2on1'], r['loss1on2'], r['loss2on1'], r['acc1'], r['acc2'], r['alienacc1'], r['alienacc2'], r['meandate1'], r['meandate2'] = get_divergence(r['name1'], r['name2'])

                write_a_row(r, outcomparisons, columns)

def get_divergence(sampleA, sampleB):
    '''
    This function applies model a to b, and vice versa, and returns
    a couple of measures of divergence: notably lost accuracy and
    z-tranformed spearman correlation.
    '''

    # We start by constructing the paths to the sampleA
    # standard model criteria (.pkl) and
    # model output (.csv) on the examples
    # originally used to train it.

    # We're going to try applying the sampleA standard
    # criteria to another model's output, and vice-
    # versa.

    model1 = '../models/' + sampleA + '.pkl'
    meta1 = '../models/' + sampleA + '.csv'

    # Now we construct paths to the test model
    # criteria (.pkl) and output (.csv).

    model2 = '../models/' + sampleB + '.pkl'
    meta2 = '../models/' + sampleB + '.csv'

    model1on2 = versatiletrainer2.apply_pickled_model(model1, '../data/', '.tsv', meta2)
    model2on1 = versatiletrainer2.apply_pickled_model(model2, '../data/', '.tsv', meta1)

    spearman1on2 = np.arctanh(stats.spearmanr(model1on2.probability, model1on2.alien_model)[0])
    spearman2on1 = np.arctanh(stats.spearmanr(model2on1.probability, model2on1.alien_model)[0])
    spearman = (spearman1on2 + spearman2on1) / 2

    loss1on2 = accuracy_loss(model1on2)
    loss2on1 = accuracy_loss(model2on1)
    loss = (loss1on2 + loss2on1) / 2

    alienacc2 = accuracy(model1on2, 'alien_model')
    alienacc1 = accuracy(model2on1, 'alien_model')

    acc2 = accuracy(model1on2, 'probability')
    acc1 = accuracy(model2on1, 'probability')

    meandate2 = np.mean(model1on2.std_date)
    meandate1 = np.mean(model2on1.std_date)

    return spearman, loss, spearman1on2, spearman2on1, loss1on2, loss2on1, acc1, acc2, alienacc1, alienacc2, meandate1, meandate2

def create_cross_models():

    allgenres = set()
    meta = pd.read_csv('../genremeta.csv')
    for idx, row in meta.iterrows():
        genres = row.tags.split('|')
        for g in genres:
            allgenres.add(g)

    allgenres = list(allgenres)
    print(allgenres)

    for g in allgenres:
        print()
        print(g)
        print()
        sourcefolder = '../data/'
        sizecap = 100
        outmodels = '../results/crossmodels.tsv'

        c_range = [.00001, .0001, .001, .01, 0.1, 1, 10, 100]
        featurestart = 1000
        featureend = 7000
        featurestep = 100
        modelparams = 'logistic', 12, featurestart, featureend, featurestep, c_range
        metadatapath = '../genremeta.csv'

        for contrast in ['randomA', 'randomB']:

            name = g + '_' + contrast
            vocabpath = '../lexica/' + name + '.txt'
            tags4positive = {g}
            tags4negative = {contrast}
            floor = 1700
            ceiling = 2011

            checkpath = '../models/' + name + '.csv'
            if not os.path.isfile(checkpath):

                metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist = versatiletrainer2.get_simple_data(sourcefolder, metadatapath, vocabpath, tags4positive, tags4negative, sizecap, excludebelow = floor, excludeabove = ceiling, force_even_distribution = False, negative_strategy = 'closely match', numfeatures = 7000, forbid4positive = set(), forbid4negative = set())

                # notice that I am excluding children's lit this time!

                matrix, maxaccuracy, metadata, coefficientuples, features4max, best_regularization_coef = versatiletrainer2.tune_a_model(metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist, tags4positive, tags4negative, modelparams, name, '../models/' + name + '.csv')

                meandate = int(round(np.sum(metadata.firstpub) / len(metadata.firstpub)))

                with open(outmodels, mode = 'a', encoding = 'utf-8') as f:
                    outline = name + '\t' + str(meandate) + '\t' + str(maxaccuracy) + '\t' + str(features4max) + '\t' + str(best_regularization_coef) + '\n'
                    f.write(outline)

                os.remove(vocabpath)

def create_model_assignments():
    '''
    To make sure that overlaps aren't biasing the model, we'll need to train
    extra models for comparisons where there is an overlap. This is quite a task
    and may need to be distributed across nodes. So first let's generate a list
    of assignments.
    '''

    genres = pd.read_csv('../metadata/selected_genres.tsv', sep = '\t')

    intersections = set(genres.loc[genres.genretype == 'intersection', 'genre'])
    primaries = list(genres.loc[genres.genretype == 'primary', 'genre'])
    bgenres = set(genres.loc[genres.genretype == 'B genre', 'genre'])

    models = set()

    for p1 in primaries:
        for p2 in primaries:
            if p1 == p2:
                models.add((p1, 'self'))
                bversion = p1 + ' B'
                if bversion in bgenres:
                    models.add((bversion, 'self'))
            else:
                models.add((p1, 'self'))

                intersect1 = p1 + '-Not-' + p2
                intersect2 = p2 + '-Not-' + p1

                if intersect1 in intersections:
                    models.add((p1, intersect1))
                    if intersect2 in intersections:
                        models.add((p2, intersect2))
                    else:
                        print('weird error you should check on')

    models = list(models)
    modelct = len(models)
    print(modelct)

    for floor in range(0, modelct, 25):
        with open('assignment' + str(floor) + '.tsv', mode = 'w', encoding = 'utf-8') as f:
            for positive, other in models[floor: floor + 25]:
                f.write(positive + '\t' + other + '\n')

def implement_assignment(assignment_file):

    assignments = dict()

    with open(assignment_file, encoding = 'utf-8') as f:
        for line in f:
            row = line.strip().split('\t')

            name = row[0].replace(': ', '')
            name = name.replace(' ', '')
            name = name.replace(',', '')

            positive_genres = [row[0]]

            if row[1] != 'self':
                positive_genres.append(row[1])
                exclusion = row[1].split('-Not-')[1]
                excludename = exclusion.replace(' ', '')
                excludename = excludename.replace(':', '')
                excludename = excludename.replace(',', '')
                name = name + '-Not-' + excludename

            assignments[name] = positive_genres

    sourcefolder = '../data/'
    sizecap = 100
    outmodels = '../results/crossmodels.tsv'

    for posname, assigned_positives in assignments.items():
        print()
        print(name, assigned_positives)
        print()

        if len(assigned_positives) > 1:
            exclusion = assigned_positives[1].split('-Not-')[1]
            exclusionB = exclusion + ' B'
            set2exclude = {exclusion, exclusionB}

        else:
            set2exclude = set()

        c_range = [.00001, .0001, .001, .01, 0.1, 1, 10, 100]
        featurestart = 500
        featureend = 6800
        featurestep = 100
        modelparams = 'logistic', 12, featurestart, featureend, featurestep, c_range
        metadatapath = '../metadata/genremeta.csv'

        for contrast in ['randomA', 'randomB']:

            name = posname + '_' + contrast
            vocabpath = '../lexica/' + name + '.txt'
            tags4positive = set(assigned_positives)

            tags4negative = {contrast}
            floor = 1700
            ceiling = 2011

            checkpath = '../models/' + name + '.csv'
            if not os.path.isfile(checkpath):

                metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist = versatiletrainer2.get_simple_data(sourcefolder, metadatapath, vocabpath, tags4positive, tags4negative, sizecap, excludebelow = floor, excludeabove = ceiling, force_even_distribution = False, negative_strategy = 'closely match', numfeatures = 6900, forbid4positive = set2exclude, forbid4negative = set())

                matrix, maxaccuracy, metadata, coefficientuples, features4max, best_regularization_coef = versatiletrainer2.tune_a_model(metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist, tags4positive, tags4negative, modelparams, name, '../models/' + name + '.csv')

                meandate = int(round(np.sum(metadata.firstpub) / len(metadata.firstpub)))

                with open(outmodels, mode = 'a', encoding = 'utf-8') as f:
                    outline = name + '\t' + str(meandate) + '\t' + str(maxaccuracy) + '\t' + str(features4max) + '\t' + str(best_regularization_coef) + '\n'
                    f.write(outline)

                os.remove(vocabpath)

def genrespace():

    outcomparisons = '../results/genrespace.tsv'
    columns = ['testype', 'name1', 'name2', 'meandate1', 'meandate2', 'acc1', 'acc2', 'alienacc1', 'alienacc2', 'spearman', 'spear1on2', 'spear2on1', 'loss', 'loss1on2', 'loss2on1']

    if not os.path.isfile(outcomparisons):
        with open(outcomparisons, mode = 'a', encoding = 'utf-8') as f:
            scribe = csv.DictWriter(f, delimiter = '\t', fieldnames = columns)
            scribe.writeheader()

    periods = ['1800to1899', '1900to1919', '1920to1949', '1950to1969', '1970to1979', '1980to1989', '1990to1999', '2000to2010']

    groups = dict()
    keys = []

    for genre in ['sfnojuv', 'fantasynojuv']:
        for p in periods:
            group = []
            for i in range(5):
                name = genre + p + 'v' + str(i)

                if not os.path.isfile('../modeloutput/' + name + '.pkl'):
                    print('error, missing ' + name)
                    sys.exit(0)
                else:
                    group.append(name)

            key = genre + p
            groups[key] = group
            keys.append(key)


    for genre in ['scarborough_random', 'bailey_random']:
        group = []
        for backdrop in ['_', '_B']:
            for i in range(3):
                if not os.path.isfile('../modeloutput/' + name + '.pkl'):
                    print('error, missing ' + name)
                    sys.exit(0)
                else:
                    group.append(name)

        key = genre
        groups[key] = group
        keys.append(key)

    for k1 in keys:
        for k2 in keys:

            for name1 in groups[k1]:
                for name2 in groups[k2]:

                    r = dict()
                    if k1 == k2:
                        r['testype'] = k1 + '|self'
                    else:
                        r['testype'] = k1 + '|' + k2

                    r['name1'] = name1
                    r['name2'] = name2

                    r['spearman'], r['loss'], r['spear1on2'], r['spear2on1'], r['loss1on2'], r['loss2on1'], r['acc1'], r['acc2'], r['alienacc1'], r['alienacc2'], r['meandate1'], r['meandate2'] = get_divergence(r['name1'], r['name2'])

                    write_a_row(r, outcomparisons, columns)


## MAIN

command = sys.argv[1]

if command == "crossmodels":
    create_cross_models()
elif command == "comparecross":
    compare_cross_models()
elif command == 'create_model_assignments':
    create_model_assignments()
elif command == 'assign':
    assignment_file = sys.argv[2]
    implement_assignment(assignment_file)

else:
    print('Not an allowable command.')



