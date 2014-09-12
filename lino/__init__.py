# -*- coding: UTF-8 -*-
# Copyright 2002-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

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
