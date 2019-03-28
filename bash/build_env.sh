#!/usr/bin/env bash


# Clone sources

mkdir src
cd src

for pro in atelier lino xl cosi noi book voga welfare care avanti extjs6 presto vilma tera riche react openui5 etgen

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

# appy
sudo apt-get install subversion
svn checkout https://svn.forge.pallavi.be/appy-dev
pip install -e appy-dev/dev1


sudo apt-get install libreoffice python3-uno python-pygraphviz virtualenv build-essential libssl-dev libffi-dev python-dev python3-dev gcc

# Notification service
sudo apt-get install redis redis-server

pip install -U pip
pip install -U setuptools
pip install mock ipython

# order is important.
for i in atelier/ lino/ xl/ noi/ django-mailbox/ extjs6/ commondata/ commondata-be/ commondata-ee/ commondata-eg/ \
         cosi/ voga/ welfare/ vilma/ avanti/ presto/ care/ riche/ tera/ react/ openui5/ book/ etgen/
do
    pip install -e $i
done




