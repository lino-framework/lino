# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Creates minimal accounting demo data:

- a minimal accounts chart
- some journals


"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


from django.conf import settings
from lino.api import dd, rt, _
from lino.modlib.accounts.utils import DEBIT

accounts = dd.resolve_app('accounts')
vat = dd.resolve_app('vat')
sales = dd.resolve_app('sales')
ledger = dd.resolve_app('ledger')
finan = dd.resolve_app('finan')
declarations = dd.resolve_app('declarations')
#~ partners = dd.resolve_app('partners')


def pcmnref(ref, pcmn):
    if settings.SITE.plugins.ledger.use_pcmn:
        return pcmn
    return ref

CUSTOMERS_ACCOUNT = pcmnref('customers', '4000')
SUPPLIERS_ACCOUNT = pcmnref('suppliers',  '4400')

VAT_DUE_ACCOUNT = pcmnref('vat_due',   '4510')
VAT_DEDUCTIBLE_ACCOUT = pcmnref('vat_deductible', '4512')
VATDCL_ACCOUNT = pcmnref('vatdcl', '4513')

BESTBANK_ACCOUNT = pcmnref('bestbank', '5500')
CASH_ACCOUNT = pcmnref('cash', '5700')

PURCHASE_OF_GOODS = pcmnref('goods', '6040')
PURCHASE_OF_SERVICES = pcmnref('services', '6010')
PURCHASE_OF_INVESTMENTS = pcmnref('investments', '6020')

PO_BESTBANK_ACCOUNT = pcmnref('bestbankpo', '5810')

SALES_ACCOUNT = pcmnref('sales', '7000')

current_group = None


