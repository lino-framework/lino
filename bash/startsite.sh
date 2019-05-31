#!/bin/bash
# Copyright 2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
#
# Create a new Lino production site on this server
# This is meant as template for a script to be adapted to your system.
# This is not meant to be used as is.
#

set -e  # exit on error
umask 0007

# CONFIG SECTION:

PROJECTS_ROOT=/usr/local/lino
ARCH_DIR=/var/backups/lino
ENVDIR=env
REPOSDIR=repositories

if ! [ -d $PROJECTS_ROOT ] ; then
    echo Oops, $PROJECTS_ROOT does not exist.
    echo Check the config section of your $0 script
    echo or say: sudo mkdir $PROJECTS_ROOT
    exit -1
fi


function usage() {
    cat <<USAGE
Usage:

  $0 <prjname> <appname>

Where <prjname> is your local name for the new site
<appname> is the name of the Lino app to run on this site.

USAGE
    exit -1
}

if [ "$1" = "-h"  -o "$1" = "--help" ] ; then
   usage
fi

if [ $# -ne 2 ] ; then
    usage
fi


prjname=$1
appname=$2
prjdir=$PROJECTS_ROOT/$prjname

if [ -d $prjdir ] ; then
    echo Oops, a directory $prjdir exists already. Delete it yourself if you dare!
    exit -1
fi

echo Create a new production site into $prjdir using Lino $appname
read -r -p "Are you sure? [y/N] " response
if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]
then
    echo "User abort"
    exit -1
fi


sudo mkdir $prjdir
sudo chmod g+wx $prjdir
cd $prjdir

virtualenv $ENVDIR
. $ENVDIR/bin/activate
mkdir $REPOSDIR
cd $REPOSDIR
git clone https://github.com/lino-framework/$appname.git
pip install -e $appname
