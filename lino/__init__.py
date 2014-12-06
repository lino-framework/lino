# -*- coding: UTF-8 -*-
# Copyright 2002-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The ``lino`` module can be imported even from a Django :xfile:`settings.py`
file since it does not import any django module.

"""

from __future__ import unicode_literals

import os

from os.path import join, dirname

execfile(join(dirname(__file__), 'setup_info.py'))
__version__ = SETUP_INFO['version']
intersphinx_urls = dict(docs="http://www.lino-framework.org")
srcref_url = 'https://github.com/lsaffre/lino/blob/master/%s'


def setup_project(settings_module):
    os.environ['DJANGO_SETTINGS_MODULE'] = settings_module
    from lino.runtime import settings


from django.utils.translation import ugettext_lazy as _
"""The above is here so we can write a single import statement in
plugins::

  from lino import ad, _

"""

DJANGO_DEFAULT_LANGUAGE = 'en-us'


def assert_django_code(django_code):
    if '_' in django_code:
        raise Exception("Invalid language code %r. "
                        "Use values like 'en' or 'en-us'." % django_code)


from django import VERSION

if VERSION[0] == 1:
    if VERSION[1] > 6:
        AFTER17 = True
    else:
        AFTER17 = False
else:
    raise Exception("Unsupported Django version %s" % VERSION)


def startup():
    # called from `lino.models`
    from django.conf import settings
    if False:
        settings.SITE.startup()
    else:
        try:
            settings.SITE.startup()
        except ImportError as e:
            import traceback
            #~ traceback.print_exc(e)
            #~ sys.exit(-1)
            raise Exception("ImportError during startup:\n" +
                            traceback.format_exc(e))




if AFTER17:

    from django.apps import AppConfig

    class AppConfig(AppConfig):
        name = 'lino'
        # verbose_name = "Djangosite"
    
        def ready(self):
            
            startup()

    default_app_config = 'lino.AppConfig'


