#!/bin/bash

# Remove the existing rgb opk.
rm -f retro-galaxy-blast.opk

# Compile the *.py to *.pyc
python -m compileall ./ .

# Create the OPK. It is a squashfs archive so we just list all the files and
# the last name will be the archive name,
#mksquashfs default.gcw0.desktop icon.png constants.py game.py main.py assets modules sprites states retro-galaxy-blast.opk -no-xattrs -noappend -no-exports
mksquashfs  default.gcw0.desktop ball.pyc ball.py ball2.pyc ball2.py main.pyc main.py game.pyc game.py constants.pyc constants.py icon.png ball.png bin assets modules sprites states retro-galaxy-blast.opk -no-xattrs -noappend -no-exports

scp retro-galaxy-blast.opk root@10.1.1.2:/media/data/apps