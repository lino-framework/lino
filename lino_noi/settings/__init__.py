# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""

.. autosummary::
   :toctree:

   public
   doctests
   demo



"""

from __future__ import print_function
from __future__ import unicode_literals

from lino.projects.std.settings import *


class Site(Site):

    verbose_name = "Lino Noi"
    url = "http://noi.lino-framework.org/"
    version = '0.0.1'

    demo_fixtures = ['std', 'demo', 'demo2']
                     # 'linotickets',
                     # 'tractickets', 'luc']

    project_model = 'tickets.Project'
    textfield_format = 'html'
    user_profiles_module = 'lino_noi.lib.noi.roles'

    def get_installed_apps(self):
        """Implements :meth:`lino.core.site.Site.get_installed_apps` for Lino
        Noi.

        """
        yield super(Site, self).get_installed_apps()
        # yield 'lino.modlib.extjs'
        # yield 'lino.modlib.bootstrap3'
        yield 'lino.modlib.contenttypes'
        # yield 'lino.modlib.system'
        yield 'lino_noi.lib.users'
        yield 'lino_noi.lib.contacts'
        yield 'lino.modlib.cal'
        yield 'lino_noi.lib.products'
        # yield 'lino.modlib.tickets'
        yield 'lino.modlib.clocking'
        yield 'lino.modlib.lists'

        # yield 'lino.modlib.uploads'
        # yield 'lino.modlib.excerpts'
        yield 'lino.modlib.export_excel'
        yield 'lino.modlib.tinymce'
        yield 'lino.modlib.smtpd'
        yield 'lino.modlib.stars'

        # yield 'lino.modlib.awesomeuploader'

        yield 'lino_noi.lib.noi'

    def get_default_required(self, **kw):
        # overrides the default behaviour which would add
        # `auth=True`. In Lino Noi everybody can see everything.
        return kw

    def get_admin_main_items(self, ar):
        yield self.modules.clocking.InvestedTimes
        # yield self.modules.tickets.MyTickets
        # yield self.modules.tickets.ActiveTickets
        yield self.modules.tickets.InterestingTickets
        yield self.modules.tickets.PublicTickets

    def setup_quicklinks(self, ar, tb):
        super(Site, self).setup_quicklinks(ar, tb)

        tb.add_action(self.modules.tickets.TicketsToTriage)
        tb.add_action(self.modules.tickets.TicketsToTalk)
        tb.add_action(self.modules.tickets.TicketsToDo)

# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
