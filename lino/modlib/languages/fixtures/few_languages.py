# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.
"""
Adds an arbitrary selection of a few demo languages.
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from lino.utils.instantiator import Instantiator
from lino import dd


def objects():

    Language = Instantiator('languages.Language', "id").build

    yield Language('ger', **dd.str2kw('name', _("German")))
    yield Language('fre', **dd.str2kw('name', _("French")))
    yield Language('eng', **dd.str2kw('name', _("English")))
    yield Language('dut', **dd.str2kw('name', _("Dutch")))
    yield Language('est', **dd.str2kw('name', _("Estonian")))
