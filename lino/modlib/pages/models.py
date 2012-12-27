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
      
#~ class Page(dd.Model):
class Page(mixins.Referrable,mixins.Hierarizable):
      
    """
    Deserves more documentation.
    """
    
    class Meta:
        #~ abstract = True
        verbose_name = _("Page") 
        verbose_name_plural = _("Pages")
        #~ verbose_name = _("Page")
        #~ verbose_name_plural = _("Pages")
        #~ unique_together = ['ref','language']
        
    #~ ref = dd.NullCharField(_("Reference"),blank=True,max_length=100) # ,unique=True)
    #~ ref = models.CharField(_("Reference"),max_length=100,blank=True,unique=True)
    #~ language = babel.LanguageField(default=babel.get_language,blank=True)
    #~ language = babel.LanguageField(blank=True)
    
    #~ type = models.ForeignKey(PageType,blank=True,null=True)
    title = babel.BabelCharField(_("Title"),max_length=200,blank=True) # ,null=True)
    special = models.BooleanField(_("Special"),default=False)
    #~ abstract = dd.RichTextField(_("Abstract"),blank=True,format='html')
    body = babel.BabelTextField(_("Body"),blank=True,format='plain')
    
    
    
    #~ def __unicode__(self):
        #~ return "%s -> %s (%s)" % (self.ref,self.title,self.language)
        #~ return "%s -> %s (%s)" % (self.ref,self.title,self.language)
        #~ return u'%s %s' % (self._meta.verbose_name,self.ref)
        
        
    #~ def get_mailable_type(self):
        #~ return self.type
        
    def get_sidebar_menu(self,request):
        #~ qs = self.get_siblings()
        qs = Page.objects.filter(parent__isnull=True)
        #~ qs = self.children.all()
        yield ('/', 'index', unicode(_('Home')))
            #~ yield ('/downloads/', 'downloads', 'Downloads')
        #~ yield ('/about', 'about', 'About')
        #~ if qs is not None:
        for obj in qs:
            if obj.ref and obj.title:
                yield ('/'+obj.ref,obj.ref,babel.babelattr(obj,'title'))
            #~ else:
                #~ yield ('/','index',obj.title)
        


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
    ref parent seqno 
    title 
    body
    """


    
class Pages(dd.Table):
    model = 'pages.Page'
    detail_layout = PageDetail()
    column_names = "ref title *"
    #~ column_names = "ref language title user type project *"
    order_by = ["ref"]


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
    #~ logger.info("20121219 create_page(%r)",kw['ref'])
    return Page(**kw)


def lookup(ref):
    if ref == '': 
        ref = None
    return Page.get_by_ref(ref)
    #~ try:
        #~ return Page.objects.get_by_ref(ref)
    #~ except Page.DoesNotExist:
        #~ pass
    

def get_sidebar_html(site,request=None,node=None,**context):
    html = ''
    for n in Page.objects.exclude(special=True):
        if not n.language or (n.language == get_language()):
            text = cgi.escape(n.title or n.ref or "Home")
            if n == node:
                html += '<br/>%s' % text
            else:
                url = '/'+n.ref
                html += '<br/><a href="%s">%s</a> ' % (url,text)
    return html
 
from lino.modlib.pages.dummy import render_node 

    
#~ def unused_customize_siteconfig():
    #~ """
    #~ Injects application-specific fields to :class:`SiteConfig <lino.models.SiteConfig>`.
    #~ """
    #~ dd.inject_field(lino.SiteConfig,
        #~ 'sidebar_page',
        #~ models.ForeignKey(Page,
            #~ blank=True,null=True,
            #~ related_name='sidebar_page_set',
            #~ verbose_name=_("Left sidebar page"),
            #~ help_text=_("Page to use for left sidebar.")))
            
    #~ dd.inject_field(lino.SiteConfig,
        #~ 'header_page',
        #~ models.ForeignKey(Page,
            #~ blank=True,null=True,
            #~ related_name='header_page_set',
            #~ verbose_name=_("Header page"),
            #~ help_text=_("Page to use for header.")))
  
    #~ dd.inject_field(lino.SiteConfig,
        #~ 'footer_page',
        #~ models.ForeignKey(Page,
            #~ blank=True,null=True,
            #~ related_name='footer_page_set',
            #~ verbose_name=_("Footer page"),
            #~ help_text=_("Page to use for footer.")))
  

#~ def setup_main_menu(site,ui,profile,m):
    #~ m  = m.add_menu("office",lino.OFFICE_MODULE_LABEL)
    #~ m.add_action(MyPages)
  
def setup_my_menu(site,ui,profile,m): 
    pass
  
lino = dd.resolve_app('lino')
def setup_config_menu(site,ui,profile,m): 
    #~ m  = m.add_menu("pages",_("~Pages"))
    m  = m.add_menu("office",lino.OFFICE_MODULE_LABEL)
    m.add_action(Pages)
    #~ m.add_action(PageTypes)
  
#~ def setup_explorer_menu(site,ui,profile,m):
    #~ m  = m.add_menu("office",lino.OFFICE_MODULE_LABEL)
    #~ m.add_action(Pages)
  
#~ customize_siteconfig()  


        
def get_all_pages():
    return Page.objects.all()

#~ def get_urls():
    #~ refs = set()
    #~ urlpatterns = []
    #~ for page in Page.objects.all():
        #~ refs.add(page.ref)
    #~ for ref in refs:
        #~ urlpatterns += patterns('',
           #~ (r'^%s$' % ref, WebIndex.as_view(),dict(ref=ref)))
    #~ return urlpatterns
