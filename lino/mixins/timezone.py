# -*- coding: UTF-8 -*-
# Copyright 2015 Hamza Khchine
# License: BSD (see file COPYING for details)


import logging

logger = logging.getLogger(__name__)

import pytz

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.api import dd

from lino.core import model


class TimezoneHolder(model.Model):
    """Base class to represent a timezone field.
    """

    class Meta:
        abstract = True

    if settings.USE_TZ:
        timezone = models.CharField(_("Time zone"), max_length=15, blank=True)
    else:
        timezone = dd.DummyField()

    @dd.chooser(simple_values=True)
    def timezone_choices(cls, partner):

        if partner and partner.country:
            return pytz.country_timezones[partner.country.isocode]
        return pytz.common_timezones
