# Copyright 2009-2011 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Default settings for :mod:`lino.projects.crl`.

"""

import os
import lino

from lino.projects.std.settings import *

from lino.utils.jsgen import js_code


class Site(Site):

    languages = ('en', 'fr', 'de')

    #~ source_dir = os.path.dirname(__file__)
    title = "Lino/CRL"
    #~ domain = "dsbe.saffre-rumma.net"
    help_url = "http://lino.saffre-rumma.net/crl/index.html"

    def is_abstract_model(self, name):
        if name == 'contacts.Person':
            return True
        return False


SITE = Site(globals())



TIME_ZONE = 'Europe/Brussels'

# ~ SITE_ID = 1 # see also fill.py

INSTALLED_APPS = (
    #~ 'django.contrib.auth',
    'lino.modlib.users',
    'lino.modlib.gfks',
    #~ 'django.contrib.sessions',
    #~ 'django.contrib.sites',
    #~ 'django.contrib.markup',
    #~ 'lino.modlib.system',
    'lino',
    'lino.modlib.countries',
    #~ 'lino.modlib.documents',
    'lino.modlib.properties',
    'lino.modlib.contacts',
    #~ 'lino.modlib.projects',
    'lino.modlib.notes',
    #~ 'lino.modlib.links',
    'lino.modlib.uploads',
    #~ 'lino.modlib.thirds',
    'lino.modlib.cal',
    #~ 'lino.modlib.jobs',
    'lino.projects.crl',
    # ~ 'south', # http://south.aeracode.org
)
