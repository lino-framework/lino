# -*- coding: UTF-8 -*-
# Copyright 2002-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
The :mod:`lino` package is the core of the Lino framework.

This is the base plugin for all Lino applications, added automatically
to your `INSTALLED_APPS`. It defines no models, but some template
files, django admin commands, translation messages and the core
:xfile:`help_texts.py` file.

.. rubric:: submodules

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
   management.commands


"""

# from __future__ import unicode_literals
# from __future__ import absolute_import
# from builtins import str

import sys
import os
from os.path import join, dirname

# Python 3 equivalent of "execfile(filename)":
filename = join(dirname(__file__), 'setup_info.py')
exec(compile(open(filename, "rb").read(), filename, 'exec'))

__version__ = SETUP_INFO['version']
intersphinx_urls = dict(docs="http://www.lino-framework.org")
srcref_url = 'https://github.com/lino-framework/lino/blob/master/%s'


if sys.version_info[0] > 2:
    PYAFTER26 = True
elif sys.version_info[0] == 2 and sys.version_info[1] > 6:
    PYAFTER26 = True
else:
    PYAFTER26 = False

import warnings
warnings.filterwarnings(
    "error", "DateTimeField .* received a naive datetime (.*) while time zone support is active.",
    RuntimeWarning, "django.db.models.fields")

from django.conf import settings
from django.apps import AppConfig


# def setup_project(settings_module):
#     os.environ['DJANGO_SETTINGS_MODULE'] = settings_module
#     from lino.api.shell import settings


DJANGO_DEFAULT_LANGUAGE = 'en-us'


def assert_django_code(django_code):
    if '_' in django_code:
        raise Exception("Invalid language code %r. "
                        "Use values like 'en' or 'en-us'." % django_code)


from django import VERSION

AFTER17 = True
AFTER18 = True
DJANGO2 = True
if VERSION[0] == 1:
    DJANGO2 = False
    if VERSION[1] < 10:
        raise Exception("Unsupported Django version %s" % VERSION)
    # if VERSION[1] > 6:
    #     AFTER17 = True
    #     if VERSION[1] > 8:
    #         AFTER18 = True
elif VERSION[0] == 2:
    AFTER17 = True
    AFTER18 = True
else:
    raise Exception("Unsupported Django version %s" % VERSION)


def startup(settings_module=None):
    """
    Start up Django and Lino.

    Optional `settings_module` is the name of a Django settings
    module.  If this is specified, set the
    :envvar:`DJANGO_SETTINGS_MODULE` environment variable.

    This is called automatically when a process is invoked by an
    *admin command*.

    In a document to be tested using :cmd:`doctest` you need to call
    it manually using e.g.:

    >>> import lino
    >>> lino.startup('my.project.settings')

    Above two lines are recommended over the old-style method (the
    only one only until Django 1.6)::

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'my.project.settings'
    """
    if settings_module:
        os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

    import django
    django.setup()


class AppConfig(AppConfig):
    """This is the only :class:`django.apps.AppConfig` object used by
Lino.

    Lino applications use the :class:`lino.core.plugins.Plugin`
    because it has some additional functionality.

    """
    name = 'lino'

    def ready(self):
        if False:
            settings.SITE.startup()
        else:
            try:
                settings.SITE.startup()
            except ImportError as e:
                import traceback
                # traceback.print_exc(e)
                # sys.exit(-1)
                raise Exception("ImportError during startup:\n" +
                                traceback.format_exc(e))
            except Exception as e:
                print(e)
                raise

default_app_config = 'lino.AppConfig'

# deprecated use, only for backwards compat:
from django.utils.translation import ugettext_lazy as _

intersphinx_urls = dict(docs="http://core.lino-framework.org")
srcref_url = 'https://github.com/lino-framework/lino/blob/master/%s'
doc_trees = ['docs']
