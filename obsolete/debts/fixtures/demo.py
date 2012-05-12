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
    group = Instantiator('debts.ItemGroup').build
    g = group(account_type=AccountType.income,**babel_values('name',
          de=u"Monatliche Einkünfte",
          fr=u"Revenus mensuels",
          en=u"Monthly incomes"
          ))
    yield g
    item = Instantiator('debts.Item',group=g).build
    yield item(**babel_values('name',
          de=u"Gehälter",
          fr=u"Salaires",
          en=u"Salaries"
          ))
    yield item(**babel_values('name',
          de=u"Renten",
          fr=u"Pension",
          en=u"Pension"
          ))
    yield item(**babel_values('name',
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
    item = Instantiator('debts.Item',group=g).build
    yield item(**babel_values('name',
          de=u"Urlaubsgeld",
          fr=u"Congé payé",
          en=u""
          ))
    yield item(**babel_values('name',
          de=u"Jahresendzulage",
          fr=u"Prime de fin d'année",
          en=u""
          ))

    g = group(account_type=AccountType.expense,**babel_values('name',
          de=u"Monatliche Ausgaben",
          fr=u"Dépenses mensuelles",
          en=u"Monthly expenses"
          ))
    yield g
    item = Instantiator('debts.Item',group=g).build
    yield item(**babel_values('name',
          de=u"Miete",
          fr=u"Loyer",
          en=u""
          ))
    yield item(**babel_values('name',
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
    item = Instantiator('debts.Item',group=g,yearly=True).build
    yield item(**babel_values('name',
          de=u"Müllsteuer",
          fr=u"Taxe déchets",
          en=u""
          ))

    budget = Instantiator('debts.Budget').build
    from lino.modlib.users.models import User
    root = User.objects.get(username='root')
    
    Family = resolve_model('families.Family')
    for fam in Family.objects.all():
        #~ yield budget(partner_id=118,user=root)
        yield budget(partner=fam,user=root)
        
    Budget = resolve_model('debts.Budget')
    Debt = resolve_model('debts.Debt')
    Company = resolve_model('contacts.Company')
    #~ AMOUNTS = Cycler(10,200,0,30,40,0,0,50)
    AMOUNTS = Cycler([i*5 for i in range(10)])
    PARTNERS = Cycler(Company.objects.all())
    for b in Budget.objects.all():
        n = min(3,b.actor_set.count())
        for e in b.entry_set.all():
            for i in range(n):
                setattr(e,'amount%d'%(i+1),AMOUNTS.pop())
                e.save()
        for i in range(3):
            yield Debt(budget=b,partner=PARTNERS.pop(),amount=AMOUNTS.pop()*5)
