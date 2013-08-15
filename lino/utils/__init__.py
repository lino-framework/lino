# -*- coding: UTF-8 -*-
## Copyright 2009-2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""


:func:`str2hex` and :func:`hex2str`
-----------------------------------

>>> str2hex('-L')
'2d4c'

>>> hex2str('2d4c')
'-L'

>>> hex2str('')
''
>>> str2hex('')
''

:func:`join_words`
------------------

>>> print join_words('This','is','a','test')
This is a test

>>> print join_words('This','is','','another','test')
This is another test

>>> print join_words(None,None,None,'Third','test')
Third test


"""

#~ import logging
#~ logger = logging.getLogger(__name__)


import os, sys, locale, types, time
import datetime
import re
import fnmatch
from decimal import Decimal
import stat

# encapsulate where they come from:

from atelier.utils import AttrDict, iif, ispure, assert_pure, confirm
from atelier import rstgen
from atelier import sphinxconf
from atelier.utils import i2d
from atelier.utils import i2t
from north.utils import Cycler
from lino.utils.code import codefiles, codetime


def isiterable(x):
    "Returns `True` if the specified object is iterable."
    try:
        it = iter(x)
    except TypeError: 
        return False
    return True
    
    

def join_words(*words):
    """
    Remove any empty item (None or ''), call unicode on each and 
    join the remaining word using a single space.
    """
    return ' '.join([unicode(x) for x in words if x])
    
def join_elems(elems,sep=' '):
    """
    Examples::
    >>> join_elems([1,2,3])
    [1, ' ', 2, ' ', 3]
    >>> join_elems([1,2,3],' / ')
    [1, ' / ', 2, ' / ', 3]
    >>> join_elems([])
    []
    """
    if not callable(sep):
        sep_value = sep
        def sep():
            return sep_value
    l = []  
    s = None
    for e in elems:
        if s is not None:
            l.append(s)
        s = sep()
        l.append(e)
    return l
    
      

def d2iso(d):
    "Supports also dates before 1900."
    return "%04d-%02d-%02d" % (d.year, d.month, d.day)

    
def get_class_attr(cl,name):
    value = getattr(cl,name,None)
    if value is not None:
        return value
    for b in cl.__bases__:
        value = getattr(b,name,None)
        if value is not None:
            return value
            
def class_dict_items(cl,exclude=None):
    if exclude is None:
        exclude = set()
    for k,v in cl.__dict__.items(): 
        if not k in exclude:
            yield k,v
            exclude.add(k)
    for b in cl.__bases__:
        for k,v in class_dict_items(b,exclude): 
            yield k,v


def call_optional_super(cls,self,name,*args,**kw):
    """
    Doesn't work. See `20110914`.
    """
    s = super(cls,self)
    m = getattr(s,'name',None)
    if m is not None:
        return m(*args,**kw)

def call_on_bases(cls,name,*args,**kw):
    """
    Doesn't work. See `20110914`.
    This is necessary because we want to call `setup_report`
    on the model and all base classes of the model.
    We cannot use super() for this because the `setup_report` 
    method is optional.
    """
    for b in cls.__bases__: call_on_bases(b,name,*args,**kw)
    if True:
        m = getattr(cls,name,None)
        # getattr will also return the classmethod defined on a base class, 
        # which has already been called. 
        if m is not None and m.im_class is cls:
            m(cls,*args,**kw)
        
    """Note: the following algorithm worked in Python 2.7 but not in 2.6,
    a classmethod object in 2.6 has no attribute `im_func`
    """
      
    #~ m = cls.__dict__.get(name)
    #~ if m:
        #~ func = getattr(m,'im_func',None)
        #~ if func is None:
            #~ raise Exception("Oops, %r in %s (%r) has no im_func" % (name,cls,m))
        #~ func(cls,*args,**kw)
        #~ # m.__func__(cls,*args,**kw)




def str2hex(s):
    """Convert a string to its hexadecimal representation."""
    r = ''
    for c in s:
        r += hex(ord(c))[2:]
    return r
    
def hex2str(value):
    """Convert the hexadecimal representation of a string to the original string."""
    if len(value) % 2 != 0:
        raise Exception("hex2str got value %r" % value)
    r = ''
    for i in range(len(value) / 2):
       s = value[i*2:i*2+2]
       h = int(s,16)
       r += chr(h)
    return r
    
# http://snippets.dzone.com/posts/show/2375
curry = lambda func, *args, **kw:\
            lambda *p, **n:\
                 func(*args + p, **dict(kw.items() + n.items()))
                 
    

    
class IncompleteDate:
    """
    Naive representation of a potentially incomplete gregorian date.
    
    Once upon a time in the year 2011:
    >>> print IncompleteDate(2011,0,0).strftime("%d.%m.%Y")
    00.00.2011
    
    >>> print IncompleteDate(1532,0,0)
    1532-00-00
    >>> print IncompleteDate(1990,0,1)
    1990-00-01
    >>> print IncompleteDate(0,6,1)
    0000-06-01
    
    W.A. Mozart's birth date:
    
    >>> print IncompleteDate(1756,1,27)
    1756-01-27
    
    Christ's birth date:
    
    >>> print IncompleteDate(-7,12,25)
    -7-12-25
    >>> print IncompleteDate(-7,12,25).strftime("%d.%m.%Y")
    25.12.-7
    
    Note that you cannot convert all incomplete dates 
    to real datetime.date objects:
    
    >>> IncompleteDate(-7,12,25).as_date() 
    Traceback (most recent call last):
    ...
    ValueError: year is out of range
    
    >>> IncompleteDate(1756,1,27).as_date()
    datetime.date(1756, 1, 27)
    
    An IncompleteDate is allowed to be complete:
    
    >>> d = IncompleteDate.parse('2011-11-19')
    >>> print d
    2011-11-19
    >>> d.is_complete()
    True
    >>> print repr(d.as_date())
    datetime.date(2011, 11, 19)
    
    """
    
    def __init__(self,year,month,day):
        self.year, self.month, self.day = year, month, day
        
    @classmethod
    def parse(cls,s):
        if s.startswith('-'):
            bc = True
            s = s[1:]
        else:
            bc = False
        y,m,d = map(int,s.split('-'))
        if bc: y = - y
        return cls(y,m,d)
        
    @classmethod
    def from_date(cls,date):
        return cls(date.year,date.month,date.day)
        
    def is_complete(self):
        if self.year and self.month and self.day:
            return True
        return False
        
    def __eq__(self,other):
        return str(self) == str(other)
        
    def __ne__(self,other):
        return str(self) != str(other)

    def __len__(self):
        return len(str(self))
        
    def __repr__(self):
        return "IncompleteDate(%r)" % str(self)
        
    def __str__(self):
        return self.strftime()
        
    def strftime(self,fmt="%Y-%m-%d"):
        #~ s = fmt.replace("%Y",iif(self.bc,'-','')+str(self.year))
        if self.year == 0:
            s = fmt.replace("%Y",'0000')
        else:
            s = fmt.replace("%Y",str(self.year))
        s = s.replace("%m","%02d" % self.month)
        s = s.replace("%d","%02d" % self.day)
        return s
        
        #~ return self.strftime_(fmt,
            #~ iif(self.bc,-1,1)*self.year,
            #~ self.month,
            #~ self.day)
        
    def as_date(self):
        return datetime.date(
            #~ (self.year * iif(self.bc,-1,1)) or 1900, 
            self.year or 1900, 
            self.month or 1, 
            self.day or 1)


#~ class Warning(Exception): 
    #~ """
    #~ An Exception whose message is meant to be 
    #~ understandable by the user.
    #~ """
    
