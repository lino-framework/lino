# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Some calendar utilities

.. autosummary::


.. This is a tested document. You can test it using:

    $ python setup.py test -s tests.LibTests.test_cal_utils

..
  >>> import datetime
  >>> import os
  >>> os.environ['DJANGO_SETTINGS_MODULE'] = \\
  ...     'lino.projects.docs.settings.demo'
  >>> from lino.api.shell import *


"""

from __future__ import unicode_literals

import datetime

from dateutil.tz import tzlocal

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

from babel.dates import format_date as babel_format_date

from lino.core.site import to_locale

from lino.api import dd, rt


def format_date(d, fmt):
    """Return the given date `d` formatted using Django's current language
    combined with `Babel's date formatting
    <http://babel.edgewall.org/wiki/Documentation/dates.html>`_

    """
    return babel_format_date(
        d, fmt, locale=to_locale(translation.get_language()))


def aware(d):
    "Convert the given datetime into a timezone-aware datetime."
    return datetime.datetime(d.year, d.month, d.day, tzinfo=tzlocal())


def dt2kw(dt, name, **d):
    """Store given timestamp `dt` in a field dict.  `name` is the base
    name of the fields.

    Examples:
    
    >>> dt = datetime.datetime(2013,12,25,17,15,00)
    >>> dt2kw(dt,'foo')
    {u'foo_date': datetime.date(2013, 12, 25), u'foo_time': datetime.time(17, 15)}

    """
    if dt:
        if isinstance(dt, datetime.datetime):
            d[name + '_date'] = dt.date()
            if dt.time():
                d[name + '_time'] = dt.time()
            else:
                d[name + '_time'] = None
        elif isinstance(dt, datetime.date):
            d[name + '_date'] = dt
            d[name + '_time'] = None
        else:
            raise Exception("Invalid datetime value %r" % dt)
    else:
        d[name + '_date'] = None
        d[name + '_time'] = None
    return d


def setkw(obj, **kw):
    for k, v in kw.items():
        setattr(obj, k, v)


def when_text(d, t=None):
    """Return a string with a concise representation of the given date
    and time combination.

    Examples:

    >>> when_text(datetime.date(2013,12,25))
    u'Wed 12/25/13'
    
    >>> when_text(datetime.date(2013,12,25),datetime.time(17,15,00))
    u'Wed 12/25/13 (17:15)'
    
    >>> when_text(None)
    u''

    """
    if d is None:
        return ''
    # fmt = 'yyyy MMM dd (EE)'
    # txt = d.strftime(settings.SITE.date_format_strftime)
    txt = format_date(d, 'EE ')
    txt += dd.fds(d)
    if t is not None:
        txt += ' (%s)' % t.strftime(settings.SITE.time_format_strftime)
    return txt


class Weekdays(dd.ChoiceList):
    """A choicelist with the seven days of a week.

    .. django2rst::

            rt.show(cal.Weekdays)


    """
    verbose_name = _("Weekday")
add = Weekdays.add_item
add('1', _('Monday'), 'monday')
add('2', _('Tuesday'), 'tuesday')
add('3', _('Wednesday'), 'wednesday')
add('4', _('Thursday'), 'thursday')
add('5', _('Friday'), 'friday')
add('6', _('Saturday'), 'saturday')
add('7', _('Sunday'), 'sunday')

WORKDAYS = frozenset([
    Weekdays.get_by_name(k)
    for k in 'monday tuesday wednesday thursday friday'.split()])
"The five workdays of the week (Monday to Friday)."


class DurationUnit(dd.Choice):
    """Base class for the choices in the :class:`DurationUnits`
    choicelist.

    """

    def add_duration(unit, orig, value):
        """Return a date or datetime obtained by adding `value`
        times this `unit` to the specified value `orig`.
        Returns None is `orig` is empty.
        
        This is intended for use as a `curried magic method` of a
        specified list item:
        
        Examples:
    
        >>> start_date = datetime.date(2011, 10, 26)
        >>> DurationUnits.months.add_duration(start_date, 2)
        datetime.date(2011, 12, 26)
        
        >>> from lino.utils import i2d
        >>> start_date = i2d(20111026)
        >>> DurationUnits.months.add_duration(start_date, 2)
        datetime.date(2011, 12, 26)
        >>> DurationUnits.months.add_duration(start_date, -2)
        datetime.date(2011, 8, 26)

        >>> start_date = i2d(20110131)
        >>> DurationUnits.months.add_duration(start_date, 1)
        datetime.date(2011, 2, 28)
        >>> DurationUnits.months.add_duration(start_date, -1)
        datetime.date(2010, 12, 31)
        >>> DurationUnits.months.add_duration(start_date, -2)
        datetime.date(2010, 11, 30)

        >>> start_date = i2d(20140401)
        >>> DurationUnits.months.add_duration(start_date, 3)
        datetime.date(2014, 7, 1)
        >>> DurationUnits.years.add_duration(start_date, 1)
        datetime.date(2015, 4, 1)


        """
        if orig is None:
            return None
        if unit.value == 's':
            return orig + datetime.timedelta(seconds=value)
        if unit.value == 'm':
            return orig + datetime.timedelta(minutes=value)
        if unit.value == 'h':
            return orig + datetime.timedelta(hours=value)
        if unit.value == 'D':
            return orig + datetime.timedelta(days=value)
        if unit.value == 'W':
            return orig + datetime.timedelta(days=value * 7)
        day = orig.day
        while True:
            year = orig.year
            try:
                if unit.value == 'M':
                    m = orig.month + value
                    while m > 12:
                        m -= 12
                        year += 1
                    while m < 1:
                        m += 12
                        year -= 1
                    return orig.replace(month=m, day=day, year=year)
                if unit.value == 'Y':
                    return orig.replace(year=orig.year + value, day=day)
                raise Exception("Invalid DurationUnit %s" % unit)
            except ValueError:
                if day > 28:
                    day -= 1
                else:
                    raise


class DurationUnits(dd.ChoiceList):

    """A list of possible values for the `duration_unit` field of an
