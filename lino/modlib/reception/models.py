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
Defines models for :mod:`lino.modlib.reception`.

Guest

    state   ---action--> new state

    present ---checkin--> waiting
    waiting ---receive-->  busy
    busy    ---checkout--> gone

"""

import logging
logger = logging.getLogger(__name__)

import os
import sys
import cgi
import datetime
import base64


from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import IntegrityError
from django.utils.encoding import force_unicode
from django.core.exceptions import ValidationError
from django.contrib.humanize.templatetags.humanize import naturaltime

from lino.utils.xmlgen.html import E
from lino.utils import ssin
from lino.utils import join_words
from lino.utils import join_elems

from lino import dd

cal = dd.resolve_app('cal')
system = dd.resolve_app('system')

from lino.modlib.cal.models import GuestStates, EventStates

#~ EventStates.add_item('30', _("Visit"), 'visit',fixed=False)

add = GuestStates.add_item
add('44', _("Waiting"),'waiting')
add('45', _("Busy"),'busy')
add('46', _("Gone"),'gone')



from lino.modlib.reception import App
from lino.mixins import beid

#~ add = GuestStates.add_item
#~ add('21', _("Waiting"),'waiting')

dd.inject_field('cal.Guest','waiting_since',
    models.DateTimeField(_("Waiting since"),
    editable=False,blank=True,null=True,
    help_text = _("Time when the visitor arrived (checked in).")))
dd.inject_field('cal.Guest','busy_since',
    models.DateTimeField(_("Waiting until"),
    editable=False,blank=True,null=True,
    help_text = _("Time when the visitor was received by agent.")))
dd.inject_field('cal.Guest','gone_since',
    models.DateTimeField(_("Present until"),
    editable=False,blank=True,null=True,
    help_text = _("Time when the visitor left (checked out).")))
    

dd.inject_field('system.SiteConfig','prompt_calendar',
    dd.ForeignKey('cal.Calendar',
        verbose_name=_("Default calendar for prompt events"),
        related_name='prompt_calendars',
        blank=True,null=True))
        
        
@dd.receiver(dd.pre_save,sender=system.SiteConfig)
def beware(sender,instance=None,**kw):
    if instance.prompt_calendar is not None:
        if instance.prompt_calendar.invite_client:
            raise Warning("prompt calendar may not invite client!")
    
#~ dd.inject_field('cal.Event','is_prompt',
    #~ models.BooleanField(_("Prompt event"),default=False))    

def create_prompt_event(project,partner,user,summary,guest_role,now=None):
    """
    Create a "prompt event".
    """
    ekw = dict(project=project) 
    #~ ekw.update(state=cal.EventStates.draft)
    #~ ekw.update(state=EventStates.published)
    today = datetime.date.today()
    ekw.update(start_date=today)
    ekw.update(end_date=today)
    ekw.update(calendar=settings.SITE.site_config.prompt_calendar)
    #~ ekw.update(state=EventStates.visit)
    #~ ekw.update(state=EventStates.accepted)
    ekw.update(state=EventStates.published)
    ekw.update(user=user)
    if summary:
        ekw.update(summary=summary)
    event = cal.Event(**ekw)
    event.save()
    if now is None:
        now = datetime.datetime.now()
    cal.Guest(
        event=event,
        partner=partner,
        state=cal.GuestStates.waiting,
        role=guest_role,
        #~ role=settings.SITE.site_config.client_guestrole,
        waiting_since=now
    ).save()
    #~ event.full_clean()
    #~ print 20130722, ekw, ar.action_param_values.user, ar.get_user()
    return event

    

    
class CreateNote(dd.Action): 
    label = _("Attestation")
    show_in_workflow = True
    #~ show_in_row_actions = True
    parameters = dict(
        #~ date=models.DateField(_("Date"),blank=True,null=True),
        note_type=dd.ForeignKey('notes.NoteType'),
        subject=models.CharField(verbose_name=_("Subject"),blank=True))
    params_layout = """
    note_type
    subject
    """
    #~ required = dict(states='coached')
    
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        notes = dd.resolve_app('notes')
        ekw = dict(project=obj,user=ar.get_user()) 
        ekw.update(type=ar.action_param_values.note_type)
        ekw.update(date=datetime.date.today())
        if ar.action_param_values.subject:
            ekw.update(subject=ar.action_param_values.subject)
        note = notes.Note(**ekw)
        note.save()
        #~ kw.update(success=True)
        #~ kw.update(refresh=True)
        return ar.goto_instance(note,**kw)

    

    
        
class CheckinVisitor(dd.NotifyingAction):
    label = _("Checkin")
    help_text = _("Mark this visitor as arrived")
    show_in_workflow = True
    
    #~ required = dict(states='invited accepted') 
    required = dd.Required(user_groups='reception',states='invited accepted present')
    
    def unused_get_action_permission(self,ar,obj,state):
        if obj.event.start_date != datetime.date.today():
            return False
        if obj.waiting_since is not None:
            return False
        return super(CheckinVisitor,self).get_action_permission(ar,obj,state)
    
    def get_notify_subject(self,ar,obj):
        return _("%(partner)s has started waiting for %(user)s") % dict(
            event=obj,
            user=obj.event.user,
            partner=obj.partner)
    
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        def doit():
            obj.waiting_since = datetime.datetime.now()
            obj.state = GuestStates.busy
            obj.busy_since = None
            obj.save()
            kw.update(success=True)
            return super(CheckinVisitor,self).run_from_ui(ar,**kw)
        if obj.event.assigned_to is not None:
            def ok():
                obj.event.user = obj.event.assigned_to
                obj.event.assigned_to = None
                obj.event.save()
                return doit()
            return ar.confirm(ok,
                _("Checkin in will reassign the event from %(old)s to %(new)s.") % 
                dict(old=obj.event.user,new=obj.event.assigned_to),_("Are you sure?"))
        return doit()
        
    
#~ class ReceiveVisitor(dd.NotifyingAction):
class ReceiveVisitor(dd.Action):
    label = _("Receive")
    help_text = _("Visitor was received by agent")
    show_in_workflow = True
    
    #~ required = dd.Required(user_groups='reception',states='invited accepted present')
    
    required = dd.Required(states='waiting')
    
    def unused_get_action_permission(self,ar,obj,state):
        if obj.waiting_since is None:
            return False
        if obj.busy_since is not None:
            return False
        if obj.gone_since is not None:
            return False
        if obj.event.start_date != datetime.date.today():
            return False
        return super(ReceiveVisitor,self).get_action_permission(ar,obj,state)
    
    #~ def get_notify_subject(self,ar,obj):
        #~ return _("%(partner)s received by %(user)s") % dict(
            #~ event=obj,
            #~ user=obj.event.user,
            #~ partner=obj.partner)
     
    #~ def before_row_save(self,row,ar):
        #~ row.busy_since = datetime.datetime.now()
    
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        def ok():
            obj.state = GuestStates.busy
            obj.busy_since = datetime.datetime.now()
            #~ if obj.state in ExpectedGuestsStates:
                #~ obj.state = GuestStates.present
            obj.save()
            #~ kw = super(ReceiveGuest,self).run_from_ui(obj,ar,**kw)
            kw.update(refresh=True)
            return ar.success(**kw)
        #~ if ar.get_user() == obj.event.user:
        return ar.confirm(ok,
            _("%(guest)s begins consultation with %(user)s.") % 
            dict(user=obj.event.user,guest=obj.partner),_("Are you sure?"))
        
        
"""

