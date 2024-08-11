#!/bin/sh

git switch -c B
mkdir B
touch B/b
git add B/b
git commit -m "Add b"

git switch -
git merge --ff-only B
