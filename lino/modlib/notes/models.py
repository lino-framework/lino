# -*- coding: UTF-8 -*-
## Copyright 2009-2012 Luc Saffre
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
The :xfile:`models.py` file for :mod:`lino.modlib.notes`.
"""

import logging
logger = logging.getLogger(__name__)

import os
import sys
import cgi
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy 

#~ from django.contrib.contenttypes.models import ContentType
#~ from django.contrib.contenttypes import generic
from django.db import IntegrityError
from django.utils.encoding import force_unicode


#~ from lino import tools
from lino import dd
#~ from lino import reports
#~ from lino import layouts
#~ from lino.utils import perms
from lino.utils.restify import restify
#~ from lino.utils import printable
from lino import mixins
from django.conf import settings
#~ from lino import choices_method, simple_choices_method
#~ from lino.modlib.contacts import models as contacts
#~ from lino.modlib.outbox import models as outbox
#~ from lino.modlib.postings import models as postings


outbox = dd.resolve_app('outbox')
postings = dd.resolve_app('postings')
contacts = dd.resolve_app('contacts')

#~ TEMPLATE_GROUP = 'notes'

class NoteType(dd.BabelNamed,mixins.PrintableType,outbox.MailableType):
  
    templates_group = 'notes/Note'
    
    class Meta:
        verbose_name = _("Note Type")
        verbose_name_plural = _("Note Types")
        
    #~ name = models.CharField(max_length=200)
    important = models.BooleanField(
        verbose_name=_("important"),
        default=False)
    remark = models.TextField(verbose_name=_("Remark"),blank=True)
    
    body_template = models.CharField(max_length=200,
      verbose_name=_("Body template"),
      blank=True,help_text="""The body template to be used when 
