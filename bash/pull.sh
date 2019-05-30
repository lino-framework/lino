#!/bin/bash
# Copyright 2015-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
#
# Run `pip --update` for this environment. 
# Run `git pull` on repositories in develop mode (`pip -e`)
# Also remove all `*.pyc` files in these repositories.
#
# NOTE THIS IS A TEMPLATE TO BE COPIED TO A PRODUCTION SITE.
# YOU SHOULD ADAPT IT MANUALLY AND THEN REMOVE THIS NOTE.

set -e
umask 0007

PRJDIR=`pwd`

. env/bin/activate

echo "Run pull.sh in $PRJDIR" >> freeze.log
date >> freeze.log
pip freeze >> freeze.log

pip install -U lino
pip install -U xl

function pull() {
    repo=$1
    cd $repo
    pwd
    git pull
    find -name '*.pyc' -exec rm -f {} +
    cd $PRJDIR
}


pull repositories/cosi

