## Awoo importers

This repository contains two scripts that can be used for importing threads from the now-deprecated [danger/u/](https://github.com/dangeru/danger-u-) board software to our new textboard platform [awoo](https://github.com/dangeru/awoo)

They both export an `output.sql` file that CLEARS THE POSTS TABLE then inserts the imported posts.

They both require a locally running mysql installation for sql sanitization

The file importer expects to be in a directory where each subdirectory is the name of a board, and each board folder has a `thread` subdirectory. It will attempt to set the date created and date last bumped on the imported thread to the modify time of the thread's text file

It will fail on deleted (0 byte) threads.
