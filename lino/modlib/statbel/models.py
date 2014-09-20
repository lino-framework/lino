# -*- coding: UTF-8 -*-
# Copyright 2011-2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""
This just adds `inscode` fields to `countries.Place`
and `countries.Country`.

"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import dd, rt


dd.inject_field('countries.Place',
                'inscode',
                models.CharField(
                    max_length=5,
                    verbose_name=_("INS code"),
                    blank=True,
                    help_text=_("The official code for this place \
                    used by statbel.fgov.be")
                ))

dd.inject_field('countries.Country',
                'inscode',
                models.CharField(
                    max_length=3,
                    verbose_name=_("INS code"),
                    blank=True,
                    help_text=_("The official code for this country \
                    used by statbel.fgov.be")
                ))
