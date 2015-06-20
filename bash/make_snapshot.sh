#!/bin/bash
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
#
# Make a snapshot of a Lino database.
# This is meant as template for a script to be adapted to your system.
# This is not meant to be used as is.
#

set -e  # exit on error

# edit the following line if this is also to be called from
# /etc/cron.d/lino_backup where cwd is not set:
# cd /path/to/project/dir

# Directory where to put the temporary snapshot files.
# WARNING: everything in this directory will be deleted without confirmation
SNAPSHOTDIR=snapshot

# name of target zip file to be created:
ZIPFILE=snapshot.zip

# uncomment the following if you have no virtualenv:
ENVDIR=env

# make new files writable for other group members:
umask 0007

if [ -f $ZIPFILE ]
  then
  mv $ZIPFILE `date -r $ZIPFILE +%Y%m%d_%H%M.zip`
  # echo "Sorry, there is already a file $ZIPFILE. Delete it yourself if you dare."
  # exit -1
fi

if [ -d $ENVDIR ]
  then
  . $ENVDIR/bin/activate
fi

if [ -d $SNAPSHOTDIR ]
  then
    rm $SNAPSHOTDIR/* 
    rmdir $SNAPSHOTDIR
fi

python manage.py dump2py $SNAPSHOTDIR
pip freeze > $SNAPSHOTDIR/requirements.txt
if $MYSQL_USERNAME ; then
  mysqldump -u $MYSQL_USERNAME --password=$MYSQL_PASSWORD $MYSQL_DBNAME > $SNAPSHOTDIR/dump.sql
fi
zip -r $ZIPFILE $SNAPSHOTDIR
zip -r $ZIPFILE fixtures
zip -r $ZIPFILE media/webdav
zip -r $ZIPFILE media/beid
zip $ZIPFILE *.py *.sh
