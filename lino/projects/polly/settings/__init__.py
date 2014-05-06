# -*- coding: UTF-8 -*-
# Copyright 2013 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
Default settings module for a :ref:`polly` project.
"""

from __future__ import unicode_literals

from lino.projects.std.settings import *

from django.utils.translation import ugettext_lazy as _


class Site(Site):

    """
    Base class for a :ref:`polly` application,
    designed to be instantiated into the :setting:`SITE` setting.
    """

    verbose_name = "Lino Polly"
    description = _("a Lino application to make surveys and polls.")
    version = "0.1"
    url = "http://www.lino-framework.org/polly"
    author = 'Luc Saffre'
    author_email = 'luc.saffre@gmail.com'

    demo_fixtures = 'std few_countries few_cities few_languages demo demo2'.split(
    )

    languages = 'en de et'

    user_model = 'users.User'

    def setup_choicelists(self):
        """
        Defines application-specific default user profiles.
        Local site administrators can override this in their :xfile:.
        """
        from lino import dd
        from django.utils.translation import ugettext_lazy as _
        dd.UserProfiles.reset('* office polls')
        add = dd.UserProfiles.add_item
        add('000', _("Anonymous"),       '_ _ _',
            'anonymous', readonly=True, authenticated=False)
        add('100', _("User"),            'U U U', 'user')
        add('900', _("Administrator"),   'A A A', 'admin')

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'django.contrib.contenttypes'
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        #~ yield 'lino.modlib.countries'
        #~ yield 'lino.modlib.properties'
        #~ yield 'lino.modlib.' + self.partners_app_label
        #~ yield 'lino.modlib.households'
        yield 'lino.modlib.polls'
        #~ yield 'lino.modlib.pages'
        #~ yield 'lino.projects.polly'
        yield 'lino.modlib.appypod'
