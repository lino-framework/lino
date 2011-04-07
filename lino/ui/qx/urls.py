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


urlpatterns = patterns('',
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', 
        {'url': settings.MEDIA_URL + 'lino/favicon.ico'})
)

    
import lino

settings.LINO.setup()

from lino.ui.qx.qx_ui import UI

ui = UI(settings.LINO)

urlpatterns += patterns('',
    (r'', include(ui.get_urls())),
)

if sys.platform == 'win32':

    #~ QXAPP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'app'))
    if False and settings.DEBUG:
        # doesn't yet work
        QXAPP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'app','source'))
    else:
        QXAPP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'app','build'))
    #~ QXAPP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'app','source'))
    #~ QX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'sdk'))
    #~ QX_PATH = os.path.abspath(os.path.dirname(__file__))
    #~ QXAPP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'app','build'))
    #~ QX_PATH = "S:/qooxdoo-1.3-sdk"
    #~ QX_PATH = "L:/snapshots/qooxdoo/qooxdoo",
    #~ LINO_MEDIA = os.path.abspath(os.path.join(os.path.dirname(lino.__file__),'..','media'))
    #~ LINO_MEDIA = os.path.join(lino_site.lino_site.ui.source_dir(),'media')
    #~ print 'LINO_MEDIA=',LINO_MEDIA
    
    #~ if not os.path.exists(QX_PATH):
        #~ raise Exception("QX_PATH %s does not exist" % QX_PATH)
        #~ logger.warning("EXTJS_ROOT %s does not exist",EXTJS_ROOT)
        
    prefix = settings.MEDIA_URL[1:]
    assert prefix.endswith('/')
    
    #~ urlpatterns += patterns('django.views.static',
    #~ (r'^%sqxapp/(?P<path>.*)$' % prefix, 
        #~ 'serve', {
        #~ 'document_root': QXAPP_PATH,
        #~ }),)
        
    urlpatterns += patterns('django.views.static',
    (r'^%sqooxdoo/(?P<path>.*)$' % prefix, 
        'serve', {
        #~ 'document_root': QX_PATH,
        'document_root': settings.QOOXDOO_PATH,
        # 'show_indexes': True 
        }),)

    #~ print LINO_MEDIA
  
    urlpatterns += patterns('django.views.static',
        #~ (r'^%s(?P<path>.*)$' % prefix, 'serve', { 'document_root': QXAPP_ROOT, 'show_indexes': True }),
        (r'^%s(?P<path>.*)$' % prefix, 'serve', { 'document_root': settings.MEDIA_ROOT, 'show_indexes': False }),
        #~ (r'^lino_media/(?P<path>.*)$', 'serve', { 'document_root': LINO_MEDIA, 'show_indexes': True }),
    )


