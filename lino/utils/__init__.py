# -*- coding: UTF-8 -*-
# Copyright 2009-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

""":mod:`lino.utils` (the top-level module) contains a few often-used
function for general use. It has also many subpackages and submodules.

.. autosummary::
   :toctree:

    addressable
    ajax
    choosers
    code
    config
    dates
    demonames
    daemoncommand
    dataserializer
    dbfreader
    dblogger
    diag
    djangotest
    dpy
    html2odf
    html2xhtml
    mytidylib
    instantiator
    jinja
    jscompressor
    jsgen
    latex
    log
    mdbtools
    media
    mldbc
    mti
    odsreader
    pdf
    pythontest
    pyuca
    quantities
    ranges
    requests
    restify
    screenshots
    sendchanges
    sqllog
    ssin
    test
    textfields
    ucsv
    report


"""

#~ import logging
#~ logger = logging.getLogger(__name__)
from past.utils import old_div
from future.types import newstr
import sys
import datetime
from dateutil.relativedelta import relativedelta
import re
from decimal import Decimal
from collections import OrderedDict
# import locale
import dateparser

# import rstgen
from etgen.utils import join_elems

from lino.utils.cycler import Cycler
from lino.utils.code import codefiles, codetime

from rstgen.utils import confirm, i2d, i2t


class AttrDict(dict):

    """
    Dictionary-like helper object.

    Usage example:

    >>> from lino.utils import AttrDict
    >>> a = AttrDict()
    >>> a.define('foo', 1)
    >>> a.define('bar', 'baz', 2)
    >>> a == {"bar": {"baz": 2}, "foo": 1}
    True
    >>> print(a.foo)
    1
    >>> print(a.bar.baz)
    2
    >>> print(a.resolve('bar.baz'))
    2
    >>> print(a.bar)
    {'baz': 2}

    """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(
                "AttrDict instance has no key '%s' (keys are %s)" % (
                    name, ', '.join(list(self.keys()))))

    def define2(self, name, value):
        return self.define(*name.split('.') + [value])

    def define(self, *args):
        "args must be a series of names followed by the value"
        assert len(args) >= 2
        d = s = self
        for n in args[:-2]:
            d = s.get(n, None)
            if d is None:
                d = AttrDict()
                s[n] = d
            s = d
        oldvalue = d.get(args[-2], None)
        d[args[-2]] = args[-1]
        return oldvalue

    def resolve(self, name, default=None):
        """
        return an attribute with dotted name
        """
        o = self
        for part in name.split('.'):
            o = getattr(o, part, default)
            # o = o.__getattr__(part)
        return o


def date_offset(ref, days=0, **offset):
    """
    Compute a date using a "reference date" and an offset.

    >>> r = i2d(20140222)

    In 10 days:
    >>> date_offset(r, 10)
    datetime.date(2014, 3, 4)

    Four hundred days ago:
    >>> date_offset(r, -400)
    datetime.date(2013, 1, 18)


    """
    if days:
        offset.update(days=days)
    if offset:
        return ref + datetime.timedelta(**offset)
    return ref

def iif(condition, true_value, false_value=None):
    """
    "Inline If" : an ``if`` statement as a function.

    Examples:

    >>> from lino.utils import iif
    >>> print("Hello, %s world!" % iif(1+1==2, "real", "imaginary"))
    Hello, real world!
    >>> iif(True, "true")
    'true'
    >>> iif(False, "true")

    """
    if condition:
        return true_value
    return false_value


def last_day_of_month(d):
    """Return the last day of the month of the given date.

    >>> from lino.utils import i2d
    >>> last_day_of_month(i2d(20160212))
    datetime.date(2016, 2, 29)
    >>> last_day_of_month(i2d(20161201))
    datetime.date(2016, 12, 31)
    >>> last_day_of_month(i2d(20160123))
    datetime.date(2016, 1, 31)
    >>> last_day_of_month(i2d(20161123))
    datetime.date(2016, 11, 30)

    Thanks to `stackoverflow.com
    <http://stackoverflow.com/questions/42950/get-last-day-of-the-month-in-python>`_.

    """
    return d + relativedelta(day=31)
    # d = datetime.date(d.year, d.month + 1, 1)
    # return relativedelta(d, days=-1)


