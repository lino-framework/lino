# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.api import rt, dd, _
from lino.utils import Cycler


def objects():
    TT = rt.modules.tickets.TicketType
    Ticket = rt.modules.tickets.Ticket
    yield TT(**dd.str2kw('name', _("Bugfix")))
    yield TT(**dd.str2kw('name', _("Enhancement")))
    yield TT(**dd.str2kw('name', _("Deployment")))

    TYPES = Cycler(TT.objects.all())
    User = rt.modules.users.User
    USERS = Cycler(User.objects.all())

    def ticket(s):
        return Ticket(
            ticket_type=TYPES.pop(), summary=s, reporter=USERS.pop())
    yield ticket("Foo")
    yield ticket("Bar")
    yield ticket("Baz")
