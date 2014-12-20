# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models.py` module for the :mod:`lino.modlib.rooms` app.
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

from lino import dd

contacts = dd.resolve_app('contacts', strict=True)
#~ cal = dd.resolve_app('cal',strict=True)

from lino.modlib.cal.utils import Recurrencies
from lino.modlib.cal.mixins import Reservation


class BookingStates(dd.Workflow):
    required = dd.required(user_level='admin')

add = BookingStates.add_item
add('10', _("Draft"), 'draft', editable=True)
add('20', _("Option"), 'option', editable=False)
add('30', _("Registered"), 'registered', editable=False)
add('40', _("Cancelled"), 'cancelled', editable=False)


@dd.receiver(dd.pre_analyze)
def setup_BookingStates_workflow(sender=None, **kw):

    #~ BookingStates.draft.add_transition(
        #~ states='option registered cancelled',
        #~ icon_name="pencil")
    #~ BookingStates.registered.add_transition(_("Register"),
        #~ states='draft option',
        #~ icon_name="accept")

    #~ Bookings.deregister_action.add_requirements(states='option registered cancelled')
    #~ Bookings.register_action.add_requirements(states='option draft cancelled')
    BookingStates.draft.add_transition(
        states='registered option cancelled',
        icon_name="pencil")
    BookingStates.option.add_transition(
        states='draft registered',
        icon_name="eye",
        help_text=_("Optionally booked. Ask customer before any decision."))
    BookingStates.registered.add_transition(
        states='draft option cancelled',
        icon_name="accept")
    BookingStates.cancelled.add_transition(
        states='draft option registered',
        icon_name='cross')


class Booking(contacts.ContactRelated, Reservation):

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Booking')
        verbose_name = _("Booking")
        verbose_name_plural = _('Bookings')

    #~ workflow_state_field = 'state'

    #~ required_to_register = dict(states='draft option cancelled')
    #~ required_to_deregister = dict(states='registered option cancelled')

    state = BookingStates.field(default=BookingStates.draft)

    event_type = dd.ForeignKey('cal.EventType', null=True, blank=True,
        help_text=_("""The Event Type to which events will be generated."""))

    #~ def full_clean(self,*args,**kw):
        #~ if self.every_unit is None:
            #~ self.every_unit = 1
        #~ if self.every is None:
            #~ self.every = Recurrencies.once
        #~ super(Booking,self).full_clean(*args,**kw)

    def __unicode__(self):
        return u"%s #%s (%s)" % (self._meta.verbose_name, self.pk, self.room)

    def update_cal_from(self, ar):
        return self.start_date

    def update_cal_until(self):
        return self.end_date

    def update_cal_calendar(self):
        return self.event_type

    def update_cal_summary(self, i):
        if self.every_unit == Recurrencies.once:
            return dd.babelattr(self.event_type, 'event_label')
        return "%s %s" % (dd.babelattr(self.event_type, 'event_label'), i)

    def before_auto_event_save(self, event):
        """
        Sets room and start_time for automatic events.
        This is a usage example for :meth:`EventGenerator.before_auto_event_save 
        <lino.modlib.cal.models.EventGenerator.before_auto_event_save>`.
        """
        #~ logger.info("20131008 before_auto_event_save")
        assert not settings.SITE.loading_from_dump
        assert event.owner == self
        if event.is_user_modified():
            return
        event.room = self.room
        event.start_time = self.start_time
        event.end_time = self.end_time

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super(Booking, cls).get_registrable_fields(site):
            yield f
        yield 'company'
        yield 'contact_person'
        yield 'event_type'

    # don't inherit default actions:
    #~ register_action = None
    #~ deregister_action = None

    def before_state_change(self, ar, old, new):
        if new.name == 'registered':
            if self.get_existing_auto_events().count() == 0:
                #~ ar.confirm("Booking has no events! Are you sure?")
                raise Warning("Booking has no events!")

    def after_ui_save(self, ar):
        super(Booking, self).after_ui_save(ar)
        if self.state.editable:
            self.update_reminders(ar)


dd.update_field(Booking, 'contact_person', verbose_name=_("Contact person"))
dd.update_field(Booking, 'company', verbose_name=_("Organizer"))
dd.update_field(Booking, 'every_unit', default=Recurrencies.once)
dd.update_field(Booking, 'every', default=1)


class BookingDetail(dd.FormLayout):
    #~ start = "start_date start_time"
    #~ end = "end_date end_time"
    #~ freq = "every every_unit"
    #~ start end freq
    main = "general sales.InvoicingsByInvoiceable"
    general = dd.Panel("""
    start_date start_time end_date end_time
    room event_type workflow_buttons
    max_events max_date every_unit every 
    monday tuesday wednesday thursday friday saturday sunday
    company contact_person user id:8
    cal.EventsByController
    """, label=_("General"))

    #~ def setup_handle(self,dh):
        #~ dh.start.label = _("Start")
        #~ dh.end.label = _("End")
        #~ dh.freq.label = _("Frequency")


class Bookings(dd.Table):
    model = 'rooms.Booking'
    #~ order_by = ['date','start_time']
    detail_layout = BookingDetail()
    insert_layout = """
    start_date start_time end_time
    room event_type
    company contact_person
    """
    column_names = "start_date company room  *"
    order_by = ['start_date']

    parameters = dd.ObservedPeriod(
        company=models.ForeignKey('contacts.Company', blank=True, null=True),
        state=BookingStates.field(blank=True),
    )
    params_layout = """company state"""

    simple_param_fields = 'company state'.split()

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Bookings, self).get_request_queryset(ar)
        if isinstance(qs, list):
            return qs
        for n in self.simple_param_fields:
            v = ar.param_values.get(n)
            if v:
                qs = qs.filter(**{n: v})
                #~ print 20130530, qs.query

        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Bookings, self).get_title_tags(ar):
            yield t

        for n in self.simple_param_fields:
            v = ar.param_values.get(n)
            if v:
                yield unicode(v)


class BookingsByCompany(Bookings):
    master_key = "company"


def setup_main_menu(site, ui, profile, main):
    m = main.get_item("cal")
    m.add_action(Bookings)
