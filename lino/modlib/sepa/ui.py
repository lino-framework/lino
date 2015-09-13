# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Tables for `lino.modlib.sepa`.

"""

from __future__ import unicode_literals

from lino.api import dd
from lino.modlib.contacts.roles import ContactsUser, ContactsStaff


class Accounts(dd.Table):
    required_roles = dd.login_required(ContactsStaff)
    model = 'sepa.Account'


class AccountsByPartner(Accounts):
    required_roles = dd.login_required(ContactsUser)
    master_key = 'partner'
    column_names = 'iban bic remark primary *'
    order_by = ['iban']
    auto_fit_column_widths = True

class Statements(dd.Table):
    required_roles = dd.login_required(ContactsStaff)
    model = 'sepa.Statement'

class Movements(dd.Table):
    required_roles = dd.login_required(ContactsStaff)
    model = 'sepa.Movement'

