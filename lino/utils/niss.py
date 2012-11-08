# -*- coding: UTF-8 -*-
## Copyright 2008-2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

ur"""

>>> n = gen_niss(datetime.date(1968,6,1),Gender.male,53)
>>> print n
680601 053-29
>>> niss_validator(n)

>>> n = gen_niss(datetime.date(2002,4,5),Gender.female)
>>> print n
020405 002=15
>>> niss_validator(n)

>>> from lino.utils import babel
>>> babel.set_language('en')

>>> niss_validator('123')
Traceback (most recent call last):
...
ValidationError: [u'Invalid Belgian SSIN 123 : An SSIN has always 13 positions']
"""

#~ import logging
#~ logger = logging.getLogger(__name__)

import os
import cgi
import datetime

#~ from django.db import models
#~ from django.db.models import Q
#~ from django.db.utils import DatabaseError
#~ from django.conf import settings

from django.core.exceptions import ValidationError
from django.utils.encoding import force_unicode 
from django.utils.translation import ugettext_lazy as _

from lino.modlib.contacts.utils import Gender

def gen_niss(birth_date,gender,seq=None):
    """
    """
    year = birth_date.year
    sep1 = ' '
    if year >= 2000:
        year -= 2000
        sep2 = '='
    elif year >= 1900:
        year -= 1900
        sep2 = '-'
    else:
        raise Exception("1800?")
    niss = "%02d%02d%02d" % (year,birth_date.month,birth_date.day)
    if seq is None:
        if gender == Gender.male:
            seq = 1
        else:
            seq = 2
    niss += '%03d' % seq
    checksum = 97 - (int(niss) % 97)
    if checksum == 0: checksum = 97 
    niss += '%02d' % checksum
    niss = niss[0:6] + sep1 + niss[6:9] + sep2 + niss[9:11]
    return niss
    
#~ def format_niss(niss):
    

def is_valid_niss(national_id):
    try:
        niss_validator(national_id)
        return True
    except ValidationError:
        return False
        
def niss_validator(national_id):
    """
    Checks whether the specified `national_id` is a valid 
    Belgian NISS (No. d'identification de sécurité sociale).
    
    Official format is ``YYMMDDx123-97``, where ``YYMMDD`` is the birth date, 
    ``x`` indicates the century (``*`` for the 19th, `` `` (space) for the 20th
    and ``=`` for the 21st century), ``123`` is a sequential number for persons 
    born the same day (odd numbers for men and even numbers for women), 
    and ``97`` is a check digit (remainder of previous digits divided by 97).
    
    """
    national_id = national_id.strip()
    if not national_id:
        return
    if len(national_id) != 13:
        raise ValidationError(
          force_unicode(_('Invalid Belgian SSIN %s : ') % national_id) 
          + force_unicode(_('An SSIN has always 13 positions'))
          ) 
    xtest = national_id[:6] + national_id[7:10]
    if national_id[6] == "=":
        xtest = "2" + xtest
    try:
        xtest = int(xtest)
    except ValueError,e:
        raise ValidationError(
          _('Invalid Belgian SSIN %s : ') % national_id + str(e)
          )
    xtest = abs((xtest-97*(int(xtest/97)))-97)
    if xtest == 0:
        xtest = 97
    found = int(national_id[11:13])
    if xtest != found:
        raise ValidationError(
            force_unicode(_("Invalid Belgian SSIN %s :") % national_id)
            + _("Check digit is %(found)d but should be %(expected)d") % dict(
              expected=xtest, found=found)
            )

    
    
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
