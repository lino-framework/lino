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
from django.utils.translation import get_language

from django import http
from django.views.generic import View

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
#~ from lino.utils.restify import restify
#~ from lino.utils import printable
from lino.utils import babel
from lino.utils import iif
from lino.utils.xmlgen import html as xghtml

from lino import mixins
from django.conf import settings
#~ from lino import choices_method, simple_choices_method
#~ from lino.modlib.contacts import models as contacts
#~ from lino.modlib.outbox import models as outbox


#~ outbox = dd.resolve_app('outbox')
#~ postings = dd.resolve_app('postings')
#~ contacts = dd.resolve_app('contacts')

#~ from lino.modlib.pages import dummy

#~ class PageType(babel.BabelNamed,mixins.PrintableType,outbox.MailableType):
  
    #~ templates_group = 'pages/Page'
    
    #~ class Meta:
        #~ verbose_name = _("Page Type")
        #~ verbose_name_plural = _("Page Types")
        
    #~ remark = models.TextField(verbose_name=_("Remark"),blank=True)
    
    #~ def __unicode__(self):
        #~ return self.name


#~ class PageTypes(dd.Table):
    #~ """
    #~ Displays all rows of :class:`PageType`.
    #~ """
    #~ model = 'pages.PageType'
    #~ column_names = 'name build_method template *'
    #~ order_by = ["name"]
    
    #~ detail_layout = """
    #~ id name
    #~ build_method template email_template attach_to_email
    #~ remark:60x5
    #~ pages.PagesByType
    #~ """


#~ class Page(mixins.TypedPrintable,
      #~ mixins.AutoUser,
      #~ mixins.Controllable,
      #~ mixins.CreatedModified,
      #~ mixins.ProjectRelated,
      #~ outbox.Mailable,
      #~ postings.Postable, 
      #~ ):
      
class Page(dd.Model):
      
    """
    Deserves more documentation.
    """
    
    class Meta:
        #~ abstract = True
        verbose_name = _("Page") 
        verbose_name_plural = _("Pages")
        #~ verbose_name = _("Page")
        #~ verbose_name_plural = _("Pages")
        unique_together = ['ref','language']
        
    #~ ref = dd.NullCharField(_("Reference"),max_length=40) # ,unique=True)
    ref = models.CharField(_("Reference"),max_length=100,blank=True)
    #~ language = babel.LanguageField(default=babel.get_language,blank=True)
    language = babel.LanguageField(blank=True)
    
    #~ type = models.ForeignKey(PageType,blank=True,null=True)
    title = models.CharField(_("Title"),max_length=200,blank=True) # ,null=True)
    special = models.BooleanField(_("Special"),default=False)
    #~ abstract = dd.RichTextField(_("Abstract"),blank=True,format='html')
    body = dd.RichTextField(_("Body"),blank=True,format='html')
    
    
    
    def __unicode__(self):
        return "%s -> %s (%s)" % (self.ref,self.title,self.language)
        #~ return u'%s #%s' % (self._meta.verbose_name,self.pk)
        
        
    def get_mailable_type(self):
        return self.type


#~ class PageDetail(dd.FormLayout):
    #~ main = """
    #~ ref title type:25 
    #~ project id user:10 language:8 build_time
    #~ left right
    #~ """
    #~ left = """
    #~ # abstract:60x5
    #~ body:60x20
    #~ """
    #~ right="""
    #~ outbox.MailsByController
    #~ postings.PostingsByController
    #~ """
    
class PageDetail(dd.FormLayout):
    main = """
    ref language:8 title 
    body
    """


    
class Pages(dd.Table):
    model = 'pages.Page'
    detail_layout = PageDetail()
    column_names = "ref language title *"
    #~ column_names = "ref language title user type project *"
    order_by = ["ref",'language']


#~ class MyPages(mixins.ByUser,Pages):
    #~ required = dict(user_groups='office')
    #~ column_names = "modified title type project *"
    #~ label = _("My pages")
    #~ order_by = ["-modified"]
    

  
#~ class PagesByType(Pages):
    #~ master_key = 'type'
    #~ column_names = "title user *"
    #~ order_by = ["-modified"]

#~ if settings.LINO.project_model:
  
    #~ class PagesByProject(Pages):
        #~ master_key = 'project'
        #~ column_names = "type title user *"
        #~ order_by = ["-modified"]
        

def create_page(**kw):
    #~ logger.info("20121219 create_page(%r)",kw)
    return Page(**kw)

