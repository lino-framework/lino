# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Lino CMS is yet another simple Content Management System.

"""

from django.utils.translation import ugettext_lazy as _

from lino.projects.std.settings import *


class Site(Site):

    #~ title = __name__
    verbose_name = "Lino CMS"
    #~ description = _("yet another Content Management System.")
    version = "0.1"
    author = 'Luc Saffre'
    author_email = 'luc.saffre@fsfe.org'

    default_ui = 'bootstrap3'

    languages = 'en de fr'

    project_model = 'tickets.Project'
    user_model = 'users.User'

    sidebar_width = 3

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.contenttypes'
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.contacts'
        #~ yield 'lino.modlib.outbox'
        yield 'lino.modlib.blogs'
        yield 'lino.modlib.tickets'
        yield 'lino.modlib.pages'
        yield 'lino.projects.cms'


    # def get_apps_modifiers(self, **kk):
    #     kw = super(Site, self).get_apps_modifiers(**kk)
    #     kw.update(extjs=None)
    #     return kw


SITE = Site(globals())
