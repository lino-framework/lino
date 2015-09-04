# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Settings for providing readonly public access to the site. This
does not use :mod:`lino.modlib.extjs` but :mod:`lino.modlib.bootstrap3`.

"""

from lino_noi.projects.team.settings.demo import *


class Site(Site):

    default_ui = 'bootstrap3'
    default_user = 'anonymous'

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.bootstrap3'

