# -*- coding: UTF-8 -*-
# Copyright 2008-2016 Luc Saffre
# License: BSD (see file COPYING for details)

r""" Utilities for manipulating *Belgian national identification
numbers*.

.. test only this doc:
   $ python setup.py test -s tests.UtilsTests.test_ssin

Belgians call their national identification number **INSZ**
("identificatienummer van de sociale zekerheid) in Dutch, **NISS**
("No. d'identification de Sécurité Sociale") in French or **INSS**
("Identifizierungsnummer der Sozialen Sicherheit") in German.  We use
the English abbreviation **SSIN** ("Social Security Identification
Number"), though some sources also speak about **INSS**
("Identification Number Social Security").

See also

- the Wikipedia articles about `Belgian national identification
  numbers
  <http://en.wikipedia.org/wiki/National_identification_number#Belgium>`__,
  `Numéro de registre national
  <http://fr.wikipedia.org/wiki/Num%C3%A9ro_de_registre_national>`_
  and `Rijksregisternummer
  <http://nl.wikipedia.org/wiki/Rijksregisternummer>`_

- http://www.ibz.rrn.fgov.be/fileadmin/user_upload/Registre/Acces_RN/RRNS003_F_IV.pdf
- http://www.simplification.fgov.be/doc/1206617650-4990.pdf


Formatting Belgian National Numbers
-----------------------------------

This module defines the functions :func:`format_ssin` and
:func:`new_format_ssin`.

An officialy obsolete but still used format for printing a Belgian
SSIN is ``YYMMDDx123-97``, where ``YYMMDD`` is the birth date, ``x``
indicates the century (``*`` for the 19th, a *space* for the 20th and
a ``=`` for the 21st century), ``123`` is a sequential number for
persons born the same day (odd numbers for men and even numbers for
women), and ``97`` is a check digit (remainder of previous digits
divided by 97).

.. doctest init:

    >>> import lino
    >>> lino.startup('lino.projects.std.settings_test')


Validation
----------

There are two validator functions, :func:`is_valid_ssin` and
:func:`ssin_validator`.  the difference between them is that one
returns True or False while the other raises a ValidationError to be
used in Django forms.  The message of this ValidationError depends on
the user language.

>>> ssin_validator('123') #doctest: +NORMALIZE_WHITESPACE +IGNORE_EXCEPTION_DETAIL +ELLIPSIS
Traceback (most recent call last):
...
ValidationError: [u'Invalid SSIN 123 : A formatted SSIN must have 13 positions']

>>> is_valid_ssin('123')
False

Here is the SSIN of a person with incomplete birth date:

>>> from lino.utils import IncompleteDate
>>> n = generate_ssin(IncompleteDate(1995, 0, 0), Genders.male, 153)
>>> print (n)
950000 153-96
>>> ssin_validator(n)


No need for special characters?
-------------------------------

In 1983 Belgians discovered that the formatting with a special
character to indicate the century is not absolutely required since the
national register no longer cared about people born before 1900, and
now the century can be deduced by trying the check digits.

>>> format_ssin('68060105329')
'680601 053-29'

In order to say whether the person is born in 19xx or 20xx, we need to
look at the check digits.

For example, the 25th boy born on June 1st in **1912** will get
another check-digit than a similar boy exactly 100 years later (in
**2012**):

>>> format_ssin('12060105317')
'120601 053-17'

>>> format_ssin('12060105346')
'120601 053=46'

Question to mathematicians: is it sure that there is no combination of
birth date and sequence number for which the check digits are the
same?

Functions
---------

"""
from __future__ import division
from builtins import str

from django.utils import six
from past.utils import old_div


from django.core.exceptions import ValidationError
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from lino.modlib.system.choicelists import Genders


YEAR2000 = '='
YEAR1900 = '-'
YEAR1800 = '*'


