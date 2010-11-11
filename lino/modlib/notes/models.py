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
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import IntegrityError

from lino import fields, tools
from lino.tools import default_language
from lino import reports
#~ from lino import layouts
from lino.utils import perms
#~ from lino.utils import printable
from lino.utils import mixins
from django.conf import settings
#~ from lino import choices_method, simple_choices_method

#~ TEMPLATE_GROUP = 'notes'

#~ tools.requires_apps('auth','contenttypes','links')

class NoteType(mixins.PrintableType):
    class Meta:
        verbose_name = _("note type")
        verbose_name_plural = _("note types")
    name = models.CharField(max_length=200)
    important = models.BooleanField(verbose_name=_("important"),default=False)
    remark = models.TextField(verbose_name=_("Remark"),blank=True)
    
    def __unicode__(self):
        return self.name
        
    #~ def disable_delete(self,request):
        #~ if self.note_set.count() > 0:
            #~ return _("Must delete all Note objects before deleting NoteType")
        
    #~ @simple_choices_method
    #~ def template_choices(cls,build_method):
        #~ return mixins.template_choices(build_method)
        
#~ class NoteTypeDetail(layouts.DetailLayout):
    #~ datalink = 'notes.NoteType'
    #~ main = """
    #~ id name
    #~ build_method
    #~ template
    #~ """



class Note(mixins.TypedPrintable,mixins.Reminder):
        
    class Meta:
        verbose_name = _("note")
        verbose_name_plural = _("notes")
        
    #~ date = fields.MyDateField()
    date = models.DateField(verbose_name=_('Date'),default=datetime.date.today)
    #~ owner_type = models.ForeignKey(ContentType,blank=True,null=True)
    #~ owner_id = models.PositiveIntegerField(blank=True,null=True)
    #~ owner = generic.GenericForeignKey('owner_type', 'owner_id')
    type = models.ForeignKey(NoteType,blank=True,null=True,verbose_name=_('Note type'))
    #,on_delete=RESTRICT)
    subject = models.CharField(max_length=200,blank=True,null=True)
    body = models.TextField(blank=True)
    
    owner_type = models.ForeignKey(ContentType)
    owner_id = models.PositiveIntegerField(verbose_name=_('Owner'))
    owner = generic.GenericForeignKey('owner_type', 'owner_id')
    
    #~ project = models.ForeignKey("projects.Project",blank=True,null=True)
    #~ person = models.ForeignKey("contacts.Person",blank=True,null=True)
    #~ company = models.ForeignKey("contacts.Company",blank=True,null=True)
    #~ url = models.URLField(verify_exists=True,blank=True,null=True)
    language = fields.LanguageField(default=default_language)
    
    # partner = models.ForeignKey("contacts.Partner",blank=True,null=True)
    
    def __unicode__(self):
        if self.user:
            s = u"(%s %s)" % (self.user,self.date)
        else:
            s = u"(Anon. %s)" % (self.date)
        if self.subject:
            return self.subject + " " + s
        return s
        

    
class NoteTypes(reports.Report):
    model = 'notes.NoteType'
    #~ label = _("Note types")
    column_names = 'name build_method template *'
    
class Notes(reports.Report):
    model = 'notes.Note'
    column_names = "id date user subject * body"
    order_by = "id"
    #~ label = _("Notes")


class MyNotes(Notes):
    fk_name = 'user'
    column_names = "date subject *"
    hide_columns = "body"
    can_view = perms.is_authenticated
    label = _("My notes")
    order_by = "date"
    
    def setup_request(self,req):
        #print 20091211, "MyNotes.setup_request"
        if req.master_instance is None:
            req.master_instance = req.get_user()
            #print req.master_instance

#~ class NotesByProject(Notes):
    #~ fk_name = 'project'
    #~ column_names = "date subject user *"
    #~ order_by = "date"
  
class NotesByOwner(Notes):
    fk_name = 'owner'
    column_names = "date subject user *"
    order_by = "date"
    #~ label = _("Notes by person")
  
#~ class NotesByCompany(Notes):
    #~ fk_name = 'company'
    #~ column_names = "date subject user *"
    #~ order_by = "date"
    #~ label = _("Notes by person")
  
class NotesByType(Notes):
    fk_name = 'type'
    column_names = "date user subject *"
    order_by = "date"
    #~ label = _("Notes by person")
  
  
