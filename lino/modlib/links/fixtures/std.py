# -*- coding: UTF-8 -*-
## Copyright 2009-2011 Luc Saffre
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
from django.conf import settings

from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType

from lino.utils.instantiator import Instantiator
from lino.utils.babel import babel_values, DEFAULT_LANGUAGE, AVAILABLE_LANGUAGES
from lino.tools import resolve_model,UnresolvedModel



def objects():
    Person = resolve_model('contacts.Person')
    Company = resolve_model('contacts.Company')
    if not isinstance(Company,UnresolvedModel):
        roletype = Instantiator('links.LinkType',
            a_type=ContentType.objects.get_for_model(Company),
            b_type=ContentType.objects.get_for_model(Person)
            ).build
        yield roletype(**babel_values('name',en="Manager",fr=u'Gérant',de=u"Geschäftsführer",et=u"Manager"))
        yield roletype(**babel_values('name',en="Director",fr=u'Directeur',de=u"Direktor",et=u"Direktor"))
        yield roletype(**babel_values('name',en="Secretary",fr=u'Sécrétaire',de=u"Sekretär",et=u"Sekretär"))
        yield roletype(**babel_values('name',en="IT Manager",fr=u'Gérant informatique',de=u"EDV-Manager",et=u"IT manager"))
