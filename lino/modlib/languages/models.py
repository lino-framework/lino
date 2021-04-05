# -*- coding: UTF-8 -*-
# Copyright 2008-2017 Luc Saffre
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Defines the :class:`Language` model.

"""
from builtins import object


from django.db import models

from lino.api import dd
from lino import mixins
from django.utils.translation import gettext_lazy as _

from lino.modlib.office.roles import OfficeStaff


class Language(mixins.BabelNamed):

    class Meta(object):
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")
        ordering = ['name']

    id = models.CharField(max_length=3, primary_key=True)
    iso2 = models.CharField(max_length=2, blank=True)  # ,null=True)


class Languages(dd.Table):
    model = 'languages.Language'
    required_roles = dd.login_required(OfficeStaff)


