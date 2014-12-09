# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)


from lino.projects.min1.settings import *


class Site(Site):
    #~ languages = 'en'
    languages = 'en de fr et nl pt-br'

SITE = Site(globals(), no_local=True)

SECRET_KEY = "20227"  # see :djangoticket:`20227`
