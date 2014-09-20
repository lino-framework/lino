# -*- coding: UTF-8 -*-
# Copyright 2012-2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


from north.dbutils import babel_values
from lino import dd, rt
notes = dd.resolve_app('notes')


def objects():
    if False and notes:
        NoteType = dd.resolve_model('notes.NoteType')
        yield NoteType(
            template="Letter.odt",
            build_method="appyodt",
            body_template="payment_reminder.body.html",
            **babel_values('name',
                           en="Payment reminder",
                           fr="Rappel de paiement",
                           de="Zahlungserinnerung"))
