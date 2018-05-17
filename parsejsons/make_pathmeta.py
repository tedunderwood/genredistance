#!/usr/bin/env python3

# make_pathmeta

import pandas as pd
import csv

meta = pd.read_csv('../metadata/genremeta.csv')

ids2get = set(meta.docid.tolist())

rows2keep = []

with open('../../noveltmmeta/get_EF/ids2pathlist.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    fieldnames = reader.fieldnames
    for row in reader:
        docid = row['docid']
        if docid not in ids2get:
            continue
        else:
            rows2keep.append(row)

with open('ids2pathlist4genres.tsv', mode = 'w', encoding = 'utf-8') as f:
    writer = csv.DictWriter(f, fieldnames = fieldnames, delimiter = '\t')
    writer.writeheader()
    for row in rows2keep:
        writer.writerow(row)



