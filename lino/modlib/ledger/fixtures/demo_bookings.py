# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Creates fictive demo bookings

- monthly purchases (causing costs)
- monthly sales
- monthly payment orders and bank statements


"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


import datetime
from dateutil.relativedelta import relativedelta as delta

from decimal import Decimal

from django.conf import settings
from lino.utils import Cycler
from lino.api import dd
vat = dd.resolve_app('vat')
sales = dd.resolve_app('sales')
ledger = dd.resolve_app('ledger')
finan = dd.resolve_app('finan')

partner_model = settings.SITE.partners_app_label + '.Partner'

current_group = None

# from lino.core.requests import BaseRequest
REQUEST = settings.SITE.login()  # BaseRequest()
MORE_THAN_A_MONTH = datetime.timedelta(days=40)


def objects():

    Company = dd.resolve_model('contacts.Company')
    Person = dd.resolve_model('contacts.Person')
    Product = dd.resolve_model('products.Product')

    if False:  # old system

        MODEL = vat.VatAccountInvoice
        vt = ledger.VoucherTypes.get_for_model(MODEL)
        JOURNALS = Cycler(vt.get_journals())
        Partner = dd.resolve_model(partner_model)
        #~ logger.info("20130105 mini Partners %s",Partner.objects.all().count())
        #~ PARTNERS = Cycler(Partner.objects.order_by('name'))
        PARTNERS = Cycler(Company.objects.order_by('id'))
        USERS = Cycler(settings.SITE.user_model.objects.all())
        AMOUNTS = Cycler([Decimal(x) for x in
                          "2.50 6.80 9.95 14.50 20 29.90 39.90 39.90 99.95 199.95 599.95 1599.99".split()])
        ITEMCOUNT = Cycler(1, 2, 3)
        for i in range(10):
            u = USERS.pop()
            jnl = JOURNALS.pop()
            invoice = MODEL(journal=jnl,
                            partner=PARTNERS.pop(),
                            user=u,
                            date=settings.SITE.demo_date(-30 + i))
            yield invoice
            ar = MODEL.request(user=u)
            for j in range(ITEMCOUNT.pop()):
                item = vat.InvoiceItem(voucher=invoice,
                                       account=jnl.get_allowed_accounts()[
                                           0],
                                       #~ product=PRODUCTS.pop(),
                                       total_incl=AMOUNTS.pop()
                )
                item.total_incl_changed(ar)
                item.before_ui_save(ar)
                #~ if item.total_incl:
                    #~ print "20121208 ok", item
                #~ else:
                    #~ if item.product.price:
                        #~ raise Exception("20121208")
                yield item
            invoice.register(ar)
            invoice.save()

    USERS = Cycler(settings.SITE.user_model.objects.all())

    if sales:

        yield Product(name="Foo", sales_price='399.90')
        yield Product(name="Bar", sales_price='599.90')
        yield Product(name="Baz", sales_price='990.00')
        PRODUCTS = Cycler(Product.objects.order_by('id'))
        JOURNAL_S = ledger.Journal.objects.get(ref="SLS")
        #~ assert JOURNAL_S.dc == accounts.DEBIT
        CUSTOMERS = Cycler(Person.objects.order_by('id'))
        ITEMCOUNT = Cycler(1, 2, 3)
        QUANTITIES = Cycler(5, 1, 2, 3)
        SALES_PER_MONTH = Cycler(2, 1, 3, 2, 0)

    PROVIDERS = Cycler(Company.objects.order_by('id'))

    JOURNAL_P = ledger.Journal.objects.get(ref="PRC")
    #~ assert JOURNAL_P.dc == accounts.CREDIT
    ACCOUNTS = Cycler(JOURNAL_P.get_allowed_accounts())
    AMOUNTS = Cycler([Decimal(x) for x in
                      "20 29.90 39.90 99.95 199.95 599.95 1599.99".split()])
    AMOUNT_DELTAS = Cycler([Decimal(x)
                           for x in "0 0.60 1.10 1.30 2.50".split()])
    DATE_DELTAS = Cycler((1, 2, 3, 4, 5, 6, 7))
    INFLATION_RATE = Decimal("0.02")

    """
    5 "purchase stories" : each story represents a provider who sends
    monthly invoices.
    """
    PURCHASE_STORIES = []
    for i in range(5):
        # provider, (account,amount)
        story = (PROVIDERS.pop(), [])
        story[1].append((ACCOUNTS.pop(), AMOUNTS.pop()))
        if i % 3:
            story[1].append((ACCOUNTS.pop(), AMOUNTS.pop()))
        PURCHASE_STORIES.append(story)

    #~ date = settings.SITE.demo_date() + delta(years=-2)
    START_YEAR = settings.SITE.start_year  # 2011
    date = datetime.date(START_YEAR, 1, 1)
    end_date = datetime.date(START_YEAR+1, 5, 1)
    while date < end_date:

        if sales:
            for i in range(SALES_PER_MONTH.pop()):
                #~ print __file__, date
                invoice = sales.VatProductInvoice(
                    journal=JOURNAL_S,
                    partner=CUSTOMERS.pop(),
                    user=USERS.pop(),
                    date=date + delta(days=10 + DATE_DELTAS.pop()))
                yield invoice
                for j in range(ITEMCOUNT.pop()):
                    item = sales.InvoiceItem(
                        voucher=invoice,
                        product=PRODUCTS.pop(),
                        qty=QUANTITIES.pop())
                    item.product_changed(REQUEST)
                    item.before_ui_save(REQUEST)
                    #~ if item.total_incl:
                        #~ print "20121208 ok", item
                    #~ else:
                        #~ if item.product.price:
                            #~ raise Exception("20121208")
                    yield item
                #~ invoice.set_workflow_state('registered')
                # ~ invoice.state = 'registered' # automatically call
                invoice.register(REQUEST)
                invoice.save()

        for story in PURCHASE_STORIES:
            invoice = vat.VatAccountInvoice(
                journal=JOURNAL_P, partner=story[0], user=USERS.pop(),
                date=date + delta(days=DATE_DELTAS.pop()))
            yield invoice
            for account, amount in story[1]:
                amount += amount + \
                    (amount * INFLATION_RATE * (date.year - START_YEAR))
                item = vat.InvoiceItem(voucher=invoice,
                                       account=account,
                                       total_incl=amount +
                                       AMOUNT_DELTAS.pop())
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

        if finan and (end_date - date) > MORE_THAN_A_MONTH:
            # last month not yet done
            #~ po = finan.PaymentOrder(journal=JOURNAL_PO,
            JOURNAL_PO = ledger.Journal.objects.get(ref="PMO")
            po = JOURNAL_PO.create_voucher(
                user=USERS.pop(),
                date=date + delta(days=20))
            yield po
            suggestions = finan.SuggestionsByPaymentOrder.request(po)
            ba = finan.SuggestionsByPaymentOrder.get_action_by_name('do_fill')
            ar = ba.request(master_instance=po)
            ar.selected_rows = [x for x in suggestions]
            ar.run()
            po.register(REQUEST)
            po.save()

            #~ bs = finan.BankStatement(journal=JOURNAL_BANK,
            JOURNAL_BANK = ledger.Journal.objects.get(ref="BNK")
            bs = JOURNAL_BANK.create_voucher(
                user=USERS.pop(),
                date=date + delta(days=28))
            yield bs
            suggestions = finan.SuggestionsByBankStatement.request(bs)
            ba = suggestions.actor.get_action_by_name('do_fill')
            ar = ba.request(master_instance=bs)
            ar.selected_rows = [x for x in suggestions]
            ar.run()
            bs.register(REQUEST)
            bs.save()

        date += delta(months=1)
