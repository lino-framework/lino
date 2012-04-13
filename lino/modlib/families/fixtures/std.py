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
The `std` fixture for `families`
================================

Adds some :class:`family roles <families.Role>`.

"""

#~ from django.contrib.contenttypes.models import ContentType
#~ from lino.utils.instantiator import Instantiator, i2d
from lino.tools import resolve_model
from django.utils.translation import ugettext_lazy as _


from django.db import models
from django.conf import settings
from lino.utils.babel import babel_values

Role = resolve_model('families.Role')


def objects():
  
    #~ yield Role(**babel_values('name',
          #~ de=u"Vater",
          #~ fr=u"père",
          #~ en=u"father",
          #~ ))
    #~ yield Role(**babel_values('name',
          #~ de=u"Mutter",
          #~ fr=u"mère",
          #~ en=u"mother",
          #~ ))
    #~ yield Role(**babel_values('name',
          #~ de=u"Tochter",
          #~ fr=u"fille",
          #~ en=u"daughter",
          #~ ))
    #~ yield Role(**babel_values('name',
          #~ de=u"Sohn",
          #~ fr=u"fils",
          #~ en=u"son",
          #~ ))
    
    kw = babel_values('name',
          de=u"Kind",
          fr=u"Enfant",
          en=u"Child",
          )
    kw.update(babel_values('male',
          de=u"Sohn",
          fr=u"Fils",
          en=u"Son",
          ))
    kw.update(babel_values('female',
          de=u"Tochter",
          fr=u"Fille",
          en=u"Daughter",
          ))
    yield Role(**kw)
    
    kw = babel_values('name',
          de=u"Adoptivkind",
          fr=u"Enfant adopté",
          en=u"Adopted child",
          )
    kw.update(babel_values('male',
          de=u"Adoptivsohn",
          fr=u"Fils adoptif",
          en=u"Adopted son",
          ))
    kw.update(babel_values('female',
          de=u"Adoptivtochter",
          fr=u"Fille adoptive",
          en=u"Adopted daughter",
          ))
    yield Role(**kw)
