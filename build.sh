#!/bin/sh

# Remove the existing opk.
rm -f retro-galaxy-blast.opk

# Compile the *.py to *.pyc
python2 -m compileall ./ .

# Create the OPK. It is a squashfs archive so we just list all the files and
# the last name will be the archive name,
mksquashfs default.gcw0.desktop main.pyc main.py game.pyc game.py constants.pyc constants.py bin assets modules sprites states retro-galaxy-blast.opk -no-xattrs -noappend -no-exports

scp retro-galaxy-blast.opk root@10.1.1.2:/media/data/apps