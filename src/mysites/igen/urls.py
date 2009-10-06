## Copyright 2008-2009 Luc Saffre.
## This file is part of the Lino project. 

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import os
# urls.py, the root URLconf module
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import databrowse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import urls as auth_urls

from django.contrib import admin
admin.autodiscover()

from lino.utils.sites import lino_site

#~ # these settings cannot be in lino_settings.py because it modifies the menu which is built by INSTALLED_APPS during their lino_setup()
#~ # TODO: put this into a separate file, similar to lino_settings.py, but executed after lino_setup()
#~ #lino_site.help_url = "http://code.google.com/p/lino/wiki/IgenUserManual"
#~ lino_site.help_url = "http://lino.saffre-rumma.ee/django/igen/userman.html"
#~ lino_site.sort_menu_items(back='config system')


urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^db/(.*)', databrowse.site.root),
    (r'^admin-media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    (r'', include(lino_site.get_urls())),
)    

if settings.EXTJS_ROOT:
   if os.path.exists(settings.EXTJS_ROOT):
      if settings.EXTJS_URL.startswith('/'):
        urlpatterns += patterns('django.views.static',
        (r'^%s(?P<path>.*)$' % settings.EXTJS_URL[1:], 
            'serve', {
            'document_root': settings.EXTJS_ROOT,
            'show_indexes': True }),)



if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
    (r'^media/(?P<path>.*)$', 
        'serve', {
        'document_root': settings.MEDIA_ROOT,
        'show_indexes': True }),)

