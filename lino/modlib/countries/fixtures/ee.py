## Copyright 2010-2011 Luc Saffre 
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
Imports file `sihtnumbrid.csv` which I obtained from
http://www.post.ee

"""

import csv
import os
import codecs

from lino.tools import resolve_model
from lino.utils.instantiator import Instantiator

# http://www.python.org/doc/current/library/csv.html#module-csv
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


city = Instantiator('countries.City',country='EE').build

input_file = os.path.join(
  os.path.dirname(__file__),
  'sihtnumbrid.csv')
  
def objects():
    f = codecs.open(input_file,'r','latin-1','replace')
    f.readline()
    r = unicode_csv_reader(f,delimiter=';')
    #r.next()
    names = set()
    for ln in r:
        #print repr(ln)
        if len(ln) > 2:
            if ln[1]:
                names.add(ln[1])
            elif ln[2]:
                names.add(ln[2])
    f.close()
    #print len(names), "Estonian cities"
    for name in names:
        if name:
            yield city(name=name)

    

