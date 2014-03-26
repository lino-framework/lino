# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import dd

config = dd.apps.badges


class Badge(dd.BabelNamed):
    class Meta:
        verbose_name = _("Badge")
        verbose_name_plural = _("Badges")


class Badges(dd.Table):
    model = 'badges.Badge'
    required = dd.required(user_level='admin')


class Award(dd.Model):

    class Meta:
        verbose_name = _("Badge Award")
        verbose_name_plural = _("Badge Awards")

    holder = dd.ForeignKey(
        config.holder_model,
        verbose_name=_("Holder"))
    badge = dd.ForeignKey('badges.Badge')
    date = models.DateField(
        _("Date"), default=datetime.date.today)
    result = models.CharField(
        _("Result"),
        blank=True, max_length=200)
    remark = models.CharField(
        _("Remark"),
        blank=True, max_length=200)


class Awards(dd.Table):
    model = 'badges.Award'
    required = dd.required(user_level='admin')


class AwardsByHolder(Awards):
    label = _("Awards")
    required = dd.required()
    master_key = 'holder'
    column_names = 'date badge result remark'
    auto_fit_column_widths = True


class AwardsByBadge(Awards):
    label = _("Awards")
    required = dd.required()
    master_key = 'badge'
    column_names = 'date holder result remark'
    auto_fit_column_widths = True


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu(config.app_label, config.verbose_name)
    m.add_action('badges.Badges')


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu(config.app_label, config.verbose_name)
    m.add_action('badges.Awards')


__all__ = [
    'Badge',
    'Badges',
    'Award',
    'Awards',
    'AwardsByHolder',
    'AwardsByBadge']

