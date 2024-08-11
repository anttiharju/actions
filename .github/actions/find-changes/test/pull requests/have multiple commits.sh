#!/bin/sh

git switch -c ABC

mkdir A
touch A/a
git add A/a
git commit -m "Add a"

mkdir B
touch B/b
git add B/b
git commit -m "Add b"

mkdir C
touch C/c
git add C/c
git commit -m "Add c"
