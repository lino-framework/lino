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

# urls.py, the root URLconf module
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import databrowse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import urls as auth_urls

from django.contrib import admin
admin.autodiscover()

from lino.django.utils.sites import lino_site

from lino.django.igen import menu
menu.lino_setup(lino_site)

if "lino.django.songs" in settings.INSTALLED_APPS:
    from lino.django.songs import models as menu
    menu.lino_setup(lino_site)

if "lino.django.voc" in settings.INSTALLED_APPS:
    from lino.django.voc import models as menu
    menu.lino_setup(lino_site)

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    #(r'^reports/', include(reports.site.urls)),
    (r'^db/(.*)', databrowse.site.root),
    (r'^admin-media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    #(r'^lino/', include(lino_site.get_urls())),
    (r'', include(lino_site.get_urls())),
    #(r'^accounts/', include(auth_urls)),
    #(r'^$', lino_site.index),
)    

#from django.contrib.auth import urls as auth_site

#urlpatterns += auth_site.urlpatterns