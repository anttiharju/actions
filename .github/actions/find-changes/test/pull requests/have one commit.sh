#!/bin/sh

git switch -c A
mkdir A
touch A/a
git add A/a
git commit -m "Add a"
