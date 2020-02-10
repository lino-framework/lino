# -*- coding: utf-8 -*-
# Copyright 2008-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""

See test cases and examples in :doc:`/specs/human`.

"""
from past.utils import old_div

import datetime
from dateutil.relativedelta import relativedelta

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
from django.conf import settings

from lino.utils import join_words
from lino.api.dd import Genders

from lino.core import fields
from lino.core import model

name_prefixes1 = set(("HET", "'T", 'VAN', 'DER', 'TER', 'DEN',
                      'VOM', 'VON', 'OF',
                      "DE", "DU",
                      "DA", "DI", "DO", "DOS",
                      "EL", "AL"))
name_prefixes2 = set(("VAN DEN", "VAN DER", "VAN DE",
                      "IN HET", "VON DER", "DE LA"))

NAME_PREFIXES = set([p + ' ' for p in name_prefixes1])
NAME_PREFIXES |= set([p + ' ' for p in name_prefixes2])



def strip_name_prefix(s):
    """Strip name prefix from given family name `s`."""
    s = s.upper()

    def strip_from(s, lst):
        for p in lst:
            p = p + ' '
            if s.startswith(p):
                s = s[len(p):]
        return s

    s = strip_from(s, name_prefixes2)
    s = strip_from(s, name_prefixes1)
    return s


def name2kw(s, last_name_first=True):
    """
    Separate first name from last name.  Split a string that contains
    both last_name and first_name.  The caller must indicate whether
    the string contains last_name first (e.g. Saffre Luc) or
    first_name first (e.g. Luc Saffre).
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
        # string of more than 3 words
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

    Extends :func:`name2kw` by raising a ValidationError if necessary and by
    capitalizing each part of the name.

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
    """
    Returns "Mr" or "Mrs" or a translation thereof, depending on the
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
    """
    Base class for models that represent a human.

    .. attribute:: title

        Used to specify a professional position or academic
        qualification like "Dr." or "PhD".

        If given, the content of this field comes always *between*
        salutation and name.

    .. attribute:: first_name

        The first name, also known as given name.

    .. attribute:: last_name

        The last name, also known as family name.

    .. attribute:: middle_name

        A space-separated list of all `middle names
        <http://en.wikipedia.org/wiki/Middle_name>`_.

    .. attribute:: gender

        The sex of this person (male or female).

        Possible values are defined in
        :class:`lino.modlib.lino.choicelists.Genders`.
    """

    class Meta(object):
        abstract = True

    title = models.CharField(
        pgettext("(of a human)", "Title"),
        max_length=200, blank=True)

    first_name = models.CharField(
        _('First name'), max_length=200, blank=True)

    middle_name = models.CharField(
        _("Middle name"), max_length=200, blank=True)

    last_name = models.CharField(
        _('Last name'), max_length=200, blank=True)

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

    def __str__(self):
        return self.get_full_name(nominative=True)

    def get_salutation(self, **salutation_options):
        return get_salutation(
            #~ translation.get_language(),
            self.gender, **salutation_options)

    def get_last_name_prefix(self):
        """
        May be used for handling special of titles (e.g. "Cardinal",
        "Graf") which come before the last name (not before the first
        name).

        Lino currently does not support titles which replace the
        salutation ("Br.", "Sr.")  or which must come at another
        position of the full name

        External links: `linguee.de
        <http://www.linguee.de/englisch-deutsch/uebersetzung/mr.+dr..html>`__
        and `wikipedia.org <https://en.wikipedia.org/wiki/Title>`__
        """
        return ''

    def get_full_name(
            self, salutation=True, upper=None, **salutation_options):
        """
        Returns a one-line string composed of salutation,
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

        If :meth:`get_after_salutation_words` yields a sequence of
        words, then these are inserted between salutation and first
        name.

        See :ref:`lino.tutorial.human` for some examples.
        """
        words = []

        if salutation:
            words.append(self.get_salutation(**salutation_options))
        if self.title:
            words.append(self.title)
        words.append(self.first_name)
        prefix = self.get_last_name_prefix()
        if prefix:
            words.append(prefix)
        if upper is None:
            upper = settings.SITE.uppercase_last_name
        if upper:
            words.append(self.last_name.upper())
        else:
            words.append(self.last_name)
        return join_words(*words)
    full_name = property(get_full_name)

    def format_family_member(self, ar, other):
        """
        Used in `humanlinks.LinksByHuman` and in
        `households.SiblingsByPerson`.
        """
        if other.last_name == self.last_name:
            text = other.first_name
        else:
            text = other.first_name + ' ' + other.last_name.upper()
        return ar.obj2html(other, text)

    @classmethod
    def get_simple_parameters(cls):
        for p in super(Human, cls).get_simple_parameters():
            yield p
        yield 'gender'

    # no longer needed after 20170826
    # @classmethod
    # def setup_parameters(cls, **fields):
    #     fields.update(
    #         gender=Genders.field(
    #             blank=True, help_text=_(
    #                 "Show only persons with the given gender.")))
    #     return super(Human, cls).setup_parameters(**fields)

    # @classmethod
    # def get_request_queryset(cls, ar):
    #     # print("20160329 Human.get_request_queryset")
    #     qs = super(Human, cls).get_request_queryset(ar)
    #     if ar.param_values.gender:
    #         qs = qs.filter(gender__exact=ar.param_values.gender)
    #     return qs

    # @classmethod
    # def get_title_tags(cls, ar):
    #     for t in super(Human, cls).get_title_tags(ar):
    #         yield t
    #     if ar.param_values.gender:
    #         yield str(ar.param_values.gender)


class Born(model.Model):
    """
    Abstract base class that adds a `birth_date` field and a virtual
    field "Age".

    .. attribute:: birth_date

      An :class:`IncompleteDateField <lino.core.fields.IncompleteDateField>`.

    .. attribute:: age

      Virtual field displaying the age in years.
    """

    class Meta(object):
        abstract = True

    birth_date = fields.IncompleteDateField(
        blank=True, verbose_name=_("Birth date"))

    def get_age(self, today=None):
        """
        Return the age (in years) of this human.  See
        :meth:`lino.utils.IncompleteDateField.get_age`.
        """
        if self.birth_date:
            return self.birth_date.get_age(today or settings.SITE.today())

    def get_exact_age(self, today=None):
        """
        Return the age as a :class:`datetime.timedelta` object.

        Optional keyword argument `today` should be a
        :class:`datetime.date` instance to replace the actual current
        date. This is used if you want the age at a given date in the past
        or the future.
        The default value calls :meth:`dd.Site.today`.
        """
        # print(20160202, self.birth_date, self)
        if self.birth_date and self.birth_date.year:
            if today is None:
                today = settings.SITE.today()
            try:
                return relativedelta(today , self.birth_date.as_date())
            except ValueError:
                pass

    @fields.displayfield(_("Age"))
    def age(self, ar, today=None):
        a = self.get_exact_age(today)
        if a is None:
            return str(_('unknown'))
        years = a.years
        if years == 1:
            s = _("{} year").format(years)
        else:
            s = _("{} years").format(years)
        if years <= 4:
            months = a.months
            if months == 1:
                s += " " + _("{} month").format(months)
            else:
                s += " " + _("{} months").format(months)
        if self.birth_date and self.birth_date.is_complete():
            return s
        return u"±" + s

    @classmethod
    def setup_parameters(cls, fields):
        fields.update(
            aged_from=models.IntegerField(
                _("Aged from"), blank=True, null=True,
                help_text=_("Select only persons aged at least "
                            "the given number of years.")),
            aged_to=models.IntegerField(
                _("Aged to"), blank=True, null=True,
                help_text=_("Select only persons aged at most "
                            "the given number of years.")))
        super(Born, cls).setup_parameters(fields)

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        qs = super(Born, cls).get_request_queryset(ar, **filter)
        pv = ar.param_values

        today = settings.SITE.today()

        if pv.aged_from:
            min_date = today - \
                datetime.timedelta(days=pv.aged_from * 365)
            qs = qs.filter(birth_date__lte=min_date.strftime("%Y-%m-%d"))

        if pv.aged_to:
            max_date = today - \
                datetime.timedelta(days=pv.aged_to * 365)
            qs = qs.filter(birth_date__gte=max_date.strftime("%Y-%m-%d"))

        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Born, self).get_title_tags(ar):
            yield t
        pv = ar.param_values
        if pv.aged_from or pv.aged_to:
            yield str(_("Aged %(min)s to %(max)s") % dict(
                min=pv.aged_from or '...',
                max=pv.aged_to or '...'))
