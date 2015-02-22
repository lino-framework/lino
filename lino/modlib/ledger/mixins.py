# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Model mixins for `lino.modlib.ledger`.

.. autosummary::

"""

from __future__ import unicode_literals

from lino import dd, rt

from .fields import MatchField


class Matchable(dd.Model):

    class Meta:
        abstract = True

    match = MatchField(blank=True, null=True)

    @dd.chooser(simple_values=True)
    def match_choices(cls, partner):
        #~ DC = voucher.journal.dc
        #~ choices = []
        qs = rt.modules.ledger.Movement.objects.filter(
            partner=partner, satisfied=False)
        qs = qs.order_by('voucher__date')
        #~ qs = qs.distinct('match')
        return qs.values_list('match', flat=True)


