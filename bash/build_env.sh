#!/usr/bin/env bash
virtualenv 2.7
. 2.7/bin/activate
mkdir src
cd src


for pro in atelier lino xl cosi noi book voga welfare avanti extjs6

do
    git clone git@github.com:lino-framework/$pro.git
done


for comm in https://github.com/lsaffre/commondata \
	    https://github.com/lsaffre/commondata-be \
	    https://github.com/lsaffre/commondata-ee \
	    https://github.com/lsaffre/commondata-eg \
            git@github.com:cylonoven/django-mailbox.git
do
    git clone $comm
done


for i in atelier lino xl noi django-mailbox extjs6 commondata commondata-be commondata-ee commondata-eg cosi voga welfare avanti book
do
    pip install -e $i
done

pip install mock ipython

sudo apt-get install libreoffice python3-uno python-pygraphviz

sudo apt-get install build-essential libssl-dev libffi-dev python-dev

