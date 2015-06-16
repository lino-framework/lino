# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.vatless`.



"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from decimal import Decimal

from django.db import models

from lino.api import dd, rt, _

from lino.utils.xmlgen.html import E

from lino.modlib.ledger.choicelists import VoucherTypes
from lino.modlib.ledger.mixins import (PartnerRelated, AccountInvoiceItem,
                                       Matchable)
from lino.modlib.ledger.ui import PartnerVouchers, ByJournal
from lino.modlib.ledger.models import Voucher
from lino.modlib.ledger.choicelists import TradeTypes

TradeTypes.purchases.update(
    partner_account_field_name='suppliers_account',
    partner_account_field_label=_("Suppliers account"))


class AccountInvoice(PartnerRelated, Voucher, Matchable):

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")

    # title = models.CharField(_("Description"), max_length=200, blank=True)

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
        super(AccountInvoice, self).full_clean(*args, **kw)

    def before_state_change(self, ar, old, new):
        if new.name == 'registered':
            self.compute_totals()
        elif new.name == 'draft':
            pass
        super(AccountInvoice, self).before_state_change(ar, old, new)


class InvoiceItem(AccountInvoiceItem):
    """An item of an :class:`AccountInvoice`."""
    voucher = dd.ForeignKey('vatless.AccountInvoice', related_name='items')
    title = models.CharField(_("Description"), max_length=200, blank=True)
    amount = dd.PriceField(_("Amount"), blank=True, null=True)


from .ui import *
