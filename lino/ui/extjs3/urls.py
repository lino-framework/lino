## Copyright 2009-2013 Luc Saffre
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
The default URLconf module, defines the variable `urlpatterns` 
as required by Django.
Application code doesn't need to worry about this.

This is found by Django because 
:mod:`lino.apps.std.settings`
:setting:`ROOT_URLCONF` 
is set to ``'lino.ui.extjs3.urls'``.

"""

from __future__ import unicode_literals


import logging
logger = logging.getLogger(__name__)

import os

from django.conf import settings
#~ urlpatterns = settings.LINO.ui.get_patterns()

from django import http

from django.conf.urls import patterns, url, include
from django.views.generic import View


import lino
settings.LINO.ui
from lino import dd
from lino.ui.extjs3 import views
from lino.core.modeltools import is_devserver


def get_media_urls():
    #~ print "20121110 get_urls"
    urlpatterns = []
    from os.path import exists, join, abspath, dirname
    
    logger.info("Checking /media URLs ")
    prefix = settings.MEDIA_URL[1:]
    assert prefix.endswith('/')
    
    def setup_media_link(short_name,attr_name=None,source=None):
        target = join(settings.MEDIA_ROOT,short_name)
        if exists(target):
            return
        if attr_name:
            source = getattr(settings.LINO,attr_name)
            if not source:
                raise Exception(
                  "%s does not exist and LINO.%s is not set." % (
                  target,attr_name))
        if not exists(source):
            raise Exception("LINO.%s (%s) does not exist" % (attr_name,source))
        if is_devserver():
            urlpatterns.extend(patterns('django.views.static',
            (r'^%s%s/(?P<path>.*)$' % (prefix,short_name), 
                'serve', {
                'document_root': source,
                'show_indexes': False })))
        else:
            logger.info("Setting up symlink %s -> %s.",target,source)
            symlink = getattr(os,'symlink',None)
            if symlink is not None:
                symlink(source,target)
        
    if not settings.LINO.extjs_base_url:
        setup_media_link('extjs','extjs_root')
    if settings.LINO.use_bootstrap:
        setup_media_link('bootstrap','bootstrap_root')
    if settings.LINO.use_jasmine:
        setup_media_link('jasmine','jasmine_root')
    if settings.LINO.use_extensible:
        setup_media_link('extensible','extensible_root')
    if settings.LINO.use_tinymce:
        setup_media_link('tinymce','tinymce_root')
    if settings.LINO.use_eid_jslib:
        setup_media_link('eid-jslib','eid_jslib_root')
        
    setup_media_link('lino',source=join(dirname(lino.__file__),'..','media'))

    if is_devserver():
        urlpatterns += patterns('django.views.static',
            (r'^%s(?P<path>.*)$' % prefix, 'serve', 
              { 'document_root': settings.MEDIA_ROOT, 
                'show_indexes': True }),
        )

    return urlpatterns
        
def get_pages_urls():
    pages = dd.resolve_app('pages')
    class PagesIndex(View):
      
        def get(self, request,ref='index'):
            if not ref: 
                ref = 'index'
          
            #~ print 20121220, ref
            obj = pages.lookup(ref,None)
            if obj is None:
                raise http.Http404("Unknown page %r" % ref)
            html = pages.render_node(request,obj)
            return http.HttpResponse(html)

    return patterns('',
        (r'^(?P<ref>\w*)$', PagesIndex.as_view()),
    )
    
def get_plain_urls():

    urlpatterns = []
    rx = '^' # + settings.LINO.plain_prefix
    urlpatterns = patterns('',
        (rx+r'$', views.PlainIndex.as_view()),
        (rx+r'(?P<app_label>\w+)/(?P<actor>\w+)$', views.PlainList.as_view()),
        (rx+r'(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$', views.PlainElement.as_view()),
    )
    return urlpatterns
  
        

def get_ext_urls():
    #~ print "20121110 get_urls"
    rx = '^'
    urlpatterns = patterns('',
        (rx+'$', views.AdminIndex.as_view()),
        (rx+r'api/main_html$', views.MainHtml.as_view()),
        (rx+r'auth$', views.Authenticate.as_view()),
        (rx+r'grid_config/(?P<app_label>\w+)/(?P<actor>\w+)$', views.GridConfig.as_view()),
        (rx+r'api/(?P<app_label>\w+)/(?P<actor>\w+)$', views.ApiList.as_view()),
        (rx+r'api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$', views.ApiElement.as_view()),
        (rx+r'restful/(?P<app_label>\w+)/(?P<actor>\w+)$', views.Restful.as_view()),
        (rx+r'restful/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$', views.Restful.as_view()),
        (rx+r'choices/(?P<app_label>\w+)/(?P<rptname>\w+)$', views.Choices.as_view()),
        (rx+r'choices/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<fldname>\w+)$', views.Choices.as_view()),
        (rx+r'apchoices/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<an>\w+)/(?P<field>\w+)$', views.ActionParamChoices.as_view()),
        (rx+r'callbacks/(?P<thread_id>\w+)/(?P<button_id>\w+)$', views.Callbacks.as_view()),
        #~ (rx+r'plain/(?P<app_label>\w+)/(?P<actor>\w+)$', views.PlainList.as_view()),
        #~ (rx+r'plain/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$', views.PlainElement.as_view()),
    )
    if settings.LINO.use_eid_applet:
        urlpatterns += patterns('',
            (rx+r'eid-applet-service$', views.EidAppletService.as_view()),
        )
    if settings.LINO.use_jasmine:
        urlpatterns += patterns('',
            (rx+r'run-jasmine$', views.RunJasmine.as_view()),
        )
    if settings.LINO.use_tinymce:
        urlpatterns += patterns('',
            (rx+r'templates/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>\w+)/(?P<fldname>\w+)$', 
                views.Templates.as_view()),
            (rx+r'templates/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>\w+)/(?P<fldname>\w+)/(?P<tplname>\w+)$', 
                views.Templates.as_view()),
        )

    return urlpatterns

       
urlpatterns = get_media_urls()

if settings.LINO.plain_prefix:
    urlpatterns += patterns('',
      ('^'+settings.LINO.plain_prefix[1:]+"/", include(get_plain_urls()))
    )
else:
    urlpatterns += get_plain_urls()
    
if settings.LINO.django_admin_prefix:
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns += patterns('',
      ('^'+settings.LINO.django_admin_prefix[1:]+"/", include(admin.site.urls))
    )
   
if settings.LINO.use_extjs:
    if settings.LINO.admin_prefix:
        urlpatterns += patterns('',
          ('^'+settings.LINO.admin_prefix[1:]+"/", include(get_ext_urls()))
        )
        urlpatterns += get_pages_urls()
    else:
        urlpatterns += get_ext_urls()
elif settings.LINO.plain_prefix:
    urlpatterns += get_pages_urls()



