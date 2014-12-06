# -*- coding: UTF-8 -*-
# Copyright 2009-2014 by Luc Saffre.
# License: BSD, see LICENSE for more details.

"""Date formatting functions
-------------------------

This module provides shortcuts to `python-babel`'s `date formatting
functions <http://babel.pocoo.org/docs/dates/>`_.

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


