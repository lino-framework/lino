# -*- coding: UTF-8 -*-
# Copyright 2015-2016 Luc Saffre
#
# This file is part of Lino Noi.
#
# Lino Noi is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Noi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Noi.  If not, see
# <http://www.gnu.org/licenses/>.


from __future__ import unicode_literals
from __future__ import print_function

import datetime

from lino.api import rt, dd, _
from lino.utils import Cycler

from lino.core.roles import SiteAdmin
from lino_xl.lib.cal.choicelists import DurationUnits
from lino_noi.lib.tickets.roles import Worker
from lino.utils.quantities import Duration


def objects():
    yield tickets_objects()
    yield clockings_objects()
    yield faculties_objects()


def tickets_objects():
    # was previously in tickets
    User = rt.modules.users.User
    # Company = rt.modules.contacts.Company
    Product = rt.modules.products.Product
    TT = rt.modules.tickets.TicketType
    Ticket = rt.modules.tickets.Ticket
    Interest = rt.modules.tickets.Interest
    Milestone = rt.modules.tickets.Milestone
    Project = rt.modules.tickets.Project
    Site = rt.modules.tickets.Site
    Link = rt.modules.tickets.Link
    LinkTypes = rt.modules.tickets.LinkTypes

    cons = rt.modules.users.UserProfiles.consultant
    dev = rt.modules.users.UserProfiles.developer
    yield User(username="mathieu", profile=cons)
    yield User(username="marc", profile=cons)
    yield User(username="luc", profile=dev)
    yield User(username="jean", profile=rt.modules.users.UserProfiles.senior)

    USERS = Cycler(User.objects.all())

    yield TT(**dd.str2kw('name', _("Bugfix")))
    yield TT(**dd.str2kw('name', _("Enhancement")))
    yield TT(**dd.str2kw('name', _("Upgrade")))

    TYPES = Cycler(TT.objects.all())

    yield Product(name="Lino Core", ref="linõ")
    yield Product(name="Lino Welfare", ref="welfäre")
    yield Product(name="Lino Cosi", ref="così")
    yield Product(name="Lino Faggio", ref="faggiö")

    PRODUCTS = Cycler(Product.objects.all())

    # kettenis = Company(name="ÖSHZ Kettenis")
    # yield kettenis
    # schaerbeek = Company(name="CPAS de Schaerbeek")
    # yield schaerbeek

    # yield Site(name="welket", partner=kettenis)
    # yield Site(name="welsch", partner=schaerbeek)

    yield Site(name="welket")
    yield Site(name="welsch")
    yield Site(name="pypi")

    for u in Site.objects.exclude(name="pypi"):
        for i in range(3):
            yield Interest(site=u, product=PRODUCTS.pop())

    SITES = Cycler(Site.objects.exclude(name="pypi"))
    for i in range(7):
        d = dd.today(i*2-20)
        yield Milestone(site=SITES.pop(), expected=d, reached=d)
    yield Milestone(site=SITES.pop(), expected=dd.today())

    yield Project(name="Framewörk", ref="linö", private=False)
    yield Project(name="Téam", ref="téam")
    yield Project(name="Documentatión", ref="docs", private=False)
    yield Project(name="Research", ref="research", private=False)
    yield Project(name="Shop", ref="shop", private=False)

    PROJECTS = Cycler(Project.objects.all())
    SITES = Cycler(Site.objects.all())

    def ticket(summary, **kwargs):
        site = SITES.pop()
        kwargs.update(
            ticket_type=TYPES.pop(), summary=summary,
            reporter=USERS.pop(),
            site=site,
            product=PRODUCTS.pop())
            
        if False:
            kwargs.update(project=PROJECTS.pop())
        return Ticket(**kwargs)

    welket = Site.objects.get(name="welket")
    yield ticket(
        "Föö fails to bar when baz", site=welket, project=PROJECTS.pop())
    yield ticket("Bar is not always baz", project=PROJECTS.pop())
    yield ticket("Baz sucks")
    yield ticket("Foo and bar don't baz", project=PROJECTS.pop())
    # a ticket without project:
    yield ticket("Cannot create Foo", description="""<p>When I try to create
    a <b>Foo</b>, then I get a <b>Bar</b> instead of a Foo.</p>""")

    yield ticket("Sell bar in baz", project=PROJECTS.pop())
    yield ticket("No Foo after deleting Bar", project=PROJECTS.pop())
    yield ticket("Is there any Bar in Foo?", project=PROJECTS.pop())
    yield ticket("Foo never matches Bar", project=PROJECTS.pop())
    yield ticket("Where can I find a Foo when bazing Bazes?",
                 project=PROJECTS.pop())
    yield ticket("Class-based Foos and Bars?", project=PROJECTS.pop())
    yield ticket("Foo cannot bar", project=PROJECTS.pop())

    # Example of memo markup:
    yield ticket("Bar cannot foo", project=PROJECTS.pop(),
                 description="""<p>Linking to [ticket 1] and to
                 [url http://luc.lino-framework.org/blog/2015/0923.html blog].</p>
                 """)
 
    yield ticket("Bar cannot baz", project=PROJECTS.pop())
    yield ticket("Bars have no foo", project=PROJECTS.pop())
    yield ticket("How to get bar from foo", project=PROJECTS.pop())

    yield Link(
        type=LinkTypes.requires,
        parent=Ticket.objects.get(pk=1),
        child=Ticket.objects.get(pk=2))