# unmodified copy from http://docs.python.org/library/decimal.html#recipes
def moneyfmt(value, places=2, curr='', sep=',', dp='.',
             pos='', neg='-', trailneg=''):
    """
    Convert Decimal to a money formatted string.

    | places:   required number of places after the decimal point
    | curr:     optional currency symbol before the sign (may be blank)
    | sep:      optional grouping separator (comma, period, space, or blank)
    | dp:       decimal point indicator (comma or period)
    |           only specify as blank when places is zero
    | pos:      optional sign for positive numbers: '+', space or blank
    | neg:      optional sign for negative numbers: '-', '(', space or blank
    | trailneg: optional trailing minus indicator:  '-', ')', space or blank

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.89'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<0.02>'

    """
    q = Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = map(str, digits)
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))
    
    
def unicode_string(x):
    """
    When we want unicode strings (e.g. translated exception messages) 
    to appear in an Exception, 
    we must first encode them using a non-strict errorhandler.
    Because the message of an Exception may not be a unicode string.
    
    """
    return unicode(x).encode(sys.getdefaultencoding(),'backslashreplace')
    # Python 2.6.6 said "Error in formatting: encode() takes no keyword arguments"
    #~ return unicode(x).encode(errors='backslashreplace')
    
    
ONE_DAY = datetime.timedelta(days=1)

def workdays(start,end):
    """
    Return the number of workdays (Monday to Friday) between the given 
    two dates. Is not aware of holidays. 
    
    Both dates start and end are included. For example if you 
    specify a Monday as start and Monday of the following 
    week as end, then you get 6 (not 5).
    
    Examples:
    >>> examples = [
    ...   (20121130,20121201,1),
    ...   (20121130,20121224,17),
    ...   (20121130,20121130,1),
    ...   (20121201,20121201,0),
    ...   (20121201,20121202,0),
    ...   (20121201,20121203,1),
    ...   (20121130,20121207,6),
    ... ]
    >>> for start,end,expected in examples:
    ...     a = i2d(start)
    ...     b = i2d(end)
    ...     if workdays(a,b) != expected:
    ...        print "Got %d instead of %d for (%s,%s)" % (workdays(a,b),expected,a,b)
    
    """
    #~ for d in range(start,end,ONE_DAY):
        #~ if d.isoweekday() <= 5:
            #~ n += 1
    n = 0
    d = start
    while d <= end:
        if d.isoweekday() <= 5:
            n += 1
        d += ONE_DAY
    return n
    
    

UNCAMEL_RE = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')      


def uncamel(s):
    """
    
    Thanks to `nickl <http://stackoverflow.com/users/1522117/nickl>`_
    in `Stackoverflow  <http://stackoverflow.com/questions/1175208>`_
    
    >>> from lino.utils import uncamel 
    >>> uncamel('EventsByClient')
    'events_by_client'
    >>> uncamel('Events')
    'events'
    >>> uncamel('HTTPResponseCodeXYZ')
    'http_response_code_xyz'
    
    """
    return UNCAMEL_RE.sub(r'_\1', s).lower()
    


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

