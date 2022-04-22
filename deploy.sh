#!/usr/bin/env sh

set -e

poetry install
poetry export -o requirements.txt
# git switch will fail if any files changed

git switch prod
git merge master --ff-only
git switch master
git push --all
