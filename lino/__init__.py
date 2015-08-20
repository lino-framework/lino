# -*- coding: UTF-8 -*-
# Copyright 2002-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""This is the main module of the Lino framework.

.. autosummary::
   :toctree:

   core
   hello
   api
   utils
   mixins
   projects
   modlib


"""

from __future__ import unicode_literals

import sys
import os
from os.path import join, dirname


execfile(join(dirname(__file__), 'setup_info.py'))
__version__ = SETUP_INFO['version']
intersphinx_urls = dict(docs="http://www.lino-framework.org")
srcref_url = 'https://github.com/lsaffre/lino/blob/master/%s'


if sys.version_info[0] > 2:
    PYAFTER26 = True
elif sys.version_info[0] == 2 and sys.version_info[1] > 6:
    PYAFTER26 = True
else:
    PYAFTER26 = False


def setup_project(settings_module):
    os.environ['DJANGO_SETTINGS_MODULE'] = settings_module
    from lino.api.shell import settings


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
    # called from `lino.models` (before Django 1.7) or below (after 1.7)
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

# deprecated use, only for backwards compat:
from django.utils.translation import ugettext_lazy as _

