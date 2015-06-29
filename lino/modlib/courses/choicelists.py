# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals
from __future__ import print_function

"""
Choicelists for :mod:`lino.modlib.courses`.

"""

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd


class CourseStates(dd.Workflow):
    required_roles = dd.required(dd.SiteAdmin)

add = CourseStates.add_item
add('10', _("Draft"), 'draft', editable=True)
add('20', _("Registered"), 'registered', editable=False)
# add('30', _("Started"), 'started', editable=False)
# add('40', _("Ended"), 'ended', editable=False)
# add('50', _("Cancelled"), 'cancelled', editable=True)

# #~ ACTIVE_COURSE_STATES = set((CourseStates.published,CourseStates.started))
# ACTIVE_COURSE_STATES = set((CourseStates.registered, CourseStates.started))


class EnrolmentStates(dd.Workflow):
    verbose_name_plural = _("Enrolment states")
    required_roles = dd.required(dd.SiteAdmin)
    invoiceable = models.BooleanField(_("invoiceable"), default=True)
    uses_a_place = models.BooleanField(_("Uses a place"), default=True)

add = EnrolmentStates.add_item
add('10', _("Requested"), 'requested', invoiceable=False, uses_a_place=False)
add('20', _("Confirmed"), 'confirmed', invoiceable=True, uses_a_place=True)
add('30', _("Cancelled"), 'cancelled', invoiceable=False, uses_a_place=False)
# add('40', _("Certified"), 'certified', invoiceable=True, uses_a_place=True)
#~ add('40', _("Started"),'started')
#~ add('50', _("Success"),'success')
#~ add('60', _("Award"),'award')
#~ add('90', _("Abandoned"),'abandoned')


