# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

from lino.projects.std.settings import *

from django.utils.translation import ugettext_lazy as _


class Site(Site):

    verbose_name = "Lino Belref"
    description = _("Belgian Reference")
    version = "0.1"
    url = "http://www.lino-framework.org/examples/belref.html"
    author = 'Luc Saffre'
    author_email = 'luc.saffre@gmail.com'

    demo_fixtures = 'demo all_countries be inscodes'

    #~ admin_prefix = 'admin'
    default_ui = 'bootstrap3'

    #~ anonymous_user_profile =

    languages = 'fr nl de'

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.bootstrap3'
        #~ yield 'lino.modlib.contenttypes'
        #~ yield 'lino.modlib.users'
        yield 'lino.modlib.system'
        yield 'lino.modlib.statbel.countries'
        #~ yield 'lino.modlib.contacts'
        #~ yield 'lino.modlib.outbox'
        #~ yield 'lino.modlib.blogs'
        #~ yield 'lino.modlib.tickets'
        #~ yield 'lino.modlib.pages'
        yield 'lino.modlib.concepts'
        yield 'lino.projects.belref'

    def setup_menu(self, profile, main):
        """
        We create a new menu from scratch because the default menu structure
        wouldn't fit.
        """
        from lino.api import dd
        mg = dd.plugins.concepts
        m = main.add_menu(mg.app_label, mg.verbose_name)
        m.add_action(self.modules.concepts.Concepts)
        m.add_action(self.modules.countries.Countries)
        m.add_action(self.modules.countries.Places)

    # def get_main_action(self, user):
    #     return self.modules.belref.Main.default_action
