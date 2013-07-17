# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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

#~ raise Exception("""
#~ This was an idea to docuemt code changes. 
#~ Didn't continue this way because I understood that 
#~ code changes must be documented in *one central place 
#~ per developer*, not per module.
#~ """)

import os
import datetime
import inspect

from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from lino.utils import i2d
from lino import dd
from lino.modlib.system.models import SYSTEM_USER_LABEL
from lino.utils.restify import restify, doc2rst

#~ CHANGES_LIST = []

#~ class Entry(object):
    #~ def __init__(self,date,title,body,module=None,tags=None):
    #~ #def __init__(self,module,date,tags,body):
        #~ self.date = i2d(date)
        #~ self.tags = tags
        #~ self.body = restify(doc2rst(body))
        #~ self.module = module

#~ class CodeChange(Entry): pass
#~ class Issue(Entry): pass

#~ def change(*args,**kw): CHANGES_LIST.append(CodeChange(*args,**kw))
#~ def issue(*args,**kw): CHANGES_LIST.append(Issue(*args,**kw))
  
#~ def change(*args,**kw):
    #~ frm = inspect.stack()[1]
    #~ m = inspect.getmodule(frm[0])
    #~ app_label = m.__name__.split('.')[-2]
    #~ CHANGES_LIST.append(CodeChange(app_label,*args,**kw))

#~ def issue(*args,**kw):
    #~ frm = inspect.stack()[1]
    #~ m = inspect.getmodule(frm[0])
    #~ app_label = m.__name__.split('.')[-2]
    #~ CHANGES_LIST.append(Issue(app_label,*args,**kw))

#~ def discover():
    #~ if len(CHANGES_LIST) == 0:
        #~ # similar logic as in django.template.loaders.app_directories
        #~ for app in settings.INSTALLED_APPS:
            #~ mod = import_module(app)
            #~ fn = os.path.join(os.path.dirname(mod.__file__), 'changes.py')
            #~ if os.path.exists(fn):
                #~ import_module(app+'.changes')

class CodeChanges(dd.VirtualTable):
  
    label = _("Code Changes")
    
    detail_layout = """
    date module 
    body
    """
    parameters = dict(
      start_date = models.DateField(_("Only changes from"),blank=True),
      end_date = models.DateField(_("until"),blank=True),
      opt_tag = models.BooleanField(_("Optimizations"),default=True),
      )
    params_layout = """
    start_date end_date opt_tag
    """
    #~ params_panel_hidden = False
    
    column_names = "date module body"
  
    @classmethod
    def get_data_rows(self,ar,qs=None):
        #~ discover()
        import lino.changes
        from lino.utils.gendoc import ENTRIES_LIST
        return ENTRIES_LIST
        
    @dd.virtualfield(models.DateField(_('Date')))
    def date(self,obj,ar):
        return obj.date
        
    @dd.displayfield(_('Body'))
    def body(self,obj,ar):
        return obj.body
        
    @dd.displayfield(_('Module'))
    def module(self,obj,ar):
        return obj.module
        
        
def setup_explorer_menu(site,ui,profile,m):
    m  = m.add_menu("system",SYSTEM_USER_LABEL)
    m.add_action(CodeChanges)
  
