# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.vatless`.



"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from decimal import Decimal

from django.conf import settings

from lino.api import dd, rt, _

from lino.modlib.ledger.choicelists import (
    FiscalYears, VoucherTypes, VoucherStates)
from lino.modlib.ledger.mixins import (PartnerRelated, AccountInvoiceItem,
                                       Matchable)
from lino.modlib.ledger.ui import PartnerVouchers, ByJournal
from lino.modlib.ledger.models import Voucher
from lino.modlib.ledger.choicelists import TradeTypes

TradeTypes.purchases.update(
    partner_account_field_name='suppliers_account',
    partner_account_field_label=_("Suppliers account"))


class Invoice(PartnerRelated, Voucher, Matchable):

    amount = dd.PriceField(_("Amount"), blank=True, null=True)
    # state = VoucherStates.field(default=VoucherStates.draft)
    # workflow_state_field = 'state'

    def compute_totals(self):
        if self.pk is None:
            return
        base = Decimal()
        for i in self.items.all():
            if i.amount is not None:
                base += i.amount
        self.amount = base

    def get_vat_sums(self):
        sums_dict = dict()

        def book(account, amount):
            if account in sums_dict:
                sums_dict[account] += amount
            else:
                sums_dict[account] = amount
        tt = self.get_trade_type()
        for i in self.items.order_by('seqno'):
            if i.amount:
                b = i.get_base_account(tt)
                if b is None:
                    raise Exception(
                        "No base account for %s (amount is %r)" % (
                            i, i.amount))
                book(b, i.amount)
        return sums_dict

    def get_wanted_movements(self):
        sums_dict = self.get_vat_sums()
        #~ logger.info("20120901 get_wanted_movements %s",sums_dict)
        sum = Decimal()
        for a, m in sums_dict.items():
            if m:
                yield self.create_movement(a, not self.journal.dc, m)
                sum += m

        a = self.get_trade_type().get_partner_account()
        if a is not None:
            yield self.create_movement(
                a, self.journal.dc, sum,
                partner=self.partner,
                project=self.project,
                match=self.match)

    def full_clean(self, *args, **kw):
        self.compute_totals()
        super(Invoice, self).full_clean(*args, **kw)

    def before_state_change(self, ar, old, new):
        if new.name == 'registered':
            self.compute_totals()
        elif new.name == 'draft':
            pass
        super(Invoice, self).before_state_change(ar, old, new)


class InvoiceItem(AccountInvoiceItem):

    voucher = dd.ForeignKey('vatless.Invoice', related_name='items')
    amount = dd.PriceField(_("Amount"), blank=True, null=True)


class InvoiceItems(dd.Table):
    model = 'vatless.InvoiceItem'
    auto_fit_column_widths = True
    order_by = ['voucher', "seqno"]


class ItemsByInvoice(InvoiceItems):
    column_names = "account title amount"
    master_key = 'voucher'
    order_by = ["seqno"]


class InvoiceDetail(dd.FormLayout):
    main = "general ledger"

    general = dd.Panel("""
    id date project partner user
    due_date your_ref workflow_buttons amount
    ItemsByInvoice
    """, label=_("General"))

    ledger = dd.Panel("""
    journal year number narration state
    ledger.MovementsByVoucher
    """, label=_("Ledger"))


class Invoices(PartnerVouchers):
    model = 'vatless.Invoice'
    order_by = ["-id"]
    parameters = dict(
        state=VoucherStates.field(blank=True),
        **PartnerVouchers.parameters)
    params_layout = "project partner state journal year"
    params_panel_hidden = True
    column_names = "date id number project partner amount user *"
    detail_layout = InvoiceDetail()
    insert_layout = """
    journal project 
    partner
    date amount
    """
    # start_at_bottom = True

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super(Invoices, cls).get_request_queryset(ar)
        pv = ar.param_values
        if pv.state:
            qs = qs.filter(state=pv.state)
        return qs

    @classmethod
    def unused_param_defaults(cls, ar, **kw):
        kw = super(Invoices, cls).param_defaults(ar, **kw)
        kw.update(pyear=FiscalYears.from_date(settings.SITE.today()))
        return kw


class InvoicesByJournal(Invoices, ByJournal):
    """
    Shows all simple invoices of a given journal (whose
    :attr:`Journal.voucher_type` must be :class:`Invoices`)
    """
    params_layout = "project partner state year"
    column_names = "number date " \
        "project partner amount due_date user workflow_buttons *"
                  #~ "ledger_remark:10 " \
    insert_layout = """
    project
    partner
    date amount
    """
    order_by = ["-number"]

VoucherTypes.add_item(Invoice, InvoicesByJournal)
