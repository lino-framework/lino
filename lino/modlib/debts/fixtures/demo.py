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

def n2dec(v):
    return decimal.Decimal("%.2d" % v)
   
def objects():
    
    User = resolve_model('users.User')
    kerstin = User(username="kerstin",
        first_name="Kerstin",last_name=u"Küpper",
        level=UserLevel.user,
        debts_level=UserLevel.user)
    yield kerstin
    
    
    Household = resolve_model('households.Household')
    Budget = resolve_model('debts.Budget')
    Actor = resolve_model('debts.Actor')
    for hh in Household.objects.all():
        yield Budget(partner_id=hh.id,user=kerstin)
        
    Budget = resolve_model('debts.Budget')
    Entry = resolve_model('debts.Entry')
    Account = resolve_model('debts.Account')
    Company = resolve_model('contacts.Company')
    AMOUNTS = Cycler([i*5.24 for i in range(10)])
    PARTNERS = Cycler(Company.objects.all())
    LIABILITIES = Cycler(Account.objects.filter(type=AccountType.liability))
    for b in Budget.objects.all():
        #~ n = min(3,b.actor_set.count())
        for e in b.entry_set.all():
            #~ for i in range(n):
            if e.account.required_for_household:
                e.amount1 = n2dec(AMOUNTS.pop())
            if e.account.required_for_person:
                e.amount2 = n2dec(AMOUNTS.pop())
                e.amount3 = n2dec(AMOUNTS.pop())
            e.save()
        for i in range(5):
            a = int(AMOUNTS.pop()*5)
            yield Entry(budget=b,
                account=LIABILITIES.pop(),
                partner=PARTNERS.pop(),
                amount1=a,
                monthly_rate=n2dec(a/20))
    
    