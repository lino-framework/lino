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

"""
My personal attempt to create a "universal account chart".
To be used for simple demo setups in different countries.

"""

from decimal import Decimal

from django.conf import settings
from lino.utils import Cycler
from lino.utils.babel import babel_values
from lino import dd
accounts = dd.resolve_app('accounts')
vat = dd.resolve_app('vat')
sales = dd.resolve_app('sales')
ledger = dd.resolve_app('ledger')
contacts = dd.resolve_app('contacts')


current_group = None

REQUEST = None


def objects():
    chart  = accounts.Chart(**babel_values('name',
        en="Minimal Accounts Chart",
        fr=u"Plan comptable réduit",
        de=u"Reduzierter Kontenplan"))
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
          
    yield Group('10','capital',u"Capital",u"Kapital","Capital")
    
    yield Group('40','asset',  u"Créances commerciales", u"Forderungen aus Lieferungen und Leistungen", "Commercial receivable(?)")
    yield Account('customers','asset',u"Clients",u"Kunden","Customers") # PCMN 4000
    yield Account('suppliers','liability',u"Fournisseurs",u"Lieferanten","Suppliers") # PCMN 4400
    
    yield Group('45','asset',u"TVA à payer",u"Geschuldete MWSt","VAT to pay") # PCMN 451
    yield Account('vat_due','income',u"TVA due",u"MWSt zu regularisieren","VAT due") # PCMN 4510
    yield Account('vat_deductible','asset',u"TVA déductible",u"Geschuldete MWSt","VAT deductible") # PCMN 4512
    
    yield Group('6','expense',u"Charges",u"Aufwendungen","Expenses") # 
    yield Account('products','expense',
        u"Achat de marchandise",u"Wareneinkäufe","Purchase of goods",
        purchases_allowed=True) # PCMN 6040
    yield Account('services','expense',
        u"Services et biens divers",u"Dienstleistungen","Purchase of services",
        purchases_allowed=True) 
    yield Account('invests','expense',
        u"Investissements",u"Anlagen","Purchase of investments",
        purchases_allowed=True) 
    
    yield Group('7','income',u"Produits",u"Erträge","Revenues") 
    yield Account('sales','income',
        u"Ventes",u"Verkäufe","Sales",
        sales_allowed=True) # PCMN 7000



    if sales:
        #~ yield sales.Orders.create_journal("VKR",'sales',name=u"Aufträge")
        yield sales.Invoice.create_journal('sales',chart=chart,**babel_values('name',
          de=u"Verkaufsrechnungen",fr=u"Factures vente",en="Sales invoices",et=u"Müügiarved"))
    else:
        yield ledger.AccountInvoice.create_journal('sales',
            chart=chart,**babel_values('name',
            de=u"Verkaufsrechnungen",fr=u"Factures vente",en="Sales invoices",et=u"Müügiarved"))
          
    yield ledger.AccountInvoice.create_journal('purchases',
        chart=chart,
        **babel_values('name',
            de=u"Einkaufsrechnungen",fr=u"Factures achat",en="Purchase invoices",et=u"Ostuarved"))


    MODEL = ledger.AccountInvoice
    vt = ledger.VoucherTypes.get_for_model(MODEL)
    JOURNALS = Cycler(vt.get_journals())
    PARTNERS = Cycler(contacts.Partner.objects.all())
    USERS = Cycler(settings.LINO.user_model.objects.all())
    AMOUNTS = Cycler([Decimal(x) for x in 
        "2.50 6.80 9.95 14.50 20 29.90 39.90 39.90 99.95 199.95 599.95 1599.99".split()])
    ITEMCOUNT = Cycler(1,2,3)
    for i in range(10):
        jnl = JOURNALS.pop()
        invoice = MODEL(journal=jnl,
          partner=PARTNERS.pop(),
          user=USERS.pop(),
          date=settings.LINO.demo_date(-30+i))
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

    