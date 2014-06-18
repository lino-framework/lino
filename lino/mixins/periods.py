# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.core.choicelists import Choice, ChoiceList
from lino.core.model import Model
from lino.utils.ranges import isrange

from atelier.utils import AttrDict


class PeriodEvent(Choice):
    
    def add_filter(self, qs, obj):

        if isinstance(obj, datetime.date):
            obj = AttrDict(start_date=obj, end_date=obj)
            
        if obj.start_date is None or obj.end_date is None:
            return qs

        if self.name == 'started':
            qs = qs.filter(start_date__gte=obj.start_date)
            qs = qs.filter(start_date__lte=obj.end_date)
        elif self.name == 'ended':
            qs = qs.filter(end_date__isnull=False)
            qs = qs.filter(end_date__gte=obj.start_date)
            qs = qs.filter(end_date__lte=obj.end_date)
        elif self.name == 'active':
            qs = qs.filter(start_date__lte=obj.end_date)
            qs = qs.filter(models.Q(end_date__isnull=True) |
                           models.Q(end_date__gte=obj.start_date))
        return qs
        
        
class PeriodEvents(ChoiceList):
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")
    item_class = PeriodEvent


add = PeriodEvents.add_item
add('10', _("Started"), 'started')
add('20', _("Active"), 'active')
add('30', _("Ended"), 'ended')


class DatePeriod(Model):

    "A period whose start and end are date fields."

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


