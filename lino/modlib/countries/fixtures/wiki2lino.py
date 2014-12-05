# -*- coding: UTF-8 -*-
# Copyright 2009-2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Analyzes two pages from wikipedia.
Currently just prints what it found.

TODO: write this into some intermediate file 
to be loaded by :mod:`lino.modlib.countries.fixtures.be`.

"""

import requests
from bs4 import BeautifulSoup


def tostring(x):
    return ' '.join(x.stripped_strings)


def extract(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    table = soup.find('table', attrs={"class": "wikitable sortable"})

    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 8:
            fr = tostring(cells[0])
            nl = tostring(cells[1])
            province = tostring(cells[2])
            type = tostring(cells[3])
            #~ countries.Place.lookup_or_create('name')
            print fr, nl, province, type
        elif len(cells) == 0:
            pass
        else:
            raise Exception("Found row %s with %d cells" %
                            (cells, len(cells)))

if __name__ == '__main__':

    extract(
        'https://fr.wikipedia.org/wiki/Liste_des_communes_de_la_R%C3%A9gion_wallonne')
    extract(
        'https://fr.wikipedia.org/wiki/Liste_des_communes_de_la_R%C3%A9gion_flamande')
