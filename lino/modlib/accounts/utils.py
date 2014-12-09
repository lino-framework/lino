# -*- coding: UTF-8 -*-
# Copyright 2012-2013 Luc Saffre
# License: BSD (see file COPYING for details)

r"""This module is a Python implementation of some basic truths of
accounting.

This module is part of the Lino test suite. You can test only this
module by issuing::

  $ python setup.py test -s tests.UtilsTests.test_accounts_utils

It has a hard-coded list of `account types`_, including the "top-level
accounts".

It has a hard-coded list of the Sheets used in annual accounting
reports.

Debit and Credit
----------------

An accounting transaction is either Debit or Credit.  We represent
this internally as a boolean, but define two names `DEBIT` and
`CREDIT`:

>>> DEBIT
True
>>> CREDIT
False

Account types
-------------

Accounting Equation:

  Assets = Liabilities + Capital
 
Expanded accounting equation:

    Assets + Expenses = Liabilities + Equity + Revenue
    
Accounts on the left side of the equation (Assets and Expenses) are
normally DEBITed and have DEBIT balances.  That's what the :attr:`dc
<AccountType.dc>` attribute means:


>>> print unicode(DCLABELS[AccountTypes.assets.dc])
Debit
>>> print unicode(DCLABELS[AccountTypes.expenses.dc])
Debit

>>> print isinstance(AccountTypes.bank_accounts,Assets)
True


`Wikipedia <http://en.wikipedia.org/wiki/Debits_and_credits>`_ gives a
Summary table of standard increasing and decreasing attributes for the
five accounting elements:

============= ===== ======
ACCOUNT TYPE  DEBIT CREDIT
============= ===== ======
Asset         \+    \−
Liability     \−    \+
Income        \−    \+
Expense       \+    \−
Equity        \−     \+      
============= ===== ======
  
The equivalent in Python is:

>>> for t in AccountTypes.filter(top_level=True):
... #doctest: +NORMALIZE_WHITESPACE
...     print "%-12s|%-15s|%-6s" % (t.name, unicode(t), DCLABELS[t.dc])
assets      |Assets         |Debit
liabilities |Liabilities    |Credit
incomes     |Incomes        |Credit
expenses    |Expenses       |Debit
capital     |Capital        |Credit


The :class:`Sheet` class
------------------------

The class :class:`Sheet` represents the basic financial statements
which every accounting package should implement.

Lino currently defines three types of financial statements and defines 
one class for each of them. 

These classes are not meant to be instantiated, they are just 
my suggestion for a standardized vocabulary.

>>> print Sheet.objects
(<class 'utils.Balance'>, <class 'utils.Earnings'>, <class 'utils.CashFlow'>)

The `verbose_name` is what users see. It is a lazily translated 
string, so we must call `unicode()` to see it:

>>> for s in Sheet.objects:
...     print unicode(s.verbose_name)
Balance sheet
Profit & Loss statement
Cash flow statement

French users will see:

>>> from django.utils import translation
>>> with translation.override('fr'):
...     for s in Sheet.objects:
...         print unicode(s.verbose_name)
Bilan
Compte de résultats
Tableau de financement


The :meth:`Sheet.account_types` method.

Assets, Liabilities and Capital are listed in the Balance Sheet.
Income and Expenses are listed in the Profit & Loss statement.

>>> print Balance.account_types()
[<AccountTypes.assets:A>, <AccountTypes.liabilities:L>, <AccountTypes.capital:C>]

>>> print Earnings.account_types()
[<AccountTypes.incomes:I>, <AccountTypes.expenses:E>]

>>> print CashFlow.account_types()
[]


As a summary here once more this hard-coded table of basic account
types:

>>> from lino import rt
>>> rt.show('accounts.AccountTypes')
==================== =============== =============== ======== ==========
 value                name            text            D/C      Sheet
-------------------- --------------- --------------- -------- ----------
 A                    assets          Assets          Debit    Balance
 L                    liabilities     Liabilities     Credit   Balance
 I                    incomes         Incomes         Credit   Earnings
 E                    expenses        Expenses        Debit    Earnings
 C                    capital         Capital         Credit   Balance
 B                    bank_accounts   Bank accounts   Debit    Balance
 **Total (6 rows)**                                   **3**
==================== =============== =============== ======== ==========
<BLANKLINE>



TODO
----

- The Belgian and French PCMN has 7+1 top-level accounts:

    | CLASSE 0 : Droits & engagements hors bilan
    | CLASSE 1 : Fonds propres, provisions pour risques & charges et Dettes à plus d'un an
    | CLASSE 2 : Frais d'établissement, actifs immobilisés et créances à plus d'un an
    | CLASSE 3 : Stock & commandes en cours d'exécution
    | CLASSE 4 : Créances et dettes à un an au plus
    | CLASSE 5 : Placements de trésorerie et valeurs disponibles
    | CLASSE 6 : Charges
    | CLASSE 7 : Produits
    

  explain the differences and how to solve this.
  See also 

  - http://code.gnucash.org/docs/help/acct-types.html
  - http://www.futureaccountant.com/accounting-process/study-notes/financial-accounting-account-types.php
  

- A Liability is Capital acquired from others. 
  Both together is what French accountants call *passif*.
  
  The accounting equation "Assets = Liabilities + Capital" 
  in French is simply:

      Actif = Passif
      
  I found an excellent definition of these two terms at 
  `plancomptable.com <http://www.plancomptable.com/titre-II/titre-II.htm>`_:

  - Un actif est un élément identifiable du patrimoine ayant une 
    valeur économique positive pour l’entité, c’est-à-dire un élément 
    générant une ressource que l’entité contrôle du fait d’événements 
    passés et dont elle attend des avantages économiques futurs.
  
  - Un passif est un élément du patrimoine ayant une valeur 
    économique négative pour l'entité, c'est-à-dire une obligation de 
    l'entité à l'égard d'un tiers dont il est probable ou certain 
    qu'elle provoquera une sortie des ressources au bénéfice de ce 
    tiers, sans contrepartie au moins équivalente attendue de celui-ci. 
  

Some vocabulary

- Provisions pour risques et charges : Gesetzliche Rücklagen.
- Créances et dettes : Kredite, Anleihen, Schulden.



"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
#~ from lino.utils.choicelists import Choice,ChoiceList
from lino import dd

DEBIT = True
CREDIT = False

DCLABELS = {
    DEBIT: _("Debit"),
    CREDIT: _("Credit")
}


from lino.ui.store import BooleanStoreField
from django.db import models


class DebitOrCreditStoreField(BooleanStoreField):

    """
    This is used as `lino_atomizer_class` for :class:`DebitOrCreditField`.
    """

    def format_value(self, ar, v):
        return unicode(DCLABELS[v])


class DebitOrCreditField(models.BooleanField):

    """A field that stores either :attr:`DEBIT
    <lino.modlib.accounts.utils.DEBIT>` or :attr:`CREDIT
    <lino.modlib.accounts.utils.CREDIT>` (see
    :mod:`lino.modlib.accounts.utils`).

    """
    lino_atomizer_class = DebitOrCreditStoreField

    def __init__(self, *args, **kw):
        kw.setdefault('help_text',
                      _("Debit (checked) or Credit (not checked)"))
        kw.setdefault('default', None)
        models.BooleanField.__init__(self, *args, **kw)


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
        return [o for o in AccountTypes.objects() if o.sheet == cls and o.top_level]


class Balance(Sheet):

    """
    In financial accounting, a 
    balance sheet or 
    statement of financial position 
    is a summary of the financial balances of an organisation.

    Assets, liabilities and ownership equity are listed as of a specific 
    date, such as the end of its financial year. 
    A balance sheet is often described as a "snapshot of a company's 
    financial condition".
    Of the four basic financial statements, the balance sheet is the only 
    statement which applies to a single point in time of a business' calendar year.

    A standard company balance sheet has three parts: assets, 
    liabilities and ownership equity. The main categories of assets are 
    usually listed first, and typically in order of liquidity. Assets 
    are followed by the liabilities. The difference between the assets 
    and the liabilities is known as equity or the net assets or the net 
    worth or capital of the company and according to the accounting 
    equation, net worth must equal assets minus liabilities.

    https://en.wikipedia.org/wiki/Balance_sheet
    
    """
    verbose_name = _("Balance sheet")  # Bilan  Bilanz  Balans  Bilanss


#~ class ProfitOrLoss(Sheet):
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
#~ def add(*args):
    #~ AccountTypes.add_item_instance(AccountType(*args))
add = AccountTypes.add_item_instance
add(Assets())
add(Liabilities())
add(Income())
add(Expenses())
add(Capital())
add(BankAccounts())


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
