# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Settings for providing readonly public access to the site. This
does not use :mod:`lino.modlib.extjs` but a traditional
Django user interface using the hand-written URLConf module
:mod:`lino_noi.urls`.

"""

from lino_noi.settings import *


class Site(Site):

    root_urlconf = 'lino_noi.urls'
    default_ui = None

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.bootstrap3'


SITE = Site(globals())
