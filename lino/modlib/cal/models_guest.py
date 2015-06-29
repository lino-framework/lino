# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Part of the :xfile:`models.py` module for `lino.modlib.cal`.

Defines the :class:`Guest` model and its tables.
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.db import models

from lino import mixins
from lino.api import dd, _
from lino.modlib.office.roles import OfficeUser

from .workflows import GuestStates
from .workflows import EventStates


class GuestRole(mixins.BabelNamed):
    templates_group = 'cal/Guest'

    class Meta:
        verbose_name = _("Guest Role")
        verbose_name_plural = _("Guest Roles")


class GuestRoles(dd.Table):
    help_text = _("The role of a guest expresses what the "
                  "partner is going to do there.")
    model = GuestRole
    required_roles = dd.required(dd.SiteStaff, OfficeUser)
    detail_layout = """
    id name
    #build_method #template #email_template #attach_to_email
    cal.GuestsByRole
    """


class Guest(dd.Model):
    """Represents the fact that a given person is expected to attend to a
   given event.

   TODO: Rename this to "Presence".

    """
    workflow_state_field = 'state'

    allow_cascaded_delete = ['event']

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Guest')
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")

    event = models.ForeignKey('cal.Event')

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


class Guests(dd.Table):
    "The default table for :class:`Guest`."
    help_text = _("""A guest is a partner invited to an event. """)
    model = 'cal.Guest'
    required_roles = dd.required(dd.SiteStaff, OfficeUser)
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

    parameters = mixins.ObservedPeriod(
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
    required_roles = dd.required(OfficeUser)
    auto_fit_column_widths = True
    column_names = 'partner role workflow_buttons'


class GuestsByRole(Guests):
    master_key = 'role'
    required_roles = dd.required(OfficeUser)

if settings.SITE.is_installed('contacts'):

    class GuestsByPartner(Guests):
        label = _("Presences")
        master_key = 'partner'
        required_roles = dd.required(OfficeUser)
        column_names = 'event__when_text workflow_buttons'
        auto_fit_column_widths = True

    class MyPresences(Guests):
        required_roles = dd.required(OfficeUser)
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
        required_roles = dd.required(OfficeUser)
        order_by = ['event__start_date', 'event__start_time']
        column_names = 'event__start_date event__start_time event_summary role workflow_buttons remark *'

        @classmethod
        def param_defaults(self, ar, **kw):
            kw = super(MyGuests, self).param_defaults(ar, **kw)
            kw.update(user=ar.get_user())
            kw.update(guest_state=GuestStates.invited)
            kw.update(start_date=settings.SITE.today())
            return kw


