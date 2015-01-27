# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""

"""

from __future__ import unicode_literals

from lino.api import dd
notes = dd.resolve_app('notes')


def objects():
    if False and notes:
        NoteType = dd.resolve_model('notes.NoteType')
        yield NoteType(
            template="Letter.odt",
            build_method="appyodt",
            body_template="payment_reminder.body.html",
            **dd.babel_values('name',
                              en="Payment reminder",
                              fr="Rappel de paiement",
                              de="Zahlungserinnerung"))
