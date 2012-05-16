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

import decimal
from dateutil.relativedelta import relativedelta
ONE_DAY = relativedelta(days=1)

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _


from lino.utils import i2d
from lino.utils.instantiator import Instantiator
from lino.tools import resolve_model
from lino.utils.babel import babel_values

from lino.modlib.debts.models import AccountType
    
def objects():
    group = Instantiator('debts.AccountGroup').build
    g = group(account_type=AccountType.income,**babel_values('name',
          de=u"Monatliche Einkünfte",
          fr=u"Revenus mensuels",
          en=u"Monthly incomes"
          ))
    yield g
    account = Instantiator('debts.Account',group=g).build
    yield account(required_for_person=True,**babel_values('name',
          de=u"Gehälter",
          fr=u"Salaires",
          en=u"Salaries"
          ))
    yield account(required_for_person=True,**babel_values('name',
          de=u"Renten",
          fr=u"Pension",
          en=u"Pension"
          ))
    yield account(required_for_person=True,**babel_values('name',
          de=u"Integrationszulage",
          fr=u"Allocation d'intégration",
          en=u"Integration aid"
          ))

    g = group(account_type=AccountType.income,**babel_values('name',
          de=u"Jährliche Einkünfte",
          fr=u"Revenus annuels",
          en=u"Yearly incomes"
          ))
    yield g
    account = Instantiator('debts.Account',group=g).build
    yield account(required_for_person=True,**babel_values('name',
          de=u"Urlaubsgeld",
          fr=u"Congé payé",
          en=u"Paid holiday"
          ))
    yield account(required_for_person=True,**babel_values('name',
          de=u"Jahresendzulage",
          fr=u"Prime de fin d'année",
          en=u"Year-end prime"
          ))

    g = group(account_type=AccountType.expense,**babel_values('name',
          de=u"Monatliche Ausgaben",
          fr=u"Dépenses mensuelles",
          en=u"Monthly expenses"
          ))
    yield g
    account = Instantiator('debts.Account',group=g).build
    yield account(required_for_household=True,**babel_values('name',
          de=u"Miete",
          fr=u"Loyer",
          en=u"Rent"
          ))
    yield account(required_for_household=True,**babel_values('name',
          de=u"Strom",
          fr=u"Electricité",
          en=u"Electricity"
          ))


    g = group(account_type=AccountType.expense,**babel_values('name',
          de=u"Steuern",
          fr=u"Taxes",
          en=u"Taxes"
          ))
    yield g
    account = Instantiator('debts.Account',group=g,periods=12).build
    yield account(required_for_household=True,**babel_values('name',
          de=u"Müllsteuer",
          fr=u"Taxe déchets",
          en=u"Waste tax"
          ))

    g = group(account_type=AccountType.asset,**babel_values('name',
          de=u"Aktiva, Vermögen, Kapital",
          fr=u"Actifs",
          en=u"Assets"
          ))
    yield g
    account = Instantiator('debts.Account',group=g).build
    yield account(**babel_values('name',
          de=u"Vermögen",
          fr=u"Propriété",
          en=u"Assets"
          ))
    account = Instantiator('debts.Account',group=g).build
    yield account(**babel_values('name',
          de=u"Haus",
          fr=u"Maison",
          en=u"House"
          ))
    yield account(**babel_values('name',
          de=u"Auto",
          fr=u"Voiture",
          en=u"Car"
          ))
    
    
    g = group(account_type=AccountType.liability,**babel_values('name',
          de=u"Guthaben, Schulden, Verbindlichkeit",
          fr=u"Créances et dettes",
          en=u"Liabilities"
          ))
    yield g
    account = Instantiator('debts.Account',group=g).build
    yield account(**babel_values('name',
          de=u"Kredite",
          fr=u"Crédits",
          en=u"Loans"
          ))
    yield account(**babel_values('name',
          de=u"Schulden",
          fr=u"Emprunts",
          en=u"Debts"
          ))
    yield account(**babel_values('name',
          de=u"Gerichtsvollzieher",
          fr=u"Juge",
          en=u"Judge"
          ))
    yield account(**babel_values('name',
          de=u"Zahlungsrückstände",
          fr=u"Factures à payer",
          en=u"Invoices to pay"
          ))

    #~ budget = Instantiator('debts.Budget').build
    from lino.modlib.users.models import User
    root = User.objects.get(username='root')
    
    Household = resolve_model('households.Household')
    Budget = resolve_model('debts.Budget')
    Actor = resolve_model('debts.Actor')
    for hh in Household.objects.all():
        #~ sub_budgets = []
        for p in hh.member_set.all():
            yield Budget(partner_id=p.person.id,user=root)
            #~ sub_budgets.append(b)
            #~ yield b
        yield Budget(partner_id=hh.id,user=root)
        #~ yield b
        #~ for sb in sub_budgets:
            #~ yield Actor(budget=b,sub_budget=sb)
        
    Budget = resolve_model('debts.Budget')
    #~ Debt = resolve_model('debts.Debt')
    Entry = resolve_model('debts.Entry')
    Account = resolve_model('debts.Account')
    Company = resolve_model('contacts.Company')
    AMOUNTS = Cycler([i*5.24 for i in range(10)])
    PARTNERS = Cycler(Company.objects.all())
    ACCOUNTS = Cycler(Account.objects.filter(type=AccountType.liability))
    for b in Budget.objects.all():
        #~ n = min(3,b.actor_set.count())
        for e in b.entry_set.all():
            #~ for i in range(n):
            e.amount = AMOUNTS.pop()
            e.save()
        for i in range(3):
            a = int(AMOUNTS.pop()*5)
            yield Entry(budget=b,
                account=ACCOUNTS.pop(),
                partner=PARTNERS.pop(),amount=a,
                monthly_rate=decimal.Decimal("%.2d" % (a/20)))
