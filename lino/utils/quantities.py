# -*- coding: UTF-8 -*-
# Copyright 2012-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

r"""
A :class:`Duration` is a Decimal expressed in ``hh:mm`` format.
A :class:`Percentage` is a Decimal expressed in ``x%`` format.

See also :doc:`/dev/quantities`.

Usage examples:

The `parse` function
====================

>>> parse('1')
Decimal('1')
>>> parse('1:15')
Duration('1:15')
>>> parse('33%')
Percentage('33%')

>>> lines = []
>>> lines.append('repr(x)              str(x)    x*3  x*100')
>>> lines.append('------------------- ------- ------ ------')
>>> for s in '2', '2.5', '33%', '2:30', '0:20':
...     v = parse(s)
...     lines.append("%-20s %6s %6s %6s" % (repr(v), v, v*3, v*100))
>>> print('\n'.join(lines))
repr(x)              str(x)    x*3  x*100
------------------- ------- ------ ------
Decimal('2')              2      6    200
Decimal('2.5')          2.5    7.5  250.0
Percentage('33%')       33%   0.99  33.00
Duration('2:30')       2:30   7:30 250:00
Duration('0:20')       0:20   1:00  33:20

Formatting
==========

>>> print(Duration("0.33334"))
0:20
>>> print(Duration("2.50"))
2:30

Decimal separator
=================

Both period and comma are accepted as decimal separator:

>>> parse('1.5')
Decimal('1.5')
>>> parse('1,5')
Decimal('1.5')

But you may not use both at the same time:

>>> parse('1,000.50')
Traceback (most recent call last):
...
Exception: Invalid decimal value '1,000.50'


"""
from __future__ import division
from builtins import str
import six
from past.utils import old_div

import datetime
from decimal import Decimal

DEC2HOUR = old_div(Decimal(1), Decimal(60))


class Quantity(Decimal):

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, str(self))

    def __add__(self, *args, **kw):
        return self.__class__(Decimal.__add__(self, *args, **kw))
    __radd__ = __add__

    def __sub__(self, *args, **kw):
        return self.__class__(Decimal.__sub__(self, *args, **kw))

    def __rsub__(self, *args, **kw):
        return self.__class__(Decimal.__rsub__(self, *args, **kw))

    def __truediv__(self, *args, **kw):
        return self.__class__(Decimal.__truediv__(self, *args, **kw))
    __rtruediv__ = __truediv__
    __div__ = __truediv__
    __rdiv__ = __rtruediv__

    def __mul__(self, *args, **kw):
        return self.__class__(Decimal.__mul__(self, *args, **kw))
    __rmul__ = __mul__


class Percentage(Quantity):

    def __new__(cls, value="0", context=None):
        if isinstance(value, six.string_types) and value.endswith('%'):
            self = Decimal.__new__(
                Percentage, old_div(Decimal(value[:-1]), 100), context)
            self._value = value
            return self
        #~ raise Exception("Invalid Percentage %r" % value)
        return cls.__new__(Quantity, value, context)

    def __str__(self):
        return self._value


class Duration(Quantity):
    """A duration, expressed in `hours:minutes`.

    >>> print(Duration('1'))
    1:00
    >>> print(Duration('2.5'))
    2:30
    >>> print (Duration('2.50'))
    2:30
    
    >>> print (Duration('1:00'))
    1:00
    >>> print (Duration('1:30'))
    1:30
    >>> print (Duration('1:55'))
    1:55
    
    >>> print (Duration('1:45') * 2)
    3:30
    >>> print (Duration('1:55') * 2)
    3:50
    
    >>> print (Duration('0:45') / 3)
    0:15
    
    >>> print (Duration('0:49') / 10)
    0:05
    
    >>> print (Duration('1:30') * 2)
    3:00
    >>> print (Duration('0:03') * 10)
    0:30
    >>> print (Duration('0:01') * 60)
    1:00
    >>> print (Duration('0:01') * 6000)
    100:00
    
    >>> print (Duration('1:55') + Duration('0:05'))
    2:00
    >>> print (Duration('1:55') + Duration('0:10'))
    2:05
    
    >>> print (Duration('1:55') - Duration('0:10'))
    1:45
    >>> print (Duration('1:05') - Duration('0:10'))
    0:55
    
    >>> print (Duration(datetime.timedelta(0)))
    0:00
    >>> print (Duration(datetime.timedelta(0, hours=10)))
    10:00
    >>> print (Duration(datetime.timedelta(0, minutes=10)))
    0:10

    A duration can be more than 24 hours, and in that case (unlike
    :class:`datetime.datetime`) it is still represented using
    `hhhh.mm`:

    >>> print (Duration(datetime.timedelta(hours=25)))
    25:00

    >>> print (Duration(datetime.timedelta(days=128)))
    3072:00

    """

    def __new__(cls, value="0", context=None):
        if isinstance(value, six.string_types):
            if ':' in value:
                h, m = value.split(':')
                value = Decimal(h) + Decimal(m) * DEC2HOUR
        elif isinstance(value, datetime.timedelta):
            hours = 0
            if value.days != 0:
                hours += value.days * 24
                value = datetime.timedelta(seconds=value.seconds)
            a = str(value).split(':')[:2]
            hours += int(a[0])
            minutes = int(a[1])
            return cls('{0}:{1}'.format(hours, minutes))
            # return cls(':'.join(a))
        self = Decimal.__new__(Duration, value, context)
        return self

    def __str__(self):
        minutes = old_div((self - int(self)), DEC2HOUR)
        return '%d:%02d' % (
            int(self),
            minutes.to_integral())


def parse(s):
    """
    """
    if not isinstance(s, six.string_types):
        raise Exception("Expected a string, got %r" % s)
    if ':' in s:
        return Duration(s)
    # if '/' in s:
    #     return Fraction(s)
    if s.endswith('%'):
        return Percentage(s)
    return parse_decimal(s)


def parse_decimal(s):
    if '.' in s and ',' in s:
        raise Exception("Invalid decimal value %r" % s)
    s = s.replace(',', '.')
    return Decimal(s)


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
