# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.api import rt, dd, _
from lino.utils import Cycler


def objects():
    User = rt.modules.users.User
    # Company = rt.modules.contacts.Company
    Product = rt.modules.products.Product
    TT = rt.modules.tickets.TicketType
    Ticket = rt.modules.tickets.Ticket
    Interest = rt.modules.tickets.Interest
    Project = rt.modules.tickets.Project
    Site = rt.modules.tickets.Site

    user = rt.modules.users.UserProfiles.user
    dev = rt.modules.users.UserProfiles.developer
    yield User(username="mathieu", profile=user)
    yield User(username="marc", profile=user)
    yield User(username="luc", profile=dev)
    yield User(username="jean", profile=rt.modules.users.UserProfiles.senior)

    USERS = Cycler(User.objects.all())

    yield TT(**dd.str2kw('name', _("Bugfix")))
    yield TT(**dd.str2kw('name', _("Enhancement")))
    yield TT(**dd.str2kw('name', _("Upgrade")))

    TYPES = Cycler(TT.objects.all())

    yield Product(name="Lino Core", ref="lino")
    yield Product(name="Lino Welfare", ref="welfare")
    yield Product(name="Lino Cosi", ref="cosi")
    yield Product(name="Lino Faggio", ref="faggio")

    PRODUCTS = Cycler(Product.objects.all())

    # kettenis = Company(name="ÖSHZ Kettenis")
    # yield kettenis
    # schaerbeek = Company(name="CPAS de Schaerbeek")
    # yield schaerbeek

    # yield Site(name="welket", partner=kettenis)
    # yield Site(name="welsch", partner=schaerbeek)

    yield Site(name="welket")
    yield Site(name="welsch")

    for u in Site.objects.all():
        for i in range(3):
            yield Interest(site=u, product=PRODUCTS.pop())

    yield Project(name="Framework", ref="lino")
    yield Project(name="Team", ref="team")
    yield Project(name="Documentation", ref="docs")

    PROJECTS = Cycler(Project.objects.all())

    def ticket(s, **kwargs):
        kwargs.update(
            ticket_type=TYPES.pop(), summary=s,
            reporter=USERS.pop(),
            product=PRODUCTS.pop())
        if False:
            kwargs.update(project=PROJECTS.pop())
        return Ticket(**kwargs)

    welket = Site.objects.get(name="welket")
    yield ticket(
        "Foo fails to bar when baz", site=welket, project=PROJECTS.pop())
    yield ticket("Bar is not always baz", project=PROJECTS.pop())
    yield ticket("Baz sucks")
    yield ticket("Foo and bar don't baz", project=PROJECTS.pop())
    yield ticket("Cannot create Foo", description="""<p>When I try to create
    a <b>Foo</b>, then I get a <b>Bar</b> instead of a Foo.</p>""")