:class:`Event`.

    .. django2rst::

            rt.show(cal.DurationUnits)

    """
    verbose_name = _("Duration Unit")
    item_class = DurationUnit


add = DurationUnits.add_item
add('s', _('seconds'), 'seconds')
add('m', _('minutes'), 'minutes')
add('h', _('hours'), 'hours')
add('D', _('days'), 'days')
add('W', _('weeks'), 'weeks')
add('M', _('months'), 'months')
add('Y', _('years'), 'years')


class Recurrencies(dd.ChoiceList):

    """
    List of possible choices for a 'recurrency' field.
    """
    verbose_name = _("Recurrency")
    item_class = DurationUnit

add = Recurrencies.add_item
add('O', _('once'), 'once')
add('D', _('daily'), 'daily')
add('W', _('weekly'), 'weekly')
add('M', _('monthly'), 'monthly')
add('Y', _('yearly'), 'yearly')
add('P', _('per weekday'), 'per_weekday')  # deprecated


def amonthago():
    return DurationUnits.months.add_duration(dd.today(), -1)


class AccessClasses(dd.ChoiceList):
    verbose_name = _("Access Class")
add = AccessClasses.add_item
add('10', _('Private'), 'private')
add('20', _('Show busy'), 'show_busy')
add('30', _('Public'), 'public')


def update_auto_event(
        autotype, user, date, summary, owner, **defaults):
    return update_auto_component(
        rt.modules.cal.Event, autotype, user, date, summary, owner, **defaults)


def update_auto_task(
        autotype, user, date, summary, owner, **defaults):
    Task = rt.modules.cal.Task
    return update_auto_component(
        Task, autotype, user, date, summary, owner, **defaults)


def update_auto_component(
        model, autotype, user, date, summary, owner, **defaults):
    """
    Creates, updates or deletes the
    automatic :class:`calendar component <Component>`
    of the specified `auto_type` and `owner`.

    Specifying `None` for `date` means that
    the automatic component should be deleted.
    """
    #~ print "20120729 update_auto_component", model,autotype,user, date, settings.SITE.loading_from_dump
    #~ if SKIP_AUTO_TASKS: return
    if settings.SITE.loading_from_dump:
            #~ print "20111014 loading_from_dump"
        return None
    ot = ContentType.objects.get_for_model(owner.__class__)
    if date and date >= settings.SITE.today() + datetime.timedelta(days=-7):
        #~ defaults = owner.get_auto_task_defaults(**defaults)
        #~ print "20120729 b"
        defaults.setdefault('user', user)
        obj, created = model.objects.get_or_create(
            defaults=defaults,
            owner_id=owner.pk,
            owner_type=ot,
            auto_type=autotype)
        if not obj.is_user_modified():
            original_state = dict(obj.__dict__)
            if obj.user != user:
                obj.user = user
            summary = force_unicode(summary)
            if obj.summary != summary:
                obj.summary = summary
            if obj.start_date != date:
                obj.start_date = date
            if created or obj.__dict__ != original_state:
                #~ obj.full_clean()
                obj.save()
        return obj
    else:
        #~ print "20120729 c"
        # delete task if it exists
        try:
            obj = model.objects.get(owner_id=owner.pk,
                                    owner_type=ot, auto_type=autotype)
        except model.DoesNotExist:
            pass
        else:
            if not obj.is_user_modified():
                obj.delete()


def update_reminder(type, owner, user, orig, msg, num, unit):
    """
    Shortcut for calling :func:`update_auto_task`
    for automatic "reminder tasks".
    A reminder task is a message about something that will
    happen in the future.
    """
    update_auto_task(
        type, user,
        unit.add_duration(orig, -num),
        msg,
        owner)

