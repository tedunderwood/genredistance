parsejsons
==========

Code used to translate extracted feature files from HTRC.

The central script here is **parsefeaturejsons.py**; most of the other files here are supporting data or "rule" files it uses to normalize text. For instance, we make an effort to normalize American spelling to British.

If you're wondering how to get extracted feature files in the first place, the page describing the resource is here: [https://wiki.htrc.illinois.edu/display/COM/Extracted+Features+Dataset](https://wiki.htrc.illinois.edu/display/COM/Extracted+Features+Dataset)

how I actually get extracted features from HTRC
--------------------------------------

This part of the work is not reproducible in a push-button way, because I download extracted-feature files using an idiosyncratic workflow, and there's a better way for you to do it. If you want to add some additional files to the experiment, I actually recommend that you consult [the HTRC documentation](https://wiki.htrc.illinois.edu/display/COM/Extracted+Features+Dataset) and download files using their, simpler process.

But what I actually do is pair HathiTrust volume IDs with a list of possible paths, in order to generate a list of paths I need.

Then (in a directory where I store raw feature files) I do this command:

> rsync -a --files-from=/Users/tunder/Dropbox/python/pmla/getdata/justpathlist.txt data.analytics.hathitrust.org::features fic

That downloads extracted-features as a pairtree in the fic directory.

I run parsefeaturejsons.py on the pairtree structure.
