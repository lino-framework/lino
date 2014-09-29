# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.projects.std.settings import *


class Site(Site):
    title = "Lino Mini 1"

    user_model = 'users.User'

    languages = "en de"

    # default_user = 'root'

    demo_fixtures = 'std demo demo2'

    def setup_quicklinks(self, ar, tb):
        tb.add_action(self.modules.contacts.Persons.detail_action)
        tb.add_action(self.modules.contacts.Companies.detail_action)

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()

        yield 'django.contrib.contenttypes'
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.contacts'
        yield 'lino.modlib.cal'
        yield 'lino.modlib.export_excel'

    def get_admin_main_items(self):
        yield self.modules.cal.MyEvents

SITE = Site(globals(), no_local=True)

SECRET_KEY = "20227"  # see :djangoticket:`20227`

DEBUG = True
