Measures of distance between genres
===================================

[![DOI](https://zenodo.org/badge/133397935.svg)](https://zenodo.org/badge/latestdoi/133397935)

Exploring textual and social measures of the distance between genres of fiction. Work in this repository supports Ted Underwood, "The Historical Significance of Textual Distances," presented at the LaTeCH-CLfL workshop associated with COLING in Santa Fe, 2018.

abstract
---------

Measuring similarity is a basic task in information retrieval, and now often a building-block for more complex arguments about cultural change. But do measures of textual similarity and distance really correspond to evidence about cultural proximity and differentiation? To explore that question empirically, this paper compares textual and social measures of the similarities between genres of English-language fiction. Existing measures of textual similarity (cosine similarity on tf-idf vectors or topic vectors) are also compared to new strategies that strive to anchor textual measurement in a social context.

map of the repository
---------------------

I'll describe folders in an order that roughly tracks the workflow of the experiment. But note that **analysis** might be where you want to start, if you're mostly interested in conclusions.

[**select_data**](https://github.com/tedunderwood/genredistance/tree/master/select_data) contains a Jupyter notebook that documents the selection of fiction volumes for the experiment, and also the social ground truth about genre proximity used to test textual distances.

[**metadata**](https://github.com/tedunderwood/genredistance/tree/master/metadata) The key file here is **genremeta.csv**.

[**parsejsons**](https://github.com/tedunderwood/genredistance/tree/master/parsejsons) contains code that translated the HathiTrust Extracted Feature files into tab-separated wordcount files.

[**lda**](https://github.com/tedunderwood/genredistance/tree/master/metadata) contains code that produced the topic model used in the article (see **lda.ipynb**)

[**logistic**](https://github.com/tedunderwood/genredistance/tree/master/logistic) Code used to train predictive models.

[**results**](https://github.com/tedunderwood/genredistance/tree/master/results) Mostly the output of predictive models.

[**analysis**](https://github.com/tedunderwood/genredistance/tree/master/analysis) May be where you want to start if you're less interested in the construction of data than in the final inferences. Contains three Jupyter notebooks documenting inferences about word vectors, topic vectors, and predictive models respectively. Also constructs data used to create figures 2, 3, and 4.

[**socialmeasures**](https://github.com/tedunderwood/genredistance/tree/master/socialmeasures) contains only one .csv file, recording the results of PMI calculation on genre pairs.

[**rplots**](https://github.com/tedunderwood/genredistance/tree/master/rplots) The R scripts used for the final stage of visualization.

data
-----

In order to actually run much of the code here, you will also need a folder named **/data** that contains the word counts for 6,846 volumes of fiction. Unzipped, it runs to almost 1GB, and is too large for this repository, so I have provided a link to my institutional repository: [https://www.ideals.illinois.edu/handle/2142/100119](https://www.ideals.illinois.edu/handle/2142/100119)
