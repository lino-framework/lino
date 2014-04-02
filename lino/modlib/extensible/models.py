# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
The :xfile:`models.py` module for the :mod:`lino.modlib.extensible.cal` app.
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import exceptions
from lino import dd
from lino.core import constants
from lino.core.actions import CalendarAction

from ..cal.models import Subscription, Calendars, Events


def parsedate(s):
    return datetime.date(*settings.SITE.parse_date(s))


class ExtDateTimeField(dd.VirtualField):

    """
    An editable virtual field needed for 
    communication with the Ext.ensible CalendarPanel
    because Lino uses two separate fields 
    `start_date` and `start_time`
    or `end_date` and `end_time` while CalendarPanel expects 
    and sends single DateTime values.
    """
    editable = True

    def __init__(self, name_prefix, alt_prefix, label):
        self.name_prefix = name_prefix
        self.alt_prefix = alt_prefix
        rt = models.DateTimeField(label)
        dd.VirtualField.__init__(self, rt, None)

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
            s = unicode(obj.project)
            if value.startswith(s):
                value = value[len(s):]
        obj.summary = value

    def value_from_object(self, obj, ar):
        #~ logger.info("20120118 value_from_object() %s",dd.obj2str(obj))
        return obj.get_event_summary(ar)


class CalendarPanel(dd.Frame):

    """
    Opens the "Calendar View" (a special window with the
    Ext.ensible CalendarAppPanel).
    """
    help_text = _("""Displays your events in a "calendar view" \
    with the possibility to switch between daily, weekly, monthly view.""")
    required = dd.required(user_groups='office')
    label = _("Calendar")

    @classmethod
    def get_default_action(self):
        return CalendarAction()


class PanelCalendars(Calendars):
    use_as_default_table = False
    required = dd.required(user_groups='office')
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
        return unicode(self)

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
    required = dd.required(user_groups='office')
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
            yield unicode(ar.subst_user)

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

        """If you override `parse_req`, then keep in mind that it will be
        called *before* Lino checks the requirements.  For example the
        user may be AnonymousUser even if the requirements won't let
        it be executed.

        `request.subst_user.profile` may be None e.g. when called 
        from `find_appointment` in :ref:`welfare.pcsw.Clients`.

        """
        if not request.user.profile.authenticated:
            raise exceptions.PermissionDenied(
                _("As %s you have no permission to run this action.")
                % request.user.profile)

        # who am i ?
        me = request.subst_user or request.user

        # show all my events
        for_me = models.Q(user__isnull=True)
        for_me |= models.Q(user=me)
        for_me |= models.Q(assigned_to=me)

        # also show events to which i am invited
        if me.partner:
            #~ me_as_guest = Guest.objects.filter(partner=request.user.partner)
            #~ for_me = for_me | models.Q(guest_set__count__gt=0)
            #~ for_me = for_me | models.Q(guest_count__gt=0)
            for_me = for_me | models.Q(guest__partner=me.partner)

        if False:
            # in team view, show also events of all my team members
            tv = rqdata.get(constants.URL_PARAM_TEAM_VIEW, False)
            if tv and constants.parse_boolean(tv):
                # positive list of ACLs for events of team members
                team_classes = (None, AccessClasses.public,
                                AccessClasses.show_busy)
                my_teams = Membership.objects.filter(user=me)
                we = settings.SITE.user_model.objects.filter(
                    users_membership_set_by_user__team__in=my_teams)
                #~ team_ids = Membership.objects.filter(user=me).values_list('watched_user__id',flat=True)
                #~ for_me = for_me | models.Q(user__id__in=team_ids,access_class__in=team_classes)
                for_me = for_me | models.Q(
                    user__in=we, access_class__in=team_classes)
        if False:
            # currently disabled. this is needed ony when you want to
            # support private events, i.e. events which are never
            # visible to other users.

            flt = flt & for_me
        # logger.info('20140402 %s', flt)
        kw.update(filter=flt)
        #~ logger.info('20130808 %s %s', tv,me)
        return kw

    #~ @classmethod
    #~ def get_request_queryset(self,ar):
        #~ qs = super(PanelEvents,self).get_request_queryset(ar)
        #~ return qs

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


def setup_main_menu(site, ui, profile, m):
    m = m.add_menu("cal", settings.SITE.plugins.cal.verbose_name)
    # m = m.add_menu("cal", _("Calendar"))
    m.add_action('extensible.CalendarPanel')


def setup_quicklinks(site, ar, m):
    m.add_action('extensible.CalendarPanel')


__all__ = ['CalendarPanel']