def page(ref,language='en',title=None,body=None,**kw):
    """
    Instantiator shortcut for use in fixtures.
    """
    if title is not None: kw.update(title=title)
    if body is not None: kw.update(body=body)
    if language is None: language = ''
    kw.update(language=language)
    #~ lang = kw.get('language')
    #~ if lang is None:
        #~ kw.update(language=babel.DEFAULT_LANGUAGE)
        #~ babel.set_language(None)
    #~ else:
        #~ babel.set_language(lang)
    #~ page = None
    #~ if language in babel.AVAILABLE_LANGUAGES:
        #~ r = DummyPage.pages_dict.get(ref)
        #~ if r is not None: 
            #~ page = r.get(language) 
        # babel.set_language(language)
    page = lookup(ref,language,True)
    if page is None:
        #~ qs = pages.Page.objects.filter(ref=ref)
        #~ if qs.count() == 0:
        return create_page(ref=ref,**kw)
    #~ if qs.count() == 1:
    #~ obj = qs[0]
    for k,v in kw.items():
        setattr(page,k,v)
    #~ page.title = title
    #~ page.body = body
    #~ logger.info("20121219 updated %s %s",ref,language)
    return page
        



def lookup(ref,language=None,strict=False): 
#~ def lookup_page(self,ref,language):
    #~ logger.info("20121219 lookup_page(%r,%r)",ref,language)
    try:
        return Page.objects.get(ref=ref,language=language)
    except Page.DoesNotExist:
        if not strict and language != babel.DEFAULT_LANGUAGE:
            try:
                return Page.objects.get(ref=ref,language=babel.DEFAULT_LANGUAGE)
            except Page.DoesNotExist:
                pass
    try:
        return Page.objects.get(ref=ref,language='')
    except Page.DoesNotExist:
        logger.debug("Unknown page reference %r. Choices are %s.",
            ref,Page.objects.all().values_list('ref',flat=True))
        return None
        #~ raise Exception("Unknown page ref %r. Choices are %s." % (
            #~ ref,Page.objects.all().values_list('ref',flat=True)))
        #~ return dummy.lookup(ref)

def get_sidebar_html(site,request=None,node=None,**context):
    html = ''
    for n in pages.Page.objects.exclude(special=True):
        if not n.language or (n.language == get_language()):
            text = cgi.escape(n.title or n.ref or "Home")
            if n == node:
                html += '<br/>%s' % text
            else:
                url = '/'+n.ref
                html += '<br/><a href="%s">%s</a> ' % (url,text)
    return html
 

lino = dd.resolve_app('lino')

from lino.modlib.pages.dummy import site_setup, render
    
def unused_customize_siteconfig():
    """
    Injects application-specific fields to :class:`SiteConfig <lino.models.SiteConfig>`.
    """
    #~ dd.inject_field(lino.SiteConfig,
        #~ 'sidebar_page',
        #~ models.ForeignKey(Page,
            #~ blank=True,null=True,
            #~ related_name='sidebar_page_set',
            #~ verbose_name=_("Left sidebar page"),
            #~ help_text=_("Page to use for left sidebar.")))
            
    dd.inject_field(lino.SiteConfig,
        'header_page',
        models.ForeignKey(Page,
            blank=True,null=True,
            related_name='header_page_set',
            verbose_name=_("Header page"),
            help_text=_("Page to use for header.")))
  
    dd.inject_field(lino.SiteConfig,
        'footer_page',
        models.ForeignKey(Page,
            blank=True,null=True,
            related_name='footer_page_set',
            verbose_name=_("Footer page"),
            help_text=_("Page to use for footer.")))
  

#~ def setup_main_menu(site,ui,profile,m):
    #~ m  = m.add_menu("office",lino.OFFICE_MODULE_LABEL)
    #~ m.add_action(MyPages)
  
def setup_my_menu(site,ui,profile,m): 
    pass
  
def setup_config_menu(site,ui,profile,m): 
    #~ m  = m.add_menu("pages",_("~Pages"))
    m  = m.add_menu("office",lino.OFFICE_MODULE_LABEL)
    m.add_action(Pages)
    #~ m.add_action(PageTypes)
  
#~ def setup_explorer_menu(site,ui,profile,m):
    #~ m  = m.add_menu("office",lino.OFFICE_MODULE_LABEL)
    #~ m.add_action(Pages)
  
#~ customize_siteconfig()  

from django.conf.urls.defaults import patterns, url, include

class WebIndex(View):
  
    #~ def get(self, request,ref='index'):
    def get(self, request,ref=''):
        #~ print 20121220, ref
        obj = lookup(ref,babel.get_language())
        html = render(request,obj)
        return http.HttpResponse(html)
        

def get_urls():
    #~ print "20121110 get_urls"
    refs = set()
    urlpatterns = []
    for page in Page.objects.all():
        refs.add(page.ref)
    for ref in refs:
        urlpatterns += patterns('',
           (r'^%s$' % ref, WebIndex.as_view(),dict(ref=ref)))
    return urlpatterns
