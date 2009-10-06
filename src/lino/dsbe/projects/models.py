## Copyright 2009 Luc Saffre.
## This file is part of the Lino project. 

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import datetime
from django.db import models
from lino.apps import fields


class Project(models.Model):
    name = models.CharField(max_length=200)
    person = models.ForeignKey('contacts.Person',blank=True,null=True)
    company = models.ForeignKey('contacts.Company',blank=True,null=True)
    started = models.DateField(blank=True,null=True) 
    stopped = models.DateField(blank=True,null=True) 
    
    def __unicode__(self):
        return self.name
        
 
    
class Note(models.Model):
    label = "Notizen"
    project = models.ForeignKey(Project,blank=True,null=True)
    person = models.ForeignKey('contacts.Person',blank=True,null=True)
    company = models.ForeignKey('contacts.Company',blank=True,null=True)
    short = models.CharField(max_length=200,blank=True,null=True)
    date = models.DateField(auto_now_add=True) 
    
    def __unicode__(self):
        return u"%s : %s" % (self.date,self.short)

##
## report definitions
##        
        
from lino.utils import reports, layouts
contacts = models.get_app('contacts')

class ProjectsPage(layouts.PageLayout):
    main = """
    name started stopped
    person company
    NotesByProject
    """

class Projects(reports.Report):
    label = "Projekte"
    model = Project
    order_by = "name"
    page_layouts = (ProjectsPage,)
    
class ProjectsByPerson(Projects):
    label = "Projekte pro Person"
    master = contacts.Person
    order_by = "started"
    columnNames = "started name company stopped"

class ProjectsByCompany(Projects):
    label = "Projekte pro Firma"
    master = contacts.Company
    order_by = "started"
    columnNames = "started name person stopped"

class Notes(reports.Report):
    model = Note
    columnNames = "date short person company"
    order_by = "date"

class NotesByPerson(Notes):
    master = contacts.Person
    
class NotesByCompany(Notes):
    master = contacts.Person
    
class NotesByProject(Notes):
    master = Project
