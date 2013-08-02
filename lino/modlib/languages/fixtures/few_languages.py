## Copyright 2009-2012 Luc Saffre
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
Adds an arbitrary selection of a few demo languages.
"""

from django.db import models
#countries = models.get_app('countries')

from lino.utils.instantiator import Instantiator
from north.dbutils import babel_values



def objects():
  
    Language = Instantiator('languages.Language',"id").build
    
    yield Language('ger',**babel_values('name',
          de=u"Deutsch",
          fr=u'Allemand',
          en=u'German',
          nl=u'Duits',
          et=u'Saksa',
          ))
    yield Language('fre',**babel_values('name',
          de=u"Französisch",
          fr=u'Français',
          en=u'French',
          nl=u'Frans',
          et=u'Prantsuse',
          ))
    yield Language('eng',**babel_values('name',
          de=u"Englisch",
          fr=u'Anglais',
          en=u'English',
          nl=u'Engels',
          et=u'Inglise',
          ))
    yield Language('dut',**babel_values('name',
          de=u"Niederländisch",
          fr=u'Néerlandais',
          en=u'Dutch',
          nl=u'Nederlands',
          et=u'Hollandi',
          ))
    yield Language('est',**babel_values('name',
          de=u"Estnisch",
          fr=u'Estonien',
          en=u'Estonian',
          et=u'Eesti',
          ))

