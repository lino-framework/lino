# -*- coding: UTF-8 -*-
## Copyright 2012-2013 Luc Saffre
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


from lino import dd
from lino.utils.instantiator import Instantiator, i2d
#~ from lino.core.dbutils import resolve_model
from django.utils.translation import ugettext_lazy as _

from north.dbutils import babelkw


def objects():
   
    #~ slot = Instantiator('courses.Slot','name start_time end_time').build
    #~ 
    #~ kw = dict(monday=True,tuesday=True,wednesday=False,thursday=True,friday=True)
    #~ yield slot("Erste Stunde","16:00","17:00",**kw)
    #~ yield slot("Zweite Stunde","17:00","18:00",**kw)
    #~ yield slot("Dritte Stunde","18:00","19:00",**kw)
    #~ 
    #~ kw = dict(wednesday=True)
    #~ yield slot("Mittwochs 13 Uhr","13:00","14:00",**kw)
    #~ yield slot("Mittwochs 14 Uhr","14:00","15:00",**kw)
    #~ yield slot("Mittwochs 15 Uhr","15:00","16:00",**kw)
    #~ yield slot("Mittwochs 16 Uhr","16:00","17:00",**kw)
    #~ yield slot("Mittwochs 17 Uhr","17:00","18:00",**kw)
    #~ yield slot("Mittwochs 18 Uhr","18:00","19:00",**kw)
    
    courses = dd.resolve_app('courses')

    yield courses.Line(**babelkw('name',
          de=u"Deutsch Anfänger",
          fr=u"Allemand débutants",
          en=u"German beginners",
          ))
    yield courses.Line(**babelkw('name',
          de=u"Französisch Anfänger",
          fr=u"Français débutants",
          en=u"French beginners",
          ))
          
