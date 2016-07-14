# -*- coding: UTF-8 -*-
# Copyright 2002-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""The :mod:`lino` package contains the core of the Lino framework.

.. autosummary::
   :toctree:

   core
   hello
   api
   utils
   mixins
   projects
   modlib
   sphinxcontrib


"""

from __future__ import unicode_literals
from __future__ import absolute_import

import logging
logger = logging.getLogger(__name__)

import sys
import os
from os.path import join, dirname

filename = join(dirname(__file__), 'setup_info.py')
exec(compile(open(filename, "rb").read(), filename, 'exec'))

# above line is equivalent to "execfile(filename)", except that it
# works also in Python 3

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

AFTER17 = False
AFTER18 = False
if VERSION[0] == 1:
    if VERSION[1] > 6:
        AFTER17 = True
        if VERSION[1] > 8:
            AFTER18 = True
else:
    raise Exception("Unsupported Django version %s" % VERSION)


def startup(settings_module=None):
    """Start up Django and Lino.

    Until Django 1.6 this was called automatically (by
    :mod:`lino.modlib.lino_startup`), but this trick no longer worked
    after 1.7.

    This is called automatically when a process is invoked by an
    *admin command*.

    For testable documents you need to call it manually using e.g.:

    >>> import lino
    >>> lino.startup('my.project.settings')

    Note that above two lines are recommended over the old-style
    method (which works only under Django 1.6)::

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'my.project.settings'

    """
    # print("20160711 startup")
    # logger.info("20160711 startup")
    if settings_module:
        import os
        os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

    if AFTER17:
        import django
        django.setup()
    # print("20160711 startup done")
    # logger.info("20160711 startup done")


def site_startup():
    """Called from `lino.models` before Django 1.7"""
    #print "site_startup"
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

