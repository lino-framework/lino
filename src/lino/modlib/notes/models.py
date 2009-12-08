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


from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from lino.modlib import fields, tools
from lino import reports
from lino import layouts

tools.requires_apps('auth','contenttypes','links')

class NoteType(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name


class Note(models.Model):
    user = models.ForeignKey("auth.User")
    date = fields.MyDateField()
    owner_type = models.ForeignKey(ContentType)
    owner_id = models.PositiveIntegerField()
    owner = generic.GenericForeignKey('owner_type', 'owner_id')
    partner = models.ForeignKey("contacts.Partner",blank=True,null=True)
    type = models.ForeignKey(NoteType,blank=True,null=True)
    short = models.CharField(max_length=200,blank=True,null=True)
    text = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.short
        
    def on_create(self,req):
        self.user = req.get_user()
        

class NoteDetail(layouts.PageLayout):
    main = """
    date type user owner 
    short partner
    text:40x5 links_LinksByOwner:40x5
    """
class Notes(reports.Report):
    page_layouts = (NoteDetail,)
    model = 'notes.Note'
    columnNames = "id date user owner short text partner"
    order_by = "id"

class MyNotes(Notes):
    fk_name = 'user'
    columnNames = "date short partner owner"
    
    #~ def get_queryset(self,req,master_instance=None,**kw):
        #~ if master_instance is None:
            #~ master_instance = req.get_user()
        #~ return super(MyNotes,self).get_queryset(req,master_instance=master_instance,**kw)

    def setup_request(self,req):
        if req.master_instance is None:
            req.master_instance = req.get_user()


class NotesByOwner(Notes):
    fk_name = 'owner'
    columnNames = "date short user partner"
    order_by = "date"
  
