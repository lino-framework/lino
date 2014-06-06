# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from lino_cosi.settings import *

class Site(Site):
    title = "My Lino Così site"
    languages = 'en es'

SITE = Site(globals())
