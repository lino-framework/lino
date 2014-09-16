# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
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
The `std` fixture for `households`
==================================

Adds some :class:`household roles <households.Role>`.

"""

from django.utils.translation import ugettext_lazy as _

from lino import dd


def objects():
    Type = dd.modules.households.Type

    yield Type(**dd.str2kw('name', _("Married couple")))
    # Ehepaar / couple marié

    yield Type(**dd.str2kw('name', _("Divorced couple")))
    # Geschiedene Ehe / Mariage divorcé

    yield Type(**dd.str2kw('name', _("Factual household")))
    # Faktischer Haushalt / Ménage de fait

    yield Type(**dd.str2kw('name', _("Legal cohabitation")))
    # Legale Wohngemeinschaft / Cohabitation légale

    yield Type(**dd.str2kw('name', _("Former household")))
    yield Type(**dd.str2kw('name', _("Other")))
