## Copyright 2009 Luc Saffre
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


import logging
import datetime
from django.db import models
from lino.modlib import fields
from lino import reports


#~ contacts = models.get_app('contacts')
#~ logging.debug(contacts.__file__)

class Project(models.Model):
    name = models.CharField(max_length=200)
    partner = models.ForeignKey("contacts.Partner",blank=True,null=True)
    started = fields.MyDateField(blank=True,null=True) 
    stopped = fields.MyDateField(blank=True,null=True) 
    
    def __unicode__(self):
        return self.name
        
 
    
class Note(models.Model):
    project = models.ForeignKey(Project,blank=True,null=True)
    partner = models.ForeignKey("contacts.Partner",blank=True,null=True)
    short = models.CharField(max_length=200,blank=True,null=True)
    date = fields.MyDateField() 
    
    def __unicode__(self):
        return self.short

##
## report definitions
##        
        
class Projects(reports.Report):
    model = Project
    order_by = "name"
    
class ProjectsByPartner(Projects):
    #master = "contacts.Partner"
    fk_name = 'partner'
    order_by = "started"
    
class Notes(reports.Report):
    model = Note

class NotesByPartner(Notes):
    #master = "contacts.Partner"
    fk_name = 'partner'
    
class NotesByProject(Notes):
    #master = Project
    fk_name = 'project'
