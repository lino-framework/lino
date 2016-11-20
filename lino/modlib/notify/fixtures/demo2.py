# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Emits a notification "The database has been initialized." to every
user.

"""

import datetime
from django.utils import translation
from atelier.utils import i2t
from lino.api import dd, rt, _


def objects():
    now = datetime.datetime.combine(dd.today(), i2t(548))
    mt = rt.models.notify.MessageTypes.system
    for u in rt.models.users.User.objects.all():
        with translation.override(u.language):
            yield rt.models.notify.Message.create_message(
                u, body=_("The database has been initialized."),
                created=now, message_type=mt, sent=now)
