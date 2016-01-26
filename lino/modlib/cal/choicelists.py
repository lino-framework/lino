# -*- coding: UTF-8 -*-
# Copyright 2011-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Choicelists for lino.modlib.cal


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
from dateutil.easter import easter

from lino.api import dd, _


class Weekdays(dd.ChoiceList):
    """A choicelist with the seven days of a week.

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
                if unit.value == 'E':
                    offset = orig - easter(year)
                    return easter(year+value) + offset
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
    """List of possible choices for a 'recurrency' field.

    Note that a recurrency (an item of this choicelist) is also a
    :class:`DurationUnit`.

    .. attribute:: easter

        Repeat events yearly, moving them together with the Easter
        data of that year.

        Lino computes the offset (number of days) between this rule's
        :attr:`start_date` and the Easter date of that year, and
        generates subsequent events so that this offset remains the
        same.

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
add('E', _('Relative to Easter'), 'easter')


def amonthago():
    return DurationUnits.months.add_duration(dd.today(), -1)


class AccessClasses(dd.ChoiceList):
    verbose_name = _("Access Class")
add = AccessClasses.add_item
add('10', _('Private'), 'private')
add('20', _('Show busy'), 'show_busy')
add('30', _('Public'), 'public')


