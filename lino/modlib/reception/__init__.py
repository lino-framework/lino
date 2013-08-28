# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
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
This module is for managing a reception desk and a waiting queue: 
register clients into a waiting queue 
as they present themselves at a reception desk (Empfangsschalter),
and unregister them when they leave again.

User documentation see :ref:`welfare.reception`.

"""
from lino import ad

from django.utils.translation import ugettext_lazy as _
#~ def _(s): return s

class App(ad.App):
    verbose_name = _("Reception")
    depends = ['cal']
    