def objects():

    JournalGroups = rt.modules.ledger.JournalGroups
    chart = rt.modules.accounts.AccountCharts.default

    # chart = accounts.Chart(**dd.babel_values(
    #     'name', en="Minimal Accounts Chart",
    #     fr="Plan comptable réduit",
    #     et="Minimaalne kontoplaan",
    #     de="Reduzierter Kontenplan"))
    # yield chart
    #~ account = Instantiator(accounts.Account,"ref name").build

    def Group(ref, type, fr, de, en, et=None):
        if et is None:
            et = en
        global current_group
        current_group = accounts.Group(
            chart=chart,
            ref=ref,
            account_type=accounts.AccountTypes.get_by_name(type),
            **dd.babel_values('name', de=de, fr=fr, en=en, et=et))
        return current_group

    def Account(ref, type, fr, de, en, et, **kw):
        kw.update(dd.babel_values('name', de=de, fr=fr, en=en, et=et))
        return accounts.Account(
            chart=chart,
            group=current_group,
            ref=ref,
            type=accounts.AccountTypes.get_by_name(type),
            **kw)

    yield Group('10', 'capital', "Capital", "Kapital", "Capital", "Kapitaal")

    yield Group('40', 'assets',
                "Créances commerciales",
                "Forderungen aus Lieferungen und Leistungen",
                "Commercial receivable(?)")

    obj = Account(CUSTOMERS_ACCOUNT, 'assets',
                  "Clients", "Kunden",
                  "Customers", "Kliendid", clearable=True)
    yield obj
    if sales:
        settings.SITE.site_config.update(clients_account=obj)

    obj = Account(SUPPLIERS_ACCOUNT, 'liabilities',
                  "Fournisseurs",
                  "Lieferanten", "Suppliers", "Hankijad",
                  clearable=True)
    yield obj
    if vat:
        settings.SITE.site_config.update(suppliers_account=obj)

    yield Group('45', 'assets', "TVA à payer",
                "Geschuldete MWSt", "VAT to pay", "Käibemaksukonto")
    obj = Account(VAT_DUE_ACCOUNT, 'incomes',
                  "TVA due",
                  "Geschuldete MWSt",
                  "VAT due", "Käibemaks maksta", clearable=True)
    yield obj
    if sales:
        settings.SITE.site_config.update(sales_vat_account=obj)

    obj = Account(
        VAT_DEDUCTIBLE_ACCOUT, 'assets',
        "TVA déductible",
        "Abziehbare MWSt",
        "VAT deductible", "Enammakstud käibemaks",
        clearable=True)
    yield obj
    if ledger:
        settings.SITE.site_config.update(purchases_vat_account=obj)

    # PCMN 55
    yield Group('55', 'assets',
                "Institutions financières", "Finanzinstitute", "Banks")
    yield Account(BESTBANK_ACCOUNT, 'bank_accounts', "Bestbank",
                  "Bestbank", "Bestbank", "Parimpank")
    yield Account(CASH_ACCOUNT, 'bank_accounts', "Caisse", "Kasse",
                  "Cash", "Sularaha")
    yield Group('58', 'assets',
                "Transactions en cours", "Laufende Transaktionen",
                "Running transactions")
    yield Account(PO_BESTBANK_ACCOUNT, 'bank_accounts',
                  "Ordres de paiement Bestbank",
                  "Zahlungsaufträge Bestbank",
                  "Payment Orders Bestbank",
                  "Maksekorraldused Parimpank", clearable=True)

    # TODO: use another account type than bank_accounts:
    yield Account(VATDCL_ACCOUNT, 'bank_accounts',
                  "TVA à declarer",
                  "MWSt zu deklarieren",
                  "VAT to declare", "Käibemaks deklareerimata")

    yield Group('6', 'expenses', u"Charges", u"Aufwendungen", "Expenses", "Kulud")
    yield Account(PURCHASE_OF_GOODS, 'expenses',
                  "Achat de marchandise",
                  "Wareneinkäufe",
                  "Purchase of goods",
                  "Varade soetamine",
                  purchases_allowed=True)
    yield Account(PURCHASE_OF_SERVICES, 'expenses',
                  "Services et biens divers",
                  "Dienstleistungen",
                  "Purchase of services",
                  "Teenuste soetamine",
                  purchases_allowed=True)
    yield Account(PURCHASE_OF_INVESTMENTS, 'expenses',
                  "Investissements", "Anlagen",
                  "Purchase of investments", "Investeeringud",
                  purchases_allowed=True)

    yield Group('7', 'incomes', "Produits", "Erträge", "Revenues", "Tulud")
    obj = Account(SALES_ACCOUNT, 'incomes',
                  "Ventes", "Verkäufe", "Sales", "Müük",
                  sales_allowed=True)
    yield obj
    if sales:
        settings.SITE.site_config.update(sales_account=obj)

    ## JOURNALS

    kw = dict(chart=chart, journal_group=JournalGroups.sales)
    if sales:
        MODEL = sales.VatProductInvoice
    else:
        MODEL = vat.VatAccountInvoice
    kw.update(dd.str2kw('name', _("Sales invoices")))
    # kw = dd.babel_values('name', de="Verkaufsrechnungen",
    #                   fr="Factures vente",
    #                   en="Sales invoices",
    #                   et="Müügiarved")
    kw.update(trade_type='sales', ref="SLS")
    yield MODEL.create_journal(**kw)

    kw.update(journal_group=JournalGroups.purchases)
    kw.update(trade_type='purchases', ref="PRC")
    kw.update(dd.str2kw('name', _("Purchase invoices")))
    yield vat.VatAccountInvoice.create_journal(**kw)

    if finan:
        kw.update(journal_group=JournalGroups.financial)
        kw.update(dd.str2kw('name', _("Bestbank")))
        kw.update(account=BESTBANK_ACCOUNT, ref="BNK")
        yield finan.BankStatement.create_journal(**kw)

        kw.update(dd.str2kw('name', _("Payment Orders")))
        # kw.update(dd.babel_values(
        #     'name', de="Zahlungsaufträge", fr="Ordres de paiement",
        #     en="Payment Orders", et="Maksekorraldused"))
        kw.update(
            trade_type='purchases',
            account=PO_BESTBANK_ACCOUNT,
            ref="PMO")
        yield finan.PaymentOrder.create_journal(**kw)

        kw.update(trade_type='')
        kw.update(account=CASH_ACCOUNT, ref="CSH")
        kw.update(dd.str2kw('name', _("Cash")))
        # kw = dd.babel_values(
        #     'name', en="Cash",
        #     de="Kasse", fr="Caisse",
        #     et="Kassa")
        yield finan.BankStatement.create_journal(**kw)

        kw.update(dd.str2kw('name', _("Miscellaneous Journal Entries")))
        # kw = dd.babel_values(
        #     'name', en="Miscellaneous Journal Entries",
        #     de="Diverse Buchungen", fr="Opérations diverses",
        #     et="Muud operatsioonid")
        kw.update(account=CASH_ACCOUNT, ref="MSG", dc=DEBIT)
        yield finan.JournalEntry.create_journal(**kw)

    if declarations:
        kw = dict(chart=chart, journal_group=JournalGroups.financial)
        kw.update(dd.str2kw('name', _("VAT declarations")))
        # kw = dd.babel_values(
        #     'name', en="VAT declarations",
        #     de="MWSt-Erklärungen", fr="Déclarations TVA",
        #     et="Käibemaksudeklaratsioonid")
        kw.update(account=VATDCL_ACCOUNT, ref="VAT", dc=None)
        yield declarations.Declaration.create_journal(**kw)

    payments = []
    if finan:
        payments += [finan.BankStatement, finan.JournalEntry,
                     finan.PaymentOrder]
    
    MatchRule = rt.modules.ledger.MatchRule
    for jnl in ledger.Journal.objects.all():
        if jnl.voucher_type.model in payments:
            yield MatchRule(
                journal=jnl,
                account=settings.SITE.site_config.clients_account)
            yield MatchRule(
                journal=jnl,
                account=settings.SITE.site_config.suppliers_account)
            a = settings.SITE.site_config.wages_account
            if a:
                yield MatchRule(journal=jnl, account=a)
        elif jnl.trade_type:
            a = jnl.trade_type.get_partner_account()
            if a:
                yield MatchRule(journal=jnl, account=a)
