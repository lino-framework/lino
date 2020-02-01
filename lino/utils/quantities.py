# -*- coding: UTF-8 -*-
# Copyright 2012-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""See :doc:`/dev/quantities`."""

from past.utils import old_div

import datetime
from decimal import Decimal

DEC2HOUR = old_div(Decimal(1), Decimal(60))

class Quantity(Decimal):

    def __new__(cls, *args, **kwargs):
        raise Exception("You cannot instantiate the Quantity base class.")

    def __str__(self):
        # return "{}%".format(self * 100)
        return self._text

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, self)

    def __add__(self, other, **kwargs):
        other = convert_from(other, **kwargs)
        return self.__class__(Decimal.__add__(self, other, **kwargs))
    __radd__ = __add__

    def __sub__(self, *args, **kw):
        return self.__class__(Decimal.__sub__(self, *args, **kw))

    def __rsub__(self, *args, **kw):
        return self.__class__(Decimal.__rsub__(self, *args, **kw))

    def __mul__(self, other, **kwargs):
        other = convert_from(other, **kwargs)
        return self.__class__(Decimal.__mul__(self, other, **kwargs))

    def __rmul__(self, other, **kwargs):
        other = convert_from(other, **kwargs)
        return self.__class__(Decimal.__rmul__(self, other, **kwargs))
        # return Decimal.__rmul__(self, other, **kwargs)
        # see Luc's blog 20190410

    def __truediv__(self, *args, **kw):
        return self.__class__(Decimal.__truediv__(self, *args, **kw))
    __rtruediv__ = __truediv__
    __div__ = __truediv__
    __rdiv__ = __rtruediv__

    def deconstruct(self):
        return (self.__module__ + "." + self.__class__.__name__, (self._text,), {})


class Percentage(Quantity):

    def __new__(cls, value="0%", context=None):
        if value is NotImplemented:
            return value
        if isinstance(value, str):
            text = value
            if text[-1] != "%":
                text += "%"
            cv = Decimal(text[:-1]) / Decimal(100)
        else:
            cv = value
            text = str(value * 100) + "%"
        self = Decimal.__new__(cls, cv, context)
        self._text = text
        return self

    # def __str__(self):
    #     return "{}%".format(self * 100)
    #     # return str(self._value)

    def __rmul__(self, other, **kwargs):
        other = convert_from(other, **kwargs)
        # return self.__class__(Decimal.__rmul__(self, other, **kwargs))
        return Decimal.__rmul__(self, other, **kwargs)
        # see Luc's blog 20190410



class Duration(Quantity):

    def __new__(cls, value="0:00", context=None):
        if isinstance(value, datetime.timedelta):
            hours = 0
            if value.days != 0:
                hours += value.days * 24
                value = datetime.timedelta(seconds=value.seconds)
            a = str(value).split(':')[:2]
            hours += int(a[0])
            minutes = int(a[1])
            cv = Decimal(hours) + Decimal(minutes) * DEC2HOUR
            text = '%d:%02d' % (hours, minutes)
        else:
            text = str(value)
            if ':' in text:
                try:
                    h, m = text.split(':')
                except ValueError:
                    raise ValueError("Cannot convert %r to Duration" % value)
                cv = Decimal(h) + Decimal(m) * DEC2HOUR
            else:
                cv = Decimal(value)
                hours = int(cv)
                minutes = old_div((cv - hours), DEC2HOUR).to_integral()
                # minutes = old_div((hours - int(self)), DEC2HOUR)
                text = '%d:%02d' % (hours, minutes)
        self = Decimal.__new__(cls, cv, context)
        self._text = text
        return self

    # def __str__(self):
    #     minutes = old_div((self - int(self)), DEC2HOUR)
    #     return '%d:%02d' % (
    #         int(self),
    #         minutes.to_integral())

    def __radd__(self, other, **kwargs):
        # add a Duration to a datetime.datetime
        if isinstance(other, datetime.datetime):
            return other + self.as_timedelta()
        other = convert_from(other, **kwargs)
        return self.__class__(Decimal.__radd__(self, other, **kwargs))

    def __rsub__(self, other, **kwargs):
        # subtract a Duration from a datetime.datatime
        if isinstance(other, datetime.datetime):
            return other - self.as_timedelta()
        other = convert_from(other, **kwargs)
        return self.__class__(Decimal.__rsub__(self, other, **kwargs))

    def as_timedelta(self):
        h, m = self._text.split(':')
        return datetime.timedelta(seconds=int(h)*60*60 + int(m)*60)


def convert_from(value, context=None):
    if isinstance(value, str):
        return parse(value)
    if isinstance(value, datetime.timedelta):
        return Duration(value)
    return value


def parse(s):
    if s.endswith('%'):
        return Percentage(s)
        # self = Decimal.__new__(
        #     Percentage, old_div(Decimal(s[:-1]), 100), context)
        # return self
    if ':' in s:
        return Duration(s)
    # if not isinstance(s, six.string_types):
    #     raise Exception("Expected a string, got %r" % s)
    # if ':' in s:
    #     return Duration(s)
    # if '/' in s:
    #     return Fraction(s)
    # if s.endswith('%'):
    #     return Percentage(s)
    return parse_decimal(s)


def parse_decimal(s):
    if '.' in s and ',' in s:
        raise Exception("Invalid decimal value %r" % s)
    s = s.replace(',', '.')
    return Decimal(s)


ZERO_DURATION = Duration('0:00')