def generate_ssin(birth_date, gender, seq=None):
    """Generate an SSIN from a given birth date, gender and optional
    sequence number.


    And a function :func:`generate_ssin` is mainly used to generate
    fictive demo data.  For example, here is the national number of the
    25th boy born in Belgium on June 1st, 1968:

    Examples:

    >>> import datetime

    >>> n = generate_ssin(datetime.date(1968, 6, 1), Genders.male, 53)
    >>> print (n)
    680601 053-29
    >>> ssin_validator(n)

    The sequence number is optional and the default value depends on
    the gender.  For boys it is 1, for girls 2.

    >>> n = generate_ssin(datetime.date(2002, 4, 5),Genders.female)
    >>> print (n)
    020405 002=44
    >>> ssin_validator(n)

    """
    year = birth_date.year
    sep1 = ' '
    if year >= 2000:
        bd = "2%02d%02d%02d" % (year - 2000, birth_date.month, birth_date.day)
        sep2 = YEAR2000
    elif year >= 1900:
        bd = "%02d%02d%02d" % (year - 1900, birth_date.month, birth_date.day)
        sep2 = YEAR1900
    else:
        raise Exception("Born before 1900")

    if seq is None:
        if gender == Genders.male:
            seq = 1
        else:
            seq = 2
    seq = '%03d' % seq
    checksum = 97 - (int(bd + seq) % 97)
    if checksum == 0:
        checksum = 97
    checksum = '%02d' % checksum
    ssin = bd[-6:] + sep1 + seq + sep2 + checksum
    return ssin


def is_valid_ssin(ssin):
    """
    Returns True if this is a valid SSIN.
    """
    try:
        ssin_validator(ssin)
        return True
    except ValidationError:
        return False


def new_format_ssin(s):
    """Formats a raw SSIN as they are printed on the back of Belgian eid
    cards, for example "68.06.01-053.09"

    """
    s = s.strip()
    if not s:
        return ''
    if len(s) != 11:
        raise Exception(
            force_text(_('Invalid SSIN %s : ') % s)
            + force_text(_('A raw SSIN must have 11 positions')))
    return s[:2] + '.' + s[2:4] + '.' + s[4:6] + '-' + s[6:9] + '.' + s[9:]


def unformat_ssin(ssin):
    """Remove formatting characters from given SSIN."""
    ssin = ssin.replace(YEAR2000, '')
    ssin = ssin.replace(YEAR1900, '')
    ssin = ssin.replace(YEAR1800, '')
    ssin = ssin.replace('.', '')
    ssin = ssin.replace(' ', '')
    return ssin


def parse_ssin(ssin):
    return format_ssin(unformat_ssin(ssin))


def format_ssin(raw_ssin):
    """
    Add formatting chars to a given raw SSIN.
    """
    raw_ssin = raw_ssin.strip()
    if not raw_ssin:
        return ''
    if len(raw_ssin) != 11:
        raise ValidationError(
            force_text(_('Invalid SSIN %s : ') % raw_ssin)
            + force_text(_('A raw SSIN must have 11 positions')))
    bd = raw_ssin[:6]
    sn = raw_ssin[6:9]
    cd = raw_ssin[9:]

    def is_ok(xtest):
        try:
            xtest = int(xtest)
        except ValueError:
            return False
        xtest = abs((xtest - 97 * (int(old_div(xtest, 97)))) - 97)
        if xtest == 0:
            xtest = 97
        return int(cd) == xtest

    if is_ok(bd + sn):
        return bd + ' ' + sn + YEAR1900 + cd
    if is_ok('2' + bd + sn):
        return bd + ' ' + sn + YEAR2000 + cd
    raise ValidationError(
        force_text(_('Invalid SSIN %s : ') % raw_ssin)
        + force_text(_('Could not recognize checkdigit')))

format_niss = format_ssin


def ssin_validator(ssin):
    """Checks whether the specified SSIN is valid.  If not, raises a
    ValidationError.

    """
    ssin = ssin.strip()
    if not ssin:
        return ''
    if len(ssin) != 13:
        raise ValidationError(
            force_text(_('Invalid SSIN %s : ') % (ssin))
            + force_text(_('A formatted SSIN must have 13 positions'))
        )
    xtest = ssin[:6] + ssin[7:10]
    if ssin[10] == "=":
        #~ print 'yes'
        xtest = "2" + xtest
    try:
        xtest = int(xtest)
    except ValueError as e:
        raise ValidationError(_('Invalid SSIN %s : ') % ssin + str(e))
    xtest = abs((xtest - 97 * (int(old_div(xtest, 97)))) - 97)
    if xtest == 0:
        xtest = 97
    found = int(ssin[11:13])
    if xtest != found:
        raise ValidationError(
            force_text(_("Invalid SSIN %s :") % ssin)
            + _("Check digit is %(found)d but should be %(expected)d") % dict(
                expected=xtest, found=found)
        )
    return

