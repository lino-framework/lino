# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Model mixins for `lino.modlib.ledger`.

.. autosummary::

"""

from __future__ import unicode_literals

from lino.api import dd, rt, _

# from .fields import MatchField


class Matchable(dd.Model):
    """Model mixin which adds a field :attr:`match` which points to the
    `ledger.Voucher` that is being cleared by this movement.

    """
    class Meta:
        abstract = True

    match = dd.ForeignKey(
        'ledger.Movement',
        help_text=_("The movement to be matched."),
        verbose_name=_("Match"),
        related_name="%(app_label)s_%(class)s_set_by_match",
        blank=True, null=True)

    @dd.chooser()
    def match_choices(cls, journal, partner):
        matchable_accounts = rt.modules.accounts.Account.objects.filter(
            matchrule__journal=journal)
        fkw = dict(account__in=matchable_accounts)
        fkw.update(satisfied=False)
        if partner:
            fkw.update(partner=partner)
        qs = rt.modules.ledger.Movement.objects.filter(**fkw)
        qs = qs.order_by('voucher__date')
        #~ qs = qs.distinct('match')
        return qs
        # return qs.values_list('match', flat=True)
