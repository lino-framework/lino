# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Installs standard values for :mod:`lino.modlib.cal`,
including a demo set of holidays.
(TODO: make them more configurable.)

"""

from __future__ import unicode_literals

import datetime
from dateutil.relativedelta import relativedelta
ONE_DAY = relativedelta(days=1)

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _

from lino.utils.instantiator import Instantiator

from lino.api import dd

cal = dd.resolve_app('cal')


def objects():

    add = Instantiator('cal.Priority', 'ref').build
    yield add('1', **dd.babel_values('name', en=u"very urgent", de=u"sehr dringend",   fr=u"très urgent", et=u"väga kiire"))
    yield add('3', **dd.babel_values('name', en=u"urgent", de=u"dringend",   fr=u"urgent", et="kiire"))
    yield add('5', **dd.babel_values('name', en=u"normal", de=u"normal",   fr=u"normal", et="keskmine"))
    yield add('9', **dd.babel_values('name', en=u"not urgent", de=u"nicht dringend",   fr=u"pas urgent", et="mitte kiire"))

    calendar = Instantiator('cal.Calendar').build
    general = calendar(**dd.str2kw('name', _("General")))
                                    # de="Allgemein",
                                    # fr="Général",
    yield general
    settings.SITE.site_config.site_calendar = general
    yield settings.SITE.site_config

    event_type = Instantiator('cal.EventType').build
    holidays = event_type(
        is_appointment=False,
        all_rooms=True, **dd.str2kw('name', _("Holidays")))
    yield holidays
    yield event_type(**dd.str2kw('name', _("Meeting")))

    RecurrentEvent = dd.resolve_model('cal.RecurrentEvent')
    add = Instantiator(RecurrentEvent, event_type=holidays).build

    def holiday(month, day, en, de, fr, et=None):
        if et is None:
            et = en
        return add(
            every_unit=cal.Recurrencies.yearly,
            monday=True, tuesday=True, wednesday=True, thursday=True,
            friday=True, saturday=True, sunday=True,
            every=1,
            start_date=datetime.date(
                year=cal.DEMO_START_YEAR,
                month=month, day=day),
            **dd.babelkw('name', en=en, de=de, fr=fr, et=et))
    yield holiday(1, 1, "New Year's Day", "Neujahr", "Jour de l'an", "Uusaasta")
    yield holiday(5, 1, "International Workers' Day", "Tag der Arbeit", "Premier Mai", "kevadpüha")
    yield holiday(7, 21, "National Day", "Nationalfeiertag", "Fête nationale", "Belgia riigipüha")
    yield holiday(8, 15, "Assumption of Mary", "Mariä Himmelfahrt", "Assomption de Marie")
    yield holiday(10, 31, "All Souls' Day", "Allerseelen", "Commémoration des fidèles défunts")
    yield holiday(11, 1, "All Saints' Day", "Allerheiligen", "Toussaint")
    yield holiday(11, 11, "Armistice with Germany", "Waffenstillstand", "Armistice")
    yield holiday(12, 25, "Christmas", "Weihnachten", "Noël", "Esimene Jõulupüha")

    summer = holiday(07, 01, "Summer holidays", "Sommerferien", "Vacances d'été", "Suvevaheaeg")
    summer.end_date = summer.start_date.replace(month=8, day=31)
    yield summer

    ar = settings.SITE.login()
    for obj in RecurrentEvent.objects.all():
        if not obj.update_reminders(ar):
            raise Exception("Oops, %s generated no events" % obj)
