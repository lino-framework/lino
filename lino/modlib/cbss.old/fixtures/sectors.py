# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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
Fills the Sectors table using the official data from 
http://www.bcss.fgov.be/binaries/documentation/fr/documentation/general/lijst_van_sectoren_liste_des_secteurs.xls    

"""

from django.conf import settings
from lino.utils import ucsv
#~ from lino.utils.babel import babel_values
from lino.utils import babel
from lino.core.modeltools import resolve_model
from os.path import join, dirname

ENCODING = 'latin1' # the encoding used by the mdb file
#~ ENCODING = 'utf8' 

GERMAN = []
GERMAN.append((17,1,u'ÖSHZ',u'Öffentliche Sozialhilfezentren'))


def objects():
  
    Sector = resolve_model('cbss.Sector')
  
    fn = join(dirname(__file__),'lijst_van_sectoren_liste_des_secteurs.csv')
    reader = ucsv.UnicodeReader(open(fn,'r'),encoding=ENCODING,delimiter=';')
    
    headers = reader.next()
    if headers != [u'Sector',u'',u'verkorte naam',u'Omschrijving',u'Abréviation',u'Nom']:
        raise Exception("Invalid file format: %r" % headers)
    reader.next() # ignore second header line
    code = None
    for row in reader:
        s0 = row[0].strip()
        s1 = row[1].strip()
        #~ if s0 == '17' and s1 == '0':
            #~ continue # 
        if s0 or s1:
            kw = {}
            if len(s0) > 0:
                #~ print repr(row[0])
                code = int(s0)
            kw.update(code=code)
            if row[1]:
                kw.update(subcode=int(row[1]))
            kw.update(**babel.babel_values('name',de=row[5],fr=row[5],nl=row[3]))
            kw.update(**babel.babel_values('abbr',de=row[4],fr=row[4],nl=row[2]))
            #~ print kw
            yield Sector(**kw)
        
    if 'de' in settings.LINO.languages:
        for code,subcode,abbr,name in GERMAN:
            sect = Sector.objects.get(code=code,subcode=subcode)
            if babel.DEFAULT_LANGUAGE == 'de':
                sect.abbr = abbr
                sect.name = name
            else :
                sect.abbr_de = abbr
                sect.name_de = name
            sect.save()

    # default value for SiteConfig.sector is "CPAS"
    #~ settings.LINO.site_config.sector = Sector.objects.get(code=17,subcode=1)
    #~ settings.LINO.site_config.save()


