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

import logging
logger = logging.getLogger(__name__)

import os
import sys
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import databrowse
#~ from django.contrib.auth.decorators import login_required
#~ from django.contrib.auth import urls as auth_urls
from django.utils import importlib
import lino
from . import ext_ui 

urlpatterns = patterns('',
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', 
        {'url': settings.MEDIA_URL + 'lino/favicon.ico'})
)

    

settings.LINO.setup()

ui = ext_ui.ExtUI(settings.LINO)

urlpatterns += patterns('',
    (r'', include(ui.get_urls())),
)

if sys.platform == 'win32':

    EXTJS_ROOT = r's:\ext-4.0.0'
    #~ EXTJS_ROOT = r's:\ext-3.3.1'
    #~ EXTJS_ROOT = r's:\ext-3.3.0'
    #~ EXTJS_ROOT = r's:\ext-3.2.1'
    #~ EXTJS_ROOT = r's:\ext-3.3.0-rc'
    #~ EXTJS_URL = "/media/extjs/"

    LINO_MEDIA = os.path.abspath(os.path.join(
        os.path.dirname(lino.__file__),'..','media'))
    #~ LINO_MEDIA = os.path.join(lino_site.lino_site.ui.source_dir(),'media')
    #~ print 'LINO_MEDIA=',LINO_MEDIA
    
    if not os.path.exists(EXTJS_ROOT):
        raise Exception("EXTJS_ROOT %s does not exist" % EXTJS_ROOT)
        #~ logger.warning("EXTJS_ROOT %s does not exist",EXTJS_ROOT)
        
    prefix = settings.MEDIA_URL[1:]
    assert prefix.endswith('/')
    
    urlpatterns += patterns('django.views.static',
    (r'^%sextjs/(?P<path>.*)$' % prefix, 
        'serve', {
        'document_root': EXTJS_ROOT,
        'show_indexes': True }),)
        
    urlpatterns += patterns('django.views.static',
    (r'^%slino/(?P<path>.*)$' % prefix, 
        'serve', {
        'document_root': LINO_MEDIA,
        'show_indexes': True }),)

    #~ print LINO_MEDIA
  
    urlpatterns += patterns('django.views.static',
        (r'^%s(?P<path>.*)$' % prefix, 'serve', { 
          'document_root': settings.MEDIA_ROOT, 
          'show_indexes': True }),
        #~ (r'^lino_media/(?P<path>.*)$', 'serve', { 'document_root': LINO_MEDIA, 'show_indexes': True }),
    )


