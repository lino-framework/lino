# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Part of the :xfile:`models.py` module for `lino.modlib.cal`.

Defines the following models and their tables:

- :class:`Calendar` 
- :class:`Subscription` 

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.office.roles import OfficeUser, OfficeStaff

from lino.api import dd, rt
from lino import mixins


def default_color():
    d = Calendar.objects.all().aggregate(models.Max('color'))
    n = d['color__max'] or 0
    return n + 1


class Calendar(mixins.BabelNamed):

    COLOR_CHOICES = [i + 1 for i in range(32)]

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Calendar')
        verbose_name = _("Calendar")
        verbose_name_plural = _("Calendars")

    description = dd.RichTextField(_("Description"), blank=True, format='html')

    color = models.IntegerField(
        _("color"), default=default_color,
        validators=[MinValueValidator(1), MaxValueValidator(32)]
    )
        #~ choices=COLOR_CHOICES)


class Calendars(dd.Table):
    required_roles = dd.required(OfficeStaff)
    model = 'cal.Calendar'

    insert_layout = """
    name
    color
    """
    detail_layout = """
    name color id
    description SubscriptionsByCalendar
    """


class Subscription(UserAuthored):

    """
    A Suscription is when a User subscribes to a Calendar.
    It corresponds to what the extensible CalendarPanel calls "Calendars"
    
    :user: points to the author (recipient) of this subscription
    :other_user:
    
    """

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Subscription')
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
        unique_together = ['user', 'calendar']

    manager_roles_required = OfficeStaff
    # manager_level_field = 'office_level'

    calendar = dd.ForeignKey(
        'cal.Calendar', help_text=_("The calendar you want to subscribe to."))

    is_hidden = models.BooleanField(
        _("hidden"), default=False,
        help_text=_("""Whether this subscription should "
        "initially be displayed as a hidden calendar."""))


class Subscriptions(dd.Table):
    required_roles = dd.required(OfficeStaff)
    model = 'cal.Subscription'
    order_by = ['calendar__name']
    #~ insert_layout = """
    #~ label
    #~ event_type
    #~ """
    #~ detail_layout = """
    #~ label user color
    #~ event_type team other_user room
    #~ description
    #~ """

#~ class MySubscriptions(Subscriptions, ByUser):
    #~ pass

#~ class SubscriptionsByCalendar(Subscriptions):
    #~ master_key = 'calendar'


class SubscriptionsByUser(Subscriptions):
    required_roles = dd.required(OfficeUser)
    master_key = 'user'
    auto_fit_column_widths = True


class SubscriptionsByCalendar(Subscriptions):
    required_roles = dd.required(OfficeUser)
    master_key = 'calendar'
    auto_fit_column_widths = True


def check_subscription(user, calendar):
    "Check whether the given subscription exists. If not, create it."
    Subscription = rt.modules.cal.Subscription
    if calendar is None:
        return
    try:
        Subscription.objects.get(user=user, calendar=calendar)
    except Subscription.DoesNotExist:
        sub = Subscription(user=user, calendar=calendar)
        sub.full_clean()
        sub.save()
