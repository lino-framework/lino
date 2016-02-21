# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from lino.projects.docs.settings.demo import *

class Site(Site):
    title = "My Lino Mini site"
    languages = 'en es'

SITE = Site(globals())
