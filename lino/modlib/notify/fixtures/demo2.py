# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Emits a notification "The database has been initialized." to every
user.

"""

import datetime
from django.utils import translation
from atelier.utils import i2t
from lino.api import dd, rt, _

from django.conf import settings
from django.utils.timezone import make_aware


def objects():
    now = datetime.datetime.combine(dd.today(), i2t(548))
    if settings.USE_TZ:
        now = make_aware(now)
    mt = rt.models.notify.MessageTypes.system
    for u in rt.models.users.User.objects.order_by('username'):
        # if u.user_type.has_required_roles()
        with translation.override(u.language):
            yield rt.models.notify.Message.create_message(
                u, subject=_("The database has been initialized."),
                mail_mode=u.mail_mode, created=now, message_type=mt,
                sent=now)
