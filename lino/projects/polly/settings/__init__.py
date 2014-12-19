# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

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
    url = "http://www.lino-framework.org/examples/polly"
    author = 'Luc Saffre'
    author_email = 'luc.saffre@gmail.com'

    demo_fixtures = 'std demo feedback demo2'.split()

    languages = 'en de et'

    user_model = 'users.User'

    def setup_choicelists(self):
        """
        Defines application-specific default user profiles.
        Local site administrators can override this in their :xfile:.
        """
        from django.utils.translation import ugettext_lazy as _
        from lino.modlib.users.mixins import UserProfiles
        UserProfiles.reset('* office polls')
        add = UserProfiles.add_item
        add('000', _("Anonymous"),       '_ _ _',
            'anonymous', readonly=True, authenticated=False)
        add('100', _("User"),            'U U U', 'user')
        add('900', _("Administrator"),   'A A A', 'admin')

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.contenttypes'
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
