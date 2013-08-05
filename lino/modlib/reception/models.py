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

from lino.modlib.cal.models import GuestStates

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
    help_text = _("Time when the visitor left (checked out).")))
    
    
    
class QuickClientEvent(dd.RowAction): # see also lino_welfare.modlib.cal.CreateClientEvent
    label = _("Appointment")
    #~ show_in_workflow = True
    show_in_row_actions = True
    parameters = dict(
        #~ date=models.DateField(_("Date"),blank=True,null=True),
        user=dd.ForeignKey(settings.SITE.user_model),
        summary=models.CharField(verbose_name=_("Summary"),blank=True))
    params_layout = """
    user 
    summary
    """
    #~ required = dict(states='coached')
    
    def get_notify_subject(self,ar,obj):
        return _("Created appointment for %(user)s with %(partner)s") % dict(
            event=obj,
            user=obj.event.user,
            partner=obj.partner)
     
    def run_from_ui(self,obj,ar,**kw):
        ekw = dict(project=obj) 
        #~ ekw.update(state=cal.EventStates.draft)
        #~ ekw.update(state=EventStates.scheduled)
        today = datetime.date.today()
        ekw.update(start_date=today)
        ekw.update(end_date=today)
        ekw.update(calendar=settings.SITE.site_config.client_calender)
        ekw.update(user=ar.action_param_values.user)
        if ar.action_param_values.summary:
            ekw.update(summary=ar.action_param_values.summary)
        event = cal.Event(**ekw)
        event.save()
        cal.Guest(
            event=event,
            partner=obj,
            role=settings.SITE.site_config.client_guestrole,
            waiting_since=datetime.datetime.now()
        ).save()
        #~ event.full_clean()
        #~ print 20130722, ekw, ar.action_param_values.user, ar.get_user()
        #~ kw = super(QuickClientEvent,self).run_from_ui(obj,ar,**kw)
        kw.update(success=True)
        #~ kw.update(eval_js=ar.renderer.instance_handler(ar,event))
        kw.update(refresh=True)
        return kw

    
class CreateNote(dd.RowAction): 
    label = _("Attestation")
    #~ show_in_workflow = True
    show_in_row_actions = True
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

    

    
class ClientDetail(dd.FormLayout):
    
    main = """
    box1:40 AppointmentsByClient:40 box2:30
    box4 image:15
    
    """
    
    box1 = """
    info
    action_buttons
    """
    
    #~ box1 = dd.Panel("""
    #~ last_name first_name:15 title:10
    #~ address_column
    #~ """,label = _("Address"))
    
    box2 = dd.Panel("""
    email
    phone
    gsm
    """,label = _("Contact"))
    
    box3 = dd.Panel("""
    gender:10 birth_date age:10 
    birth_country birth_place nationality:15 national_id:15 
    """,label = _("Birth"))
    
    eid_panel = dd.Panel("""
    card_number:12 card_valid_from:12 card_valid_until:12 card_issuer:10 card_type:12
    """,label = _("eID card"))

    box4 = """
    box3
    eid_panel
    """
    
    def override_labels(self):
        return dict(
            card_number = _("number"),
            card_valid_from = _("valid from"),
            card_valid_until = _("valid until"),
            card_issuer = _("issued by"),
            card_type = _("eID card type"))
    
def fld2html(fld,value) :
    if value:
        return ("%s: " % f.verbose_name,E.b(value))
    return []
    
class Clients(dd.Table):
    model = 'pcsw.Client'
    column_names = "name_column address_column national_id" 
    auto_fit_column_widths = True
    use_as_default_table = False
    required = dd.Required(user_groups='reception')
    detail_layout = ClientDetail()
    editable = False

    read_beid = beid.BeIdReadCardAction()
    find_by_beid = beid.FindByBeIdAction()
    
    quick_event = QuickClientEvent()
    create_note = CreateNote()
    
    #~ @dd.virtualfield(dd.HtmlBox())
    #~ def eid_card(cls,self,ar):
        #~ for fldname in 'card_number card_valid_from card_valid_until card_issuer card_type'
        #~ fld2html()
        
    @dd.virtualfield(dd.HtmlBox())
    def info(cls,self,ar):
        lines = list(self.address_person_lines()) + list(self.address_location_lines())
        #~ logger.info("20130805 %s", lines)
        elems = join_elems(lines,sep=E.br) 
        #~ logger.info("20130805 %s", elems)
        #~ elems = []
        #~ for ln in lines:
            #~ if ln:   
                #~ if len(elems): 
                    #~ elems.append(E.br())
                #~ elems.append(ln)
        return E.div(*elems,style="font-size:18px;font-weigth:bold;vertical-align:bottom;text-align:middle")
    
        
