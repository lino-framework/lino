# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
This is used by tests/__init__.py
"""

from .settings import *

SITE = Site(globals())
"""
This Site instance will normally be replaced by an instance 
in a local settings.py file
"""
