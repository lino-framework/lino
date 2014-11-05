# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from lino_cosi.projects.std.settings.demo import *

class Site(Site):
    title = "My Lino Così site"
    languages = 'en es'

SITE = Site(globals())
