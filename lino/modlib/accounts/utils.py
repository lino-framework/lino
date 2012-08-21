# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

ur"""
Lino has a hard-coded list of the five 
basic "account types" or "top-level accounts".

An accounting transaction is either Debit or Credit.
We represent this internally as a boolean, but define two names DEBIT and CREDIT:

>>> DEBIT
True
>>> CREDIT
False

Accounting Equation:

  Assets = Liabilities + Capital
 
Expanded accounting equation: 

    Assets + Expenses = Liabilities + Equity + Revenue
    
Accounts on the left side of the equation (Assets and Expenses) 
are normally DEBITed and have DEBIT balances. 

That's what the :attr:`dc <AccountType.dc>` attribute means.


>>> print unicode(DC[AccountTypes.asset.dc])
Debit
>>> print unicode(DC[AccountTypes.expense.dc])
Debit





Provisions pour risques et charges : Gesetzliche Rücklagen.
Créances et dettes : Kredite, Anleihen, Schulden.

- "Actif = Passif"
- A liability is capital acquired from others 
- Passiva is synonym for "Liabilities + Capital" in this context




  
`Wikipedia <http://en.wikipedia.org/wiki/Debits_and_credits>`_ gives a 
Summary table of standard increasing and decreasing attributes for the five 
accounting elements:

  ============= ===== ======
  ACCOUNT TYPE	DEBIT	CREDIT
  ============= ===== ======
  Asset	        +	    −
  Liability	    −	    +
  Income	      −	    +
  Expense	      +	    −
  Equity	      −	    +      
  ============= ===== ======
  
The equivalent in Lino code is:

>>> for t in AccountTypes.items(): #doctest: +NORMALIZE_WHITESPACE
...     print "%-10s|%-15s|%-6s" % (t.name, unicode(t), DC[t.dc])
asset     |Assets         |Debit
liability |Liabilities    |Credit
income    |Incomes        |Credit
expense   |Expenses       |Debit
capital   |Capital        |Credit

Yes.


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



"""

from django.utils.translation import ugettext_lazy as _
from lino.utils.choicelists import Choice,ChoiceList

DEBIT = True
CREDIT = False

DC = { 
  DEBIT: _("Debit"), 
  CREDIT: _("Credit") 
}


class AccountType(Choice):
    def __init__(self,cls,value,text,name,dc=True,**kw):
        self.dc = dc
        super(AccountType,self).__init__(cls,value,text,name)
    
class AccountTypes(ChoiceList):
    label = _("Account Type")
    item_class = AccountType
    
    
add = AccountTypes.add_item
#~ def add(*args):
    #~ AccountTypes.add_item_instance(AccountType(*args))
add('A', _("Assets"),"asset",DEBIT)   # Aktiva, Anleihe, Vermögen, Anlage
add('L', _("Liabilities"),"liability",CREDIT) # Guthaben, Schulden, Verbindlichkeit
add('I', _("Incomes"),"income",CREDIT) # Gain/Revenue     Einnahmen  Produits
add('E', _("Expenses"),"expense",DEBIT) # Loss/Cost       Ausgaben   Charges
add('C', _("Capital"),"capital",CREDIT)  # Kapital owner's Equities


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

