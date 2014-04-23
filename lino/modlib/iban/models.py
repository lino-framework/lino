# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
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
:xfile:`models.py` module for the :mod:`lino.modlib.sepa` app.

Defines the :class:`EventType` and :class:`Event` models and their tables.

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino import dd

from .fields import IBANField, BICField

dd.inject_field(
    'contacts.Partner', 'iban', IBANField(_("IBAN"), blank=True))
dd.inject_field(
    'contacts.Partner', 'bic', BICField(_("BIC"), blank=True))