#~ class CheckinGuest(dd.ChangeStateAction,dd.NotifyingAction):
class CheckinGuest(dd.NotifyingAction):
    label = _("Checkin")
    help_text = _("Mark this guest as arrived")
    show_in_workflow = True
    
    #~ required = dict(states='invited accepted') 
    required = dd.Required(user_groups='reception')
    
    def get_action_permission(self,ar,obj,state):
        if obj.event.start_date != datetime.date.today():
            return False
        if obj.waiting_since is not None and obj.waiting_until is None:
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
        
    
#~ class CheckoutGuest(dd.ChangeStateAction,dd.NotifyingAction):
class CheckoutGuest(dd.NotifyingAction):
    label = _("Checkout")
    help_text = _("Guest left from reception queue")
    show_in_workflow = True
    
    #~ required = dict(states='waiting')
    
    def get_action_permission(self,ar,obj,state):
        if obj.waiting_since is None:
            return False
        if obj.waiting_until is not None:
            return False
        if obj.event.start_date != datetime.date.today():
            return False
        return super(CheckoutGuest,self).get_action_permission(ar,obj,state)
    
    def get_notify_subject(self,ar,obj):
        return _("%(partner)s has stopped waiting for %(user)s") % dict(
            event=obj,
            user=obj.event.user,
            partner=obj.partner)
     
    #~ def before_row_save(self,row,ar):
        #~ row.waiting_until = datetime.datetime.now()
    
    def run_from_ui(self,obj,ar,**kw):
        obj.waiting_until = datetime.datetime.now()
        obj.save()
        kw = super(CheckoutGuest,self).run_from_ui(obj,ar,**kw)
        return kw
        
cal.Guest.checkin = CheckinGuest()
cal.Guest.checkout = CheckoutGuest()

class AppointmentsByClient(dd.Table):
    label = _("Appointments")
    model = cal.Guest
    #~ detail_layout = cal.Guests.detail_layout
    master_key = 'partner'
    #~ column_names = 'event__start_date event__user action_buttons'
    column_names = 'event__when_text event__user action_buttons'
    #~ slave_grid_format = 'html'
    editable = False
    auto_fit_column_widths = True
    
    @classmethod
    def get_request_queryset(self,ar):
        # logger.info("20121010 Clients.get_request_queryset %s",ar.param_values)
        qs = super(AppointmentsByClient,self).get_request_queryset(ar)
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

    
class ExpectedGuests(cal.Guests): 
    label = _("Expected Guests")
    help_text = _("""Consult this table when checking in a partner who has an appointment.""")
    filter = Q(waiting_since__isnull=True,
        state__in=[GuestStates.invited,GuestStates.accepted]
        )
    column_names = 'partner event__user event__summary action_buttons waiting_since waiting_until'
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
    
    
class WaitingGuests(cal.Guests):
    label = _("Waiting Guests")
    help_text = _("Shows the visitors in the waiting room.")
    #~ known_values = dict(state=GuestStates.waiting)
    filter = Q(waiting_since__isnull=False,waiting_until__isnull=True)
    column_names = 'since partner event__user event__summary action_buttons waiting_until'
    hidden_columns = 'waiting_until'
    order_by = ['waiting_since']
    #~ checkout = CheckoutGuest()
    required = dd.Required(user_groups='reception integ debts')

    @dd.displayfield(_('Since'))
    def since(self,obj,ar):
        return naturaltime(obj.waiting_since)
        
class MyWaitingGuests(WaitingGuests):
    column_names = 'since partner event__summary action_buttons waiting_until'
    label = _("Waiting Guests")
    
    @classmethod
    def param_defaults(self,ar,**kw):
        kw = super(MyWaitingGuests,self).param_defaults(ar,**kw)
        kw.update(user=ar.get_user())
        return kw
        
    

        
    
def get_todo_tables(ar):
    yield (MyWaitingGuests, None) 
    

def setup_main_menu(site,ui,profile,m):
    #~ m  = m.add_menu("office",lino.OFFICE_MODULE_LABEL)
    m  = m.add_menu("reception",_(App.verbose_name))
    #~ m  = m.add_menu("cal",cal.MODULE_LABEL)
    #~ m.add_separator("-")
    m.add_action(Clients,'find_by_beid')
    m.add_action(Clients)
    m.add_action(ExpectedGuests)
    m.add_action(WaitingGuests)
    #~ m.add_action(ExpectedGuests,params=dict(param_values=dict(only_expected=True)))
    #~ m.add_action(WaitingGuests,params=dict(param_values=dict(only_waiting=True)))

dd.add_user_group('reception',_(App.verbose_name))
