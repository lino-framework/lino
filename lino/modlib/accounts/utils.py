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


>>> print unicode(DC[AccountTypes.assets.dc])
Debit
>>> print unicode(DC[AccountTypes.expenses.dc])
Debit

>>> print isinstance(AccountTypes.bank_accounts,Assets)
True


  
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

>>> for t in AccountTypes.filter(top_level=True): #doctest: +NORMALIZE_WHITESPACE
...     print "%-12s|%-15s|%-6s" % (t.name, unicode(t), DC[t.dc])
assets      |Assets         |Debit
liabilities |Liabilities    |Credit
incomes     |Incomes        |Credit
expenses    |Expenses       |Debit
capital     |Capital        |Credit


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

  - Un actif est un élément identifiable du patrimoine ayant une valeur économique positive pour l’entité, c’est-à-dire un élément générant une ressource que l’entité contrôle du fait d’événements passés et dont elle attend des avantages économiques futurs.
  
  - Un passif est un élément du patrimoine ayant une valeur économique négative pour l'entité, c'est-à-dire une obligation de l'entité à l'égard d'un tiers dont il est probable ou certain qu'elle provoquera une sortie des ressources au bénéfice de ce tiers, sans contrepartie au moins équivalente attendue de celui-ci. 
  

Some vocabulary

- Provisions pour risques et charges : Gesetzliche Rücklagen.
- Créances et dettes : Kredite, Anleihen, Schulden.



"""

from django.utils.translation import ugettext_lazy as _
#~ from lino.utils.choicelists import Choice,ChoiceList
from lino import dd

DEBIT = True
CREDIT = False

DC = { 
  DEBIT: _("Debit"), 
  CREDIT: _("Credit") 
}


class AccountType(dd.Choice):
    top_level = True
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
    name  = "assets"
    dc = DEBIT

class Liabilities(AccountType):
    value = 'L'
    text = _("Liabilities") # Guthaben, Schulden, Verbindlichkeit  
    name  = "liabilities"
    dc = CREDIT

class Income(AccountType):
    value = 'I'
    text = _("Incomes") # Gain/Revenue     Einnahmen  Produits
    name  = "incomes" 
    dc = CREDIT

class Expenses(AccountType):
    value = 'E' 
    text = _("Expenses") # Loss/Cost       Ausgaben   Charges
    name = "expenses"
    dc = DEBIT

class Capital(AccountType):
    value = 'C' 
    text = _("Capital") # Kapital owner's Equities
    name = "capital"
    dc = CREDIT

class BankAccounts(Assets):
    top_level = False
    value = 'B'
    text = _("Bank accounts")
    name = 'bank_accounts'
    #~ dc = CREDIT    
    
    
    
    
class AccountTypes(dd.ChoiceList):
    verbose_name = _("Account Type")
    item_class = AccountType
    
    
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
#~ add('A', _("Assets"),"asset",DEBIT)   # Aktiva, Anleihe, Vermögen, Anlage
#~ add('L', _("Liabilities"),"liability",CREDIT) # Guthaben, Schulden, Verbindlichkeit
#~ add('I', _("Incomes"),"income",CREDIT) # Gain/Revenue     Einnahmen  Produits
#~ add('E', _("Expenses"),"expense",DEBIT) # Loss/Cost       Ausgaben   Charges
#~ add('C', _("Capital"),"capital",CREDIT)  # Kapital owner's Equities


#~ AccountTypes.add_item_instance(BankAccounts())


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

