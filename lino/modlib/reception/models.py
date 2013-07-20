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

from lino import dd

cal = dd.resolve_app('cal')

from lino.modlib.cal.models import GuestStates

from lino.modlib.reception import App

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

#~ class CheckinGuest(dd.ChangeStateAction,dd.NotifyingAction):
class CheckinGuest(dd.NotifyingAction):
    label = _("Checkin")
    help_text = _("Mark this guest as arrived")
    show_in_workflow = True
    
    #~ required = dict(states='invited accepted') 
    required = dd.Required(user_groups='reception')
    
    def get_action_permission(self,ar,obj,state):
        if obj.waiting_since is not None and obj.waiting_until is None:
            return False
        return super(CheckinGuest,self).get_action_permission(ar,obj,state)
    
    def get_notify_subject(self,ar,obj):
        return _("%(partner)s has arrived for %(event)s") % dict(
            event=obj,
           partner=obj.partner)
    
    def run_from_ui(self,obj,ar,**kw):
        obj.waiting_since = datetime.datetime.now()
        obj.waiting_until = None
        obj.save()
        kw = super(CheckinGuest,self).run_from_ui(obj,ar,**kw)
        return kw
        
    
#~ class CheckoutGuest(dd.ChangeStateAction,dd.NotifyingAction):
class CheckoutGuest(dd.NotifyingAction):
    label = _("Checkout")
    help_text = _("Guest left from reception queue")
    show_in_workflow = True
    
    #~ required = dict(states='waiting')
    
    def get_action_permission(self,ar,obj,state):
        if obj.waiting_until is not None:
            return False
        return super(CheckoutGuest,self).get_action_permission(ar,obj,state)
    
    def get_notify_subject(self,ar,obj):
        return _("%(partner)s has left for %(event)s") % dict(
            event=obj,
           partner=obj.partner)
    
    #~ def before_row_save(self,row,ar):
        #~ row.waiting_until = datetime.datetime.now()
    
    def run_from_ui(self,obj,ar,**kw):
        obj.waiting_until = datetime.datetime.now()
        obj.save()
        kw = super(CheckoutGuest,self).run_from_ui(obj,ar,**kw)
        return kw
        
cal.Guest.checkout = CheckoutGuest()
cal.Guest.checkin = CheckinGuest()


class ExpectedGuests(cal.Guests):
    label = _("Expected Guests")
    filter = Q(waiting_since__isnull=True,
        state__in=[GuestStates.invited,GuestStates.accepted])
    column_names = 'partner event__user event__summary workflow_buttons'
    #~ checkin = CheckinGuest()
    required = dd.Required(user_groups='reception')
    
class WaitingGuests(cal.Guests):
    label = _("Waiting Guests")
    help_text = _("Shows the visitors in the waiting room.")
    #~ known_values = dict(state=GuestStates.waiting)
    filter = Q(waiting_since__isnull=False,
        waiting_until__isnull=True,
        state__in=[GuestStates.invited,GuestStates.accepted])
    column_names = 'waiting_since partner event__user event__summary workflow_buttons'
    order_by = ['waiting_since']
    #~ checkout = CheckoutGuest()
    required = dd.Required(user_groups='reception integ debts')
    
#~ @dd.receiver(dd.post_analyze)
#~ def setup_workflows(sender=None,dispatch_uid='lino.modlib.welcome.setup_workflows',**kw):
#~ def setup_workflows(site):
    #~ logger.info('20130715 setup_workflows')
    #~ GuestStates.waiting.add_transition(CheckinGuest)
    #~ GuestStates.invited.add_transition(CheckoutGuest)

def setup_main_menu(site,ui,profile,m):
    #~ m  = m.add_menu("office",lino.OFFICE_MODULE_LABEL)
    #~ m  = m.add_menu("reception",_(App.verbose_name))
    m  = m.add_menu("cal",cal.MODULE_LABEL)
    m.add_action(ExpectedGuests)
    m.add_action(WaitingGuests)

dd.add_user_group('reception',_(App.verbose_name))
