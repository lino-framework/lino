## Copyright 2009-2010 Luc Saffre
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


from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _

from lino.modlib import fields, tools
from lino import reports
from lino import layouts
from lino.utils import perms
from lino.modlib.documents.utils import Printable

tools.requires_apps('auth','contenttypes','links')

class NoteType(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name


class Note(models.Model,Printable):
    #~ class Meta:
        #~ abstract = True
        
    user = models.ForeignKey("auth.User",blank=True,null=True)
    date = fields.MyDateField()
    #~ owner_type = models.ForeignKey(ContentType,blank=True,null=True)
    #~ owner_id = models.PositiveIntegerField(blank=True,null=True)
    #~ owner = generic.GenericForeignKey('owner_type', 'owner_id')
    type = models.ForeignKey(NoteType,blank=True,null=True)
    short = models.CharField(max_length=200,blank=True,null=True)
    text = models.TextField(blank=True)
    
    project = models.ForeignKey("projects.Project",blank=True,null=True)
    person = models.ForeignKey("contacts.Person",blank=True,null=True)
    company = models.ForeignKey("contacts.Company",blank=True,null=True)
    
    # partner = models.ForeignKey("contacts.Partner",blank=True,null=True)
    
    def __unicode__(self):
        if self.user:
            s = u"(%s %s)" % (self.user,self.date)
        else:
            s = u"(Anon %s)" % (self.date)
        if self.short:
            return self.short + " " + s
        return s
        
    def on_create(self,req):
        u = req.get_user()
        if u is not None:
            self.user = u
        

class NoteDetail(layouts.PageLayout):
    #~ main = """
    #~ date short type user
    #~ person company
    #~ text:40x5 links.LinksByOwner:40x5
    #~ """
    
    #~ box1 = """
    #~ date type user
    #~ short 
    #~ person 
    #~ company
    #~ """
    #~ main = """
    #~ box1 links.LinksByOwner:40
    #~ text:80x5 
    #~ """
    
    
    box1 = """
    person 
    company
    """
    main = """
    date short type user 
    box1:40 links.LinksByOwner:40
    text:80x5 
    """
    
class Notes(reports.Report):
    page_layouts = (NoteDetail,)
    model = 'notes.Note'
    columnNames = "id date user short * text"
    order_by = "id"
    button_label = _("Notes")

class MyNotes(Notes):
    fk_name = 'user'
    columnNames = "date short * text user"
    can_view = perms.is_authenticated
    button_label = _("My Notes")
    
    def setup_request(self,req):
        #print 20091211, "MyNotes.setup_request"
        if req.master_instance is None:
            req.master_instance = req.get_user()
            #print req.master_instance

class NotesByProject(Notes):
    fk_name = 'project'
    columnNames = "date short user"
    order_by = "date"
  
class NotesByPerson(Notes):
    fk_name = 'person'
    columnNames = "date short user"
    order_by = "date"
  
class NotesByCompany(Notes):
    fk_name = 'company'
    columnNames = "date short user"
    order_by = "date"
  
  
