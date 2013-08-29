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

from lino.modlib.cal.models import GuestStates, EventStates

#~ EventStates.add_item('30', _("Visit"), 'visit',fixed=False)


from lino.modlib.reception import App
from lino.mixins import beid

#~ add = GuestStates.add_item
#~ add('21', _("Waiting"),'waiting')

dd.inject_field('cal.Guest','waiting_since',
    models.DateTimeField(_("Waiting since"),
    editable=False,blank=True,null=True,
    help_text = _("Time when the visitor arrived (checked in).")))
dd.inject_field('cal.Guest','waiting_until',
    models.DateTimeField(_("Waiting until"),
    editable=False,blank=True,null=True,
    help_text = _("Time when the visitor was received by agent.")))
dd.inject_field('cal.Guest','present_until',
    models.DateTimeField(_("Present until"),
    editable=False,blank=True,null=True,
    help_text = _("Time when the visitor left (checked out).")))
    

dd.inject_field('system.SiteConfig','prompt_calendar',
    dd.ForeignKey('cal.Calendar',
        verbose_name=_("Default calendar for prompt events"),
        related_name='prompt_calendars',
        blank=True,null=True))    
    
#~ dd.inject_field('cal.Event','is_prompt',
    #~ models.BooleanField(_("Prompt event"),default=False))    

def create_prompt_event(project,partner,user,summary,guest_role):
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
    ekw.update(state=EventStates.accepted)
    ekw.update(user=user)
    if summary:
        ekw.update(summary=summary)
    event = cal.Event(**ekw)
    event.save()
    cal.Guest(
        event=event,
        partner=partner,
        state=cal.GuestStates.present,
        role=guest_role,
        #~ role=settings.SITE.site_config.client_guestrole,
        waiting_since=datetime.datetime.now()
    ).save()
    #~ event.full_clean()
    #~ print 20130722, ekw, ar.action_param_values.user, ar.get_user()
    return event

    

    
class CreateNote(dd.RowAction): 
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
    
    def run_from_ui(self,obj,ar,**kw):
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

    

    
        
class CheckinGuest(dd.NotifyingAction):
    label = _("Checkin")
    help_text = _("Mark this guest as arrived")
    show_in_workflow = True
    
    #~ required = dict(states='invited accepted') 
    required = dd.Required(user_groups='reception')
    
    def get_action_permission(self,ar,obj,state):
        if obj.event.start_date != datetime.date.today():
            return False
        if obj.waiting_since is not None:
            return False
        return super(CheckinGuest,self).get_action_permission(ar,obj,state)
    
    def get_notify_subject(self,ar,obj):
        return _("%(partner)s has started waiting for %(user)s") % dict(
            event=obj,
            user=obj.event.user,
            partner=obj.partner)
    
    def run_from_ui(self,obj,ar,**kw):
        def doit():
            obj.waiting_since = datetime.datetime.now()
            obj.waiting_until = None
            obj.save()
            kw.update(success=True)
            return super(CheckinGuest,self).run_from_ui(obj,ar,**kw)
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
        
    
#~ class ReceiveGuest(dd.NotifyingAction):
class ReceiveGuest(dd.RowAction):
    label = _("Receive")
    help_text = _("Guest was received by agent")
    show_in_workflow = True
    
    
    #~ required = dict(states='waiting')
    
    def get_action_permission(self,ar,obj,state):
        if obj.waiting_since is None:
            return False
        if obj.waiting_until is not None:
            return False
        if obj.present_until is not None:
            return False
        if obj.event.start_date != datetime.date.today():
            return False
        return super(ReceiveGuest,self).get_action_permission(ar,obj,state)
    
    #~ def get_notify_subject(self,ar,obj):
        #~ return _("%(partner)s received by %(user)s") % dict(
            #~ event=obj,
            #~ user=obj.event.user,
            #~ partner=obj.partner)
     
    #~ def before_row_save(self,row,ar):
        #~ row.waiting_until = datetime.datetime.now()
    
    def run_from_ui(self,obj,ar,**kw):
        def ok():
            obj.waiting_until = datetime.datetime.now()
            if obj.state in ExpectedGuestsStates:
                obj.state = GuestStates.present
            obj.save()
            #~ kw = super(ReceiveGuest,self).run_from_ui(obj,ar,**kw)
            kw.update(refresh=True)
            return ar.success(**kw)
        #~ if ar.get_user() == obj.event.user:
        return ar.confirm(ok,
            _("%(guest)s begins consultation with %(user)s.") % 
            dict(user=obj.event.user,guest=obj.partner),_("Are you sure?"))
        
        
"""

What                     waiting_since   waiting_until  present_until
Guest checks in          X
Agent receives the guest X               X
Guest leaves             X               X              X




"""        

