# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Part of the :xfile:`models` module for the :mod:`lino.modlib.cal` app.

Defines the :class:`Guest` model and its tables.
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

from lino import dd, mixins

from .workflows import GuestStates
from .workflows import EventStates

# outbox = dd.resolve_app('outbox')


# class GuestRole(outbox.MailableType, mixins.BabelNamed):
class GuestRole(mixins.BabelNamed):
    templates_group = 'cal/Guest'

    class Meta:
        verbose_name = _("Guest Role")
        verbose_name_plural = _("Guest Roles")


class GuestRoles(dd.Table):
    help_text = _("The role of a guest expresses what the "
                  "partner is going to do there.")
    model = GuestRole
    required = dd.required(user_groups='office', user_level='admin')
    detail_layout = """
    id name
    #build_method #template #email_template #attach_to_email
    cal.GuestsByRole
    """


class Guest(dd.Model):
    # TODO: rename to `Presence`
    workflow_state_field = 'state'

    allow_cascaded_delete = ['event']

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Guest')
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")

    event = models.ForeignKey('cal.Event',
                              verbose_name=_("Event"))

    partner = dd.ForeignKey('contacts.Partner')

    role = models.ForeignKey('cal.GuestRole',
                             verbose_name=_("Role"),
                             blank=True, null=True)

    state = GuestStates.field(default=GuestStates.invited)

    remark = models.CharField(
        _("Remark"), max_length=200, blank=True)

    def get_user(self):
        # used to apply `owner` requirement in GuestState
        return self.event.user
    user = property(get_user)

    def __unicode__(self):
        return u'%s #%s (%s)' % (
            self._meta.verbose_name, self.pk, self.event.strftime())

    # def get_printable_type(self):
    #     return self.role

    def get_mailable_type(self):
        return self.role

    def get_mailable_recipients(self):
        yield ('to', self.partner)

    @dd.displayfield(_("Event"))
    def event_summary(self, ar):
        return ar.obj2html(self.event, self.event.get_event_summary(ar))
        #~ return event_summary(self.event,ar.get_user())

    #~ def before_ui_save(self,ar,**kw):
        #~ if not self.state:
            #~ self.state = GuestStates.invited
        #~ return super(Guest,self).before_ui_save(ar,**kw)

    #~ def on_user_change(self,request):
        #~ if not self.state:
            #~ self.state = GuestState.invited


    #~ def get_recipient(self):
        #~ return self.partner
    #~ recipient = property(get_recipient)

    #~ @classmethod
    #~ def setup_report(cls,rpt):
        #~ mixins.CachedPrintable.setup_report(rpt)
        #~ outbox.Mailable.setup_report(rpt)

    #~ @dd.action(_("Invite"),required=dict(states=['']))
    #~ def invite(self,ar):
        #~ self.state = GuestState.invited

    #~ @dd.action(_("Confirm"),required=dict(states=['invited']))
    #~ def confirm(self,ar):
        #~ self.state = GuestState.confirmed

#~ class Guests(dd.Table,workflows.Workflowable):
class Guests(dd.Table):
    help_text = _("""A guest is a partner invited to an event. """)
    model = 'cal.Guest'
    required = dd.required(user_groups='office', user_level='admin')
    column_names = 'partner role workflow_buttons remark event *'
    detail_layout = """
    event partner role
    state remark workflow_buttons
    # outbox.MailsByController
    """
    insert_layout = dd.FormLayout("""
    event
    partner
    role
    """, window_size=(60, 'auto'))

    parameters = dd.ObservedPeriod(
        user=dd.ForeignKey(settings.SITE.user_model,
                           verbose_name=_("Responsible user"),
                           blank=True, null=True,
                           help_text=_("Only rows managed by this user.")),
        project=dd.ForeignKey(settings.SITE.project_model,
                              blank=True, null=True),
        partner=dd.ForeignKey('contacts.Partner',
                              blank=True, null=True),
        event_state=EventStates.field(
            blank=True,
            verbose_name=_("Event state"),
            help_text=_("Only rows having this event state.")),
        guest_state=GuestStates.field(
            blank=True,
            verbose_name=_("Guest state"),
            help_text=_("Only rows having this guest state.")),
    )

    params_layout = """start_date end_date user event_state guest_state
    project partner"""

    @classmethod
    def get_request_queryset(self, ar):
        #~ logger.info("20121010 Clients.get_request_queryset %s",ar.param_values)
        qs = super(Guests, self).get_request_queryset(ar)

        if isinstance(qs, list):
            return qs

        if ar.param_values.user:
            qs = qs.filter(event__user=ar.param_values.user)
        if settings.SITE.project_model is not None and ar.param_values.project:
            qs = qs.filter(event__project=ar.param_values.project)

        if ar.param_values.event_state:
            qs = qs.filter(event__state=ar.param_values.event_state)

        if ar.param_values.guest_state:
            qs = qs.filter(state=ar.param_values.guest_state)

        if ar.param_values.partner:
            qs = qs.filter(partner=ar.param_values.partner)

        if ar.param_values.start_date:
            if ar.param_values.end_date:
                qs = qs.filter(
                    event__start_date__gte=ar.param_values.start_date)
            else:
                qs = qs.filter(event__start_date=ar.param_values.start_date)
        if ar.param_values.end_date:
            qs = qs.filter(event__end_date__lte=ar.param_values.end_date)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Guests, self).get_title_tags(ar):
            yield t
        if ar.param_values.start_date or ar.param_values.end_date:
            yield unicode(_("Dates %(min)s to %(max)s") % dict(
                min=ar.param_values.start_date or'...',
                max=ar.param_values.end_date or '...'))

        if ar.param_values.event_state:
            yield unicode(ar.param_values.event_state)

        if ar.param_values.partner:
            yield unicode(ar.param_values.partner)

        if ar.param_values.guest_state:
            yield unicode(ar.param_values.guest_state)

        if ar.param_values.user:
            yield unicode(ar.param_values.user)

        if settings.SITE.project_model is not None and ar.param_values.project:
            yield unicode(ar.param_values.project)


