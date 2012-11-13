# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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
Defines the :class:`Page` model, the base of Lino's out-of-the-box CMS.

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
#~ from lino.utils.babel import default_language
#~ from lino import reports
#~ from lino import layouts
#~ from lino.utils import perms
from lino.utils.restify import restify
#~ from lino.utils import printable
from lino.utils import babel
from lino import mixins
from django.conf import settings
#~ from lino import choices_method, simple_choices_method
#~ from lino.modlib.contacts import models as contacts
#~ from lino.modlib.outbox import models as outbox


outbox = dd.resolve_app('outbox')
postings = dd.resolve_app('postings')
#~ contacts = dd.resolve_app('contacts')

from lino.modlib.pages import dummy

class PageType(babel.BabelNamed,mixins.PrintableType,outbox.MailableType):
  
    templates_group = 'pages/Page'
    
    class Meta:
        verbose_name = _("Page Type")
        verbose_name_plural = _("Page Types")
        
    remark = models.TextField(verbose_name=_("Remark"),blank=True)
    
    def __unicode__(self):
        return self.name


class PageTypes(dd.Table):
    """
    Displays all rows of :class:`PageType`.
    """
    model = 'pages.PageType'
    #~ label = _("Page types")
    column_names = 'name build_method template *'
    order_by = ["name"]
    
    detail_layout = """
    id name
    build_method template email_template attach_to_email
    remark:60x5
    pages.PagesByType
    """


class Page(mixins.TypedPrintable,
      mixins.AutoUser,
      mixins.Controllable,
      mixins.CreatedModified,
      mixins.ProjectRelated,
      outbox.Mailable,
      postings.Postable, 
      ):
      
    """
    Deserves more documentation.
    """
    
    class Meta:
        #~ abstract = True
        verbose_name = _("Page") 
        verbose_name_plural = _("Pages")
        #~ verbose_name = _("Page")
        #~ verbose_name_plural = _("Pages")
        
    ref = dd.NullCharField(_("Reference"),max_length=40,unique=True)
    type = models.ForeignKey(PageType,
        blank=True,null=True,
        verbose_name=_('Page Type (Content)'))
    title = models.CharField(_("Title"),max_length=200,blank=True) # ,null=True)
    abstract = dd.RichTextField(_("Abstract"),blank=True,format='html')
    body = dd.RichTextField(_("Body"),blank=True,format='html')
    
    #~ language = babel.LanguageField(default=babel.get_language,blank=True)
    language = babel.LanguageField(blank=True)
    
    
    def __unicode__(self):
        return u'%s #%s' % (self._meta.verbose_name,self.pk)
        
        
    def get_mailable_type(self):
        return self.type


class PageDetail(dd.FormLayout):
    main = """
    ref title type:25 
    project id user:10 language:8 build_time
    left right
    """
    left = """
    abstract:60x5
    body:60x20
    """
    right="""
    outbox.MailsByController
    postings.PostingsByController
    """
    



    
class Pages(dd.Table):
    model = 'pages.Page'
    detail_layout = PageDetail()
    column_names = "id user type project title * abstract"
    order_by = ["-modified"]


class MyPages(mixins.ByUser,Pages):
    required = dict(user_groups='office')
    #~ master_key = 'user'
    column_names = "title type project abstract *"
    label = _("My pages")
    order_by = ["-modified"]
    

  
class PagesByType(Pages):
    master_key = 'type'
    column_names = "title user abstract *"
    order_by = ["-modified"]


class PagesByProject(Pages):
    master_key = 'project'
    column_names = "type title abstract user *"
    order_by = ["-modified"]
    
    
def lookup(ref):
        
    try:
        return Page.objects.get(ref=ref,language=babel.get_language())
    except Page.DoesNotExist:
        if babel.get_language() != babel.DEFAULT_LANGUAGE:
            try:
                return Page.objects.get(ref=ref,language=babel.DEFAULT_LANGUAGE)
            except Page.DoesNotExist:
                pass
    try:
        return Page.objects.get(ref=ref,language=None)
    except Page.DoesNotExist:
        return dummy.lookup(ref)
        
            
    
    
    
lino = dd.resolve_app('lino')
    
def customize_siteconfig():
    """
    Injects application-specific fields to :class:`SiteConfig <lino.models.SiteConfig>`.
    """
    dd.inject_field(lino.SiteConfig,
        'guest_welcome_page',
        #~ models.ForeignKey(PageType,
        models.ForeignKey(Page,
            blank=True,null=True,
            verbose_name=_("Welcome Page"),
            help_text=_("""\
Page to display to anonymous users.""")))
  

def setup_main_menu(site,ui,user,m):
    m  = m.add_menu("office",lino.OFFICE_MODULE_LABEL)
    m.add_action(MyPages)
  
def setup_my_menu(site,ui,user,m): 
    pass
  
def setup_config_menu(site,ui,user,m): 
    #~ m  = m.add_menu("pages",_("~Pages"))
    m  = m.add_menu("office",lino.OFFICE_MODULE_LABEL)
    m.add_action(PageTypes)
  
def setup_explorer_menu(site,ui,user,m):
    m  = m.add_menu("office",lino.OFFICE_MODULE_LABEL)
    m.add_action(Pages)
  
customize_siteconfig()  