#~ class CheckoutGuest(dd.NotifyingAction):
class CheckoutGuest(dd.RowAction):
    label = _("Checkout")
    help_text = _("Guest left the centre")
    show_in_workflow = True
    
    #~ required = dict(states='waiting')
    
    def get_action_permission(self,ar,obj,state):
        if obj.waiting_since is None:
            return False
        if obj.present_until is not None:
            return False
        #~ if obj.event.start_date != datetime.date.today():
            #~ return False
        return super(CheckoutGuest,self).get_action_permission(ar,obj,state)
        
    def run_from_ui(self,obj,ar,**kw):
        def ok():
            if obj.waiting_until is None:
                obj.waiting_until = datetime.datetime.now()
            obj.present_until = datetime.datetime.now()
            obj.save()
            kw.update(refresh=True)
            return ar.success(**kw)
        if obj.waiting_until is None:
            msg = _("%(guest)s leaves without being received.") % dict(guest=obj.partner)
        else:
            msg = _("%(guest)s leaves after meeting with %(user)s.") % dict(guest=obj.partner,user=obj.user)
        return ar.confirm(ok,msg,_("Are you sure?"))
        
    
    #~ def get_notify_subject(self,ar,obj):
        #~ return _("%(partner)s has stopped waiting for %(user)s") % dict(
            #~ event=obj,
            #~ user=obj.event.user,
            #~ partner=obj.partner)
     
    #~ def run_from_ui(self,obj,ar,**kw):
        #~ if obj.waiting_until is None:
            #~ obj.waiting_until = datetime.datetime.now()
        #~ obj.present_until = datetime.datetime.now()
        #~ obj.save()
        #~ kw = super(CheckoutGuest,self).run_from_ui(obj,ar,**kw)
        #~ return kw
        
cal.Guest.checkin = CheckinGuest(sort_index=100)
cal.Guest.receive = ReceiveGuest(sort_index=101)
cal.Guest.checkout = CheckoutGuest(sort_index=102)

class AppointmentsByGuest(dd.Table):
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
        qs = super(AppointmentsByGuest,self).get_request_queryset(ar)
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
            #~ qs = qs.filter(waiting_since__isnull=False,waiting_until__isnull=True)
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
    column_names = 'partner event__user event__summary workflow_buttons waiting_since waiting_until'
    hidden_columns = 'waiting_since waiting_until'
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
    
    
class ReceivedGuests(cal.Guests):
    label = _("Received Guests")
    help_text = _("Shows the visitors being received.")
    filter = Q(waiting_since__isnull=False,waiting_until__isnull=False,present_until__isnull=True)
    column_names = 'since partner event__user event__summary workflow_buttons'
    order_by = ['waiting_since']
    #~ checkout = CheckoutGuest()
    required = dd.Required(user_groups='reception')
    auto_fit_column_widths = True
    
    @dd.displayfield(_('Since'))
    def since(self,obj,ar):
        return naturaltime(obj.waiting_until) # *received since* == *waiting until* 
    
class WaitingGuests(cal.Guests):
    label = _("Waiting Guests")
    help_text = _("Shows the visitors in the waiting room.")
    #~ known_values = dict(state=GuestStates.waiting)
    filter = Q(waiting_since__isnull=False,waiting_until__isnull=True)
    column_names = 'since partner event__user position event__summary workflow_buttons waiting_until'
    hidden_columns = 'waiting_until'
    order_by = ['waiting_since']
    #~ checkout = CheckoutGuest()
    required = dd.Required(user_groups='reception')
    auto_fit_column_widths = True

    @dd.displayfield(_('Since'))
    def since(self,obj,ar):
        return naturaltime(obj.waiting_since)
        
    @dd.displayfield(_('Position'),help_text=_("Position in waiting queue (per agent)"))
    def position(self,obj,ar):
        n = 1 + cal.Guest.objects.filter(
          waiting_since__isnull=False,
          waiting_until__isnull=True,
          event__user=obj.event.user,
          waiting_since__lt=obj.waiting_since).count()
        return str(n)
        
class MyWaitingGuests(WaitingGuests):
    label = _("Waiting Guests")
    #~ label = _("My Waiting Guests")
    required = dd.Required(user_groups='integ debts newcomers')
    column_names = 'since partner event__summary workflow_buttons'
    
    @classmethod
    def param_defaults(self,ar,**kw):
        kw = super(MyWaitingGuests,self).param_defaults(ar,**kw)
        kw.update(user=ar.get_user())
        return kw
        
    

   
#~ def get_todo_tables(ar):
    #~ yield (MyWaitingGuests, None) 
    
dd.add_user_group('reception',App.verbose_name)

def setup_main_menu(site,ui,profile,m):
    #~ m  = m.add_menu("office",lino.OFFICE_MODULE_LABEL)
    m  = m.add_menu("reception",App.verbose_name)
    #~ m  = m.add_menu("cal",cal.MODULE_LABEL)
    #~ m.add_separator("-")
    #~ m.add_action(Clients,'find_by_beid')
    #~ m.add_action(Clients)
    #~ m.add_action(ExpectedGuests)
    m.add_action(MyWaitingGuests)
    m.add_action(ReceivedGuests)
    #~ m.add_action(ExpectedGuests,params=dict(param_values=dict(only_expected=True)))
    #~ m.add_action(WaitingGuests,params=dict(param_values=dict(only_waiting=True)))

def setup_explorer_menu(site,ui,profile,m):
    m  = m.add_menu("reception",App.verbose_name)
    m.add_action(WaitingGuests)
    
