# -*- coding: UTF-8 -*-
## Copyright 2011-2013 Luc Saffre
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
This just adds `inscode` fields to `countries.City` 
and `countries.Country`.

"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import dd


dd.inject_field('countries.City',
    'inscode',
    models.CharField(
        max_length=5,
        verbose_name=_("INS code"),
        blank=True,
        help_text=_("The official code for this place used by statbel.fgov.be")
    ))
        
dd.inject_field('countries.Country',
    'inscode',
    models.CharField(
        max_length=3,
        verbose_name=_("INS code"),
        blank=True,
        help_text=_("The official code for this country used by statbel.fgov.be")
    ))
        
