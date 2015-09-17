# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Tables for `lino.modlib.sepa`.

"""

from __future__ import unicode_literals

from lino.api import dd
from lino.modlib.contacts.roles import ContactsUser, ContactsStaff
from lino.api import dd, _, rt


class AccountsDetail(dd.FormLayout):
    main = "general"

    general = dd.Panel("""
    partner:30 iban:40 bic:20 remark:15
    sepa.StatementsByAccount
    """, label=_("Account"))


class Accounts(dd.Table):
    required_roles = dd.login_required(ContactsStaff)
    model = 'sepa.Account'
    detail_layout = AccountsDetail()


class AccountsByPartner(Accounts):
    required_roles = dd.login_required(ContactsStaff)
    master_key = 'partner'
    column_names = 'iban bic remark primary *'
    order_by = ['iban']
    auto_fit_column_widths = True


class StatementDetail(dd.FormLayout):
    main = "general"

    general = dd.Panel("""
    account:30 date:40 statement_number:20 balance_start:15
    sepa.MovementsByStatement
    """, label=_("Statement"))


class Statements(dd.Table):
    required_roles = dd.login_required(ContactsStaff)
    model = 'sepa.Statement'
    column_names = 'account date statement_number balance_start balance_end *'
    order_by = ["date"]
    detail_layout = StatementDetail()
    auto_fit_column_widths = True

    # insert_layout = dd.FormLayout("""
    # account date
    # statement_number
    # balance_start balance_end
    # """, window_size=(60, 'auto'))


class StatementsByAccount(Statements):
    required_roles = dd.login_required(ContactsUser)
    master_key = 'account'
    column_names = 'date date_done statement_number balance_end'
    auto_fit_column_widths = True


class Movements(dd.Table):
    required_roles = dd.login_required(ContactsStaff)
    model = 'sepa.Movement'


class MovementsByStatement(Movements):
    required_roles = dd.login_required(ContactsUser)
    master_key = 'statement'
    column_names = 'movement_date amount partner bank_account ref'
    auto_fit_column_widths = True