def clockings_objects():
    # was previously in clockings
    SessionType = rt.modules.clocking.SessionType
    Session = rt.modules.clocking.Session
    Ticket = rt.modules.tickets.Ticket
    # TicketStates = rt.modules.tickets.TicketStates
    User = rt.modules.users.User
    UserProfiles = rt.modules.users.UserProfiles
    # devs = (UserProfiles.developer, UserProfiles.senior)
    devs = [p for p in UserProfiles.items()
            if p.has_required_roles([Worker])
            and not p.has_required_roles([SiteAdmin])]
    workers = User.objects.filter(profile__in=devs)
    WORKERS = Cycler(workers)
    TYPES = Cycler(SessionType.objects.all())
    TICKETS = Cycler(Ticket.objects.all())
    DURATIONS = Cycler([12, 138, 90, 10, 122, 209, 37, 62, 179, 233, 5])

    # every fourth ticket is unassigned and thus listed in
    # PublicTickets
    # for i, t in enumerate(Ticket.objects.exclude(private=True)):
    for i, t in enumerate(Ticket.objects.all()):
        if i % 4:
            t.assigned_to = WORKERS.pop()
            yield t

    for u in workers:

        TICKETS = Cycler(Ticket.objects.filter(assigned_to=u))
        if len(TICKETS) == 0:
            continue

        for offset in (0, -1, -3, -4):

            date = dd.demo_date(offset)
            worked = Duration()
            ts = datetime.datetime.combine(date, datetime.time(9, 0, 0))
            for i in range(7):
                obj = Session(
                    ticket=TICKETS.pop(), session_type=TYPES.pop(), user=u)
                obj.set_datetime('start', ts)
                d = DURATIONS.pop()
                worked += d
                if offset < 0:
                    ts = DurationUnits.minutes.add_duration(ts, d)
                    obj.set_datetime('end', ts)
                yield obj
                if offset == 0 or worked > 8:
                    break

    ServiceReport = rt.modules.clocking.ServiceReport
    Site = rt.modules.tickets.Site
    welket = Site.objects.get(name="welket")
    yield ServiceReport(
        start_date=dd.today(-90), interesting_for=welket)


def faculties_objects():
    "was previously in faculties.fixtures.demo2"

    Analysis = rt.modules.faculties.Faculty.objects.get(name="Analysis")
    Code_changes = rt.modules.faculties.Faculty.objects.get(name="Code changes")
    Documentation = rt.modules.faculties.Faculty.objects.get(name="Documentation")
    Testing = rt.modules.faculties.Faculty.objects.get(name="Testing")
    Configuration = rt.modules.faculties.Faculty.objects.get(name="Configuration")

    Competence = rt.modules.faculties.Competence
    Rolf = rt.modules.users.User.objects.get(first_name="Rolf")
    Romain = rt.modules.users.User.objects.get(first_name="Romain")
    mathieu = rt.modules.users.User.objects.get(username="mathieu")
    Robin = rt.modules.users.User.objects.get(first_name="Robin")
    luc = rt.modules.users.User.objects.get(username="luc")

    yield Competence(faculty=Analysis, user=Rolf)
    yield Competence(faculty=Analysis, user=Robin, weight=23)
    yield Competence(faculty=Analysis, user=luc, weight=120)

    yield Competence(faculty=Code_changes, user=luc, weight=150)
    yield Competence(faculty=Code_changes, user=Rolf, weight=70)
    yield Competence(faculty=Code_changes, user=Romain, weight=76)

    yield Competence(faculty=Documentation, user=luc, weight=75)
    yield Competence(faculty=Documentation, user=mathieu, weight=46)
    yield Competence(faculty=Documentation, user=Romain, weight=92)
    yield Competence(faculty=Documentation, user=Rolf, weight=71)

    yield Competence(faculty=Testing, user=Robin, weight=65)
    yield Competence(faculty=Testing, user=mathieu, weight=42)
    yield Competence(faculty=Testing, user=Romain, weight=98)
    yield Competence(faculty=Testing, user=Rolf, weight=42)

    yield Competence(faculty=Configuration, user=luc, weight=46)
    yield Competence(faculty=Configuration, user=Rolf, weight=62)
    yield Competence(faculty=Configuration, user=Romain, weight=68)
    yield Competence(faculty=Configuration, user=mathieu, weight=92)

    Bar_cannot_foo = rt.modules.tickets.Ticket.objects.get(summary='Bar cannot foo')
    Bar_cannot_foo.faculty = Documentation
    Bar_cannot_foo.save()

    Sell_bar_in_baz = rt.modules.tickets.Ticket.objects.get(summary='Sell bar in baz')
    Sell_bar_in_baz.faculty = Analysis
    Sell_bar_in_baz.save()

    Foo_cannot_bar = rt.modules.tickets.Ticket.objects.get(summary='Foo cannot bar')
    Foo_cannot_bar.faculty = Code_changes
    Foo_cannot_bar.save()

    Foo_never_matches_Bar = rt.modules.tickets.Ticket.objects.get(summary='Foo never matches Bar')
    Foo_never_matches_Bar.faculty = Testing
    Foo_never_matches_Bar.save()