def isiterable(x):
    "Returns `True` if the specified object is iterable."
    try:
        iter(x)
    except TypeError:
        return False
    return True

def is_string(s):
    """Return True if the specified value is a string.
    """
    # if six.PY2:
    #     return isinstance(s, six.string_types) or isinstance(s, newstr)
    return isinstance(s, str)

def isidentifier(s):
    """
    Check whether the given string can be used as a Python identifier.
    """
    # if six.PY2:
    #     return re.match("[_A-Za-z][_a-zA-Z0-9]*$", s)
    return s.isidentifier()


def ispure(s):
    """Returns `True` if the specified string `s` is either None, or
    contains only ASCII characters, or is a validly encoded unicode
    string.

    """
    if s is None:
        return True
    if isinstance(s, (str, newstr)):
        return True
    if type(s) == bytes:
        try:
            s.decode('ascii')
        except UnicodeDecodeError:
            return False
        return True
    return False


def assert_pure(s):
    """
    raise an Exception if the given string is not :func:`ispure`.
    """
    #~ assert ispure(s), "%r: not pure" % s
    if s is None:
        return
    if isinstance(s, str):
        return True
    try:
        s.decode('ascii')
    except UnicodeDecodeError as e:
        raise Exception("%r is not pure : %s" % (s, e))

def join_words(*words):
    """
    Remove any empty item (None or ''), call unicode on each and
    join the remaining word using a single space.

    TODO: move this to etgen.html ?

    >>> print(join_words('This','is','a','test'))
    This is a test

    >>> print(join_words('This','is','','another','test'))
    This is another test

    >>> print(join_words(None, None, None, 'Third', 'test'))
    Third test

    """
    return ' '.join([str(x) for x in words if x])


def d2iso(d):
    "Supports also dates before 1900."
    return "%04d-%02d-%02d" % (d.year, d.month, d.day)


def get_class_attr(cl, name):
    value = getattr(cl, name, None)
    if value is not None:
        return value
    for b in cl.__bases__:
        value = getattr(b, name, None)
        if value is not None:
            return value


def call_optional_super(cls, self, name, *args, **kw):
    """
    Doesn't work. See `20110914`.
    """
    s = super(cls, self)
    m = getattr(s, 'name', None)
    if m is not None:
        return m(*args, **kw)


def call_on_bases(cls, name, *args, **kw):
    """
    Doesn't work. See `20110914`.
    This is necessary because we want to call `setup_report`
    on the model and all base classes of the model.
    We cannot use super() for this because the `setup_report`
    method is optional.
    """
    for b in cls.__bases__:
        call_on_bases(b, name, *args, **kw)
    if True:
        m = getattr(cls, name, None)
        # getattr will also return the classmethod defined on a base class,
        # which has already been called.
        if m is not None and m.__self__.__class__ is cls:
            m(cls, *args, **kw)

    """Note: the following algorithm worked in Python 2.7 but not in 2.6,
    a classmethod object in 2.6 has no attribute `im_func`
    """

    #~ m = cls.__dict__.get(name)
    #~ if m:
        #~ func = getattr(m,'im_func',None)
        #~ if func is None:
            #~ raise Exception("Oops, %r in %s (%r) has no im_func" % (name,cls,m))
        #~ func(cls,*args,**kw)
        # ~ # m.__func__(cls,*args,**kw)


def str2hex(s):
    """
    Convert a string to its hexadecimal representation.

    See examples in :func:`hex2str`.


    """
    r = ''
    for c in s:
        r += hex(ord(c))[2:]
    return r


def hex2str(value):
    """
    Convert the hexadecimal representation of a string to the original
    string.

    See also :func:`str2hex`.

    >>> str2hex('-L')
    '2d4c'

    >>> hex2str('2d4c')
    '-L'

    >>> hex2str('')
    ''
    >>> str2hex('')
    ''


    """
    if len(value) % 2 != 0:
        raise Exception("hex2str got value %r" % value)
    r = ''
    for i in range(old_div(len(value), 2)):
        s = value[i * 2:i * 2 + 2]
        h = int(s, 16)
        r += chr(h)
    return r

