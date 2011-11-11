## Copyright 2009-2010 Luc Saffre
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

from django.db import models
#countries = models.get_app('countries')

from lino.utils.instantiator import Instantiator
from lino.utils.babel import babel_values

country = Instantiator('countries.Country',"isocode name").build

def objects():

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
    #~ yield country('EE',"Estonia")
    #~ yield country('BE',"Belgium")
    #~ yield country('DE',"Germany")
    #~ yield country('FR',"France")
    #~ yield country('NL',"Netherlands")

