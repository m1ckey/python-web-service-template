#!/usr/bin/env sh

set -e

git switch prod
git merge master --ff-only
git switch master
git push --all
