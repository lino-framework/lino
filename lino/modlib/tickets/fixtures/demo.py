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

    user = rt.modules.users.UserProfiles.user
    dev = rt.modules.users.UserProfiles.developer
    yield User(username="mathieu", profile=user)
    yield User(username="marc", profile=user)
    yield User(username="luc", profile=dev)
    yield User(username="jean", profile=dev)

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

    # note that developers has no interest, so they sees all tickets
    for u in User.objects.filter(profile=user):
        for i in range(3):
            yield Interest(user=u, product=PRODUCTS.pop())

    yield Project(name="Eupen")
    yield Project(name="Raeren")
    yield Project(name="Bütgenbach")

    PROJECTS = Cycler(Project.objects.all())

    def ticket(s, **kwargs):
        kwargs.update(
            ticket_type=TYPES.pop(), summary=s,
            reporter=USERS.pop(),
            product=PRODUCTS.pop(), project=PROJECTS.pop())
        return Ticket(**kwargs)
    yield ticket("Foo fails to bar when baz")
    yield ticket("Bar is not always baz")
    yield ticket("Baz sucks")
    yield ticket("Foo and bar don't baz")
    yield ticket("Cannot create Foo", description="""<p>When I try to create
    a <b>Foo</b>, then I get a <b>Bar</b> instead of a Foo.</p>""")

