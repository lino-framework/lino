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
from lino.utils import Cycler, i2d

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
    User = rt.models.users.User
    Partner = rt.models.contacts.Partner
    Topic = rt.models.topics.Topic
    TT = rt.models.tickets.TicketType
    Ticket = rt.models.tickets.Ticket
    Interest = rt.models.topics.Interest
    Milestone = rt.models.deploy.Milestone
    Project = rt.models.tickets.Project
    Site = rt.models.tickets.Site
    Link = rt.models.tickets.Link
    LinkTypes = rt.models.tickets.LinkTypes

    cons = rt.models.users.UserProfiles.consultant
    dev = rt.models.users.UserProfiles.developer
    yield User(username="mathieu", profile=cons)
    yield User(username="marc", profile=cons)
    yield User(username="luc", profile=dev)
    yield User(username="jean", profile=rt.models.users.UserProfiles.senior)

    USERS = Cycler(User.objects.all())

    yield TT(**dd.str2kw('name', _("Bugfix")))
    yield TT(**dd.str2kw('name', _("Enhancement")))
    yield TT(**dd.str2kw('name', _("Upgrade")))

    TYPES = Cycler(TT.objects.all())

    yield Topic(name="Lino Core", ref="linõ")
    yield Topic(name="Lino Welfare", ref="welfäre")
    yield Topic(name="Lino Cosi", ref="così")
    yield Topic(name="Lino Voga", ref="faggio")
    # ref differs from name

    TOPICS = Cycler(Topic.objects.all())

    for name in "welket welsch pypi".split():

        obj = Partner(name=name)
        yield obj
        yield Site(name=name, partner=obj)

    for u in Partner.objects.exclude(name="pypi"):
        for i in range(3):
            yield Interest(partner=u, topic=TOPICS.pop())

    SITES = Cycler(Site.objects.exclude(name="pypi"))
    for i in range(7):
        d = dd.today(i*2-20)
        yield Milestone(site=SITES.pop(), expected=d, reached=d)
    yield Milestone(site=SITES.pop(), expected=dd.today())

    prj1 = Project(
        name="Framewörk", ref="linö", private=False,
        start_date=i2d(20090101))
    yield prj1
    yield Project(
        name="Téam", ref="téam", start_date=i2d(20100101), parent=prj1)
    prj2 = Project(
        name="Documentatión", ref="docs", private=False,
        start_date=i2d(20090101), parent=prj1)
    yield prj2
    yield Project(
        name="Research", ref="research", private=False,
        start_date=i2d(19980101), parent=prj2)
    yield Project(
        name="Shop", ref="shop", private=False,
        start_date=i2d(20120201), end_date=i2d(20120630))

    PROJECTS = Cycler(Project.objects.all())
    SITES = Cycler(Site.objects.all())
    TicketStates = rt.models.tickets.TicketStates
    TSTATES = Cycler(TicketStates.objects())

    def ticket(summary, **kwargs):
        site = SITES.pop()
        kwargs.update(
            ticket_type=TYPES.pop(), summary=summary,
            reporter=USERS.pop(),
            site=site,
            state=TSTATES.pop(),
            topic=TOPICS.pop())
            
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
    SessionType = rt.models.clocking.SessionType
    Session = rt.models.clocking.Session
    Ticket = rt.models.tickets.Ticket
    User = rt.models.users.User
    UserProfiles = rt.models.users.UserProfiles
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

    ServiceReport = rt.models.clocking.ServiceReport
    Site = rt.models.contacts.Partner
    welket = Site.objects.get(name="welket")
    yield ServiceReport(
        start_date=dd.today(-90), interesting_for=welket)


def faculties_objects():
    "was previously in faculties.fixtures.demo2"

    Faculty = rt.models.faculties.Faculty
    Competence = rt.models.faculties.Competence
    User = rt.models.users.User

    yield Faculty(**dd.str2kw('name', 'Analysis'))
    yield Faculty(**dd.str2kw('name', 'Code changes'))
    yield Faculty(**dd.str2kw('name', 'Documentation'))
    yield Faculty(**dd.str2kw('name', 'Testing'))
    yield Faculty(**dd.str2kw('name', 'Configuration'))
    yield Faculty(**dd.str2kw('name', 'Enhancement'))
    yield Faculty(**dd.str2kw('name', 'Optimization'))
    yield Faculty(**dd.str2kw('name', 'Offer'))

    Analysis = Faculty.objects.get(name="Analysis")
    Code_changes = Faculty.objects.get(name="Code changes")
    Documentation = Faculty.objects.get(name="Documentation")
    Testing = Faculty.objects.get(name="Testing")
    Configuration = Faculty.objects.get(name="Configuration")

    mathieu = User.objects.get(username="mathieu")
    Robin = User.objects.get(first_name="Robin")
    luc = User.objects.get(username="luc")

    if dd.get_language_info('de'):
        Rolf = User.objects.get(first_name="Rolf")
        yield Competence(faculty=Analysis, user=Rolf)
        yield Competence(faculty=Code_changes, user=Rolf, affinity=70)
        yield Competence(faculty=Documentation, user=Rolf, affinity=71)
        yield Competence(faculty=Testing, user=Rolf, affinity=42)
        yield Competence(faculty=Configuration, user=Rolf, affinity=62)

    if dd.get_language_info('fr'):
        Romain = User.objects.get(first_name="Romain")
        yield Competence(faculty=Code_changes, user=Romain, affinity=76)
        yield Competence(faculty=Documentation, user=Romain, affinity=92)
        yield Competence(faculty=Testing, user=Romain, affinity=98)
        yield Competence(faculty=Configuration, user=Romain, affinity=68)

    yield Competence(faculty=Analysis, user=Robin, affinity=23)
    yield Competence(faculty=Analysis, user=luc, affinity=120)

    yield Competence(faculty=Code_changes, user=luc, affinity=150)

    yield Competence(faculty=Documentation, user=luc, affinity=75)
    yield Competence(faculty=Documentation, user=mathieu, affinity=46)

    yield Competence(faculty=Testing, user=Robin, affinity=65)
    yield Competence(faculty=Testing, user=mathieu, affinity=42)

    yield Competence(faculty=Configuration, user=luc, affinity=46)
    yield Competence(faculty=Configuration, user=mathieu, affinity=92)

    Bar_cannot_foo = rt.models.tickets.Ticket.objects.get(summary='Bar cannot foo')
    Bar_cannot_foo.faculty = Documentation
    Bar_cannot_foo.save()

    Sell_bar_in_baz = rt.models.tickets.Ticket.objects.get(summary='Sell bar in baz')
    Sell_bar_in_baz.faculty = Analysis
    Sell_bar_in_baz.save()

    Foo_cannot_bar = rt.models.tickets.Ticket.objects.get(summary='Foo cannot bar')
    Foo_cannot_bar.faculty = Code_changes
    Foo_cannot_bar.save()

    Foo_never_matches_Bar = rt.models.tickets.Ticket.objects.get(summary='Foo never matches Bar')
    Foo_never_matches_Bar.faculty = Testing
    Foo_never_matches_Bar.save()
