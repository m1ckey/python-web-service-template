#!/usr/bin/env sh

set -e

poetry export -o requirements.txt

git switch prod
git merge master --ff-only
git switch master
git push --all
