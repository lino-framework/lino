# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Model mixins for `lino.modlib.boards`.

"""


from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


from lino.api import dd
from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.modlib.users.mixins import UserAuthored


class BoardDecision(UserAuthored):
    # base class for aids.Confirmation
    class Meta:
        abstract = True

    decision_date = models.DateField(
        verbose_name=_('Decided'), blank=True, null=True)
    board = models.ForeignKey('boards.Board', blank=True, null=True)

    @dd.chooser()
    def board_choices(self, decision_date):
        M = dd.resolve_model('boards.Board')
        qs = M.objects.all()
        if decision_date:
            qs = dd.PeriodEvents.active.add_filter(qs, decision_date)
        return qs

