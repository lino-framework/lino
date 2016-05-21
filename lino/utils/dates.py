# Copyright 2014-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Defines classes related to date ranges.

"""

from __future__ import unicode_literals

import collections

DatePeriodValue = collections.namedtuple(
    'DatePeriodValue', ('start_date', 'end_date'))
"""
A named tuple with the following fields:

.. attribute:: start_date

    The start date

.. attribute:: end_date

    The end date
"""


