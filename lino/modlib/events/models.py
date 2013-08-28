# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
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
The :xfile:`models.py` module of :mod:`lino.modlib.events`.
"""

from __future__ import unicode_literals

import os
import cgi
import datetime

from django.db import models
#~ from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.utils.xmlgen.html import E
#~ from north import dbutils
#~ from lino import mixins
from lino import dd
from lino.core.constants import _handle_attr_name

def sepjoin(items,sep=', '):
    rv = []
    for i in items:
        if len(rv): rv.append(sep)
        rv.append(unicode(i))
    return rv



class Place(dd.BabelNamed): 
    city = dd.ForeignKey('countries.City',blank=True,null=True)

class Places(dd.Table):
    model = Place
    
class Feature(dd.BabelNamed): 
    pass

class Features(dd.Table):
    model = Feature
    
class Type(dd.BabelNamed): 
    #~ pass
    events_column_names = models.CharField(
        max_length="100",
        default="when:30 what:40 where:30")
        
    def EventsByType(self,**kw):
        return EventsByType.request(master_instance=self)

class Types(dd.Table):
    model = Type
    
class Event(dd.BabelNamed):
    date = models.DateField(_("Date"))
    place = dd.ForeignKey(Place,blank=True,null=True)
    type = dd.ForeignKey(Type)
    features = models.ManyToManyField(Feature)
    #~ cities = models.ManyToManyField('countries.City')
    #~ description = dd.BabelTextField(format='plain',blank=True)
    url = models.URLField(blank=True)

class Stage(dd.Sequenced): 
    event = dd.ForeignKey('events.Event',related_name="stages")
    city = dd.ForeignKey('countries.City',related_name="stages")
    
    def __unicode__(self):
        return unicode(self.city)
    
    def get_siblings(self):
        return self.event.stages.order_by('seqno')

dd.update_field(Event,'name',blank=True)

class StagesByEvent(dd.Table):
    model = Stage # Event.cities.through
    master_key = 'event'

class FeaturesByEvent(dd.Table):
    model = Event.features.through
    master_key = 'event'

class Events(dd.Table):
    model = Event
    order_by = ['date']
    column_names = "date place type"
    detail_layout = """
    type date place
    StagesByEvent FeaturesByEvent
    """
    
    @dd.displayfield(_("When"))
    def when(self,obj,ar):
        #~ rv = dbutils.dtosl(obj.date)
        rv = dd.fdf(obj.date)
        if obj.url:
            rv = '\n'.join(rv.split()) # replaces spaces by newline to avoid large column
            rv = E.a(rv,href=obj.url)
        return rv

    @dd.displayfield(_("Where"))
    def where(self,obj,ar):
        if obj.place is not None:
            return E.p(unicode(obj.place), ' ', E.b(unicode(obj.place.city)))
        # remember: "von Ans nach Eupen und nicht andersrum"
        return E.p(*sepjoin(obj.stages.order_by('seqno'),' -- '))

    @dd.displayfield(_("What"))
    def what(self,obj,ar):
        chunks = []
        if obj.name:
            chunks += [E.b(unicode(obj)), E.br()]
        chunks += sepjoin(obj.features.all())
        #~ if obj.url:
            #~ chunks += [E.br(),E.a(_("More"),href=obj.url)]
        return E.p(*chunks)

    
class EventsByType(Events):
    master_key = 'type'
    #~ column_names = "when what where"
    
    @classmethod
    def get_column_names(self,ar):
        return ar.master_instance.events_column_names
        
    @classmethod
    def get_handle_name(self,ar):
        hname = _handle_attr_name
        #~ hname = super(PrintEntriesByBudget,self).get_handle_name(ar)
        hname += ar.master_instance.events_column_names.replace(" ","_")
        return hname
        
    


MODULE_LABEL = _("Events")

def setup_config_menu(site,ui,profile,m): 
    m = m.add_menu("events",MODULE_LABEL)
    m.add_action(Types)
    m.add_action(Places)
    m.add_action(Features)
    
def setup_main_menu(site,ui,profile,m): 
    m = m.add_menu("events",MODULE_LABEL)
    m.add_action(Events)
