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

import os
import sys

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _

from lino.modlib import fields, tools
from lino import reports
#~ from lino import layouts
from lino.utils import perms
from lino.utils import mixins
from django.conf import settings
#~ from lino import choices_method, simple_choices_method


#~ tools.requires_apps('auth','contenttypes','links')

class NoteType(models.Model):
    name = models.CharField(max_length=200)
    print_method = models.CharField(max_length=20,choices=mixins.print_method_choices(),blank=True,null=True)
    template = models.CharField(max_length=200,blank=True,null=True)
    #~ print_method = models.CharField(max_length=20,choices=mixins.print_method_choices())
    #~ template = models.CharField(max_length=200)
    important = models.BooleanField(verbose_name=_("important"),default=False)
    
    def __unicode__(self):
        return self.name
        
    def template_choices(cls,print_method):
        return mixins.template_choices(print_method)
    template_choices.simple_values = True
    template_choices = classmethod(template_choices)
        
    #~ @simple_choices_method
    #~ def template_choices(cls,print_method):
        #~ return mixins.template_choices(print_method)
        
#~ class NoteTypeDetail(layouts.DetailLayout):
    #~ datalink = 'notes.NoteType'
    #~ main = """
    #~ id name
    #~ print_method
    #~ template
    #~ """

from lino.modlib.contacts.models import default_language

class Note(models.Model,mixins.Printable):
        
    user = models.ForeignKey("auth.User",blank=True,null=True)
    date = fields.MyDateField()
    #~ owner_type = models.ForeignKey(ContentType,blank=True,null=True)
    #~ owner_id = models.PositiveIntegerField(blank=True,null=True)
    #~ owner = generic.GenericForeignKey('owner_type', 'owner_id')
    type = models.ForeignKey(NoteType,blank=True,null=True)
    subject = models.CharField(max_length=200,blank=True,null=True)
    body = models.TextField(blank=True)
    
    #~ project = models.ForeignKey("projects.Project",blank=True,null=True)
    person = models.ForeignKey("contacts.Person",blank=True,null=True)
    company = models.ForeignKey("contacts.Company",blank=True,null=True)
    #~ language = models.ForeignKey('countries.Language',default=default_language)
    language = fields.LanguageField(default=default_language)

    url = models.URLField(verify_exists=True,blank=True,null=True)
    
    # partner = models.ForeignKey("contacts.Partner",blank=True,null=True)
    
    def __unicode__(self):
        if self.user:
            s = u"(%s %s)" % (self.user,self.date)
        else:
            s = u"(Anon %s)" % (self.date)
        if self.subject:
            return self.subject + " " + s
        return s
        
    def on_create(self,req):
        u = req.get_user()
        if u is not None:
            self.user = u
        
    #~ def get_print_method(self):
        #~ if self.type is None:
            #~ print 'get_print_method',self,'type is None'
            #~ return None
        #~ if not self.type.print_method:
            #~ print 'get_print_method',self,' : type ', self.type, 'has no print_method'
            #~ return None
        #~ return mixins.get_print_method(self.type.print_method)
        
    def get_print_method(self):
        if self.type is None:
            return None
        return self.type.print_method
        
    def get_print_templates(self,pm):
        if self.type is None:
            return mixins.Printable.get_print_templates(self,pm)
            #[self.filename_root() + pm.template_ext]
        assert self.type.template.endswith(pm.template_ext)
        return [ self.type.template ]
        



    
class NoteTypes(reports.Report):
    model = 'notes.NoteType'
NoteTypes.add_detail(label=_("Detail"),label_align = reports.LABEL_ALIGN_TOP,
desc="""
main = 
    id name
    print_method
    template
""")
    
class Notes(reports.Report):
    model = 'notes.Note'
    column_names = "id date user subject * body"
    order_by = "id"
    button_label = _("Notes")
Notes.add_detail(label=_("Detail"),label_align = reports.LABEL_ALIGN_TOP,
desc="""
box1 =
    date 
    type 
    user language

box2 =
    subject
    person 
    company
    
main =
    box1 box2
    url
    body:80x5 

""")


class MyNotes(Notes):
    fk_name = 'user'
    column_names = "date subject *"
    hide_columns = "body"
    can_view = perms.is_authenticated
    button_label = _("My Notes")
    
    def setup_request(self,req):
        #print 20091211, "MyNotes.setup_request"
        if req.master_instance is None:
            req.master_instance = req.get_user()
            #print req.master_instance

#~ class NotesByProject(Notes):
    #~ fk_name = 'project'
    #~ column_names = "date subject user *"
    #~ order_by = "date"
  
class NotesByPerson(Notes):
    fk_name = 'person'
    column_names = "date subject user *"
    order_by = "date"
  
class NotesByCompany(Notes):
    fk_name = 'company'
    column_names = "date subject user *"
    order_by = "date"
  
  
