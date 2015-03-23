"""Default settings for a :mod:`lino.projects.min1` site.

This module instantiates a :setting:`SITE` variable and thus is
designed to be used directly as a :setting:`DJANGO_SETTINGS_MODULE`.

"""

from lino.projects.min1.settings import *
from lino.utils import i2d


class Site(Site):
    the_demo_date = i2d(20141023)

SITE = Site(globals())
SECRET_KEY = "20227"  # see :djangoticket:`20227`
