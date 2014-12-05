# -*- coding: UTF-8 -*-
# Copyright 2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""
This module defines the tables 
- :class:`Partner` (and their specializations :class:`Person` and :class:`Company`)
- :class:`Role` and :class:`RoleType`

"""

from __future__ import unicode_literals


import logging
logger = logging.getLogger(__name__)


import datetime
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
#~ from django.utils.translation import ugettext

from django import forms
from django.utils import translation


import lino
#~ from lino import layouts

from lino import dd, rt
#~ from lino import fields

from lino import mixins


class LinkTypes(dd.ChoiceList):
    verbose_name = _("Link Type")
    verbose_name_plural = _("Link Types")

add = LinkTypes.add_item
#~ add('10', _("Context"),'context')
add('10', _("Jargon"), 'jargon')
add('20', _("Obsoletes"), 'obsoletes')


class Concept(mixins.BabelNamed):

    """
    """

    class Meta:
        verbose_name = _("Concept")
        verbose_name_plural = _("Concepts")

    abbr = dd.BabelCharField(_("Abbreviation"), max_length=30, blank=True)
    wikipedia = dd.BabelCharField(_("Wikipedia"), max_length=200, blank=True)

    definition = dd.BabelTextField(_("Definition"), blank=True)
    is_jargon_domain = models.BooleanField(
        _("Jargon domain"),
        help_text=_(
            "Whether this concept designates a domain of specialized vocabulary."),
        default=False)

    def summary_row(self, ar=None):
        if self.abbr:
            return ["%s (%s)" % (dd.babelattr(self, 'name'), dd.babelattr(self, 'abbr'))]
        return [dd.babelattr(self, 'name')]


class Concepts(dd.Table):
    #~ required = dd.required(user_level='manager')
    model = Concept
    column_names = 'name id abbr'
    detail_layout = """
    name
    abbr
    definition
    wikipedia
    Parents Children
    """


class TopLevelConcepts(Concepts):
    label = _("Top-level concepts")
    filter = models.Q(is_jargon_domain=True)


class Link(dd.Model):

    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")

    type = LinkTypes.field(blank=True, default=LinkTypes.jargon)
    parent = dd.ForeignKey(Concept, related_name="children")
    child = dd.ForeignKey(Concept, related_name="parents")

    @dd.chooser()
    def child_choices(cls):
        return Concept.objects.filter(is_jargon_domain=True)


class Links(dd.Table):
    model = Link


class Parents(Links):
    master_key = 'child'
    label = _("Parents")


class Children(Links):
    master_key = 'parent'
    label = _("Children")


MODULE_LABEL = _("Concepts")


def setup_main_menu(site, ui, profile, m):
    m = m.add_menu("concepts", MODULE_LABEL)
    m.add_action(Concepts)


def setup_master_menu(site, ui, profile, m):
    pass


def setup_config_menu(site, ui, profile, m):
    pass


def setup_explorer_menu(site, ui, profile, m):
    pass
