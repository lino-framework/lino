#!/bin/bash
# Copyright 2015-2017 Luc Saffre
# License: BSD (see file COPYING for details)
#
# Make a snapshot of a Lino database.
# This is meant as template for a script to be adapted to your system.
# This is not meant to be used as is.
#

set -e  # exit on error

# YOU MUST edit the following lines:
# WARNING: all files older than 60 days in ARCHDIR will be deleted
# without confirmation

PROJECT_DIR=/path/to/myproject
ARCH_DIR=/var/backups/lino/myproject
ENVDIR=$PROJECT_DIR/env

# edit the following lines if you also want to include a MySQL dump
# MYSQL_USERNAME=
# MYSQL_PASSWORD=
# MYSQL_DBNAME=

# Directory where to put the temporary snapshot files.
# This is relative to PROJECT_DIR 
# WARNING: everything in this directory will be deleted without confirmation
SNAPSHOTDIR=snapshot

# name of target zip file to be created:
# This is relative to PROJECT_DIR 
ZIPFILE=snapshot.zip

if [ ! -d "$PROJECT_DIR" ]; then
  echo "PROJECT_DIR ($PROJECT_DIR) does not exist!"
  exit -1
fi

if [ ! -d "$ARCH_DIR" ]; then
  echo "ARCH_DIR ($ARCH_DIR) does not exist!"
  exit -1
fi

umask 0007 # make new files writable for other group members

cd $PROJECT_DIR

if [ -f $ZIPFILE ]
  then
  ARCFILE=`date +$ARCH_DIR/%Y%m%d_%H%M.zip -r $ZIPFILE`
  echo "Move existing $ZIPFILE to $ARCFILE"
  mv $ZIPFILE $ARCFILE
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
if [ "$MYSQL_USERNAME" != "" ] ; then
  echo -n "Writing MySQL dump..."
  mysqldump -u "$MYSQL_USERNAME" --password="$MYSQL_PASSWORD" "$MYSQL_DBNAME" > $SNAPSHOTDIR/dump.sql
  echo " done"
fi
echo "Writing $ZIPFILE..."
zip -r $ZIPFILE $SNAPSHOTDIR
zip -r $ZIPFILE fixtures
zip -r $ZIPFILE media/webdav
zip -r $ZIPFILE media/beid
zip $ZIPFILE *.py *.sh

# delete all files older than 60 days in ARCHDIR:
find $ARCH_DIR -maxdepth 1 -depth -name '*.zip' -mtime +60 -delete

