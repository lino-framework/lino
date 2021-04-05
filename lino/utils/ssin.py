# -*- coding: UTF-8 -*-
# Copyright 2008-2017 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""See :doc:`/specs/ssin`.

"""
from __future__ import division

from past.utils import old_div


from django.core.exceptions import ValidationError
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from lino.modlib.system.choicelists import Genders


YEAR2000 = '='
YEAR1900 = '-'
YEAR1800 = '*'


def generate_ssin(birth_date, gender, seq=None):
    """Generate an SSIN from a given birth date, gender and optional
    sequence number.

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
    if ssin_veto(ssin):
        return False
    return True


def new_format_ssin(s):
    """Formats a raw SSIN as they are printed on the back of Belgian eid
    cards, for example "68.06.01-053.09"

    """
    s = s.strip()
    if not s:
        return ''
    if len(s) != 11:
        raise Exception(
            force_str(_('Invalid SSIN %s : ') % s)
            + force_str(_('A raw SSIN must have 11 positions')))
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
            force_str(_('Invalid SSIN %s : ') % raw_ssin)
            + force_str(_('A raw SSIN must have 11 positions')))
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
        force_str(_('Invalid SSIN %s : ') % raw_ssin)
        + force_str(_('Could not recognize checkdigit')))

format_niss = format_ssin


def ssin_validator(ssin):
    """Checks whether the specified SSIN is valid.  If not, raises a
    ValidationError.

    """
    msg = ssin_veto(ssin)
    if msg:
        raise ValidationError(msg)

def ssin_veto(ssin):
    ssin = ssin.strip()
    if not ssin:
        return
    if len(ssin) != 13:
        return force_str(_('Invalid SSIN %s : ') % (ssin)) + \
            force_str(_('A formatted SSIN must have 13 positions'))
    xtest = ssin[:6] + ssin[7:10]
    if ssin[10] == "=":
        #~ print 'yes'
        xtest = "2" + xtest
    try:
        xtest = int(xtest)
    except ValueError as e:
        return _('Invalid SSIN %s : ') % ssin + str(e)
    xtest = abs((xtest - 97 * (int(old_div(xtest, 97)))) - 97)
    if xtest == 0:
        xtest = 97
    found = int(ssin[11:13])
    if xtest != found:
        return force_str(_("Invalid SSIN %s :") % ssin) \
            + _("Check digit is %(found)d but should be %(expected)d") % dict(
                expected=xtest, found=found)
