## Copyright 2008 Luc Saffre.
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

from django.conf.urls.defaults import *
from lino.django.contacts import views, models
from django.views.generic import list_detail

info_dict = {
    'queryset': models.Contact.objects.all(),
}

urlpatterns = patterns('',
    (r'^$', list_detail.object_list, info_dict),
    (r'^(?P<object_id>\d+)/$', list_detail.object_detail, info_dict),
    url(r'^(?P<object_id>\d+)/results/$', 
        list_detail.object_detail, 
        dict(info_dict, template_name='polls/results.html'), 
        'poll_results'),
)


#~ urlpatterns = patterns('',
    #~ (r'^$', views.index),
    #~ (r'^(?P<poll_id>\d+)/$', views.detail),
    #~ (r'^(?P<poll_id>\d+)/results/$', views.results),
    #~ (r'^(?P<poll_id>\d+)/vote/$', views.vote),
#~ )

