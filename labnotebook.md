lab notebook for genre divergence
=================================

Project designed to compare different ways of estimating genre divergence. Based on, and extending, work undertaken for "A Measured Perspective."

May 9, 2018
-----------

Started project by beginning to construct a genre dataset based on Library of Congress genre and subject categories.

The question I want to pose, is, do measures of textual similarity and divergence really correspond to evidence about cultural proximity and difference?

May 15, 2018
------------

After some initial exploratory data analysis, I'm ready for a more formal experiment. 

Rewrote build_genre_dataset.ipynb to select a larger set of categories. Wrote **metadata/genremeta.csv** Ran parse_jsons/make_pathmeta.py to translate that into **ids2pathlist4genres.tsv.** Ran **parsefeaturejsons** to get the raw data.