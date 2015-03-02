# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines the :class:`DueMovement` class, a volatile object representing
a group of matching movements.

"""

from lino.api import rt

from lino.modlib.accounts.utils import ZERO


class DueMovement(object):
    """A **due movement** is a movement which a partner should do in order
    to satisfy their debt.  Or which we should do in order to satisfy
    our debt.

    """
    def __init__(self, dc, mvt):
        self.dc = dc
        self.partner = mvt.partner
        self.account = mvt.account
        self.match = mvt
        self.pk = self.id = mvt.id

        self.debts = []
        self.payments = []
        self.balance = ZERO
        self.due_date = None
        self.trade_type = None
        self.has_unsatisfied_movement = False
        self.has_satisfied_movement = False

        self.collect(mvt)

        qs = rt.modules.ledger.Movement.objects.filter(
            partner=self.partner, account=self.account, match=mvt)
        for mvt in qs.order_by('voucher__date'):
            self.collect(mvt)

    def collect(self, mvt):
        if mvt.satisfied:
            self.has_satisfied_movement = True
        else:
            self.has_unsatisfied_movement = True
        if self.trade_type is None:
            voucher = mvt.voucher.get_mti_leaf()
            self.trade_type = voucher.get_trade_type()
        if mvt.dc == self.dc:
            self.debts.append(mvt)
            self.balance += mvt.amount
            voucher = mvt.voucher.get_mti_leaf()
            due_date = voucher.get_due_date()
            if self.due_date is None or due_date < self.due_date:
                self.due_date = due_date
        else:
            self.payments.append(mvt)
            self.balance -= mvt.amount

    def update_satisfied(self):
        satisfied = self.balance == ZERO
        if satisfied:
            if not self.has_unsatisfied_movement:
                return
        else:
            if not self.has_satisfied_movement:
                return
        for m in self.debts + self.payments:
            if m.satisfied != satisfied:
                m.satisfied = satisfied
                m.save()


def get_due_movements(dc, **flt):
    """Analyze the movements corresponding to the given filter condition
    `flt` and yield a series of :class:`DueMovement` objects which
    --if they were booked-- would satisfy the given movements.
    
    There will be at most one :class:`DueMovement` per (account,
    partner, match), each of them grouping the movements with same
    partner, account and match.

    The balances of the :class:`DueMovement` objects will be positive
    or negative depending on the specified `dc`.

    """
    if dc is None:
        return
    qs = rt.modules.ledger.Movement.objects.filter(**flt)
    qs = qs.order_by('voucher__date')
    matches_by_account = dict()
    for mvt in qs:
        k = (mvt.account, mvt.partner)
        matches = matches_by_account.setdefault(k, set())
        m = mvt.match or mvt
        if not m in matches:
            matches.add(m)
            yield DueMovement(dc, mvt)

