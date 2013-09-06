# -*- coding: UTF-8 -*-
## Copyright 2011-2013 Luc Saffre
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
This module turns Lino into a basic calendar client. 
To be combined with :attr:`lino.site.Site.use_extensible`.
Supports remote calendars.
Events and Tasks can get attributed to a :attr:`Project <lino.Site.project_model>`.

"""

#~ class SiteMixin(object):
    #~ """
    #~ Class methods and attibutes added to a Site by this module.
    #~ """
    #~ def get_reminder_generators_by_user(self,user):
        #~ """
        #~ Override this per application to return a list of 
        #~ reminder generators from all models for a give ueser
        #~ A reminder generator is an object that has a `update_reminders` 
        #~ method.
        #~ """
        #~ return []
        
    
    #~ def get_todo_tables(self,ar):
        #~ """
        #~ Return or yield a list of tables that should be empty
        #~ """
        #~ from django.db.models import loading
        #~ for mod in loading.get_apps():
            #~ meth = getattr(mod,'get_todo_tables',None)
            #~ if meth is not None:
                #~ dblogger.debug("Running %s of %s", methname, mod.__name__)
                #~ for i in meth(self,ar):
                    #~ yield i


  
