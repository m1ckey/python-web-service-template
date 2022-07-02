#!/usr/bin/env sh

set -eux

git switch prod
git merge master --ff-only
git switch master
git push --all
