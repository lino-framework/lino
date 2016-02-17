# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.concepts`.

"""

from __future__ import unicode_literals
from builtins import object


import logging
logger = logging.getLogger(__name__)


from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt

from lino import mixins


class LinkTypes(dd.ChoiceList):
    verbose_name = _("Link Type")
    verbose_name_plural = _("Link Types")

add = LinkTypes.add_item
#~ add('10', _("Context"),'context')
add('10', _("Jargon"), 'jargon')
add('20', _("Obsoletes"), 'obsoletes')


class Concept(mixins.BabelNamed):
    """A word and its translation in different languages.
    """

    class Meta(object):
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

    class Meta(object):
        verbose_name = _("Link")
        verbose_name_plural = _("Links")

    type = LinkTypes.field(blank=True, default=LinkTypes.jargon.as_callable)
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

