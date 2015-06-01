# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.novat`.



"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from decimal import Decimal

from django.conf import settings

from lino.api import dd, rt, _

from lino.modlib.ledger.choicelists import (FiscalYears, VoucherTypes,
                                            InvoiceStates, )
from lino.modlib.ledger.mixins import (PartnerRelated, VoucherItem,
                                       Matchable)
from lino.modlib.ledger.ui import PartnerVouchers, ByJournal
from lino.modlib.ledger.models import Voucher


class SimpleInvoice(PartnerRelated, Voucher, Matchable):

    total = dd.PriceField(_("Total"), blank=True, null=True)

    def compute_totals(self):
        if self.pk is None:
            return
        base = Decimal()
        for i in self.items.all():
            if i.total is not None:
                base += i.total
        self.total = base

    def get_vat_sums(self):
        sums_dict = dict()

        def book(account, amount):
            if account in sums_dict:
                sums_dict[account] += amount
            else:
                sums_dict[account] = amount
        tt = self.get_trade_type()
        for i in self.items.order_by('seqno'):
            if i.total:
                b = i.get_base_account(tt)
                if b is None:
                    raise Exception(
                        "No base account for %s (total_base is %r)" % (
                            i, i.total))
                book(b, i.total)
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
                a, self.journal.dc, sum, partner=self.partner,
                match=self.match)

    def full_clean(self, *args, **kw):
        self.compute_totals()
        super(SimpleInvoice, self).full_clean(*args, **kw)

    def before_state_change(self, ar, old, new):
        if new.name == 'registered':
            self.compute_totals()
        elif new.name == 'draft':
            pass
        super(SimpleInvoice, self).before_state_change(ar, old, new)


class SimpleItem(VoucherItem):

    total = dd.PriceField(_("Total"), blank=True, null=True)

    def get_base_account(self, tt):
        raise NotImplementedError


class InvoiceDetail(dd.FormLayout):
    main = "general ledger"

    general = dd.Panel("""
    id date partner user
    due_date your_ref workflow_buttons total
    ItemsByInvoice
    """, label=_("General"))

    ledger = dd.Panel("""
    journal year number narration
    MovementsByVoucher
    """, label=_("Ledger"))


class SimpleInvoices(PartnerVouchers):
    model = 'novat.SimpleInvoice'
    order_by = ["-id"]
    parameters = dict(
        state=InvoiceStates.field(blank=True),
        **PartnerVouchers.parameters)
    params_layout = "partner state journal year"
    params_panel_hidden = True
    column_names = "date id number partner total user *"
    detail_layout = InvoiceDetail()
    insert_layout = """
    journal partner
    date total
    """
    # start_at_bottom = True

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super(SimpleInvoices, cls).get_request_queryset(ar)
        pv = ar.param_values
        if pv.state:
            qs = qs.filter(state=pv.state)
        return qs

    @classmethod
    def unused_param_defaults(cls, ar, **kw):
        kw = super(SimpleInvoices, cls).param_defaults(ar, **kw)
        kw.update(pyear=FiscalYears.from_date(settings.SITE.today()))
        return kw


class InvoicesByJournal(SimpleInvoices, ByJournal):
    """
    Shows all simple invoices of a given journal (whose
    :attr:`Journal.voucher_type` must be :class:`SimpleInvoices`)
    """
    params_layout = "partner state year"
    column_names = "number date due_date " \
        "partner total user workflow_buttons *"
                  #~ "ledger_remark:10 " \
    insert_layout = """
    partner
    date total
    """

VoucherTypes.add_item(SimpleInvoice, InvoicesByJournal)


