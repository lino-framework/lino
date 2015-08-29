# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines the :class:`DueMovement` class, a volatile object representing
a group of matching movements.

"""

from lino.api import rt, dd

from lino.modlib.accounts.utils import ZERO


class Balance(object):
    """Light-weight object to represent a balance, i.e. an amount together
    with its booking direction (debit or credit).

    Attributes:

    .. attribute:: d

        The amount of this balance when it is debiting, otherwise zero.

    .. attribute:: c

        The amount of this balance when it is crediting, otherwise zero.

    """

    def __init__(self, d, c):
        if d > c:
            self.d = d - c
            self.c = ZERO
        else:
            self.c = c - d
            self.d = ZERO


class DueMovement(object):
    """A **due movement** is a movement which a partner should do in
    order to satisfy their debt.  Or which we should do in order to
    satisfy our debt.

    It represents a group of "matching" movements.

    The "matching" movements of a given movement are those whose
    `match`, `partner` and `account` fields have the same values.
    
    These movements are themselves grouped into "debts" and "payments".
    A "debt" increases the debt and a "payment" decreases it.
    
    .. attribute:: dc

        Whether I mean *my* debts and payments (towards that partner)
        or those *of the partner* (towards me).

    .. attribute:: match

        The first :class:`Movement` object of the group.

    .. attribute:: partner

    .. attribute:: account

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
        self.bank_account = None

        self.collect(mvt)

        qs = rt.modules.ledger.Movement.objects.filter(
            partner=self.partner, account=self.account, match=mvt)
        for mvt in qs.order_by('voucher__date'):
            self.collect(mvt)

    def collect(self, mvt):
        """Add the given movement to the list of movements that are being
        satisfied by this DueMovement.

        """
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
            bank_account = voucher.get_bank_account()
            if bank_account is not None:
                if self.bank_account != bank_account:
                    self.bank_account = bank_account
                elif self.bank_account != bank_account:
                    raise Exception("More than one IBAN/BIC")
            # else:
            #     dd.logger.info(
            #         "20150810 no bank account for {0}".format(voucher))

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

    Generates and yields a list of the :class:`DueMovement` objects
    specified by the filter criteria.

    Arguments:

        dc (boolean): The caller must specify whether he means the debts and
               payments *towards the partner* or *towards myself*.

        **flt: Any keyword argument is forwarded to Django's `filter()
            <https://docs.djangoproject.com/en/dev/ref/models/querysets/#filter>`_
            method in order to specifiy which :class:`Movement`
            objects to consider.

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
