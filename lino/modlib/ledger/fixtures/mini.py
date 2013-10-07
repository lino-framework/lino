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
- monthly purchases (causing costs) 
- monthly sales 
- monthly payment orders and bank statements


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

partner_model = settings.SITE.partners_app_label + '.Partner'

current_group = None

REQUEST = None
MORE_THAN_A_MONTH = datetime.timedelta(days=40) 


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
        JOURNAL_BANK = finan.BankStatement.create_journal(chart=chart,name="Bestbank",account='bestbank',ref="B")
        yield JOURNAL_BANK
        kw = babel_values('name',de="Zahlungsaufträge",fr="Ordres de paiement",en="Payment Orders",et="Maksekorraldused")
        JOURNAL_PO = finan.PaymentOrder.create_journal('purchases',chart=chart,account='bestbankpo',ref="PO",**kw)
        yield JOURNAL_PO
        yield finan.BankStatement.create_journal(chart=chart,name="Cash",account='cash',ref="C")
        yield finan.JournalEntry.create_journal(chart=chart,name="Miscellaneous Journal Entries",ref="M",dc=accounts.DEBIT)

    if declarations:
        yield declarations.Declaration.create_journal(chart=chart,name=u"VAT declarations",ref="V",account='vatdcl')

    Company = dd.resolve_model('contacts.Company')
    Person = dd.resolve_model('contacts.Person')
    Product = dd.resolve_model('products.Product')
    
    if False: # old system
    
        MODEL = ledger.AccountInvoice
        vt = ledger.VoucherTypes.get_for_model(MODEL)
        JOURNALS = Cycler(vt.get_journals())
        Partner = dd.resolve_model(partner_model)
        #~ logger.info("20130105 mini Partners %s",Partner.objects.all().count())
        #~ PARTNERS = Cycler(Partner.objects.order_by('name'))
        PARTNERS = Cycler(Company.objects.order_by('id'))
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
            
        
    USERS = Cycler(settings.SITE.user_model.objects.all())
    
    
    if sales:
        
        yield Product(name="Foo",sales_price='399.90')
        yield Product(name="Bar",sales_price='599.90')
        yield Product(name="Baz",sales_price='990.00')
        PRODUCTS = Cycler(Product.objects.order_by('id'))
        JOURNAL_S = ledger.Journal.objects.get(ref="S")
        #~ assert JOURNAL_S.dc == accounts.DEBIT
        CUSTOMERS = Cycler(Person.objects.order_by('id'))
        ITEMCOUNT = Cycler(1,2,3)
        QUANTITIES = Cycler(5,1,2,3)
        SALES_PER_MONTH = Cycler(2,1,3,2,0)
        
    PROVIDERS = Cycler(Company.objects.order_by('id'))
        
    JOURNAL_P = ledger.Journal.objects.get(ref="P")
    #~ assert JOURNAL_P.dc == accounts.CREDIT
    ACCOUNTS = Cycler(JOURNAL_P.get_allowed_accounts())
    AMOUNTS = Cycler([Decimal(x) for x in 
        "20 29.90 39.90 99.95 199.95 599.95 1599.99".split()])
    AMOUNT_DELTAS = Cycler([Decimal(x) for x in "0 0.60 1.10 1.30 2.50".split()])
    DATE_DELTAS = Cycler((1,2,3,4,5,6,7))
    INFLATION_RATE = Decimal("0.02")
    
    """
    5 "purchase stories" : each story represents a provider who sends 
    monthly invoices.
    """
    PURCHASE_STORIES = []
    for i in range(5):
        # provider, (account,amount)
        story = ( PROVIDERS.pop(), [] )
        story[1].append( (ACCOUNTS.pop(),AMOUNTS.pop()) )
        if i % 3:
            story[1].append( (ACCOUNTS.pop(),AMOUNTS.pop()) )
        PURCHASE_STORIES.append(story)
    
    
    #~ date = settings.SITE.demo_date() + delta(years=-2)
    START_YEAR = settings.SITE.start_year # 2011
    date = datetime.date(START_YEAR,1,1)
    end_date = datetime.date(2013,5,1)
    while date < end_date:
        
        if sales:
            for i in range(SALES_PER_MONTH.pop()):
                #~ print __file__, date
                invoice = sales.Invoice(journal=JOURNAL_S,
                    partner=CUSTOMERS.pop(),
                    user=USERS.pop(),
                    date=date+delta(days=10+DATE_DELTAS.pop()))
                yield invoice
                for j in range(ITEMCOUNT.pop()):
                    item = sales.InvoiceItem(voucher=invoice,
                        product=PRODUCTS.pop(),
                        qty=QUANTITIES.pop()
                        )
                    item.product_changed(REQUEST)
                    item.before_ui_save(REQUEST)
                    #~ if item.total_incl:
                        #~ print "20121208 ok", item
                    #~ else:
                        #~ if item.product.price:
                            #~ raise Exception("20121208")
                    yield item
                invoice.register(REQUEST)
                invoice.save()
            
        for story in PURCHASE_STORIES:
            invoice = ledger.AccountInvoice(journal=JOURNAL_P,
                partner=story[0],
                user=USERS.pop(),
                date=date+delta(days=DATE_DELTAS.pop()))
            yield invoice
            for account,amount in story[1]:
                amount += amount + (amount * INFLATION_RATE * (date.year - START_YEAR))
                item = ledger.InvoiceItem(voucher=invoice,
                    account=account,
                    total_incl=amount+AMOUNT_DELTAS.pop()
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
        
        if finan and (end_date - date) > MORE_THAN_A_MONTH: # last month not yet done
            #~ po = finan.PaymentOrder(journal=JOURNAL_PO,
            po = JOURNAL_PO.create_voucher(
                user=USERS.pop(),
                date=date+delta(days=20))
            yield po
            suggestions = finan.SuggestionsByPaymentOrder.request(po)
            ba = finan.SuggestionsByPaymentOrder.get_action_by_name('do_fill')
            ar = ba.request(master_instance=po)
            ar.selected_rows = [x for x in suggestions]
            ar.run()
            po.register(REQUEST)
            po.save()
            
            #~ bs = finan.BankStatement(journal=JOURNAL_BANK,
            bs = JOURNAL_BANK.create_voucher(
                user=USERS.pop(),
                date=date+delta(days=28))
            yield bs
            suggestions = finan.SuggestionsByBankStatement.request(bs)
            ba = suggestions.actor.get_action_by_name('do_fill')
            ar = ba.request(master_instance=bs)
            ar.selected_rows = [x for x in suggestions]
            ar.run()
            bs.register(REQUEST)
            bs.save()
            
            
        date += delta(months=1)
    
    
    

    
