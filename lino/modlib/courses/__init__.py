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


    
