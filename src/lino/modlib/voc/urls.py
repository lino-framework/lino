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

from django.conf.urls.defaults import *
#from django.views.generic.list_detail import object_list, object_detail

from lino.voc import views, models

#~ info_dict = {
    #~ 'queryset': models.Unit.objects.all(),
#~ }

#~ ENTRIES = dict(
  #~ queryset=models.Entry.objects.all(),
  #~ paginate_by=1)

# 'template_object_name' : 'unit'

#~ urlpatterns = patterns('',
    #~ (r'^$', object_list, info_dict, "voc_unit_list"),
    #~ (r'^units/(?P<object_id>\d+)/$', object_detail, info_dict, "voc_unit_detail"),
    #~ (r'^units/(?P<object_id>\d+)/(?P<page>\d+)/$', object_list, 
      #~ dict(queryset=models.Entry.objects.all(),
  #~ paginate_by=1), "voc_entry_list"),
    #~ (r'^entries/(?P<object_id>\d+)/$', object_detail, ENTRIES, "voc_entry_detail"),
#~ )

urlpatterns = patterns('',
    (r'^$', views.unit_list ),
    (r'^unit/(?P<unit_id>\d+)$', views.unit_detail),
    (r'^entry/(?P<entry_id>\d+)$', views.entry_detail),
)

#    (r'^(?P<course_id>\d+)/(?P<page>\d+)$', views.entry_page),
