# -*- coding: UTF-8 -*-
## Copyright 2012-2013 Luc Saffre
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

"""
Creates minimal accounting demo data:

- a minimal accounts chart
- some journals


"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


import datetime
#~ from datetime import timedelta as delta
from dateutil.relativedelta import relativedelta as delta

from decimal import Decimal

from django.conf import settings
from lino.utils import Cycler
from north.dbutils import babel_values
from lino import dd
accounts = dd.resolve_app('accounts')
vat = dd.resolve_app('vat')
sales = dd.resolve_app('sales')
ledger = dd.resolve_app('ledger')
finan = dd.resolve_app('finan')
declarations = dd.resolve_app('declarations')
#~ partners = dd.resolve_app('partners')
notes = dd.resolve_app('notes')

current_group = None


def objects():
    if notes:
        NoteType = dd.resolve_model('notes.NoteType')
        yield NoteType(
            template="Letter.odt",
            build_method="appyodt",
            body_template="payment_reminder.body.html",
            **babel_values('name',
                en="Payment reminder",
                fr="Rappel de paiement",
                de="Zahlungserinnerung"))
        
    chart  = accounts.Chart(**babel_values('name',
        en="Minimal Accounts Chart",
        fr="Plan comptable réduit",
        de="Reduzierter Kontenplan"))
    yield chart
    #~ account = Instantiator(accounts.Account,"ref name").build
    def Group(ref,type,fr,de,en):
        global current_group
        current_group = accounts.Group(
          chart=chart,
          ref=ref,
          account_type=accounts.AccountTypes.get_by_name(type),
          **babel_values('name',de=de,fr=fr,en=en))
        return current_group
          
    def Account(ref,type,fr,de,en,**kw):
        kw.update(babel_values('name',de=de,fr=fr,en=en))
        return accounts.Account(
          chart=chart,
          group=current_group,
          ref=ref,
          type=accounts.AccountTypes.get_by_name(type),
          **kw)
          
    yield Group('10','capital',"Capital","Kapital","Capital")
    
    yield Group('40','assets',  "Créances commerciales", "Forderungen aus Lieferungen und Leistungen", "Commercial receivable(?)")
    
    obj = Account('customers','assets',"Clients","Kunden","Customers",clearable=True) # PCMN 4000
    yield obj
    if sales:
        settings.SITE.site_config.update(clients_account=obj)
    
    obj = Account('suppliers','liabilities',"Fournisseurs","Lieferanten","Suppliers",clearable=True) # PCMN 4400
    yield obj
    if vat:
        settings.SITE.site_config.update(suppliers_account=obj)
    
    yield Group('45','assets',"TVA à payer","Geschuldete MWSt","VAT to pay") # PCMN 451
    obj = Account('vat_due','incomes',u"TVA due",u"MWSt zu regularisieren","VAT due",clearable=True) # PCMN 4510
    yield obj
    if sales:
        settings.SITE.site_config.update(sales_vat_account=obj)
    
    obj = Account('vat_deductible','assets',"TVA déductible",
        "Geschuldete MWSt","VAT deductible",clearable=True) # PCMN 4512
    yield obj
    if ledger:
        settings.SITE.site_config.update(purchases_vat_account=obj)
    
    yield Group('55','assets',u"Institutions financières",u"Finanzinstitute","Banks") # PCMN 55
    yield Account('bestbank','bank_accounts',u"Bestbank",u"Bestbank","Bestbank") 
    yield Account('cash','bank_accounts',u"Cash",u"Cash","Cash") 
    yield Account('bestbankpo','bank_accounts',"Ordres de paiement Bestbank",
        "Zahlungsaufträge Bestbank","Payment Orders Bestbank",clearable=True) 
    
    # TODO: use another account type than bank_accounts:
    yield Account('vatdcl','bank_accounts',u"VAT",u"VAT","VAT") 
    
    yield Group('6','expenses',u"Charges",u"Aufwendungen","Expenses") # 
    yield Account('products','expenses',
        u"Achat de marchandise",u"Wareneinkäufe","Purchase of goods",
        purchases_allowed=True) # PCMN 6040
    yield Account('services','expenses',
        "Services et biens divers","Dienstleistungen","Purchase of services",
        purchases_allowed=True) 
    yield Account('investments','expenses',
        "Investissements","Anlagen","Purchase of investments",
        purchases_allowed=True) 
    
    yield Group('7','incomes',u"Produits",u"Erträge","Revenues") 
    obj = Account('sales','incomes',
        "Ventes","Verkäufe","Sales",
        sales_allowed=True) # PCMN 7000
    yield obj
    if sales:
        settings.SITE.site_config.update(sales_account=obj)
        

    if sales:
        MODEL = sales.Invoice
        #~ yield sales.Orders.create_journal("VKR",'sales',name=u"Aufträge")
    else:
        MODEL = ledger.AccountInvoice
    kw = babel_values('name',de="Verkaufsrechnungen",fr="Factures vente",en="Sales invoices",et="Müügiarved")
    yield MODEL.create_journal('sales',ref="S",chart=chart,**kw)
          
    yield ledger.AccountInvoice.create_journal('purchases',
        chart=chart,
        ref="P",
        **babel_values('name',
            de="Einkaufsrechnungen",fr="Factures achat",en="Purchase invoices",et="Ostuarved"))
            
    if finan:
        yield finan.BankStatement.create_journal(chart=chart,name="Bestbank",account='bestbank',ref="B")
        kw = babel_values('name',de="Zahlungsaufträge",fr="Ordres de paiement",en="Payment Orders",et="Maksekorraldused")
        yield finan.PaymentOrder.create_journal('purchases',chart=chart,account='bestbankpo',ref="PO",**kw)
        yield finan.BankStatement.create_journal(chart=chart,name="Cash",account='cash',ref="C")
        yield finan.JournalEntry.create_journal(chart=chart,name="Miscellaneous Journal Entries",ref="M",dc=accounts.DEBIT)

    if declarations:
        yield declarations.Declaration.create_journal(chart=chart,name=u"VAT declarations",ref="V",account='vatdcl')

