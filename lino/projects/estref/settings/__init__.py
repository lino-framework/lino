# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

from lino.projects.std.settings import *

from django.utils.translation import ugettext_lazy as _


class Site(Site):

    verbose_name = "Lino EstRef"
    description = _("Estonian Reference")
    version = "0.1"
    url = "http://www.lino-framework.org/estref.html"
    author = 'Luc Saffre'
    author_email = 'luc.saffre@gmail.com'

    demo_fixtures = 'all_countries est demo2'

    languages = 'et en'

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.system'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.contacts'
        yield 'lino.projects.estref'

