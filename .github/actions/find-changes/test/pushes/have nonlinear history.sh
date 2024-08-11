#!/bin/sh

# * common ancestor
# |
# |‾‾‾‾\
# |\    \
# | * A  * B
# |/    /
# * A  /
# |___/
# |
# * B <- only B should be found, even though A is between common ancestor and B

git branch A
git branch B

git switch A
mkdir A
touch A/a
git add A/a
git commit -m "Add a"
git switch -
git merge A

git switch B
mkdir B
touch B/b
git add B/b
git commit -m "Add b"
git switch -
git merge B
