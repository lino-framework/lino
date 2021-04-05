# Copyright 2013-2016 Luc Saffre
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
This is used by tests/__init__.py
"""

from .settings import *


class Site(Site):
    languages = 'en de fr et nl pt-br es'
    project_name = 'lino_std'

SITE = Site(globals())
"""
This Site instance will normally be replaced by an instance
in a local settings.py file
"""
