#!/bin/bash
# Copyright 2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
#
# Create a new Lino production site on this server
# This is meant as template for a script to be adapted to your system.
# This is not meant to be used as is.
# INSTALLATION:
#
# $ wget https://raw.githubusercontent.com/lino-framework/lino/master/bash/startsite.sh
# $ nano startsite.sh
# Edit the config section of the file to adapt it to your system-wide server preferences.
# $ sudo chmod a+x startsite.sh
# $ sudo mv startsite.sh /usr/local/bin

set -e  # exit on error
umask 0007

# CONFIG SECTION:

PROJECTS_ROOT=/usr/local/lino
PROJECTS_PREFIX=prod_sites
ARCH_DIR=/var/backups/lino
ENVDIR=env
REPOSDIR=repositories
USERGROUP=www-data

# END OF CONFIG SECTION. IF YOU EDIT BELOW THIS ROW, PLEASE CONSIDER
# SHARING YOUR THOUGHTS BACK TO THE PROJECT.

if groups | grep &>/dev/null '\b$USERGROUP\b'
then
    echo OK you belong to the $USERGROUP user group.
else
    echo "ERROR: you don't belong to the $USERGROUP user group."
    echo "Maybe you want to run:"
    # echo sudo usermod -a -G $USERGROUP `whoami`
    echo sudo adduser `whoami` $USERGROUP
    exit -1
fi

if ! [ -d $PROJECTS_ROOT ] ; then
    echo Oops, $PROJECTS_ROOT does not exist.
    echo Check the config section of your $0 script or invoke with --install
    exit -1
fi

function usage() {
    cat <<USAGE
Usage:

  $0 [options] [<prjname> <appname>]

Where <prjname> is your local name for the new site
<appname> is the name of the Lino app to run on this site.

Options:

  -h, --help: show this help
  -i, --install : install system software


USAGE
    exit -1
}


function check_dir_exist() {
    name=$1
    if ! [ -d $name ] ; then
        echo Create $name
        sudo mkdir $name
    fi
    sudo chmod g+ws $name
    sudo chown :$USERGROUP $name
}

function install() {
    check_dir_exist $PROJECTS_ROOT
    check_dir_exist $PROJECTS_ROOT/$PROJECTS_PREFIX

    sudo apt install virtualenv

    sudo pip install cookiecutter

}

if [ "$1" = "-h"  -o "$1" = "--help" ] ; then
   usage
fi

if [ "$1" = "-i"  -o "$1" = "--install" ] ; then
   install
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

mkdir $prjdir
cd $prjdir


cookiecutter https://github.com/lino-framework/cookiecutter-startsite
