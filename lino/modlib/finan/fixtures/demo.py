# -*- coding: UTF-8 -*-
## Copyright 2009-2011 Luc Saffre
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

#import time
#from datetime import date
#from dateutil import parser as dateparser
#from lino.apps.finan import models as finan
import decimal
from lino.utils.instantiator import Instantiator, i2d
from lino.tools import resolve_model

#from lino.apps.ledger import models as ledger
#from lino.apps.contacts import models as contacts
#from lino.apps.journals import models as journals
#from lino.apps.ledger.fixtures import be

from lino import reports
#contacts = reports.get_app('contacts')
ledger = reports.get_app('ledger')
finan = reports.get_app('finan')

#~ Company = resolve_model('contacts.Company')
Contact = resolve_model('contacts.Contact')

def objects():
    ba = ledger.Account.objects.get(match="5500")
    #BANK = journals.get_journal_by_docclass(finan.BankStatement)
    BANK = finan.BankStatement.create_journal(
        "BANK",account=ba,name="FirstAndOnly Bank")
    yield BANK
    
    EL = ledger.Account.objects.get(match='61202')
    IN = ledger.Account.objects.get(match='61211')
    PR = ledger.Account.objects.get(match='4400')
    
    doc = BANK.create_document(
      date=i2d(20090501),
      balance1=decimal.Decimal('1056.40'))
    doc.add_item(
      account=PR,
      contact=Contact.objects.all()[0],
      debit='12.49')
    doc.book()
    yield doc
    