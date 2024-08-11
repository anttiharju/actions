#!/bin/sh

git switch -c A
mkdir A

touch A/a1
git add A/a1
git commit -m "Add a1"

touch A/a2
git add A/a2
git commit -m "Add a2"

touch A/a3
git add A/a3
git commit -m "Add a3"
