# -*- coding: UTF-8 -*-
# Copyright 2012 Luc Saffre
# License: BSD (see file COPYING for details)

r"""
A :class:`Duration` is a Decimal expressed in ``hh:mm`` format.
A :class:`Percentage` is a Decimal expressed in ``x%`` format.
A :class:`Fraction` is a number expressed in ``a/b`` format.

Usage examples:

>>> parse('1')
Decimal('1')
>>> parse('1/3')
Fraction(1, 3)
>>> parse('33%')
Percentage('33%')

>>> lines = []
>>> lines.append('repr(x)              str(x)   x*3')
>>> lines.append('-------------------- ------ -----')
>>> for s in '2','2.5','5/12','1/3','33%','2:30':
...     v = parse(s)
...     lines.append("%-20s %6s %6s" % (repr(v), v, v*3))
>>> print '\n'.join(lines)
repr(x)              str(x)   x*3
-------------------- ------ -----
Decimal('2')              2      6
Decimal('2.5')          2.5    7.5
Fraction(5, 12)        5/12    5/4
Fraction(1, 3)          1/3      1
Percentage('33%')       33%   0.99
Duration('2:30')       2:30   7:30

Both period and comma are accepted as decimal separator:

>>> parse('1.5')
Decimal('1.5')
>>> parse('1,5')
Decimal('1.5')


"""

from decimal import Decimal
from fractions import Fraction

#~ from decimal import Decimal, ROUND_UP,ROUND_HALF_UP,ROUND_HALF_DOWN, getcontext
#~ getcontext().rounding = ROUND_UP


class Quantity(Decimal):

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, str(self))

    def __add__(self, *args, **kw):
        return self.__class__(Decimal.__add__(self, *args, **kw))
    __radd__ = __add__

    def __truediv__(self, *args, **kw):
        return self.__class__(Decimal.__truediv__(self, *args, **kw))
    __rtruediv__ = __truediv__
    __div__ = __truediv__
    __rdiv__ = __rtruediv__

    def __mul__(self, *args, **kw):
        return self.__class__(Decimal.__mul__(self, *args, **kw))
    __rmul__ = __mul__


DEC2HOUR = Decimal(1) / Decimal(60)


#~ class Fraction(Quantity):
    #~ def __new__(cls, value="0", context=None):
        #~ if isinstance(value,basestring) and '/' in value:
            #~ a,b = value.split('/')
            #~ a = Decimal(a)
            #~ b = Decimal(b)
            #~ self = Decimal.__new__(Fraction,a/b,context)
            #~ self._a = a
            #~ self._b = b
            #~ return self
        #~ return cls.__new__(Quantity,value,context)

    #~ def __str__(self):
        #~ return str(self._a) + '/' + str(self._b)

    #~ def simplify(self):
        #~ pass

    #~ def __mul__(self, other, context=None):
        #~ return Fraction("%s/%s" % (self._a * other,self._b))
    #~ __rmul__ = __mul__


class Percentage(Quantity):

    def __new__(cls, value="0", context=None):
        if isinstance(value, basestring) and value.endswith('%'):
            self = Decimal.__new__(
                Percentage, Decimal(value[:-1]) / 100, context)
            self._value = value
            return self
        #~ raise Exception("Invalid Percentage %r" % value)
        return cls.__new__(Quantity, value, context)

    def __str__(self):
        return self._value


class Duration(Quantity):

    """
    >>> print Duration('1')
    1:00
    >>> print Duration('2.5')
    2:30
    >>> print Duration('2.50')
    2:30
    
    >>> print Duration('1:00')
    1:00
    >>> print Duration('1:30')
    1:30
    >>> print Duration('1:55')
    1:55
    
    >>> print Duration('1:45') * 2
    3:30
    >>> print Duration('1:55') * 2
    3:50
    
    >>> print Duration('0:45') / 3
    0:15
    
    >>> print Duration('0:49') / 10
    0:05
    
    >>> print Duration('1:30') * 2
    3:00
    >>> print Duration('0:03') * 10
    0:30
    >>> print Duration('0:01') * 60
    1:00
    >>> print Duration('0:01') * 6000
    100:00
    
    >>> print Duration('1:55') + Duration('0:05')
    2:00
    >>> print Duration('1:55') + Duration('0:10')
    2:05
    
    >>> print Duration('1:55') - Duration('0:10')
    1:45
    >>> print Duration('1:05') - Duration('0:10')
    0:55
    
    
    """

    #~ _hh_mm = False

    #~ __slots__ = Decimal.__slots__ + ('_hh_mm',)
    #~ __slots__ = ('_exp','_int','_sign', '_is_special')

    def __new__(cls, value="0", context=None):
    #~ def __init__(self,value,**kw):
        if isinstance(value, basestring) and ':' in value:
            h, m = value.split(':')
            value = Decimal(h) + Decimal(m) * DEC2HOUR

        #~ self = super(Duration,cls).__new__(Duration,value,context)
        self = Decimal.__new__(Duration, value, context)
        #~ self._hh_mm = True
        return self
        #~ self = super(Duration,cls).__new__(Decimal,value,context)
        #~ self = Decimal.__new__(Decimal,value,context)
        #~ self._hh_mm = False
        #~ return self
        #~ return Decimal.__new__(value,context)
        #~ assert isinstance(value,Decimal)
        #~ self.value = value
        #~ self.format = format
        #~ for n in '__add__', '__mul__', '__sub__':
            #~ setattr(self,n,getattr(self.value,n))

    def __str__(self):
        minutes = (self - int(self)) / DEC2HOUR
        return '%d:%02d' % (
            int(self),
            minutes.to_integral())


def parse(s):
    """
    """
    if not isinstance(s, basestring):
        raise Exception("Expected a string, got %r" % s)
    if ':' in s:
        return Duration(s)
    if '/' in s:
        return Fraction(s)
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