What                       waiting_since   busy_since  gone_since
Visitor checks in          X
Agent receives the visitor X               X
Visitor leaves             X               X              X




"""        

#~ class CheckoutVisitor(dd.NotifyingAction):
class CheckoutVisitor(dd.Action):
    label = _("Checkout")
    help_text = _("Visitor left the centre")
    show_in_workflow = True
    
    #~ required = dict(states='waiting')
    required = dd.Required(states='busy waiting')
    
    def unused_get_action_permission(self,ar,obj,state):
        if obj.waiting_since is None:
            return False
        if obj.gone_since is not None:
            return False
        #~ if obj.event.start_date != datetime.date.today():
            #~ return False
        return super(CheckoutVisitor,self).get_action_permission(ar,obj,state)
        
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        def ok():
            if obj.busy_since is None:
                obj.busy_since = datetime.datetime.now()
            obj.gone_since = datetime.datetime.now()
            obj.state = GuestStates.gone 
            obj.save()
            kw.update(refresh=True)
            return ar.success(**kw)
        #~ if obj.busy_since is None:
            #~ msg = _("%(guest)s leaves without being received.") % dict(guest=obj.partner)
        #~ else:
        msg = _("%(guest)s leaves after meeting with %(user)s.") % dict(guest=obj.partner,user=obj.user)
        return ar.confirm(ok,msg,_("Are you sure?"))
        
    
    #~ def get_notify_subject(self,ar,obj):
        #~ return _("%(partner)s has stopped waiting for %(user)s") % dict(
            #~ event=obj,
            #~ user=obj.event.user,
            #~ partner=obj.partner)
     
    #~ def run_from_ui(self,obj,ar,**kw):
        #~ if obj.busy_since is None:
            #~ obj.busy_since = datetime.datetime.now()
        #~ obj.gone_since = datetime.datetime.now()
        #~ obj.save()
        #~ kw = super(CheckoutGuest,self).run_from_ui(obj,ar,**kw)
        #~ return kw
        
        
cal.Guest.checkin = CheckinVisitor(sort_index=100)
cal.Guest.receive = ReceiveVisitor(sort_index=101)
cal.Guest.checkout = CheckoutVisitor(sort_index=102)

class AppointmentsByPartner(dd.Table):
    label = _("Appointments")
    model = cal.Guest
    #~ detail_layout = cal.Guests.detail_layout
    master_key = 'partner'
    #~ column_names = 'event__start_date event__user workflow_buttons'
    column_names = 'event__when_text event__user workflow_buttons'
    #~ slave_grid_format = 'html'
    editable = False
    auto_fit_column_widths = True
    
    @classmethod
    def get_request_queryset(self,ar):
        # logger.info("20121010 Clients.get_request_queryset %s",ar.param_values)
        qs = super(AppointmentsByPartner,self).get_request_queryset(ar)
        if isinstance(qs,list): return qs
        start_date = datetime.date.today() - datetime.timedelta(days=17)
        end_date = datetime.date.today() + datetime.timedelta(days=17)
        qs = qs.filter(event__start_date__gte=start_date,event__start_date__lte=end_date)
        return qs



#~ class Guests(cal.Guests):
    #~ 
    #~ use_as_default_table = False
    #~ 
    #~ parameters = dd.ParameterPanel(
        #~ only_waiting = models.BooleanField(verbose_name=_("Waiting")),
        #~ only_expected = models.BooleanField(verbose_name=_("Expected")),
        #~ **cal.Guests.parameters)
    #~ 
    #~ params_layout = cal.Guests.params_layout + " only_waiting only_expected"
    #~ 
    #~ @classmethod
    #~ def get_request_queryset(self,ar):
        #~ # logger.info("20121010 Clients.get_request_queryset %s",ar.param_values)
        #~ qs = super(Guests,self).get_request_queryset(ar)
            #~ 
        #~ if ar.param_values.only_waiting:
            #~ qs = qs.filter(waiting_since__isnull=False,busy_since__isnull=True)
        #~ if ar.param_values.only_expected:
            #~ today = datetime.date.today()
            #~ qs = qs.filter(
                #~ waiting_since__isnull=True,
                #~ # state__in=[GuestStates.invited,GuestStates.accepted],
                #~ event__start_date=today,
                #~ event__end_date=today)
        #~ return qs
        #~ 
    #~ @classmethod
    #~ def get_title_tags(self,ar):
        #~ for t in super(Guests,self).get_title_tags(ar):
            #~ yield t
            #~ 
        #~ if ar.param_values.only_waiting:
            #~ yield unicode(self.parameters['only_waiting'].verbose_name)
        #~ if ar.param_values.only_expected:
            #~ yield unicode(self.parameters['only_expected'].verbose_name)

    
ExpectedGuestsStates = (GuestStates.invited,GuestStates.accepted)

class ExpectedGuests(cal.Guests): 
    label = _("Expected Guests")
    help_text = _("""Consult this table when checking in a partner who has an appointment.""")
    filter = Q(waiting_since__isnull=True,
        state__in=ExpectedGuestsStates)
    column_names = 'partner event__user event__summary workflow_buttons waiting_since busy_since'
    hidden_columns = 'waiting_since busy_since'
    #~ checkin = CheckinGuest()
    required = dd.Required(user_groups='reception')
    
    @classmethod
    def param_defaults(self,ar,**kw):
        kw = super(ExpectedGuests,self).param_defaults(ar,**kw)
        #~ kw.update(only_expected=True)
        today = datetime.date.today()
        kw.update(start_date=today)
        kw.update(end_date=today)
        return kw
    
    
if False:    
  class ReceivedVisitors(cal.Guests):
    label = _("Received Visitors")
    help_text = _("Shows the visitors being received.")
    filter = Q(waiting_since__isnull=False,busy_since__isnull=False,gone_since__isnull=True)
    column_names = 'since partner event__user event__summary workflow_buttons'
    order_by = ['waiting_since']
    #~ checkout = CheckoutGuest()
    required = dd.Required(user_groups='reception')
    auto_fit_column_widths = True
    
    @dd.displayfield(_('Since'))
    def since(self,obj,ar):
        return naturaltime(obj.busy_since) # *received since* == *waiting until* 
    
class Visitors(cal.Guests):
    """
    No subclass should be editable because deleting would leave the 
    useless cal.Event.
    """
    editable = False 
    abstract = True
    column_names = 'since partner event__user event__summary workflow_buttons'
    #~ hidden_columns = 'waiting_since busy_since gone_since'
    auto_fit_column_widths = True
    
    visitor_state = None

    @classmethod
    def param_defaults(self,ar,**kw):
        kw = super(Visitors,self).param_defaults(ar,**kw)
        #~ k = self.visitor_state.name+'_since'
        kw.update(guest_state=self.visitor_state)
        return kw

    #~ doesn't work because cls is always Visitors
    #~ @dd.displayfield(_('Since'))
    #~ def since(cls,obj,ar):
        #~ # either waiting_since, busy_since or gone_since
        #~ if cls.visitor_state is None: return 'x'
        #~ k = cls.visitor_state.name+'_since'
        #~ return naturaltime(getattr(obj,k))
        
        
class MyVisitors(object):
    @classmethod
    def param_defaults(self,ar,**kw):
        kw = super(MyVisitors,self).param_defaults(ar,**kw)
        kw.update(user=ar.get_user())
        return kw
        
        
class BusyVisitors(Visitors):
    label = _("Busy visitors")
    help_text = _("Shows the visitors who are busy with some agent.")
    visitor_state = GuestStates.busy
    order_by = ['busy_since']
    required = dd.Required(user_groups='reception')
    
    @dd.displayfield(_('Since'))
    def since(self,obj,ar):
        return naturaltime(obj.busy_since)
        
class WaitingVisitors(Visitors):
    label = _("Waiting visitors")
    help_text = _("Shows the visitors in the waiting room.")
    #~ known_values = dict(state=GuestStates.waiting)
    #~ filter = Q(waiting_since__isnull=False,busy_since__isnull=True)
    column_names = 'since partner event__user position event__summary workflow_buttons'
    visitor_state = GuestStates.waiting
    
    order_by = ['waiting_since']
    required = dd.Required(user_groups='reception')

    @dd.displayfield(_('Since'))
    def since(self,obj,ar):
        return naturaltime(obj.waiting_since)
        
    @dd.displayfield(_('Position'),help_text=_("Position in waiting queue (per agent)"))
    def position(self,obj,ar):
        n = 1 + cal.Guest.objects.filter(
          #~ waiting_since__isnull=False,
          #~ busy_since__isnull=True,
          state=GuestStates.waiting,
          event__user=obj.event.user,
          waiting_since__lt=obj.waiting_since).count()
        return str(n)
        
class GoneVisitors(Visitors):
    label = _("Gone visitors")
    help_text = _("Shows the visitors who have gone.")
    visitor_state = GuestStates.gone
    order_by = ['gone_since-']
    required = dd.Required(user_groups='reception')
    
    @dd.displayfield(_('Since'))
    def since(self,obj,ar):
        return naturaltime(obj.gone_since)
        
class MyWaitingVisitors(MyVisitors,WaitingVisitors):
    label = _("Visitors waiting for me")
    required = dd.Required(user_groups='integ debts newcomers')
    #~ column_names = 'since partner event__summary workflow_buttons'
    
class MyBusyVisitors(MyVisitors,BusyVisitors):
    label = _("Visitors busy with me")
    required = dd.Required(user_groups='integ debts newcomers')
    
    @classmethod
    def get_welcome_messages(cls,ar):
        guests = []
        sar = ar.spawn(cls)
        for g in sar:
            guests.append(g)
        #~ print "20130909 MyBusyVisitors get_welcome_messages", guests
        if len(guests) > 0:
            #~ print 20130909, guests[0].get_default_table()
            chunks = [ unicode(_("You are busy with ")) ]
            def f(g):
                #~ return sar.obj2html(g,unicode(g.partner))
                return sar.row_action_button(g,cls.detail_action,unicode(g.partner),icon_name=None)
            chunks += join_elems([f(g) for g in guests],sep=unicode(_(" and ")))
            chunks.append('.')
            yield E.span(*chunks)
                
    
class MyGoneVisitors(MyVisitors,GoneVisitors):
    label = _("My gone visitors")
    required = dd.Required(user_groups='integ debts newcomers')
    

   
#~ def get_todo_tables(ar):
    #~ yield (MyBusyVisitors, None) 
    
dd.add_user_group('reception',App.verbose_name)

def setup_main_menu(site,ui,profile,m):
    #~ m  = m.add_menu("office",lino.OFFICE_MODULE_LABEL)
    m  = m.add_menu("reception",App.verbose_name)
    #~ m  = m.add_menu("cal",cal.MODULE_LABEL)
    #~ m.add_separator("-")
    #~ m.add_action(Clients,'find_by_beid')
    #~ m.add_action(Clients)
    #~ m.add_action(ExpectedGuests)
    #~ m.add_action(MyWaitingVisitors)
    #~ m.add_action(MyBusyVisitors)
    
    m.add_action(WaitingVisitors)
    m.add_action(BusyVisitors)
    m.add_action(GoneVisitors)
    
    """
    MyWaitingVisitors is maybe not needed as a menu entry since it is also a get_admin_main_items
    if i remove it then i must edit pcsw_tests.py
    Waiting for user feedback before doing this.
    """
    m.add_action(MyWaitingVisitors)
    #~ m.add_action(ReceivedVisitors)
    #~ m.add_action(ExpectedGuests,params=dict(param_values=dict(only_expected=True)))
    #~ m.add_action(WaitingVisitors,params=dict(param_values=dict(only_waiting=True)))

#~ def setup_explorer_menu(site,ui,profile,m):
    #~ m  = m.add_menu("reception",App.verbose_name)
    #~ m.add_action(WaitingVisitors)
    
