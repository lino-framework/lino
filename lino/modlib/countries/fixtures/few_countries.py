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
Adds an arbitrary selection of a few demo countries.
"""

from __future__ import unicode_literals


from django.db import models
#countries = models.get_app('countries')

from lino.utils.instantiator import Instantiator
from north.babel import babel_values


def objects():

    country = Instantiator('countries.Country',"isocode name").build
    
    yield country('EE',**babel_values('name',
          de=u"Estland",
          fr=u'Estonie',
          en=u"Estonia",
          nl=u'Estland',
          et=u'Eesti',
          ))
    yield country('BE',**babel_values('name',
          de=u"Belgien",
          fr=u'Belgique',
          en=u"Belgium",
          nl=u'Belgie',
          et=u'Belgia',
          ))
    yield country('DE',**babel_values('name',
          de=u"Deutschland",
          fr=u'Allemagne',
          en=u"Germany",
          nl=u'Duitsland',
          et=u'Saksamaa',
          ))
    yield country('FR',**babel_values('name',
          de=u"Frankreich",
          fr=u'France',
          en=u"France",
          nl=u'Frankrijk',
          et=u'Prantsusmaa',
          ))
    yield country('NL',**babel_values('name',
          de=u"Niederlande",
          fr=u'Pays-Bas',
          en=u"Netherlands",
          nl=u'Nederlande',
          et=u'Holand',
          ))
          
    yield country('MA',**babel_values('name',
          de=u"Marokko",
          fr=u'Maroc',
          en=u"Maroc",
          nl=u'Marocco',
          et=u'Marokko',
          ))
          
    yield country('RU',**babel_values('name',
          de=u"Russland",
          fr=u'Russie',
          en=u"Russia",
          nl=u'Rusland',
          et=u'Venemaa',
          ))
          
    yield country('CD',**babel_values('name',
          de=u"Kongo (Demokratische Republik)",
          fr=u'Congo (République Démocratique)',
          en=u"Congo (Democratic Republic)",
          nl=u'Congo (Democratische Republiek)',
          et=u'Kongo (Demokraatlik Vabariik)',
          ))
    #~ yield country('EE',"Estonia")
    #~ yield country('BE',"Belgium")
    #~ yield country('DE',"Germany")
    #~ yield country('FR',"France")
    #~ yield country('NL',"Netherlands")

