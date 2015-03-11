==========================
Introduction to accounting
==========================

This chapter explains some basic truths about accounting as seen by a
Lino application developer.

    When designing an accounting package, the programmer operates as a
    mediator between people having different ideas: how it must
    operate, how its reports must appear, and how it must conform to
    the tax laws. By contrast, an operating system is not limited by
    outside appearances. When designing an operating system, the
    programmer seeks the simplest harmony between machine and
    ideas. This is why an operating system is easier to design.  
    
    -- Tao of programming


About this document
-------------------

This document is part of the Lino test suite. You can test only this
document by issuing::

  $ python setup.py test -s tests.DocsTests.test_accounting

General stuff:

>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.presto.settings.doctests'
>>> from lino.api.doctest import *
>>> from lino.modlib.accounts.utils import *
>>> from lino.modlib.accounts.fields import *
>>> from lino.modlib.accounts.choicelists import *


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

Lino has a hard-coded list of "account types", including the
"top-level accounts".

Accounting Equation:

  Assets = Liabilities + Capital
 
Expanded accounting equation:

    Assets + Expenses = Liabilities + Equity + Revenue
    
Accounts on the left side of the equation (Assets and Expenses) are
normally DEBITed and have DEBIT balances.  That's what the :attr:`dc
<AccountType.dc>` attribute means:


>>> print(unicode(DCLABELS[AccountTypes.assets.dc]))
Debit
>>> print(unicode(DCLABELS[AccountTypes.expenses.dc]))
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

It has a hard-coded list of the Sheets used in annual accounting
reports.

The class :class:`Sheet` represents the basic financial statements
which every accounting package should implement.

Lino currently defines three types of financial statements and defines
one class for each of them.

These classes are not meant to be instantiated, they are just Lino's
suggestion for a standardized vocabulary.

>>> print Sheet.objects
(<class 'lino.modlib.accounts.choicelists.Balance'>, <class 'lino.modlib.accounts.choicelists.Earnings'>, <class 'lino.modlib.accounts.choicelists.CashFlow'>)

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

>>> from lino.api import rt
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


