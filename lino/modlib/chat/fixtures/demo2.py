# Copyright 2016-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
"""
#
# import datetime
# from django.utils import translation
# from lino.utils import i2t
from lino.api import dd, rt, _
#
# from django.conf import settings
# from django.utils.timezone import make_aware
from lino.modlib.chat.models import ChatGroup, ChatGroupMember


def objects():
    groups = ['General', 'Customers request']
    for group in groups:
        g = ChatGroup(title=group)
        g.save()
        yield g

        for u in rt.models.users.User.objects.order_by('username'):

            gm = ChatGroupMember(group=g, user=u)
            gm.save()
            yield gm

    # todo Create
    # todo spawn some random chats

