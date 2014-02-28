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

import logging
logger = logging.getLogger(__name__)

import datetime

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

from django_iban.fields import IBANField, SWIFTBICField

from lino import dd


class AccountTypes(dd.ChoiceList):
    verbose_name = _("Account type")
    verbose_name_plural = _("Account types")
add = AccountTypes.add_item

add("01", _("Giro"), 'giro')
add("02", _("Savings"), 'savings')
add("03", _("Other"), 'other')


class Account(dd.Model):
    class Meta:
        abstract = dd.is_abstract_model('sepa.Account')
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    partner = dd.ForeignKey('contacts.Partner')
    iban = IBANField()
    bic = SWIFTBICField()
    # account_type = dd.ForeignKey('sepa.AccountType')
    account_type = AccountTypes.field(default=AccountTypes.giro)


class Accounts(dd.Table):
    model = 'sepa.Account'


class AccountsByPartner(Accounts):
    master_key = 'partner'
    column_names = 'account_type iban bic managed'
    order_by = ['iban']
    auto_fit_column_widths = True
