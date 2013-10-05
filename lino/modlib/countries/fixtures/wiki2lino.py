# -*- coding: UTF-8 -*-
## Copyright 2009-2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
Analyzes two pages from wikipedia.
Currently just prints what it found.

TODO: write this into some intermediate file 
to be loaded by :mod:`lino.modlib.countries.fixtures.be`.

"""

import requests
from bs4 import BeautifulSoup

import urllib2

#~ from north.dbutils import babel_values

def tostring(x):
    return ' '.join(x.stripped_strings)

def extract(url):
    #~ text = urllib2.urlopen(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    table = soup.find('table',attrs={"class": "wikitable sortable"})

    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 8:
            fr=tostring(cells[0])
            nl=tostring(cells[1])
            province=tostring(cells[2])
            type=tostring(cells[3])
            #~ countries.City.lookup_or_create('name')
            print fr, nl, province,type
        elif len(cells) == 0:
            pass
        else:
            raise Exception("Found row %s with %d cells"  % (cells,len(cells)))

if __name__ == '__main__':

    extract('https://fr.wikipedia.org/wiki/Liste_des_communes_de_la_R%C3%A9gion_wallonne')
    extract('https://fr.wikipedia.org/wiki/Liste_des_communes_de_la_R%C3%A9gion_flamande')

