# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# This file is part of the Lino-Welfare project.
# Lino-Welfare is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino-Welfare is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino-Welfare; if not, see <http://www.gnu.org/licenses/>.

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
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

