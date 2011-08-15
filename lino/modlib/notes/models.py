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
import cgi
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
#~ from django.contrib.contenttypes.models import ContentType
#~ from django.contrib.contenttypes import generic
from django.db import IntegrityError
from django.utils.encoding import force_unicode


from lino import fields, tools
#~ from lino.utils.babel import default_language
from lino import reports
#~ from lino import layouts
from lino.utils import perms
from lino.utils.restify import restify
#~ from lino.utils import printable
from lino.utils import babel
from lino import mixins
from django.conf import settings
#~ from lino import choices_method, simple_choices_method

#~ TEMPLATE_GROUP = 'notes'

class NoteType(mixins.PrintableType):
  
    templates_group = 'notes/Note'
    
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
    remark = models.TextField(verbose_name=_("Remark"),blank=True)
    
    def __unicode__(self):
        return babel.babelattr(self,'name')

class EventTypes(reports.Report):
    model = 'notes.EventType'
    column_names = 'name *'
    order_by = ["name"]

class Note(mixins.TypedPrintable,mixins.AutoUser):
#~ class Note(mixins.TypedPrintable,mixins.Reminder):
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
        verbose_name=_('Note Type (Form)'))
    event_type = models.ForeignKey(EventType,
        blank=True,null=True,
        verbose_name=_('Event Type (Content)'))
    #,on_delete=RESTRICT)
    subject = models.CharField(_("Subject"),max_length=200,blank=True,null=True)
    #~ body = models.TextField(_("Body"),blank=True)
    body = fields.RichTextField(_("Body"),blank=True,format='html')
    
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
        return u'%s #%s' % (self._meta.verbose_name,self.pk)
        
    def unused__unicode__(self):
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
        
    #~ def body_html(self,rr):
        #~ """
        #~ Return self.body restified and wrapped into a DIV of class "htmlText".
        
        #~ This logic should be generalized and automatically be done in a new 
        #~ MemoField type. A MemoField would be a field that is seen by Django 
        #~ like a normal multiline text field, but interpreted as reStructuredText 
        #~ markup "when necessary". 
        #~ The markup language (or optionally plain HTML to be edited using a HtmlTextArea)
        #~ should later get configurable and stored in each value.        
        
        #~ Deserves more documentation.
        #~ """
        #~ if self.body:
            #~ if rr.expand_memos:
                #~ return html_text(restify(self.body))
            #~ else:
                #~ # print 20110512, "yes", __file__
                #~ a = self.body.split('\n',1)
                #~ ellipsis = False
                #~ if len(a) > 1:
                    #~ ellipsis = True
                #~ ln = self.body.split('\n',1)[0]
                #~ if len(ln) > 30:
                    #~ ln = ln[:30]
                    #~ ellipsis = True
                #~ if ellipsis:     
                    #~ ln += "..."
                #~ return ln
        #~ return ''
    #~ body_html.return_type = fields.DisplayField(_("Body"))
    
    def disabled_fields(self,request):
        if self.must_build:
            return []
        return settings.LINO.NOTE_PRINTABLE_FIELDS

    @classmethod
    def site_setup(cls,lino):
        lino.NOTE_PRINTABLE_FIELDS = reports.fields_list(cls,
        '''date subject body language type event_type''')
        
    def summary_row(self,ui,rr,**kw):
        s = super(Note,self).summary_row(ui,rr)
        #~ s = contacts.ContactDocument.summary_row(self,ui,rr)
        if self.subject:
            s += ' ' + cgi.escape(self.subject) 
        return s
    
def html_text(s):
    return '<div class="htmlText">' + s + '</div>'
    
class NoteTypes(reports.Report):
    model = 'notes.NoteType'
    #~ label = _("Note types")
    column_names = 'name build_method template *'
    
class Notes(reports.Report):
    model = 'notes.Note'
    #~ column_names = "id date user type event_type subject * body_html"
    column_names = "id date user type event_type subject * body"
    #~ hide_columns = "body"
    #~ hidden_columns = frozenset(['body'])
    order_by = ["id"]
    #~ label = _("Notes")


class MyNotes(mixins.ByUser,Notes):
    #~ fk_name = 'user'
    column_names = "date type event_type subject body *"
    #~ column_names = "date type event_type subject body_html *"
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
    column_names = "date event_type subject user *"
    order_by = ["date"]
    #~ label = _("Notes by person")
  
  
class NotesByEventType(Notes):
    fk_name = 'event_type'
    column_names = "date type subject user *"
    order_by = ["date"]
    #~ label = _("Notes by person")
  
  
def setup_main_menu(site,ui,user,m): pass
  
def setup_my_menu(site,ui,user,m): 
    m.add_action('cal.MyEvents')
    m.add_action('cal.MyTasks')
  
def setup_config_menu(site,ui,user,m): 
    m  = m.add_menu("notes",_("~Notes"))
    m.add_action('notes.NoteTypes')
    m.add_action('notes.EventTypes')
  
def setup_explorer_menu(site,ui,user,m):
    m.add_action('notes.Notes')
  