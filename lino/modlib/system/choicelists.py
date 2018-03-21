# -*- coding: UTF-8 -*-
# Copyright 2011-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Choicelists included with `lino.modlib.system`.

"""

from __future__ import unicode_literals
import datetime

from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from atelier.utils import isidentifier

from lino.core.choicelists import ChoiceList, Choice
from lino.utils.dates import DateRangeValue


class YesNo(ChoiceList):
    """
    A choicelist with two values "Yes" and "No".

    Used e.g. to define parameter panel fields for BooleanFields::

      foo = dd.YesNo.field(_("Foo"), blank=True)


    """
    verbose_name_plural = _("Yes or no")
    preferred_width = 12
    
add = YesNo.add_item
add('y', _("Yes"), 'yes')
add('n', _("No"), 'no')


class Genders(ChoiceList):
    """
    Defines the two possible choices "male" and "female"
    for the gender of a person.

    See :ref:`lino.tutorial.human` for examples.
    See :doc:`/dev/choicelists`.
    """

    verbose_name = _("Gender")

add = Genders.add_item
add('M', _("Male"), 'male')
add('F', _("Female"), 'female')


class ObservedEvent(Choice):
    """Base class for choices of "observed event"-style choicelists."""

    def __init__(self, value, name=None, **kwargs):
        if name is None and isidentifier(value):
            name = value
        super(ObservedEvent, self).__init__(value, name=name, **kwargs)

    def add_filter(self, qs, pv):
        """Add a filter to the given Django queryset. The given `obj` must be
        either a `datetime.date` object or must have two attributes
        `start_date` and `end_date`. The easiest way is to have it an
        instance of :class:`DateRange
        <lino.mixins.periods.DateRange>` or :class:`DateRangeValue
        <lino.utils.dates.DateRangeValue>`.

        """
        return qs


class PeriodStarted(ObservedEvent):
    # name = 'started'
    text = _("Starts")

    def add_filter(self, qs, obj):
        if isinstance(obj, datetime.date):
            obj = DateRangeValue(obj, obj)
        qs = qs.filter(start_date__isnull=False)
        if obj.start_date:
            qs = qs.filter(start_date__gte=obj.start_date)
        if obj.end_date:
            qs = qs.filter(start_date__lte=obj.end_date)
        return qs


class PeriodActive(ObservedEvent):
    # name = 'active'
    text = _("Is active")

    def add_filter(self, qs, obj):
        if isinstance(obj, datetime.date):
            obj = DateRangeValue(obj, obj)
        if obj.end_date:
            qs = qs.filter(Q(start_date__isnull=True) |
                           Q(start_date__lte=obj.end_date))
        if obj.start_date:
            qs = qs.filter(Q(end_date__isnull=True) |
                           Q(end_date__gte=obj.start_date))
        return qs


class PeriodEnded(ObservedEvent):
    # name = 'ended'
    text = _("Ends")

    def add_filter(self, qs, obj):
        if isinstance(obj, datetime.date):
            obj = DateRangeValue(obj, obj)
        qs = qs.filter(end_date__isnull=False)
        if obj.start_date:
            qs = qs.filter(end_date__gte=obj.start_date)
        if obj.end_date:
            qs = qs.filter(end_date__lte=obj.end_date)
        return qs


# class PeriodEvent(ObservedEvent):
#     """Every item of :class:`PeriodEvents` is an instance of this."""
#     def add_filter(self, qs, obj):
#         elif self.name == 'ended':


class PeriodEvents(ChoiceList):
    """The list of things you can observe on a
    :class:`lino.mixins.periods.DateRange`.

    """
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")


PeriodEvents.add_item_instance(PeriodStarted('10', 'started'))
PeriodEvents.add_item_instance(PeriodActive('20', 'active'))
PeriodEvents.add_item_instance(PeriodEnded('30', 'ended'))

# add = PeriodEvents.add_item
# add('10', _("Starts"), 'started')
# add('20', _("Is active"), 'active')
# add('30', _("Ends"), 'ended')


