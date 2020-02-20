# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
"""
#
# import datetime
# from django.utils import translation
# from atelier.utils import i2t
# from lino.api import dd, rt, _
#
# from django.conf import settings
# from django.utils.timezone import make_aware
from lino.modlib.chat.models import ChatGroup


def objects():
    groups = ['General', 'Customers request']
    for group in groups:
        yield ChatGroup(name=group).save()
