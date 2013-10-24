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
The :xfile:`models.py` module for the :mod:`lino.modlib.rooms` app.
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

from lino import dd

contacts = dd.resolve_app('contacts',strict=True)
#~ cal = dd.resolve_app('cal',strict=True)

from lino.modlib.cal.utils import Recurrencies
from lino.modlib.cal.mixins import Reservation

from . import App

class BookingStates(dd.Workflow):
    required = dd.required(user_level='admin')

add = BookingStates.add_item
add('10', _("Interested"),'interested')
add('20', _("Option"),'option')
add('30', _("Booked"),'booked')
add('40', _("Cancelled"),'cancelled')



class Booking(contacts.ContactRelated,Reservation,dd.Printable):
    
    class Meta:
        abstract = settings.SITE.is_abstract_model('rooms.Booking')
        verbose_name = _("Booking")
        verbose_name_plural = _('Bookings')
        
    workflow_state_field = 'state'
    
    state = BookingStates.field(default=BookingStates.interested)
    
    event_type = dd.ForeignKey('cal.EventType',null=True,blank=True,
        help_text=_("""The Event Type to which events will be generated."""))
    
    #~ def full_clean(self,*args,**kw):
        #~ if self.every_unit is None:
            #~ self.every_unit = 1
        #~ if self.every is None:
            #~ self.every = Recurrencies.once
        #~ super(Booking,self).full_clean(*args,**kw)
        
        
    def __unicode__(self):
        return u"%s #%s (%s)" % (self._meta.verbose_name,self.pk,self.room)
    
    def update_cal_from(self,ar):
        return self.start_date
        
    def update_cal_until(self):
        return self.end_date
        
    def update_cal_calendar(self):
        return self.event_type
        
    def update_cal_summary(self,i):
        return "%s %s" % (dd.babelattr(self.event_type,'event_label'),i)
        
    def before_auto_event_save(self,event):
        """
        Sets room and start_time for automatic events.
        This is a usage example for :meth:`EventGenerator.before_auto_event_save 
        <lino.modlib.cal.models.EventGenerator.before_auto_event_save>`.
        """
        #~ logger.info("20131008 before_auto_event_save")
        assert not settings.SITE.loading_from_dump
        assert event.owner == self
        if event.is_user_modified(): return
        event.room = self.room
        event.start_time = self.start_time
        event.end_time = self.end_time


dd.update_field(Booking,'contact_person',verbose_name = _("Contact person"))
dd.update_field(Booking,'company',verbose_name = _("Organizer"))
dd.update_field(Booking,'every_unit',default=Recurrencies.once)
dd.update_field(Booking,'every',default=1)


class BookingDetail(dd.FormLayout):
    #~ start = "start_date start_time"
    #~ end = "end_date end_time"
    #~ freq = "every every_unit"
    #~ start end freq
    main = "general courses.EnrolmentsByCourse"
    general = dd.Panel("""
    start_date start_time end_date end_time
    room event_type state id:8
    max_events max_date every_unit every 
    monday tuesday wednesday thursday friday saturday sunday
    company contact_person user 
    cal.EventsByController
    """,label=_("General"))
    
    #~ def setup_handle(self,dh):
        #~ dh.start.label = _("Start")
        #~ dh.end.label = _("End")
        #~ dh.freq.label = _("Frequency")
  
class Bookings(dd.Table):
    model = 'rooms.Booking'
    #~ order_by = ['date','start_time']
    detail_layout = BookingDetail() 
    insert_layout = """
    start_date 
    company contact_person
    """
    column_names = "start_date company room  *"
    order_by = ['start_date']
    
    parameters = dd.ObservedPeriod(
        company = models.ForeignKey('contacts.Company',blank=True,null=True),
        state = BookingStates.field(blank=True),
        )
    params_layout = """company state"""
    
    simple_param_fields = 'company state'.split()
    
    @classmethod
    def get_request_queryset(self,ar):
        qs = super(Bookings,self).get_request_queryset(ar)
        if isinstance(qs,list): return qs
        for n in self.simple_param_fields:
            v = ar.param_values.get(n)
            if v:
                qs = qs.filter(**{n:v})
                #~ print 20130530, qs.query
            
        return qs
        
    @classmethod
    def get_title_tags(self,ar):
        for t in super(Bookings,self).get_title_tags(ar):
            yield t
            
        for n in self.simple_param_fields:
            v = ar.param_values.get(n)
            if v:
                yield unicode(v)
                
    

#~ class CoursesByCompany(Courses):
class BookingsByCompany(Bookings):
    master_key = "company"
    

def setup_main_menu(site,ui,profile,main):
    m = main.get_item("cal")
    #~ m = main.add_menu("rooms",App.verbose_name)
    m.add_action(Bookings)
