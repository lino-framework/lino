# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""

"""


from __future__ import unicode_literals

#~ try:

from lino.projects.std.settings import *

#~ from django.utils.translation import ugettext_lazy as _


class Site(Site):

    title = "Lino Events"
    verbose_name = "Lino Events"
    #~ verbose_name = "Lino Cosi"
    #~ description = _("a Lino application to make Belgian accounting simple.")
    #~ version = "0.1"
    #~ url = "http://www.lino-framework.org/autodoc/lino.projects.cosi"
    #~ author = 'Luc Saffre'
    #~ author_email = 'luc.saffre@gmail.com'

    # demo_fixtures = 'std few_countries few_cities vor'.split()
    demo_fixtures = 'std demo vor'.split()

    languages = 'de fr nl'
    #~ languages = ['de','fr','nl']
    #~ languages = 'de fr et en'.split()

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.system'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.events'


SITE = Site(globals())

#~ except Exception as e:
    #~ import traceback
    #~ traceback.print_exc(e)
    #~ sys.exit(1)
  #~
