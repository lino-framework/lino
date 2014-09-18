# -*- coding: UTF-8 -*-
# Copyright 2002-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The ``lino`` module can be imported even from a Django :xfile:`settings.py` 
file since it does not import any django module.

"""

from __future__ import unicode_literals

import os

from os.path import join, abspath, dirname, normpath, isdir

execfile(join(dirname(__file__), 'setup_info.py'))
__version__ = SETUP_INFO['version']
intersphinx_url = "http://docs.lino-framework.org"
srcref_url = 'https://github.com/lsaffre/lino/blob/master/%s'


def setup_project(settings_module):
    os.environ['DJANGO_SETTINGS_MODULE'] = settings_module
    from lino.runtime import settings


from django.utils.translation import ugettext_lazy as _
