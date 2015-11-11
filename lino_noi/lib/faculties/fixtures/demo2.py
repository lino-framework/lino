# -*- coding: UTF-8 -*-
"""

"""
from __future__ import unicode_literals
from __future__ import print_function

import datetime

from lino.api import rt, dd
from lino.utils import Cycler

from lino.core.roles import SiteAdmin
from lino.modlib.cal.utils import DurationUnits
from lino_noi.lib.tickets.roles import Worker
from lino.utils.quantities import Duration


def objects():
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
