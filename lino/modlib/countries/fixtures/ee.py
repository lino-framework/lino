# -*- coding: UTF-8 -*-
## Copyright 2010-2012 Luc Saffre 
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
Imports file :file:`sihtnumbrid.csv` which you can obtain from
`Estonian Post office <http://www.post.ee/ariklient_sihtnumbrid_allalaadimiseks>`_.

A copy of file :file:`sihtnumbrid.csv` was accidentally published here 
between June 2010 and May 2012, until we realized that 
this wasn't allowed due to copyright restrictions.

You must download the file yourself and place it into your 
:attr:`project directory <lino.Lino.project_dir>`.

"""

import csv
import os
import codecs

from django.conf import settings

from lino.core.modeltools import resolve_model
from lino.utils.instantiator import Instantiator
from lino.utils.ucsv import UnicodeReader

if True:
  
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

from lino.modlib.countries.models import CityTypes
city = Instantiator('countries.City',country='EE').build

CITY_TYPES = {
  u'küla' : CityTypes.village,
  u'linn' : CityTypes.town,
  u'alev' : CityTypes.borough,
  u'alevik' : CityTypes.smallborough,
  u'asum' : CityTypes.township,
  #~ u'aiandusühistu' : CityTypes.quarter,
  u'aiandusühistu' : None, # ignore them
  }


#~ input_file = os.path.join(
  #~ os.path.dirname(__file__),
  #~ 'sihtnumbrid.csv')
  
input_file = os.path.join(
  settings.LINO.project_dir,
  'sihtnumbrid.csv')
  
u"""  
MAAKOND;VALD;LINN/ ALEV/ ALEVIK/ KÜLA;TÄNAV/TALU;AADRESSILIIK;MAJAALGUS;MAJALOPP;SIHTNUMBER   
"""
  
def objects():
    f = codecs.open(input_file,'r','latin-1','replace')
    #~ f = codecs.open(input_file,'r','utf-8','replace')
    f.readline()
    r = unicode_csv_reader(f,delimiter=';')
    #~ r = UnicodeReader(f,delimiter=';')
    #r.next()
    maakonnad = dict()
    mk_names_dict = dict()
    #~ vallad = dict()
    #~ laakid = dict()
    #~ names = set()
    for ln in r:
        #print repr(ln)
        if len(ln) > 2:
            mk = maakonnad.get(ln[0])
            if mk is None:
                mk = city(name=ln[0],type=CityTypes.county)
                yield mk
                #~ print "20120822 maakond", mk, mk.pk
                maakonnad[ln[0]] = mk
                mk_names_dict[ln[0]] = dict()
                
            names = mk_names_dict[ln[0]]
                
            if ln[1]:
                vald = names.get(ln[1])
                if vald is None:
                    #~ ct = CITY_TYPES[ln[4]]
                    vald = city(name=ln[1],
                        type=CityTypes.municipality,
                        parent=mk,zip_code=ln[7])
                    yield vald
                    #~ if ct != CityTypes.municipality:
                        #~ print "20120822", vald, "expected municipality, found", ct
                    #~ else:
                    #~ print "20120822 vald", vald, vald.pk
                    names[ln[1]] = vald
                else:
                    vald.zip_code = ''
                    vald.save()
                    
            else:
                vald = None
                
            laak = names.get(ln[2])
            if laak is None:
                #~ ct = CITY_TYPES.get(ln[4])
                ct = CITY_TYPES[ln[4]]
                if ct is None:
                    #~ print "20120822 ignored addressiliik", ln[4]
                    continue
                elif vald is None:
                    laak = city(name=ln[2],type=ct,parent=mk,zip_code=ln[7])
                else:
                    laak = city(name=ln[2],type=ct,parent=vald,zip_code=ln[7])
                yield laak
                #~ print "20120822", laak.type, laak, laak.pk
                names[ln[2]] = laak
                #~ else:
                    #~ print "20120822 pole vald ega Tallinn:", ln
                    #~ names.add(ln[2])
            else:
                laak.zip_code = ''
                laak.save()
    f.close()
    #print len(names), "Estonian cities"
    #~ for name in names:
        #~ if name:
            #~ yield city(name=name)

    

