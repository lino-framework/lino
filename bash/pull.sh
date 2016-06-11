#!/bin/bash
# Copyright 2015-2016 Luc Saffre
# License: BSD (see file COPYING for details)
#
# Run `git pull` on all repositories used by this project. Also remove
# all `*.pyc` files.
#

set -e

function pull_here() {
    pwd
    git pull
    find -name '*.pyc' -exec rm -f {} +
}

REPOS=/path/to/your/repositories

cd $REPOS/lino ; pull_here
cd $REPOS/xl ; pull_here
cd $REPOS/cosi ; pull_here
cd $REPOS/voga ; pull_here

