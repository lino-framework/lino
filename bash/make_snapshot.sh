#!/bin/bash
# Copyright 2015-2016 Luc Saffre
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

PROJECT_DIR=/path/to/myproject
ARCH_DIR=/var/backups/lino/myproject

if [ ! -d "$PROJET_DIR" ]; then
  echo $PROJET_DIR does not exist!
  exit -1
fi

# edit the following lines if you also want to include a MySQL dump
MYSQL_USERNAME=
MYSQL_PASSWORD=
MYSQL_DBNAME=

# Directory where to put the temporary snapshot files.
# WARNING: everything in this directory will be deleted without confirmation
SNAPSHOTDIR=$PROJECT_DIR/snapshot

# name of target zip file to be created:
ZIPFILE=$ARCH_DIR/snapshot.zip
# ZIPFILE=snapshot.zip

# uncomment the following if you have no virtualenv:
ENVDIR=$PROJECT_DIR/env

# make new files writable for other group members:
umask 0007

if [ -f $ZIPFILE ]
  then
  ARCFILE=`date +$ARCH_DIR/%Y%m%d_%H%M.zip -r $ZIPFILE`
  mv $ZIPFILE $ARCFILE
  echo Moved $ZIPFILE to $ARCFILE
fi

cd $PROJECT_DIR

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

# delete all files older than 60 days in ARCHDIR:
find $ARCH_DIR -maxdepth 1 -depth -mtime +60 -delete

