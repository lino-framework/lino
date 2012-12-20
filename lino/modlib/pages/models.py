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
        
    
#~ def render(*args,**kw): 
    #~ return dummy.render(*args,**kw)
    
class Parser(dummy.Parser):
  
    def create_page(self,**kw):
        #~ logger.info("20121219 create_page(%r)",kw)
        return Page(**kw)
        
    def lookup_page(self,ref,language=None,strict=False): 
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
        
MEMO_PARSER = Parser()
            
page = MEMO_PARSER.instantiate_page
lookup = MEMO_PARSER.lookup_page
render = MEMO_PARSER.render

    
    
lino = dd.resolve_app('lino')

#~ self-made, inspired by http://de.selfhtml.org/css/layouts/mehrspaltige.htm
SELFHTML_PAGE_TEMPLATE = """\
<html>
<head>
<title>[=title]</title>
<style type="text/css">
body {
  font-family:Arial;
  color:black;
  background-color:#c7dffc;
  padding:0em;
  margin:0em;
}
div#left_sidebar {
  float: left; width: 16em;
  background-color:#c0d0f0;
  padding:6pt;
}
div#main_area {
  margin-left: 16em;
  min-width: 14em; 
  padding:2em;
}
</style>
</head>
<body>
<div id="left_sidebar">%s</div>
<div id="main_area">
<h1>[=title]</h1>
[=parse(obj.body)]
<div id="footer">
[include footer]
</div>
</div>
</body>
</html>
"""

# https://github.com/joshuaclayton/blueprint-css/wiki/Quick-start-tutorial

def stylesheet(*args):
    url = settings.LINO.ui.media_url(*args) 
    return '<link rel="stylesheet" type="text/css" href="%s" />' % url

def BLUEPRINT_PAGE_TEMPLATE(site):
    yield "<html><head>"
    yield "<title>[=title]</title>"
    p = site.ui.media_url('blueprint','screen.css')
    yield '<link rel="stylesheet" href="%s" type="text/css" media="screen, projection">' % p
    p = site.ui.media_url('blueprint','print.css')
    yield '<link rel="stylesheet" href="%s" type="text/css" media="print">' % p
    yield '<!--[if lt IE 8]>'
    p = site.ui.media_url('blueprint','ie.css')
    yield '  <link rel="stylesheet" href="%s" type="text/css" media="screen, projection">'
    yield '<![endif]-->'
    p = site.ui.media_url('lino','blueprint.css')
    yield '<link rel="stylesheet" href="%s" type="text/css">' % p
    yield '</head><body><div class="container">'
    
    if settings.LINO.site_config.header_page:
        yield '<div class="span-24 header">'
        yield settings.LINO.site_config.header_page.body
        yield '</div>'
        
    main_width = 24

    if settings.LINO.site_config.sidebar_page:
        main_width -= 4
        yield '<div class="span-4 border">'
        yield settings.LINO.site_config.sidebar_page.body
        yield '</div>'

    yield '<div class="span-%d last">' % main_width
    yield '<h1>[=title]</h1>'
    yield '[=parse(obj.body)]'
    yield '</div>'

    if settings.LINO.site_config.footer_page:
        yield '<div class="span-24 footer">'
        yield settings.LINO.site_config.footer_page.body
        yield '</div>'
    yield '</div></body></html>'
    
def bootstrap_page_template(site):
    yield '<!DOCTYPE html>'
    yield '<html language="en"><head>'
    yield '<meta charset="utf-8"/>'
    yield "<title>[=title]</title>"
    p = site.ui.media_url('bootstrap','css','bootstrap.css')
    yield '<link rel="stylesheet" href="%s" type="text/css">' % p
    p = site.ui.media_url('lino','bootstrap.css')
    yield '<link rel="stylesheet" href="%s" type="text/css">' % p
    yield '</head><body><div class="container-fluid">'
    if site.site_config.header_page:
        yield '  <div class="row-fluid header">'
        yield settings.LINO.site_config.header_page.body
        yield '  </div>'
    yield '  <div class="row-fluid">'
    main_width = 12
    if site.site_config.sidebar_page:
        main_width -= 2
        yield '    <div class="span2">'
        yield site.site_config.sidebar_page.body
        yield '    </div>'
    yield '    <div class="span%d">' % main_width
    #~ yield '<h1>[=title]</h1>'
    yield '[=iif(obj.title,E.h1(obj.title),"")]'
    yield '[=parse(obj.body)]'
    yield '    </div>'
    yield '  </div>'
    if site.site_config.footer_page:
        yield '  <div class="row-fluid footer">'
        yield settings.LINO.site_config.footer_page.body
        yield '  </div>'
    
    yield '</div></body></html>'
    
    


def site_setup(site):
    #~ if settings.LINO.site_config.sidebar_page:
        #~ if settings.LINO.site_config.footer_page:
            #~ MEMO_PARSER.page_template =  BLUEPRINT_PAGE_TEMPLATE % settings.LINO.site_config.sidebar_page.body
    #~ MEMO_PARSER.page_template =  '\n'.join(list(BLUEPRINT_PAGE_TEMPLATE(site)))
    MEMO_PARSER.page_template =  '\n'.join(list(bootstrap_page_template(site)))
    site.modules.lino.SiteConfigs.set_detail_layout("""
    sidebar_page footer_page header_page
    """)
  

    
def customize_siteconfig():
    """
    Injects application-specific fields to :class:`SiteConfig <lino.models.SiteConfig>`.
    """
    dd.inject_field(lino.SiteConfig,
        'sidebar_page',
        models.ForeignKey(Page,
            blank=True,null=True,
            related_name='sidebar_page_set',
            verbose_name=_("Left sidebar page"),
            help_text=_("Page to use for left sidebar.")))
            
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
  
customize_siteconfig()  

from django.conf.urls.defaults import patterns, url, include

class WebIndex(View):
  
    #~ def get(self, request,ref='index'):
    def get(self, request,ref=''):
        print 20121220, ref
        obj = lookup(ref,babel.get_language())
        html = render(obj)
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
