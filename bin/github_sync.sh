#!/bin/bash

set -e

# this script should be run from the repo
cd $(dirname $(dirname $(readlink -m $0)))

git remote add github git@github.com:Internet-of-People/titania-os.git || true
git push github "refs/heads/develop"
git push github "refs/heads/master"
git push github "refs/tags/v*"
