# -*- coding: UTF-8 -*-
## Copyright 2009-2011 Luc Saffre
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
#~ from django.contrib.contenttypes.models import ContentType
#~ from django.contrib.contenttypes import generic
from django.db import IntegrityError

from lino import fields, tools
#~ from lino.utils.babel import default_language
from lino import reports
#~ from lino import layouts
from lino.utils import perms
#~ from lino.utils import printable
from lino.utils import babel
from lino import mixins
from django.conf import settings
#~ from lino import choices_method, simple_choices_method

#~ TEMPLATE_GROUP = 'notes'

class NoteType(mixins.PrintableType):
    class Meta:
        verbose_name = _("Note Type")
        verbose_name_plural = _("Note Types")
    name = models.CharField(max_length=200)
    important = models.BooleanField(
        verbose_name=_("important"),
        default=False)
    remark = models.TextField(verbose_name=_("Remark"),blank=True)
    
    def __unicode__(self):
        return self.name

class EventType(models.Model):
    """
    """
    class Meta:
        verbose_name = _("Event Type")
        verbose_name_plural = _("Event Types")
    name = babel.BabelCharField(max_length=200,verbose_name=_("Designation"))
    
    def __unicode__(self):
        return babel.babelattr(self,'name')

class EventTypes(reports.Report):
    model = 'notes.EventType'
    column_names = 'name *'
    order_by = ["name"]

class Note(mixins.TypedPrintable,mixins.Reminder):
    """
    Deserves more documentation.
    """
    class Meta:
        abstract = True
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")
        
    #~ date = fields.MyDateField()
    date = models.DateField(verbose_name=_('Date'),default=datetime.date.today)
    #~ owner_type = models.ForeignKey(ContentType,blank=True,null=True)
    #~ owner_id = models.PositiveIntegerField(blank=True,null=True)
    #~ owner = generic.GenericForeignKey('owner_type', 'owner_id')
    type = models.ForeignKey(NoteType,
        blank=True,null=True,
        verbose_name=_('Note Type'))
    event_type = models.ForeignKey(EventType,
        blank=True,null=True,
        verbose_name=_('Event Type'))
    #,on_delete=RESTRICT)
    subject = models.CharField(_("Subject"),max_length=200,blank=True,null=True)
    body = models.TextField(_("Body"),blank=True)
    
    #~ owner_type = models.ForeignKey(ContentType,verbose_name=_('Owner type'))
    #~ owner_id = models.PositiveIntegerField(verbose_name=_('Owner'))
    #~ owner = generic.GenericForeignKey('owner_type', 'owner_id')
    
    #~ project = models.ForeignKey("projects.Project",blank=True,null=True)
    #~ person = models.ForeignKey("contacts.Person",blank=True,null=True)
    #~ company = models.ForeignKey("contacts.Company",blank=True,null=True)
    #~ url = models.URLField(verify_exists=True,blank=True,null=True)
    language = fields.LanguageField(default=babel.default_language)
    
    # partner = models.ForeignKey("contacts.Partner",blank=True,null=True)
    
    def __unicode__(self):
        s = u''
        if self.event_type:
            s += unicode(self.event_type) + ' '
        if self.subject:
            s += self.subject + ' '
        if self.type:
            s += unicode(self.type) + ' '
        if self.user:
            s += u"(%s %s)" % (self.user,self.date)
        else:
            s += u"(%s)" % (self.date)
        return s
        

    
class NoteTypes(reports.Report):
    model = 'notes.NoteType'
    #~ label = _("Note types")
    column_names = 'name build_method template *'
    
class Notes(reports.Report):
    model = 'notes.Note'
    column_names = "id date user subject * body"
    order_by = ["id"]
    #~ label = _("Notes")


class MyNotes(mixins.ByUser,Notes):
    #~ fk_name = 'user'
    column_names = "date subject *"
    hide_columns = "body"
    #~ can_view = perms.is_authenticated
    label = _("My notes")
    order_by = ["date"]
    
    #~ def setup_request(self,req):
        #~ if req.master_instance is None:
            #~ req.master_instance = req.get_user()

#~ class NotesByProject(Notes):
    #~ fk_name = 'project'
    #~ column_names = "date subject user *"
    #~ order_by = "date"
  
#~ class NotesByOwner(Notes):
    #~ fk_name = 'owner'
    #~ column_names = "date subject user *"
    #~ order_by = "date"
  
class NotesByType(Notes):
    fk_name = 'type'
    column_names = "date user subject event_type *"
    order_by = ["date"]
    #~ label = _("Notes by person")
  
  
class NotesByEventType(Notes):
    fk_name = 'event_type'
    column_names = "date user subject type *"
    order_by = ["date"]
    #~ label = _("Notes by person")
  
  
