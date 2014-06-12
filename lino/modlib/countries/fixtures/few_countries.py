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
Adds an arbitrary selection of a few demo countries.
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino import dd

Country = dd.resolve_model('countries.Country')


def objects():

    def country(isocode, **kw):
        try:
            return Country.objects.get(isocode=isocode)
        except Country.DoesNotExist:
            return Country(isocode=isocode, **kw)

    yield country('EE', **dd.str2kw(_("Estonia"), 'name'))
    yield country('BE', **dd.str2kw(_("Belgium"), 'name'))
    yield country('DE', **dd.str2kw(_("Germany"), 'name'))
    yield country('FR', **dd.str2kw(_("France"), 'name'))
    yield country('NL', **dd.str2kw(_("Netherlands"), 'name'))
    yield country('MA', **dd.str2kw(_("Maroc"), 'name'))
    yield country('RU', **dd.str2kw(_("Russia"), 'name'))
    yield country('CD', **dd.str2kw(_("Congo (Democratic Republic)"), 'name'))
