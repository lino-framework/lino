# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
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


from lino.projects.std.settings import *

class Site(Site):
    title = "Lino/MinimalApp 2"
    #~ help_url = "http://lino.saffre-rumma.net/az/index.html"

    #~ project_model = 'contacts.Person'
    #~ project_model = 'contacts.Person'
    project_model = 'projects.Project'
    user_model = "users.User"

    #~ languages = ('de', 'fr')
    languages = 'en et'

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'django.contrib.contenttypes'
        yield 'lino.modlib.system'
        yield 'lino.modlib.changes'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'
        yield 'lino.projects.min2.modlib.contacts'
        yield 'lino.modlib.addresses'
        yield 'lino.modlib.reception'
        yield 'lino.modlib.iban'
        yield 'lino.modlib.sepa'
        yield 'lino.modlib.notes'
        yield 'lino.modlib.projects'
        yield 'lino.modlib.uploads'
        yield 'lino.modlib.humanlinks'
        yield 'lino.modlib.households'
        yield 'lino.modlib.cal'
        # yield 'lino.modlib.extensible'
        yield 'lino.modlib.outbox'
        yield 'lino.modlib.pages'
        #~ yield 'lino.projects.min2'
        yield 'lino.modlib.export_excel'

    def setup_choicelists(self):
        """
        Defines a set of user profiles.
        """
        from lino import dd
        from django.utils.translation import ugettext_lazy as _
        dd.UserProfiles.reset(
            '* office reception')
        add = dd.UserProfiles.add_item
        add('000', _("Anonymous"),      '_ _ _',
            name='anonymous',
            readonly=True,
            authenticated=False)
        add('100', _("User"),           'U U U')
        add('900', _("Administrator"),  'A A A',
            name='admin')


SITE = Site(globals(), no_local=True)

SECRET_KEY = "20227"  # see :djangoticket:`20227`

DEBUG = True
