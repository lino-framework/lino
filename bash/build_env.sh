#!/usr/bin/env bash


# Clone sources

mkdir src
cd src

for pro in atelier lino xl cosi noi book voga welfare care avanti extjs6 presto vilma tera riche

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

sudo apt-get install libreoffice python3-uno python-pygraphviz virtualenv build-essential libssl-dev libffi-dev python-dev python3-dev gcc

cd ..

virtualenv -p python2 2.7
virtualenv -p python3 3.5

cd src

for PY in 3.5 2.7
do . ../$PY/bin/activate

pip install -U pip
pip install -U setuptools

for i in atelier lino xl noi django-mailbox extjs6 commondata commondata-be commondata-ee commondata-eg cosi voga welfare vilma avanti presto care riche tera book
do
    pip install -e $i
done

pip install mock ipython radicale
done


