# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""
The :xfile:`models` module for the :mod:`lino.modlib.finan` app.
"""


from django.db import models
from django.core.exceptions import ValidationError

from lino.modlib.accounts.utils import ZERO
from lino.modlib.accounts.fields import DebitOrCreditField
from lino.modlib.ledger.mixins import Matchable

from lino.api import dd, rt, _
from lino import mixins

from .choicelists import VoucherStates

ledger = dd.resolve_app('ledger')


class FinancialVoucher(ledger.Voucher):
    """Base class for all financial vouchers:
    :class:`Grouper`,
    :class:`JournalEntry`,
    :class:`PaymentOrder` and
    :class:`BankStatement`.
    """
    state = VoucherStates.field(default=VoucherStates.draft)

    class Meta:
        abstract = True

    def register(self, ar):
        super(FinancialVoucher, self).register(ar)
        self.update_satisfied()

    def deregister(self, ar):
        super(FinancialVoucher, self).deregister(ar)
        self.update_satisfied()

    def update_satisfied(self):
        partners = set()
        #~ matches = dict()
        for i in self.items.all():
            if i.partner:
                partners.add(i.partner)
        for p in partners:
            ledger.update_partner_satisfied(p)

    def get_wanted_movements(self):
        amount, movements = self.get_finan_movements()
        if amount:
            raise Exception("Missing amount %s in movements" % amount)
        return movements

    def get_finan_movements(self):
        amount = ZERO
        mvts = []
        for i in self.items.all():
            if i.dc == self.journal.dc:
                amount += i.amount
            else:
                amount -= i.amount
            if i.match:
                match = i.match
            elif i.partner:
                match = "%s#%s-%s" % (self.journal.ref, self.pk, i.seqno)
            else:
                match = ''
            b = self.create_movement(
                i.account, i.dc, i.amount,
                seqno=i.seqno,
                match=match,
                partner=i.partner)
            mvts.append(b)

        return amount, mvts


class FinancialVoucherItem(mixins.Sequenced, ledger.VoucherItem, Matchable):
    """Base class for items of all financial vouchers
    (:class:`FinancialVoucher`).

    """
    class Meta:
        abstract = True
        verbose_name = _("Item")
        verbose_name_plural = _("Items")

    amount = dd.PriceField(default=0)
    dc = DebitOrCreditField()
    remark = models.CharField(_("Remark"), max_length=200, blank=True)
    account = dd.ForeignKey('accounts.Account', blank=True)
    partner = dd.ForeignKey('contacts.Partner', blank=True, null=True)

    def get_default_match(self):
        return str(self.date)

    def get_siblings(self):
        return self.voucher.items.all()

    def match_changed(self, ar):
        if self.match:
            dc = not self.voucher.journal.dc
            m = ledger.DueMovement(dc, self)
            self.dc = dc
            self.amount = m.balance
            #~ if m.balance > 0:
                #~ self.dc = not self.voucher.journal.dc
                #~ self.amount = m.balance
            #~ else:
                #~ self.dc = self.voucher.journal.dc
                #~ self.amount = - m.balance

    def partner_changed(self, ar):
        if self.partner:
            flt = dict(partner=self.partner, satisfied=False)
            if self.match:
                flt.update(match=self.match)
            suggestions = list(ledger.get_due_movements(
                self.voucher.journal.dc, **flt))

            if len(suggestions) == 0:
                pass
            elif len(suggestions) == 1:
                match = suggestions[0]
                if match.trade_type is not None:
                    self.account = match.trade_type.get_partner_account()
                if self.account_id is None:
                    self.account = match.account
                self.dc = match.dc
                self.amount = - match.balance
                self.match = match.match
            else:
                raise NotImplementedError("20150222")
                grouper = rt.modules.finan.Grouper.get_or_create(self.partner)
                for match in suggestions:
                    if match.trade_type is not None:
                        self.account = match.trade_type.get_partner_account()
                    if self.account_id is None:
                        self.account = match.account
                    if self.account == match.account:
                        self.dc = match.dc
                        self.amount = - match.balance
                        self.match = match.match
            if self.account_id is None:
                raise ValidationError(
                    _("Could not determine the general account"))

    def full_clean(self, *args, **kw):
        if self.dc is None:
            self.dc = self.voucher.journal.dc
        if self.amount < 0:
            self.amount = - self.amount
            self.dc = not self.dc
        return super(FinancialVoucherItem, self).full_clean(*args, **kw)


