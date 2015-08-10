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

from lino.api import dd, _

from lino.modlib.ledger.mixins import (
    ProjectRelated, PartnerRelated, AccountVoucherItem, Matching)
from lino.modlib.sepa.mixins import Payable
from lino.modlib.ledger.models import Voucher
from lino.modlib.ledger.choicelists import TradeTypes

TradeTypes.purchases.update(
    partner_account_field_name='suppliers_account',
    partner_account_field_label=_("Suppliers account"))


class AccountInvoice(PartnerRelated, Payable, Voucher, Matching):

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")

    amount = dd.PriceField(_("Amount"), blank=True, null=True)

    def compute_totals(self):
        if self.pk is None:
            return
        base = Decimal()
        for i in self.items.all():
            if i.amount is not None:
                base += i.amount
        self.amount = base

    def get_sums_dict(self):
        sums_dict = dict()

        def book(account, prj, amount):
            k = (account, prj)
            if k in sums_dict:
                sums_dict[k] += amount
            else:
                sums_dict[k] = amount
        tt = self.get_trade_type()
        for i in self.items.order_by('seqno'):
            if i.amount:
                b = i.get_base_account(tt)
                if b is None:
                    raise Exception(
                        "No base account for %s (amount is %r)" % (
                            i, i.amount))
                book(b, i.project, i.amount)
        return sums_dict

    def get_wanted_movements(self):
        sums_dict = self.get_sums_dict()
        #~ logger.info("20120901 get_wanted_movements %s",sums_dict)
        sum = Decimal()
        for k, m in sums_dict.items():
            a, prj = k
            if m:
                yield self.create_movement(a, prj, not self.journal.dc, m)
                sum += m

        a = self.get_trade_type().get_partner_account()
        if a is not None:
            yield self.create_movement(
                a, None, self.journal.dc, sum,
                partner=self.partner,
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


class InvoiceItem(AccountVoucherItem, ProjectRelated):
    """An item of an :class:`AccountInvoice`."""
    voucher = dd.ForeignKey('vatless.AccountInvoice', related_name='items')
    title = models.CharField(_("Description"), max_length=200, blank=True)
    amount = dd.PriceField(_("Amount"), blank=True, null=True)


from .ui import *
