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
My personal attempt to create a "universal account chart".
To be used for simple demo setups in different countries.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


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

partner_model = settings.SITE.partners_app_label + '.Partner'

current_group = None

REQUEST = None


def objects():
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
    
    obj = Account('customers','assets',u"Clients",u"Kunden","Customers") # PCMN 4000
    yield obj
    if sales:
        settings.SITE.site_config.update(clients_account=obj)
    
    obj = Account('suppliers','liabilities',u"Fournisseurs",u"Lieferanten","Suppliers") # PCMN 4400
    yield obj
    if vat:
        settings.SITE.site_config.update(suppliers_account=obj)
    
    yield Group('45','assets',u"TVA à payer",u"Geschuldete MWSt","VAT to pay") # PCMN 451
    obj = Account('vat_due','incomes',u"TVA due",u"MWSt zu regularisieren","VAT due") # PCMN 4510
    yield obj
    if sales:
        settings.SITE.site_config.update(sales_vat_account=obj)
    
    obj = Account('vat_deductible','assets',u"TVA déductible",u"Geschuldete MWSt","VAT deductible") # PCMN 4512
    yield obj
    if ledger:
        settings.SITE.site_config.update(purchases_vat_account=obj)
    
    yield Group('55','assets',u"Institutions financières",u"Fainanzinstitute","Banks") # PCMN 55
    yield Account('bestbank','bank_accounts',u"Bestbank",u"Bestbank","Bestbank") 
    yield Account('cash','bank_accounts',u"Cash",u"Cash","Cash") 
    
    # TODO: use another account type than bank_accounts:
    yield Account('vatdcl','bank_accounts',u"VAT",u"VAT","VAT") 
    
    yield Group('6','expenses',u"Charges",u"Aufwendungen","Expenses") # 
    yield Account('products','expenses',
        u"Achat de marchandise",u"Wareneinkäufe","Purchase of goods",
        purchases_allowed=True) # PCMN 6040
    yield Account('services','expenses',
        u"Services et biens divers",u"Dienstleistungen","Purchase of services",
        purchases_allowed=True) 
    yield Account('invests','expenses',
        u"Investissements",u"Anlagen","Purchase of investments",
        purchases_allowed=True) 
    
    yield Group('7','incomes',u"Produits",u"Erträge","Revenues") 
    obj = Account('sales','incomes',
        u"Ventes",u"Verkäufe","Sales",
        sales_allowed=True) # PCMN 7000
    yield obj
    if sales:
        settings.SITE.site_config.update(sales_account=obj)
        



    if sales:
        #~ yield sales.Orders.create_journal("VKR",'sales',name=u"Aufträge")
        yield sales.Invoice.create_journal('sales',ref="S",chart=chart,**babel_values('name',
          de=u"Verkaufsrechnungen",fr=u"Factures vente",en="Sales invoices",et=u"Müügiarved"))
    else:
        yield ledger.AccountInvoice.create_journal('sales',
            ref="S",chart=chart,**babel_values('name',
            de=u"Verkaufsrechnungen",fr=u"Factures vente",en="Sales invoices",et=u"Müügiarved"))
          
    yield ledger.AccountInvoice.create_journal('purchases',
        chart=chart,
        ref="P",
        **babel_values('name',
            de=u"Einkaufsrechnungen",fr=u"Factures achat",en="Purchase invoices",et=u"Ostuarved"))
            
    if finan:
        yield finan.BankStatement.create_journal(chart=chart,name=u"Bestbank",account='bestbank',ref="B")
        yield finan.BankStatement.create_journal(chart=chart,name=u"Cash",account='cash',ref="C")

    if declarations:
        yield declarations.Declaration.create_journal(chart=chart,name=u"VAT declarations",ref="V",account='vatdcl')


    MODEL = ledger.AccountInvoice
    vt = ledger.VoucherTypes.get_for_model(MODEL)
    JOURNALS = Cycler(vt.get_journals())
    Partner = dd.resolve_model(partner_model)
    #~ logger.info("20130105 mini Partners %s",Partner.objects.all().count())
    PARTNERS = Cycler(Partner.objects.order_by('name'))
    USERS = Cycler(settings.SITE.user_model.objects.all())
    AMOUNTS = Cycler([Decimal(x) for x in 
        "2.50 6.80 9.95 14.50 20 29.90 39.90 39.90 99.95 199.95 599.95 1599.99".split()])
    ITEMCOUNT = Cycler(1,2,3)
    for i in range(10):
        jnl = JOURNALS.pop()
        invoice = MODEL(journal=jnl,
          partner=PARTNERS.pop(),
          user=USERS.pop(),
          date=settings.SITE.demo_date(-30+i))
        yield invoice
        for j in range(ITEMCOUNT.pop()):
            item = ledger.InvoiceItem(voucher=invoice,
                account=jnl.get_allowed_accounts()[0],
                #~ product=PRODUCTS.pop(),
                total_incl=AMOUNTS.pop()
                )
            item.total_incl_changed(REQUEST)
            item.before_ui_save(REQUEST)
            #~ if item.total_incl:
                #~ print "20121208 ok", item
            #~ else:
                #~ if item.product.price:
                    #~ raise Exception("20121208")
            yield item
        invoice.register(REQUEST)
        invoice.save()

    
