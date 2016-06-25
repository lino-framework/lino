# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Choicelists for this plugin."""

from lino.api import dd, _


class PartnerEvents(dd.ChoiceList):
    """A choicelist of observable partner events.

    """
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")
    max_length = 50


