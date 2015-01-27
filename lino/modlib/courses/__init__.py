# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds functionality for managing courses.

A **Course** is a series of scheduled calendar events where a
given teacher teaches a given group of participants about a given
topic.

There is a configurable list of **topics**.
Courses are grouped into **Lines** (meaning "series") of courses.
A course line is a series of courses on a same **topic**.

The participants of a course are stored as **Enrolments**.


.. autosummary::
   :toctree:

   models
   choicelists
   workflows

"""


from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Courses")
    teacher_model = 'contacts.Person'
    pupil_model = 'contacts.Person'

    def day_and_month(self, d):
        if d is None:
            return "-"
        return d.strftime("%d.%m.")

    def setup_main_menu(config, site, profile, main):
        m = main.add_menu("courses", config.verbose_name)
        m.add_action('courses.Courses')
        m.add_action('courses.Lines')
        m.add_action('courses.PendingRequestedEnrolments')
        m.add_action('courses.PendingConfirmedEnrolments')

    def setup_config_menu(config, site, profile, m):
        m = m.add_menu("courses", config.verbose_name)
        #~ m.add_action(Rooms)
        m.add_action('courses.Topics')
        m.add_action('courses.Slots')

    def setup_explorer_menu(config, site, profile, m):
        m = m.add_menu("courses", config.verbose_name)
        #~ m.add_action(Presences)
        #~ m.add_action(Events)
        m.add_action('courses.Enrolments')
        # m.add_action('courses.Options')
        m.add_action('courses.EnrolmentStates')