class GuestsByEvent(Guests):
    master_key = 'event'
    required = dd.required(user_groups='office')
    auto_fit_column_widths = True
    column_names = 'partner role workflow_buttons'


class GuestsByRole(Guests):
    master_key = 'role'
    required = dd.required(user_groups='office')

if settings.SITE.is_installed('contacts'):

    class GuestsByPartner(Guests):
        label = _("Presences")
        master_key = 'partner'
        required = dd.required(user_groups='office')
        column_names = 'event__when_text workflow_buttons'
        auto_fit_column_widths = True

    class MyPresences(Guests):
        required = dd.required(user_groups='office')
        order_by = ['event__start_date', 'event__start_time']
        label = _("My presences")
        help_text = _(
            """Shows all my presences in calendar events, independently of their state.""")
        column_names = 'event__start_date event__start_time event_summary role workflow_buttons remark *'
        params_panel_hidden = True

        @classmethod
        def get_request_queryset(self, ar):
            #~ logger.info("20130809 MyPresences")
            if ar.get_user().partner is None:
                raise Warning("Action not available for users without partner")
            return super(MyPresences, self).get_request_queryset(ar)

        @classmethod
        def get_row_permission(cls, obj, ar, state, ba):
            if ar.get_user().partner is None:
                return False
            return super(MyPresences, cls).get_row_permission(obj, ar, state, ba)

        @classmethod
        def param_defaults(self, ar, **kw):
            kw = super(MyPresences, self).param_defaults(ar, **kw)
            u = ar.get_user()
            if u is not None:
                kw.update(partner=u.partner)
            #~ kw.update(guest_state=GuestStates.invited)
            #~ kw.update(start_date=settings.SITE.today())
            return kw

        #~ @classmethod
        #~ def get_request_queryset(self,ar):
            #~ ar.master_instance = ar.get_user().partner
            #~ return super(MyPresences,self).get_request_queryset(ar)

    #~ class MyPendingInvitations(Guests):
    class MyPendingPresences(MyPresences):
        label = _("My pending invitations")
        help_text = _(
            """Received invitations which I must accept or reject.""")
        #~ filter = models.Q(state=GuestStates.invited)
        column_names = 'event__when_text role workflow_buttons remark'
        params_panel_hidden = True

        @classmethod
        def param_defaults(self, ar, **kw):
            kw = super(MyPendingPresences, self).param_defaults(ar, **kw)
            #~ kw.update(partner=ar.get_user().partner)
            #~ kw.update(user=None)
            kw.update(guest_state=GuestStates.invited)
            kw.update(start_date=settings.SITE.today())
            return kw

    class MyGuests(Guests):
        label = _("My guests")
        required = dd.required(user_groups='office')
        order_by = ['event__start_date', 'event__start_time']
        column_names = 'event__start_date event__start_time event_summary role workflow_buttons remark *'

        @classmethod
        def param_defaults(self, ar, **kw):
            kw = super(MyGuests, self).param_defaults(ar, **kw)
            kw.update(user=ar.get_user())
            kw.update(guest_state=GuestStates.invited)
            kw.update(start_date=settings.SITE.today())
            return kw


# __all__ = [
#     'Guest', 'Guests',
# ]
