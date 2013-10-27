# -*- coding: UTF-8 -*-
## Copyright 2011-2013 Luc Saffre
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
Part of the :xfile:`models` module for the :mod:`lino.modlib.cal` app.

Defines the :class:`Guest` model and its tables.
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator

from lino import dd

  


class Calendar(dd.BabelNamed):
    
    COLOR_CHOICES = [i + 1 for i in range(32)]
    
    class Meta:
        abstract = settings.SITE.is_abstract_model('cal.Calendar')
        verbose_name = _("Calendar")
        verbose_name_plural = _("Calendars")
        
    description = dd.RichTextField(_("Description"),blank=True,format='html')
    
    color = models.IntegerField(
        _("color"),default=1,
        validators=[MinValueValidator(1), MaxValueValidator(32)]
        )
        #~ choices=COLOR_CHOICES)
        
        
class Calendars(dd.Table):
    required = dd.required(user_groups='office',user_level='manager')
    model = 'cal.Calendar'
    
    insert_layout = """
    name
    color
    """
    detail_layout = """
    name color id
    description
    """
        
class Subscription(dd.UserAuthored):
    """
    A Suscription is when a User subscribes to a Calendar.
    It corresponds to what the extensible CalendarPanel calls "Calendars"
    
    :user: points to the author (recipient) of this subscription
    :other_user: 
    
    """
    
    class Meta:
        abstract = settings.SITE.is_abstract_model('cal.Subscription')
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
        
    manager_level_field = 'office_level'
    
    #~ label = models.CharField(_("Label"),max_length=200)
    
    #~ quick_search_fields = ('user__username','user__first_name','user__last_name')

    #~ other_user = dd.ForeignKey('users.User',blank=True,null=True,
        #~ help_text=_("If nonempty, show only events of that user"))
    #~ event_type = dd.ForeignKey('cal.EventType',blank=True,null=True)
    #~ room = dd.ForeignKey('cal.Room',blank=True,null=True)
    #~ team = dd.ForeignKey('users.Team',blank=True,null=True)
    calendar = dd.ForeignKey('cal.Calendar',help_text=_("The calendar you want to subscribe to."))

    is_hidden = models.BooleanField(
        _("hidden"),default=False,help_text=_("""\
Whether this subscription should initially be displayed as a hidden calendar."""))

    #~ def contains_event(self,event):
        #~ if self.event_type is not None and event.event_type != self.event_type:
            #~ return False
        #~ if self.room is not None and event.room != self.room:
            #~ return False
        #~ if self.other_user is not None and event.user != self.other_user:
            #~ return False
        #~ return True

    #~ def add_events_filter(self,qs,ar):
        #~ """
        #~ Add filter criteria to the specified Queryset (on Event model)
        #~ """
    


class Subscriptions(dd.Table):
    required = dd.required(user_groups='office',user_level='manager')
    model = 'cal.Subscription'
    #~ insert_layout = """
    #~ label
    #~ event_type
    #~ """
    #~ detail_layout = """
    #~ label user color
    #~ event_type team other_user room
    #~ description
    #~ """
    
#~ class MySubscriptions(Subscriptions,dd.ByUser):
    #~ pass

#~ class SubscriptionsByCalendar(Subscriptions):
    #~ master_key = 'calendar'

class SubscriptionsByUser(Subscriptions):
    required = dd.required(user_groups='office')
    master_key = 'user'
    auto_fit_column_widths = True

    


__all__ = [
    'Calendar',
    'Calendars',
    'Subscription',
    'Subscriptions',
    ]
