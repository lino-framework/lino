# -*- coding: UTF-8 -*-
# Copyright 2011-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models for `lino.modlib.extensible`.

.. autosummary::

"""


from __future__ import unicode_literals
from builtins import str

import logging
logger = logging.getLogger(__name__)

import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from lino.api import dd
from lino.core import constants

from lino.modlib.office.roles import OfficeUser

from ..cal.models import Subscription, Calendars, Events


def parsedate(s):
    return datetime.date(*settings.SITE.parse_date(s))


class CalendarAction(dd.Action):
    """The Action for opening the calendar panel."""
    extjs_main_panel = "Lino.CalendarApp().get_main_panel()"
    opens_a_window = True
    action_name = 'grid'  # because...
    default_format = 'html'
    icon_name = 'calendar'


class ExtDateTimeField(dd.VirtualField):

    """An editable virtual field needed for communication with the
    Ext.ensible CalendarPanel because Lino uses two separate fields
    `start_date` and `start_time` or `end_date` and `end_time` while
    CalendarPanel expects and sends single DateTime values.

    """
    editable = True

    def __init__(self, name_prefix, alt_prefix, label):
        self.name_prefix = name_prefix
        self.alt_prefix = alt_prefix
        return_type = models.DateTimeField(label)
        dd.VirtualField.__init__(self, return_type, None)

    def set_value_in_object(self, request, obj, value):
        obj.set_datetime(self.name_prefix, value)

    def value_from_object(self, obj, ar):
        #~ logger.info("20120118 value_from_object() %s",dd.obj2str(obj))
        return obj.get_datetime(self.name_prefix, self.alt_prefix)


class ExtSummaryField(dd.VirtualField):

    """
    An editable virtual field needed for 
    communication with the Ext.ensible CalendarPanel
    because we want a customized "virtual summary" 
    that includes the project name.
    """
    editable = True

    def __init__(self, label):
        rt = models.CharField(label)
        dd.VirtualField.__init__(self, rt, None)

    def set_value_in_object(self, request, obj, value):
        if obj.project:
            s = str(obj.project)
            if value.startswith(s):
                value = value[len(s):]
        obj.summary = value

    def value_from_object(self, obj, ar):
        #~ logger.info("20120118 value_from_object() %s",dd.obj2str(obj))
        return obj.get_event_summary(ar)


class CalendarPanel(dd.Frame):
    """Opens the "Calendar View" (a special window with the Ext.ensible
    CalendarAppPanel).

    """

    help_text = _("""Displays your events in a "calendar view" \
    with the possibility to switch between daily, weekly, monthly view.""")
    required_roles = dd.required(OfficeUser)
    label = _("Calendar")

    @classmethod
    def get_default_action(self):
        return CalendarAction()


class PanelCalendars(Calendars):
    use_as_default_table = False
    required_roles = dd.required(OfficeUser)
    #~ column_names = 'id name description color is_hidden'
    #~ column_names = 'id babel_name description color is_hidden'
    column_names = 'id summary description color is_hidden'

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(PanelCalendars, self).get_request_queryset(ar)
        subs = Subscription.objects.filter(
            user=ar.get_user()).values_list('calendar__id', flat=True)
        return qs.filter(id__in=subs)

        #~ return qs.filter(user=ar.get_user())
        #~ for sub in Subscription.objects.filter(user=ar.get_user()):
            #~ qs = sub.add_events_filter(qs,ar)
        #~ return qs
        #~ return user_calendars(qs,ar.get_user())

    @dd.displayfield()
    def summary(cls, self, ar):
        #~ return dd.babelattr(self,'name')
        return str(self)

    @dd.virtualfield(models.BooleanField(_('Hidden')))
    def is_hidden(cls, self, ar):
        #~ return False
        #~ if self.user == ar.get_user():
            #~ return False
        try:
            sub = self.subscription_set.get(user=ar.get_user())
        except self.subscription_set.model.DoesNotExist:
            return True
        return sub.is_hidden


class PanelEvents(Events):

    """
    The table used for Ext.ensible CalendarPanel.
    """
    required_roles = dd.required(OfficeUser)
    use_as_default_table = False
    #~ parameters = dict(team_view=models.BooleanField(_("Team View")))

    column_names = 'id start_dt end_dt summary description user \
    room calendar #rset url all_day reminder'

    start_dt = ExtDateTimeField('start', None, _("Start"))
    end_dt = ExtDateTimeField('end', 'start', _("End"))

    summary = ExtSummaryField(_("Summary"))
    #~ overrides the database field of same name

    @classmethod
    def get_title_tags(self, ar):
        for t in super(PanelEvents, self).get_title_tags(ar):
            yield t
        if ar.subst_user:
            yield str(ar.subst_user)

    @classmethod
    def parse_req(self, request, rqdata, **kw):
        """
        Handle the request parameters issued by Ext.ensible CalendarPanel.
        """
        #~ filter = kw.get('filter',{})
        assert not 'filter' in kw
        fkw = {}
        #~ logger.info("20120118 filter is %r", filter)
        endDate = rqdata.get(constants.URL_PARAM_END_DATE, None)
        if endDate:
            d = parsedate(endDate)
            fkw.update(start_date__lte=d)
        startDate = rqdata.get(constants.URL_PARAM_START_DATE, None)
        if startDate:
            d = parsedate(startDate)
            #~ logger.info("startDate is %r", d)
            fkw.update(start_date__gte=d)
        #~ logger.info("20120118 filter is %r", filter)

        #~ subs = Subscription.objects.filter(user=request.user).values_list('calendar__id',flat=True)
        #~ filter.update(calendar__id__in=subs)

        fkw.update(event_type__is_appointment=True)

        flt = models.Q(**fkw)

        # who am i ?
        me = request.subst_user or request.user

        # show all my events
        for_me = models.Q(user__isnull=True)
        for_me |= models.Q(user=me)
        for_me |= models.Q(assigned_to=me)

        # also show events to which i am invited
        if me.partner:
            for_me = for_me | models.Q(guest__partner=me.partner)

        if False:
            # currently disabled. this is needed only when you want to
            # support private events, i.e. events which are never
            # visible to other users.

            flt = flt & for_me
        # logger.info('20140402 %s', flt)
        kw.update(filter=flt)
        #~ logger.info('20130808 %s %s', tv,me)
        return kw

    @classmethod
    def create_instance(self, ar, **kw):
        """This handles a rather hackerish method used to make appointments
        for a predifined "project", concrete use case is the "find
        appointment" button for a given client and user.

        """
        obj = super(PanelEvents, self).create_instance(ar, **kw)
        if ar.current_project is not None:
            obj.project = settings.SITE.project_model.objects.get(
                pk=ar.current_project)
            #~ obj.state = EventStates.published
        # logger.info('20140402 create_instance %s ', obj)
        return obj


def setup_quicklinks(site, ar, m):
    m.add_action('extensible.CalendarPanel')


# __all__ = ['CalendarPanel']
