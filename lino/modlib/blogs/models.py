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


#~ from lino import tools
from lino import dd
#~ from lino import reports
#~ from lino import layouts
from lino.utils.restify import restify
#~ from lino.utils import printable
from lino import mixins
from django.conf import settings
#~ from lino import choices_method, simple_choices_method
#~ from lino.modlib.contacts import models as contacts
#~ contacts = dd.resolve_app('contacts')

#~ TEMPLATE_GROUP = 'notes'

class EntryType(dd.BabelNamed,mixins.PrintableType):
  
    templates_group = 'blogs/Entry'
    
    class Meta:
        verbose_name = _("Blog Entry Type")
        verbose_name_plural = _("Blog Entry Types")
        
    #~ name = models.CharField(max_length=200)
    important = models.BooleanField(
        verbose_name=_("important"),
        default=False)
    remark = models.TextField(verbose_name=_("Remark"),blank=True)
    
    def __unicode__(self):
        return self.name




def html_text(s):
    return '<div class="htmlText">' + s + '</div>'
    
class EntryTypes(dd.Table):
    model = EntryType
    column_names = 'name build_method template *'
    order_by = ["name"]
    
    detail_layout = """
    id name
    build_method template
    remark:60x5
    blogs.EntriesByType
    """
    
    
class Entry(mixins.TypedPrintable,
      mixins.CreatedModified,
      mixins.AutoUser,
      mixins.Controllable):
      
    """
    Deserves more documentation.
    """
    class Meta:
        verbose_name = _("Blog Entry") 
        verbose_name_plural = _("Blog Entries")
        
    #~ date = fields.MyDateField()
    #~ date = models.DateField(verbose_name=_('Date'),default=datetime.date.today)
    #~ owner_type = models.ForeignKey(ContentType,blank=True,null=True)
    #~ owner_id = models.PositiveIntegerField(blank=True,null=True)
    #~ owner = generic.GenericForeignKey('owner_type', 'owner_id')
    language = dd.LanguageField()
    type = models.ForeignKey(EntryType,blank=True,null=True)
    title = models.CharField(_("Heading"),max_length=200,blank=True) # ,null=True)
    #~ summary = dd.RichTextField(_("Summary"),blank=True,format='html') 
    body = dd.RichTextField(_("Body"),blank=True,format='html')
    
    def __unicode__(self):
        return u'%s #%s' % (self._meta.verbose_name,self.pk)
        
    

class EntryDetail(dd.FormLayout):
    main = """
    title type:12 user:10 id 
    # summary    
    language:10 created modified owner build_time
    body
    """
    



    
class Entries(dd.Table):
    model = Entry
    detail_layout = EntryDetail()
    column_names = "id modified user type title * body"
    #~ hide_columns = "body"
    #~ hidden_columns = frozenset(['body'])
    order_by = ["id"]
    #~ label = _("Notes")


class MyEntries(mixins.ByUser,Entries):
    #~ master_key = 'user'
    column_names = "modified type title body *"
    #~ column_names = "date event_type type subject body *"
    #~ column_names = "date type event_type subject body_html *"
    #~ can_view = perms.is_authenticated
    order_by = ["-modified"]
    
    #~ def setup_request(self,req):
        #~ if req.master_instance is None:
            #~ req.master_instance = req.get_user()

#~ class NotesByProject(Notes):
    #~ master_key = 'project'
    #~ column_names = "date subject user *"
    #~ order_by = "date"
  
#~ class NotesByController(Notes):
    #~ master_key = 'owner'
    #~ column_names = "date subject user *"
    #~ order_by = "date"
  
class EntriesByType(Entries):
    master_key = 'type'
    column_names = "modified title user *"
    order_by = ["modified-"]
    #~ label = _("Notes by person")
  
  
class EntriesByController(Entries):
    master_key = 'owner'
    column_names = "modified title user *"
    order_by = ["modified-"]
    #~ label = _("Notes by person")
  
  
MODULE_NAME = _("~Blog")  
  
#~ def setup_main_menu(site,ui,user,m): pass
  
def setup_main_menu(site,ui,profile,m): 
    m  = m.add_menu("blogs",MODULE_NAME)
    m.add_action(MyEntries)
  
def setup_config_menu(site,ui,profile,m): 
    m  = m.add_menu("blogs",MODULE_NAME)
    m.add_action(EntryTypes)
  
def setup_explorer_menu(site,ui,profile,m):
    m  = m.add_menu("blogs",MODULE_NAME)
    m.add_action(Entries)
  
