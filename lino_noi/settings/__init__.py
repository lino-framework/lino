# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)


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

    root_urlconf = 'lino_noi.urls'
    # site_prefix = '/admin/'
    default_ui = None

    def get_installed_apps(self):
        """Implements :meth:`lino.core.site.Site.get_installed_apps` for Lino
        Noi.

        """
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.contenttypes'
        yield 'lino.modlib.system'
        yield 'lino_noi.lib.users'
        yield 'lino_noi.lib.contacts'
        yield 'lino.modlib.cal'
        yield 'lino_noi.lib.products'
        # yield 'lino.modlib.tickets'
        yield 'lino.modlib.clocking'
        yield 'lino.modlib.lists'

        # yield 'lino.modlib.uploads'
        yield 'lino.modlib.excerpts'
        yield 'lino.modlib.appypod'
        yield 'lino.modlib.export_excel'
        yield 'lino.modlib.tinymce'
        yield 'lino.modlib.smtpd'
        yield 'lino.modlib.stars'

        # yield 'lino.modlib.awesomeuploader'

        yield 'lino_noi.lib.noi'

    def setup_user_profiles(self):
        """Implements :meth:`lino.core.site.Site.setup_user_profiles` for Lino
        Noi.

        """
        from lino.modlib.users.choicelists import UserProfiles
        from django.utils.translation import ugettext_lazy as _
        UserProfiles.reset('* office')
        add = UserProfiles.add_item
        add('000', _("Anonymous"),       '_ _', 'anonymous',
            readonly=True, authenticated=False)
        add('100', _("User"),            'U U', 'user')
        add('200', _("Consultant"),      'U U', 'consultant')
        add('300', _("Hoster"),          'U U', 'hoster')
        add('400', _("Developer"),       'U U', 'developer')
        add('490', _("Senior"),          'U U', 'senior')
        add('900', _("Administrator"),   'A A', 'admin')

    def get_default_required(self, **kw):
        # overrides the default behaviour which would add
        # `auth=True`. In Lino Noi everybody can see everything.
        return kw

    def get_admin_main_items(self, ar):
        yield self.modules.clocking.InvestedTimes
        # yield self.modules.tickets.MyTickets
        # yield self.modules.tickets.ActiveTickets
        yield self.modules.tickets.InterestingTickets

# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