# http://snippets.dzone.com/posts/show/2375
curry = lambda func, *args, **kw:\
    lambda *p, **n:\
    func(*args + p, **dict(list(kw.items()) + list(n.items())))


class IncompleteDate(object):

    """
    Naive representation of a potentially incomplete gregorian date.

    For example you can say "Once upon a time in the year 2011":

    >>> print(IncompleteDate(2011, 0, 0).strftime("%d.%m.%Y"))
    00.00.2011

    Unlike :class:`datetime.date` objects an incomplete date can hold years
    before 1970.

    >>> print(IncompleteDate(1532, 0, 0))
    1532-00-00

    On June 1st (but we don't say the year):

    >>> print(IncompleteDate(0, 6, 1))
    0000-06-01

    On the first day of the month in 1990:

    >>> print(IncompleteDate(1990, 0, 1))
    1990-00-01

    W.A. Mozart's birth date:

    >>> print(IncompleteDate(1756, 1, 27))
    1756-01-27

    Christ's birth date:

    >>> print(IncompleteDate(-7, 12, 25))
    -7-12-25
    >>> print(IncompleteDate(-7, 12, 25).strftime("%d.%m.%Y"))
    25.12.-7

    Note that you cannot convert all incomplete dates
    to real datetime.date objects:

    >>> IncompleteDate(-7, 12, 25).as_date()
    ... #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: year...is out of range

    >>> IncompleteDate(1756, 1, 27).as_date()
    datetime.date(1756, 1, 27)

    An IncompleteDate is allowed to be complete:

    >>> d = IncompleteDate.parse('2011-11-19')
    >>> print(d)
    2011-11-19
    >>> d.is_complete()
    True
    >>> print(repr(d.as_date()))
    datetime.date(2011, 11, 19)

    >>> d = IncompleteDate.parse('2008-03-24')
    >>> d.get_age(i2d(20131224))
    5
    >>> d.get_age(i2d(20140323))
    5
    >>> d.get_age(i2d(20140324))
    6
    >>> d.get_age(i2d(20140325))
    6
    >>> d.get_age(i2d(20141025))
    6

    Note that IncompleteDate can store invalid dates:

    >>> d = IncompleteDate(2009, 2, 30)
    >>> d.get_age(i2d(20160202))
    6

    >>> IncompleteDate(2009, 2, 32)
    IncompleteDate('2009-02-32')

    >>> IncompleteDate(2009, 32, 123)
    IncompleteDate('2009-32-123')

    """

    def __init__(self, year, month, day):
        self.year, self.month, self.day = year, month, day

    @classmethod
    def parse(cls, s):
        """
        Parse the given string and return an :class:`IncompleteDate`
        object.

        >>> IncompleteDate.parse('2008-03-24')
        IncompleteDate('2008-03-24')

        Belgian eID cards gave us some special challenges:

        >>> IncompleteDate.parse('01.JUN. 1968')
        IncompleteDate('1968-06-01')

        >>> IncompleteDate.parse('JUN. 1968')
        IncompleteDate('1968-06-00')
        """

        if s.startswith('-'):
            bc = True
            s = s[1:]
        else:
            bc = False
        try:
            y, m, d = list(map(int, s.split('-')))
        except ValueError:
            pd = dateparser.parse(
                s, settings={'STRICT_PARSING': True})
            if pd is None:
                pd = dateparser.parse(
                    s, settings={'PREFER_DAY_OF_MONTH': 'first'})
                y, m, d = pd.year, pd.month, 0
            else:
                y, m, d = pd.year, pd.month, pd.day
            # raise Exception("Invalid date value {}".format(s))
        if bc:
            y = - y
        return cls(y, m, d)

    @classmethod
    def from_date(cls, date):
        return cls(date.year, date.month, date.day)

    def is_complete(self):
        if self.year and self.month and self.day:
            return True
        return False

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return str(self) != str(other)

    def __len__(self):
        return len(str(self))

    def __repr__(self):
        return "IncompleteDate(%r)" % str(self)

    def __str__(self):
        return self.strftime()

    def strftime(self, fmt="%Y-%m-%d"):
        #~ s = fmt.replace("%Y",iif(self.bc,'-','')+str(self.year))
        if self.year == 0:
            s = fmt.replace("%Y", '0000')
        else:  # year might be negative
            s = fmt.replace("%Y", str(self.year))
        s = s.replace("%m", "%02d" % self.month)
        s = s.replace("%d", "%02d" % self.day)
        return s

    def as_date(self):
        return datetime.date(
            self.year or 1900,
            self.month or 6,
            self.day or 15)

    def get_age(self, today):
        "Return age in years as integer."
        a = (self.month, self.day)
        b = (today.month, today.day)
        if a > b:
            return today.year - self.year - 1
        return today.year - self.year


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
    >>> print(moneyfmt(d, curr='$'))
    -$1,234,567.89
    >>> print(moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-'))
    1.234.568-
    >>> print(moneyfmt(d, curr='$', neg='(', trailneg=')'))
    ($1,234,567.89)
    >>> print(moneyfmt(Decimal(123456789), sep=' '))
    123 456 789.00
    >>> print(moneyfmt(Decimal('-0.02'), neg='<', trailneg='>'))
    <0.02>

    """
    q = Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = list(map(str, digits))
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
    return str(x).encode(sys.getdefaultencoding(), 'backslashreplace')
    # Python 2.6.6 said "Error in formatting: encode() takes no keyword arguments"
    #~ return unicode(x).encode(errors='backslashreplace')


ONE_DAY = datetime.timedelta(days=1)
ONE_WEEK = datetime.timedelta(days=7)


def workdays(start, end):
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
    ...        print("Got %d instead of %d for (%s,%s)" % (workdays(a,b),expected,a,b))

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


def camelize(s):
    """
    >>> camelize("ABC DEF")
    'Abc Def'
    >>> camelize("ABC def")
    'Abc def'
    >>> camelize("eID")
    'eID'

    """
    def f(k):
        if k.upper() != k:
            return k
        return k[0].upper() + k[1:].lower()
    return ' '.join([f(k) for k in s.split()])


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


def puts(s):
    """A simplistic replacement for the `puts` function of `clint` which
    has the problem of not supporting
    `unicode strings <https://github.com/kennethreitz/clint/issues/48>`__.

    This method is meant for issuing to the interactive console
    messages which do not need to be logged because they just give
    information about what's going on.

    Currently this just prints the string to stdout using ``print``. I
    prefer to use this over a plain ``print`` statement because I
    guess that there will be problems (mainly thinking about the fact
    that writing to stdout is considered an error in a wsgi
    application).

    """
    # if isinstance(s, unicode):
    #     print s.encode(locale.getpreferredencoding())
    print(s)


class SumCollector(object):
    """A dictionary of sums to be collected using an arbitrary key.

    Usage examples:

    >>> sc = SumCollector()
    >>> sc.collect("a", 12)
    >>> sc.collect("a", None)
    >>> sc.collect("a", 5)
    >>> sc.a
    17

    >>> sc = SumCollector()
    >>> sc.collect("a", 12)
    >>> sc.collect("b", 23)
    >>> sc.collect("a", 34)
    >>> sc
    OrderedDict([('a', 46), ('b', 23)])

    >>> sc = SumCollector()
    >>> from lino.utils.quantities import Duration
    >>> sc.collect("a", Duration("0:30"))
    >>> sc.collect("a", Duration("0:35"))
    >>> sc.collect("b", Duration("0:00"))
    >>> sc.a
    Duration('1:05')
    >>> sc.b
    Duration('0:00')

    This is also included in the default context used by the Jinja
    renderer (:mod:`lino.modlib.jinja`) when rendering templates,
    which makes it a more complete solution for a problem asked also
    elsewhere, e.g. on `Stackoverflow
    <http://stackoverflow.com/questions/7537439/how-to-increment-a-variable-on-a-for-loop-in-jinja-template>`__.

    """
    def __init__(self):
        self._sums = OrderedDict()

    def collect(self, k, value):
        """Add the given value to the sum at the given key k."""
        if value is None:
            return
        if k in self._sums:
            self._sums[k] += value
        else:
            self._sums[k] = value

    def __getattr__(self, k):
        return self._sums.get(k)

    def items(self, *args, **kwargs):
        return self._sums.items(*args, **kwargs)

    def __str__(self):
        return str(self._sums)

    def __repr__(self):
        return repr(self._sums)


class SimpleSingleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance




def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
