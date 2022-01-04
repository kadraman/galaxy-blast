# Remove the existing rgb opk.
rm -f rgb.opk && \

# Compile the *.py to *.pyc
python -m compileall ./ && \

# Create the OPK. It is a squashfs archive so we just list all the files and
# the last name will be the archive name,
mksquashfs  default.gcw0.desktop icon.png constants.pyc game.pyc main.pyc assets modules sprites states bouncing_ball.opk -all-root -no-xattrs -noappend -no-exports