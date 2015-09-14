# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Choicelists for `lino.modlib.accounts`.

"""

from __future__ import unicode_literals


from django.db import models
from lino.api import dd, rt, _

from .fields import DebitOrCreditField
from .utils import DEBIT, CREDIT


class AccountChart(dd.Choice):
    """An **account chart** is a collection of accounts which are
    considered a whole. See also :class:`AccountCharts`.

    """
    def get_account_by_ref(self, ref):
        Account = rt.modules.accounts.Account
        try:
            #~ print 20121203, dict(ref=account,chart=self.journal.chart)
            return Account.objects.get(ref=ref, chart=self)
        except Account.DoesNotExist:
            raise Warning("No account with reference %r" % ref)


class AccountCharts(dd.ChoiceList):
    """The global list of account charts available in this application.
    In normal applications there is one single account chart named
    :attr:`default`.

    .. attribute:: default

        The default account chart.

    """
    verbose_name = _("Account Chart")
    verbose_name_plural = _("Account Charts")
    item_class = AccountChart
    required_roles = dd.required(dd.SiteStaff)

    detail_layout = """
    name
    GroupsByChart
    """

AccountCharts.add_item("default", _("Default"), 'default')


class Sheet(object):

    """
    Base class for a financial statement.
    """
    # Comptes annuels Jahresabschluss Jaarverslag  Aastaaruanne
    verbose_name = _("Financial statement")

    @classmethod
    def account_types(cls):
        """
        Return a list the top-level account types included in this Sheet
        """
        return [o for o in AccountTypes.objects()
                if o.sheet == cls and o.top_level]


class Balance(Sheet):

    """In financial accounting, a balance sheet or statement of financial
    position is a summary of the financial balances of an
    organisation.

    Assets, liabilities and ownership equity are listed as of a
    specific date, such as the end of its financial year.  A balance
    sheet is often described as a "snapshot of a company's financial
    condition".  Of the four basic financial statements, the balance
    sheet is the only statement which applies to a single point in
    time of a business' calendar year.

    A standard company balance sheet has three parts: assets,
    liabilities and ownership equity. The main categories of assets
    are usually listed first, and typically in order of
    liquidity. Assets are followed by the liabilities. The difference
    between the assets and the liabilities is known as equity or the
    net assets or the net worth or capital of the company and
    according to the accounting equation, net worth must equal assets
    minus liabilities.

    https://en.wikipedia.org/wiki/Balance_sheet

    """
    verbose_name = _("Balance sheet")  # Bilan  Bilanz  Balans  Bilanss


class Earnings(Sheet):

    """
    https://en.wikipedia.org/wiki/Statement_of_comprehensive_income#Requirements_of_IFRS
    """
    # Compte de résultat Gewinn- und Verlustrechnung
    # Winst-en-verliesrekening ...
    verbose_name = _("Profit & Loss statement")


class CashFlow(Sheet):
    verbose_name = _("Cash flow statement")

# La balance des comptes (généraux|particuliers|fournisseurs|clients)


class AccountsBalance(Sheet):
    verbose_name = _("Cash flow statement")


Sheet.objects = (Balance, Earnings, CashFlow)


class AccountType(dd.Choice):
    """The base class for all **account types**."""
    top_level = True
    sheet = None
    #~ def __init__(self,value,text,name,dc=True,**kw):
        #~ self.dc = dc
        #~ super(AccountType,self).__init__(value,text,name)

    def __init__(self):
        pass
        #~ self.dc = dc
        #~ super(AccountType,self).__init__(value,text,name)


class Assets(AccountType):
    value = 'A'
    text = _("Assets")   # Aktiva, Anleihe, Vermögen, Anlage
    name = "assets"
    dc = DEBIT
    sheet = Balance


class Liabilities(AccountType):
    value = 'L'
    text = _("Liabilities")  # Guthaben, Schulden, Verbindlichkeit
    name = "liabilities"
    dc = CREDIT
    sheet = Balance


class Capital(AccountType):  # aka Owner's Equities
    value = 'C'
    text = _("Capital")  # Kapital
    name = "capital"
    dc = CREDIT
    sheet = Balance


class Income(AccountType):
    value = 'I'
    text = _("Incomes")  # Gain/Revenue     Einnahmen  Produits
    name = "incomes"
    dc = CREDIT
    balance_sheet = True
    sheet = Earnings


class Expenses(AccountType):
    value = 'E'
    text = _("Expenses")  # Loss/Cost       Ausgaben   Charges
    name = "expenses"
    dc = DEBIT
    sheet = Earnings


class BankAccounts(Assets):
    top_level = False
    value = 'B'
    text = _("Bank accounts")
    name = 'bank_accounts'
    #~ dc = CREDIT


class AccountTypes(dd.ChoiceList):
    """The global list of account types. See :class:`AccountType`."""
    verbose_name = _("Account Type")
    item_class = AccountType
    column_names = 'value name text dc sheet'

    @dd.virtualfield(DebitOrCreditField(_("D/C")))
    def dc(cls, choice, ar):
        return choice.dc

    @dd.virtualfield(models.CharField(_("Sheet"), max_length=20))
    def sheet(cls, choice, ar):
        return choice.sheet.__name__


add = AccountTypes.add_item
add = AccountTypes.add_item_instance
add(Assets())
add(Liabilities())
add(Income())
add(Expenses())
add(Capital())
add(BankAccounts())


