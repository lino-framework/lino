# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.sepa`.

Defines the :class:`EventType` and :class:`Event` models and their tables.

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino.api import dd

from .fields import IBANField, BICField

dd.inject_field(
    'contacts.Partner', 'iban', IBANField(_("IBAN"), blank=True))
dd.inject_field(
    'contacts.Partner', 'bic', BICField(_("BIC"), blank=True))


