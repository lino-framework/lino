# -*- coding: utf-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""

See test cases and examples in :doc:`/tutorials/human/index`.

.. autosummary::


"""

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext
from django.conf import settings

from lino.utils import join_words
from lino.api.dd import Genders

from lino.core import fields
from lino.core import model

name_prefixes1 = set(("HET", "'T", 'VAN', 'DER', 'TER', 'DEN',
                      'VOM', 'VON', 'OF', "DE", "DU", "EL", "AL", "DI"))
name_prefixes2 = set(("VAN DEN", "VAN DER", "VAN DE",
                      "IN HET", "VON DER", "DE LA"))

NAME_PREFIXES = set([p + ' ' for p in name_prefixes1])
NAME_PREFIXES |= set([p + ' ' for p in name_prefixes2])


def strip_name_prefix(s):
    """Strip name prefix from given family name `s`."""
    s = s.upper()
    for p in NAME_PREFIXES:
        if s.startswith(p):
            s = s[len(p):]
    return s



def name2kw(s, last_name_first=True):
    """Separate first name from last name.  Split a string that contains
both last_name and first_name.  The caller must indicate whether the
string contains last_name first (e.g. Saffre Luc) or first_name first
(e.g. Luc Saffre).

    """
    kw = {}
    a = s.split(',')
    if len(a) == 2:
        if last_name_first:
            return dict(last_name=a[0].strip(), first_name=a[1].strip())
    a = s.strip().split()
    if len(a) == 0:
        return dict()
    elif len(a) == 1:
        return dict(last_name=a[0])
    elif len(a) == 2:
        if last_name_first:
            return dict(last_name=a[0], first_name=a[1])
        else:
            return dict(last_name=a[1], first_name=a[0])
    else:
        # string consisting of more than 3 words
        if last_name_first:
            a01 = a[0] + ' ' + a[1]
            if a01.upper() in name_prefixes2:
                return dict(
                    last_name=a01 + ' ' + a[2],
                    first_name=' '.join(a[3:]))
            elif a[0].upper() in name_prefixes1:
                return dict(
                    last_name=a[0] + ' ' + a[1],
                    first_name=' '.join(a[2:]))
            else:
                return dict(last_name=a[0],
                            first_name=' '.join(a[1:]))
        else:
            if len(a) >= 4:
                pc = a[-3] + ' ' + a[-2]  # prefix2 candidate
                if pc.upper() in name_prefixes2:
                    return dict(
                        last_name=pc + ' ' + a[-1],
                        first_name=' '.join(a[:-3]))
            pc = a[-2]  # prefix candidate
            if pc.upper() in name_prefixes1:
                return dict(
                    last_name=pc + ' ' + a[-1],
                    first_name=' '.join(a[:-2]))
        return dict(
            last_name=a[-1],
            first_name=' '.join(a[:-1]))

    return kw


def upper1(s):
    if ' ' in s:
        return s  # don't change
    return s[0].upper() + s[1:]


def parse_name(text):
    """Parse the given `text` and return a dict of `first_name` and
    `last_name` value.

    Extends :func:`name2kw` by raising a  ValidationError if necessary.

    """
    kw = name2kw(text, last_name_first=False)
    if len(kw) != 2:
        raise ValidationError(
            _("Cannot find first and last name in \"{0}\"").format(text))
    for k in ('last_name', 'first_name'):
        if kw[k] and not kw[k].isupper():
            kw[k] = upper1(kw[k])
    return kw


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
    """Base class for all models that represent a human.

    .. attribute:: title

        An optional name prefix like "Dr." or "PhD", used to specify a
        professional position or academic qualification.

        If given, the content of this field comes always *between*
        salutation and name.  It does not handle special cases like
        titles which replace the salutation ("Br.", "Sr.") or which must
        come at another position of the full name (e.g. "Cardinal", "Graf"
        before the last name).

        External links: `linguee.de
        <http://www.linguee.de/englisch-deutsch/uebersetzung/mr.+dr..html>`__
        and `wikipedia.org <https://en.wikipedia.org/wiki/Title>`__

    .. attribute:: first_name

        The first name, also known as given name.

    .. attribute:: last_name

        The last name, also known as family name.

    .. attribute:: middle_name

        A space-separated list of all `middle names
        <http://en.wikipedia.org/wiki/Middle_name>`_.

    .. attribute:: gender

        The sex of this person (male or female).  Possible values are
        defined in :class:`lino.modlib.lino.choicelists.Genders`.

    """

    class Meta:
        abstract = True

    title = models.CharField(
        pgettext("(of a human)", "Title"),
        max_length=200, blank=True,
        help_text=_(
            "Text to print between salutation and name as part "
            "of the first address line."))

    first_name = models.CharField(
        _('First name'), max_length=200, blank=True,
        help_text=_("First or given name."))

    middle_name = models.CharField(
        _("Middle name"), max_length=200, blank=True,
        help_text=_("Space-separated list of all middle names."))

    last_name = models.CharField(
        _('Last name'), max_length=200, blank=True,
        help_text=_("Last name (family name)."))

    gender = Genders.field(blank=True)

    def mf(self, m, f, u=None):
        """
        Taking three parameters `m`, `f` and `u` of any type, returns one
        of them depending on whether this Person is male, female or of
        unknown gender.

        See :ref:`lino.tutorial.human` for some examples.


        """
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
        """Returns a one-line string composed of salutation,
        :attr:`first_name` and :attr:`last_name`.

        The optional keyword argument `salutation` can be set to
        `False` to suppress salutations.

        The optional keyword argument `upper` can be specified to
        override the Site's default value
        (:attr:`lino.core.site.Site.uppercase_last_name`). `True`
        means to convert the last name to uppercase as is usually done
        in French.

        Any other keyword arguments are forwarded to
        :func:`lino.mixins.human.get_salutation` (see there).

        See :ref:`lino.tutorial.human` for some examples.

        """
        words = []

        if salutation:
            words.append(self.get_salutation(**salutation_options))
        if self.title:
            words.append(self.title)
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
    """
    Abstract base class that adds a `birth_date`
    field and a virtual field "Age".

    .. attribute:: birth_date

      An :class:`IncompleteDateField <lino.core.fields.IncompleteDateField>`.

    .. attribute:: age

      Virtual field displaying the age in years.

    """

    class Meta:
        abstract = True

    birth_date = fields.IncompleteDateField(
        blank=True, verbose_name=_("Birth date"))

    def get_age(self, today=None):
        """
        Return the age as a :class:`datetime.timedelta` object.

        `ar` is the requesting :class:`ActionRequest` which can be `None`
        because it is ignored.

        Optional keyword argument `today` should be a
        :class:`datetime.date` instance to replace the actual current
        date. This is used if you want the age at a given date in the past
        or the future.
        The default value calls :meth:`dd.Site.today`.
        """
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
