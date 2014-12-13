# -*- coding: utf-8 -*-
# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)
"""

See :ref:`lino.tutorial.human`.

"""

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext
from django.conf import settings

from lino.utils import join_words
from lino.dd import Genders

from lino.core import fields
from lino.core import model


def get_salutation(gender, nominative=False):
    """Returns "Mr" or "Mrs" or a translation thereof, depending on the
    gender and the current language.
    
    Note that the English abbreviations `Mr
    <http://en.wikipedia.org/wiki/Mr.>`_ and `Mrs
    <http://en.wikipedia.org/wiki/Mrs.>`_ are written either *with*
    (AE) or *without* (BE) a dot.
    
    The optional keyword argument `nominative` is used only in certain
    languages like German: specifying ``nominative=True`` for a male
    person will return the nominative or direct form "Herr" instead of
    the default (accusative or indirect form) "Herrn".

    """
    if not gender:
        return ''
    if gender == Genders.female:
        return _("Mrs")
    if nominative:
        return pgettext("nominative salutation", "Mr")
    return pgettext("indirect salutation", "Mr")


class Human(model.Model):
    "See :class:`dd.Human`."

    class Meta:
        abstract = True

    first_name = models.CharField(
        _('First name'),
        max_length=200,
        blank=True,
        help_text=_("First or given name."))

    middle_name = models.CharField(
        _("Middle name"), max_length=200, blank=True,
        help_text=_("Space-separated list of all middle names."))

    last_name = models.CharField(
        _('Last name'), max_length=200, blank=True,
        help_text=_("Last name (family name).")
        )

    gender = Genders.field(blank=True)

    def mf(self, m, f, u=None):
        if self.gender is Genders.male:
            return m
        if self.gender is Genders.female:
            return f
        return u or m

    def __unicode__(self):
        return self.get_full_name(nominative=True)

    def get_salutation(self, **salutation_options):
        return get_salutation(
            #~ translation.get_language(),
            self.gender, **salutation_options)

    def get_full_name(
            self, salutation=True, upper=None, **salutation_options):
        words = []
        if salutation:
            words.append(self.get_salutation(**salutation_options))
        words.append(self.first_name)
        if upper is None:
            upper = settings.SITE.uppercase_last_name
        if upper:
            words.append(self.last_name.upper())
        else:
            words.append(self.last_name)
        return join_words(*words)
    full_name = property(get_full_name)

    def format_family_member(self, ar, other):
        """used in `humanlinks.LinksByHuman` and in
`households.SiblingsByPerson`.

        """
        if other.last_name == self.last_name:
            text = other.first_name
        else:
            text = other.first_name + ' ' + other.last_name.upper()
        return ar.obj2html(other, text)


class Born(model.Model):
    "See :class:`dd.Born`."

    class Meta:
        abstract = True

    birth_date = fields.IncompleteDateField(
        blank=True, verbose_name=_("Birth date"))

    def get_age(self, today=None):
        if self.birth_date and self.birth_date.year:
            if today is None:
                today = settings.SITE.today()
            try:
                return today - self.birth_date.as_date()
            except ValueError:
                pass

    @fields.displayfield(_("Age"))
    def age(self, request, today=None):
        a = self.get_age(today)
        if a is None:
            return unicode(_('unknown'))
        s = _("%d years") % (a.days / 365)
        if self.birth_date and self.birth_date.is_complete():
            return s
        return u"±" + s
