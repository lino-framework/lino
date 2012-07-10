## Copyright 2011-2012 Luc Saffre
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

from os.path import join, abspath, dirname

from lino.apps.std.settings import *

class Lino(Lino):
  
    title = "lino.apps.presto"
    languages = ['en']
    #~ languages = 'de fr et en'.split()
    
    project_model = 'tickets.Project'
    
    #~ remote_user_header = "REMOTE_USER"
    
    def get_app_source_file(self): return __file__
        
    #~ def setup_quicklinks(self,ui,user,tb):
        #~ tb.add_action(self.modules.contacts.Persons.detail_action)
        
    def setup_choicelists(self):
        """
        Defines application-specific default user profiles.
        Local site administrators can override this in their :xfile:.
        """
        from lino import dd
        from django.utils.translation import ugettext_lazy as _
        dd.UserProfiles.reset('* office')
        add = dd.UserProfiles.add_item
        add('100', _("User"),            'U U')
        add('900', _("Administrator"),   'A A')
        
        #~ for p in dd.UserProfiles.items():
            #~ print 20120705, repr(p)
            
        
    
LINO = Lino(__file__,globals()) 

INSTALLED_APPS = (
  #~ 'django.contrib.auth',
  'django.contrib.contenttypes',
  #~ 'django.contrib.sessions',
  #~ 'django.contrib.sites',
  #~ 'django.contrib.markup',
  #~ 'lino.modlib.system',
  'lino',
  'lino.modlib.users',
  'lino.modlib.countries',
  #~ 'lino.modlib.documents',
  'lino.modlib.properties',
  'lino.modlib.contacts',
  #~ 'lino.modlib.projects',
  'lino.modlib.blogs',
  'lino.modlib.tickets',
  #~ 'lino.modlib.links',
  'lino.modlib.uploads',
  #~ 'lino.modlib.thirds',
  'lino.modlib.cal',
  'lino.modlib.outbox',
  'lino.apps.presto',
)


