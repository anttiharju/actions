#!/bin/sh

git switch -c "add-potato"
mkdir potato
touch potato/.gitkeep
git add potato/.gitkeep
git commit -m "Add potato"
