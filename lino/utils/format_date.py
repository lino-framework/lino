# -*- coding: UTF-8 -*-
# Copyright 2009-2014 by Luc Saffre.
# License: BSD, see LICENSE for more details.

"""Date formatting functions
-------------------------

To run the Lino test suite on this module::

  $ python setup.py test -s tests.UtilsTests.test_format_date

This module provides shortcuts to `python-babel`'s `date formatting
functions <http://babel.pocoo.org/docs/dates/>`_.

>>> import datetime
>>> d = datetime.date(2013,8,26)
>>> print(fds(d)) # short
8/26/13
>>> print(fdm(d)) # medium
Aug 26, 2013
>>> print(fdl(d)) # long
August 26, 2013
>>> print(fdf(d)) # full
Monday, August 26, 2013
>>> print(fdmy(d)) # full
August 2013



The :func:`lino.core.dbutils.format_date` function is a thin wrapper 
to the corresponding function in `babel.dates`, 
filling the `locale` parameter according to Django's 
current language (and doing the conversion).

The major advantage over using `date_format` from `django.utils.formats` 
is that Babel offers a "full" format:

>>> today = datetime.date(2013,01,18)

>>> print(format_date(today,'full'))
Friday, January 18, 2013

>>> with translation.override('fr'):
...    print(format_date(today,'full'))
vendredi 18 janvier 2013

>>> with translation.override('de'):
...    print(format_date(today,'full'))
Freitag, 18. Januar 2013

You can use this also for languages that aren't on your site:

>>> with translation.override('et'):
...    print(format_date(today,'full'))
reede, 18. jaanuar 2013

>>> with translation.override('nl'):
...    print(format_date(today,'full'))
vrijdag 18 januari 2013


>>> print(fds('')) # empty string is tolerated
<BLANKLINE>
>>> print(fds('2014-10-12')) # not tolerated
Traceback (most recent call last):
  ...
AssertionError

"""

from __future__ import unicode_literals, print_function

import datetime
from babel.dates import format_date as babel_format_date

from django.utils import translation
from django.template import defaultfilters

from lino.core.site_def import to_locale


def monthname(n):
    """
    Return the monthname for month # n in current language.
    """
    d = datetime.date(2013, n, 1)
    return defaultfilters.date(d, 'F')


def fdmy(d):
    """
    "format date as month and year" :
    return the specified date as a localized string of type 'June 2011'."""
    if d is None:
        return ''
    return defaultfilters.date(d, 'F Y')


def format_date(d, format='medium'):
    if not d:
        return ''
    return babel_format_date(
        d, format=format, locale=to_locale(translation.get_language()))


def fdf(d):
    return format_date(d, format='full')


def fdl(d):
    return format_date(d, format='long')


def fdm(d):
    return format_date(d, format='medium')


def fds(d):
    return format_date(d, format='short')


# backwards compatibility:
dtosl = fdf
dtosm = fdm
dtos = fds
dtomy = fdmy  # backward compat


def day_and_month(d):
    return format_date(d, "dd. MMMM")


