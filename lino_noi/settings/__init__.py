# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)


from __future__ import print_function
from __future__ import unicode_literals

from lino.projects.std.settings import *


class Site(Site):

    verbose_name = "Lino Noi"

    version = '0.0.1'

    demo_fixtures = ['std', 'demo', 'demo2',
                     # 'linotickets',
                     'tractickets', 'luc']

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.contenttypes'
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.contacts'
        yield 'lino.modlib.cal'
        # yield 'lino.modlib.products'
        yield 'lino.modlib.tickets'
        yield 'lino.modlib.lists'

        yield 'lino.modlib.excerpts'
        yield 'lino.modlib.appypod'
        yield 'lino.modlib.export_excel'
        yield 'lino.modlib.smtpd'

        # yield 'lino.modlib.awesomeuploader'

        yield 'lino_noi'

    def get_default_required(self, **kw):
        # overrides the default behaviour which would add
        # `auth=True`. In Lino Noi everybody can see everything.
        return kw

    def get_admin_main_items(self, ar):
        yield self.modules.tickets.MyTickets
        yield self.modules.tickets.RecentTickets

# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
