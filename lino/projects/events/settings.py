# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

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
    
    demo_fixtures = 'std few_countries few_cities vor'.split()
    
    languages = 'de fr nl'
    #~ languages = ['de','fr','nl']
    #~ languages = 'de fr et en'.split()
    
            
    def get_installed_apps(self):
        for a in super(Site,self).get_installed_apps():
            yield a
        yield 'lino.modlib.system'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.events'


SITE = Site(globals())
    
#~ except Exception as e:
    #~ import traceback
    #~ traceback.print_exc(e)
    #~ sys.exit(1)
  #~   
