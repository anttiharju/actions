#!/bin/sh

# * common ancestor
# |
# |‾‾‾‾\
# |\    * B
# | * A * C
# |/    * D
# * A  /
# |___/
# |
# * B, C, D <- only these should be found, even though A is between them and the common ancestor

git branch A
git branch BC

git switch A
mkdir A
touch A/a
git add A/a
git commit -m "Add a"
git switch -
git merge A

git switch BC

mkdir B
touch B/b
git add B/b
git commit -m "Add b"

mkdir C
touch C/c
git add C/c
git commit -m "Add c"

git switch -
git merge BC
