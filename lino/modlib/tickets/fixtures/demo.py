# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.api import rt, dd, _
from lino.utils import Cycler


def objects():
    User = rt.modules.users.User
    Product = rt.modules.products.Product
    TT = rt.modules.tickets.TicketType
    Ticket = rt.modules.tickets.Ticket
    Interest = rt.modules.tickets.Interest
    Project = rt.modules.tickets.Project

    p = rt.modules.users.UserProfiles.user
    yield User(username="mathieu", profile=p)
    yield User(username="marc", profile=p)
    yield User(username="luc", profile=p)
    yield User(username="jean", profile=p)

    USERS = Cycler(User.objects.all())

    yield TT(**dd.str2kw('name', _("Bugfix")))
    yield TT(**dd.str2kw('name', _("Enhancement")))
    yield TT(**dd.str2kw('name', _("Deployment")))

    TYPES = Cycler(TT.objects.all())

    yield Product(name="Lino Core")
    yield Product(name="Lino Welfare")
    yield Product(name="Lino Cosi")
    yield Product(name="Lino Faggio")

    PRODUCTS = Cycler(Product.objects.all())

    # note that robin has no interest, so he sees all tickets
    for u in User.objects.filter(profile=p):
        for i in range(3):
            yield Interest(user=u, product=PRODUCTS.pop())

    yield Project(name="Eupen")
    yield Project(name="Raeren")
    yield Project(name="Bütgenbach")

    PROJECTS = Cycler(Project.objects.all())

    def ticket(s):
        return Ticket(
            ticket_type=TYPES.pop(), summary=s,
            reporter=USERS.pop(),
            product=PRODUCTS.pop(), project=PROJECTS.pop())
    yield ticket("Foo fails to bar when baz")
    yield ticket("Bar is not always baz")
    yield ticket("Baz sucks")
    yield ticket("Foo and bar don't baz")
    yield ticket("Cannot create Foo")

