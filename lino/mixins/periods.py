# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Defines classes related to date ranges.

.. autosummary::

"""

from __future__ import unicode_literals

import datetime

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from lino.core.model import Model
from lino.utils.ranges import isrange
from lino.utils.format_date import fds
from lino.core.utils import ParameterPanel


def rangefmt(r):
    return fds(r[0]) + '...' + fds(r[1])


class DatePeriod(Model):

    """A model mixin for models which represent a period whose start and
    end are date fields.

    Designed for usage with
    :class:`lino.modlib.system.mixins.PeriodEvents`.

    """

    class Meta:
        abstract = True

    start_date = models.DateField(
        _("Start date"),
        blank=True, null=True)
    end_date = models.DateField(
        _("End date"),
        blank=True, null=True)

    def full_clean(self, *args, **kw):
        if not isrange(self.start_date, self.end_date):
            raise ValidationError(_("Date period ends before it started."))
        super(DatePeriod, self).full_clean(*args, **kw)

    def get_period(self):
        return (self.start_date, self.end_date)


class ObservedPeriod(ParameterPanel):
    """:class:`lino.core.param_panel.ParameterPanel` with two fields
    `start_date` and `end_date` which default to empty.

    """

    get_default_start_date = None
    get_default_end_date = None

    def __init__(self,
                 verbose_name_start=_("Period from"),
                 verbose_name_end=_("until"), **kw):
        kw.update(
            start_date=models.DateField(
                verbose_name_start, blank=True, null=True,
                default=self.get_default_start_date,
                help_text=_("Start date of observed period")),
            end_date=models.DateField(
                verbose_name_end,
                blank=True, null=True,
                default=self.get_default_end_date,
                help_text=_("End date of observed period")),
        )
        super(ObservedPeriod, self).__init__(**kw)


class Yearly(ObservedPeriod):

    """An :class:`ObservedPeriod` for which `start_date` defaults to Jan
    1st and `end_date` to Dec 31 of the current year.

    """

    def get_default_start_date(self):
        D = datetime.date
        return D(D.today().year, 1, 1)

    def get_default_end_date(self):
        D = datetime.date
        return D(D.today().year, 12, 31)


class Today(ParameterPanel):
    """:class:`lino.core.param_panel.ParameterPanel` with a field `today`
which defaults to today."""
    def __init__(self, verbose_name=_("Situation on"), **kw):
        kw.update(
            today=models.DateField(
                verbose_name, blank=True, null=True,
                default=settings.SITE.today,
                help_text=_("Date of observation")),
        )
        super(Today, self).__init__(**kw)