rendering a printable of this type. This is a list of files 
with extension `.body.html`.""")
    
    @dd.chooser(simple_values=True)
    def body_template_choices(cls):
        return settings.SITE.list_templates('.body.html',cls.get_templates_group())


class NoteTypes(dd.Table):
    """
    Displays all rows of :class:`NoteType`.
    """
    model = 'notes.NoteType'
    required = dd.required(user_level='admin',user_groups='office')
    #~ label = _("Note types")
    column_names = 'name build_method template *'
    order_by = ["name"]
    
    detail_layout = """
    id name
    build_method template body_template email_template attach_to_email
    remark:60x5
    notes.NotesByType
    """

class EventType(dd.BabelNamed):
    """
    A possible choice for :attr:`Note.event_type`.
    """
    class Meta:
        verbose_name = pgettext_lazy(u"notes",u"Event Type")
        #~ verbose_name = _("Event Type")
        verbose_name_plural = _("Event Types")
    #~ name = dd.BabelCharField(max_length=200,verbose_name=_("Designation"))
    remark = models.TextField(verbose_name=_("Remark"),blank=True)
    body = dd.BabelTextField(_("Body"),blank=True,format='html')
    



class EventTypes(dd.Table):
    """
    List of all Event Types.
    """
    model = 'notes.EventType'
    required = dd.required(user_level='admin',user_groups='office')
    column_names = 'name *'
    order_by = ["name"]
    
    detail_layout = """
    id name
    remark:60x3
    notes.NotesByEventType:60x6
    """
    

class Note(mixins.TypedPrintable,
      mixins.UserAuthored,
      mixins.Controllable,
      contacts.ContactRelated,
      mixins.ProjectRelated,
      outbox.Mailable,
      postings.Postable, #~ mixins.DiffingMixin
      ):
      
    """
    Deserves more documentation.
    """
    
    manager_level_field = 'office_level'
    
    
    class Meta:
        abstract = settings.SITE.is_abstract_model('notes.Note')
        #~ abstract = True
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")
        #~ verbose_name = _("Note")
        #~ verbose_name_plural = _("Notes")
        
    #~ date = fields.MyDateField()
    date = models.DateField(verbose_name=_('Date'),default=datetime.date.today)
    #~ owner_type = models.ForeignKey(ContentType,blank=True,null=True)
    #~ owner_id = models.PositiveIntegerField(blank=True,null=True)
    #~ owner = generic.GenericForeignKey('owner_type', 'owner_id')
    type = models.ForeignKey(NoteType,
        blank=True,null=True,
        verbose_name=_('Note Type (Content)'))
    event_type = models.ForeignKey(EventType,
        blank=True,null=True,
        verbose_name=_('Event Type (Form)'))
    #,on_delete=RESTRICT)
    subject = models.CharField(_("Subject"),max_length=200,blank=True) # ,null=True)
    #~ body = models.TextField(_("Body"),blank=True)
    body = dd.RichTextField(_("Body"),blank=True,format='html')
    
    #~ owner_type = models.ForeignKey(ContentType,verbose_name=_('Owner type'))
    #~ owner_id = models.PositiveIntegerField(verbose_name=_('Owner'))
    #~ owner = generic.GenericForeignKey('owner_type', 'owner_id')
    
    #~ project = models.ForeignKey("projects.Project",blank=True,null=True)
    #~ person = models.ForeignKey("contacts.Person",blank=True,null=True)
    #~ company = models.ForeignKey("contacts.Company",blank=True,null=True)
    #~ url = models.URLField(verify_exists=True,blank=True,null=True)
    language = dd.LanguageField()
    
    # partner = models.ForeignKey("contacts.Partner",blank=True,null=True)
    
    def __unicode__(self):
        return u'%s #%s' % (self._meta.verbose_name,self.pk)
        
    #~ def get_mailable_body(self,ar):
        #~ return self.body
        
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
    
    #~ def disabled_fields(self,ar):
        #~ if not self.build_time:
            #~ return []
        #~ return settings.SITE.NOTE_PRINTABLE_FIELDS

    #~ @classmethod
    #~ def site_setup(cls,lino):
        #~ lino.NOTE_PRINTABLE_FIELDS = dd.fields_list(cls,
        #~ '''date subject body language person company type event_type''')
        
    #~ @classmethod
    #~ def site_setup(cls,lino):
        #~ lino.NOTE_PRINTABLE_FIELDS = dd.fields_list(cls,
        #~ '''date subject body language type event_type''')
        

    def summary_row(self,ar,**kw):
        #~ s = super(Note,self).summary_row(ui,rr)
        s = super(Note,self).summary_row(ar)
        #~ s = contacts.ContactDocument.summary_row(self,ui,rr)
        if self.subject:
            s += [' ',self.subject]
        return s
    
    #~ def update_owned_instance(self,task):
        #~ mixins.AutoUser.update_owned_instance(self,task)
        #~ contacts.PartnerDocument.update_owned_instance(self,task)
        #~ super(ContractBase,self).update_owned_instance(other)
        
    def get_mailable_type(self):
        return self.type
        
    #~ def get_person(self):
        #~ return self.project
    #~ person = property(get_person)
    
    def get_print_language(self):
        return self.language
        
    
    def get_printable_context(self,ar,**kw):
        kw = super(Note,self).get_printable_context(ar,**kw)
        tplname = self.type.body_template
        if tplname:
            tplname = self.type.get_templates_group() + '/' + tplname
            template = settings.SITE.jinja_env.get_template(tplname)
            kw.update(body=template.render(**kw))
        else:
            kw.update(body=self.body)
        return kw
        
    
        

dd.update_field(Note,'company',verbose_name=_("Recipient (Organization)"))
dd.update_field(Note,'contact_person',verbose_name=_("Recipient (Person)"))
    
def html_text(s):
    return '<div class="htmlText">' + s + '</div>'
    

class NoteDetail(dd.FormLayout):
    main = """
    date:10 event_type:25 type:25
    subject project 
    id user:10 language:8 build_time
    body outbox.MailsByController
    """
    



    
class Notes(dd.Table):
    required = dd.required(user_groups='office',user_level='admin')
    
    model = 'notes.Note'
    detail_layout = NoteDetail()
    #~ column_names = "id date user type event_type subject * body_html"
    column_names = "id date user event_type type project subject * body"
    #~ hide_columns = "body"
    #~ hidden_columns = frozenset(['body'])
    order_by = ["id"]
    #~ label = _("Notes")


class MyNotes(mixins.ByUser,Notes):
    required = dd.required(user_groups='office')
    #~ master_key = 'user'
    column_names = "date event_type type subject project body *"
    #~ column_names = "date event_type type subject body *"
    #~ column_names = "date type event_type subject body_html *"
    #~ can_view = perms.is_authenticated
    #~ label = _("My notes")
    order_by = ["date"]
    

  
class NotesByType(Notes):
    master_key = 'type'
    column_names = "date event_type subject user *"
    order_by = ["date"]
  
  
class NotesByEventType(Notes):
    master_key = 'event_type'
    column_names = "date type subject user *"
    order_by = ["date"]
    
    

class NotesByProject(Notes):
    required = dd.required(user_groups='office')
    master_key = 'project'
    column_names = "date event_type type subject body user *"
    order_by = ["-date"]
    
class NotesByOwner(NotesByProject):
    master_key = 'owner'
    column_names = "date event_type type subject body user *"
    
    
def add_system_note(ar,owner,subject,body,**kw):
    #~ if not settings.SITE.site_config.system_note_type:
        #~ return
    nt = owner.get_system_note_type(ar)
    if not nt: 
        return
    prj = owner.get_related_project(ar)
    if prj:
        kw.update(project=prj)
    #~ note = Note(type=nt,owner=owner,
    note = Note(event_type=nt,owner=owner,
        subject=subject,body=body,user=ar.get_user(),**kw)
    #~ owner.update_system_note(note)
    note.save()
    
    
    
system = dd.resolve_app('system')
    
def customize_siteconfig():
    """
    Injects application-specific fields to :class:`SiteConfig <lino.modlib.system.SiteConfig>`.
    """
    dd.inject_field('system.SiteConfig',
        'system_note_type',
        #~ models.ForeignKey(NoteType,
        models.ForeignKey(EventType,
            blank=True,null=True,
            verbose_name=_("Default system note type"),
            help_text=_("""\
Note Type used by system notes.
If this is empty, then system notes won't create any entry to the Notes table.""")))
  

def setup_main_menu(site,ui,profile,m):
    m  = m.add_menu("office",system.OFFICE_MODULE_LABEL)
    m.add_action('notes.MyNotes')
  
def setup_config_menu(site,ui,profile,m): 
    #~ m  = m.add_menu("notes",_("~Notes"))
    m  = m.add_menu("office",system.OFFICE_MODULE_LABEL)
    m.add_action('notes.NoteTypes')
    m.add_action('notes.EventTypes')
  
def setup_explorer_menu(site,ui,profile,m):
    m  = m.add_menu("office",system.OFFICE_MODULE_LABEL)
    m.add_action('notes.Notes')
  
customize_siteconfig()  
