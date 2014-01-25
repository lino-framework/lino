# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
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
Default settings module for a :ref:`cosi` project.
"""

from __future__ import unicode_literals

from lino_cosi.settings import *

from django.utils.translation import ugettext_lazy as _


class Site(Site):

    """
    Base class for a :ref:`cosi` application,
    designed to be instantiated into the :setting:`SITE` setting.
    
    """

    #~ title = __name__
    verbose_name = "Lino Start"
    description = _("a Lino application for startup projects.")
    version = "0.1"
    # url = "http://www.lino-framework.org/cosi"
    #~ author = 'Luc Saffre'
    #~ author_email = 'luc.saffre@gmail.com'

    demo_fixtures = 'std intro furniture demo demo2'.split()

    default_ui = 'pages'
    
    sidebar_width = 3
    user_model = 'users.User'

    languages = 'en et'
    #~ languages = 'de fr et en'.split()

    # def setup_plugins(self):
    #     self.configure_plugin('extjs', url_prefix='admin')

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()

        yield 'lino.modlib.pages'
        yield 'lino.modlib.blogs'
        yield 'lino.modlib.extensible'
        yield 'lino.modlib.cal'
        yield 'lino.modlib.uploads'
        yield 'lino.modlib.outbox'
        yield 'lino.modlib.importfilters'
