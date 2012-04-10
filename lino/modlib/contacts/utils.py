# -*- coding: UTF-8 -*-
## Copyright 2010-2012 Luc Saffre
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



import re

#~ from django.utils.translation import ugettext_lazy as _
#~ from django.db import models
#~ from django.conf import settings


name_prefixes1 = ("HET", "'T",'VAN','DER', 'TER',
  'VOM','VON','OF', "DE", "DU", "EL", "AL")
name_prefixes2 = ("VAN DEN","VAN DER","VAN DE",
  "IN HET", "VON DER","DE LA")



def name2kw(s,last_name_first=True):
    """
Split a string that contains both last_name and first_name.
The caller must indicate whether the string contains 
last_name first (e.g. Saffre Luc) or first_name first (e.g. Luc Saffre).

Examples:

>>> name2kw("Saffre Luc")
{'first_name': 'Luc', 'last_name': 'Saffre'}
>>> name2kw("Rilke Rainer Maria")
{'first_name': 'Rainer Maria', 'last_name': 'Rilke'}
>>> name2kw("Van Rompuy Herman")
{'first_name': 'Herman', 'last_name': 'Van Rompuy'}
>>> name2kw("'T Jampens Jan")
{'first_name': 'Jan', 'last_name': "'T Jampens"}
>>> name2kw("Van den Bossche Marc Antoine Bernard")
{'first_name': 'Marc Antoine Bernard', 'last_name': 'Van den Bossche'}

In more complicated cases, a comma is required to help:

>>> name2kw("Mombanga born Ngungi, Maria Magdalena")
{'first_name': 'Maria Magdalena', 'last_name': 'Mombanga born Ngungi'}

Some examples with `first_name` first:

>>> name2kw("Luc Saffre",False)
{'first_name': 'Luc', 'last_name': 'Saffre'}
>>> name2kw("Rainer Maria Rilke",False)
{'first_name': 'Rainer Maria', 'last_name': 'Rilke'}
>>> name2kw("Herman Van Rompuy",False)
{'first_name': 'Herman', 'last_name': 'Van Rompuy'}
>>> name2kw("Jan 'T Jampens",False)
{'first_name': 'Jan', 'last_name': "'T Jampens"}
>>> name2kw("Marc Antoine Bernard Van den Bossche",False)
{'first_name': 'Marc Antoine Bernard', 'last_name': 'Van den Bossche'}

Edge cases:

>>> name2kw("")
{}


Bibliography:

#. http://en.wikipedia.org/wiki/Dutch_name
#. http://www.myheritage.com/support-post-130501/dutch-belgium-german-french-surnames-with-prefix-such-as-van


    """
    kw = {}
    a = s.split(',')
    if len(a) == 2:
        if last_name_first:
            return dict(last_name=a[0].strip(),first_name= a[1].strip())
    a = s.strip().split()
    if len(a) == 0:
        return dict()
    elif len(a) == 1:
        return dict(last_name=a[0])
    elif len(a) == 2:
        if last_name_first:
            return dict(last_name=a[0],first_name= a[1])
        else:
            return dict(last_name=a[1],first_name= a[0])
    else:
        # string consisting of more than 3 words
        if last_name_first:
            a01 = a[0] + ' ' + a[1]
            if a01.upper() in name_prefixes2:
                return dict(
                  last_name = a01 + ' ' + a[2],
                  first_name = ' '.join(a[3:]))
            elif a[0].upper() in name_prefixes1:
                return dict(
                    last_name = a[0] + ' ' + a[1],
                    first_name = ' '.join(a[2:]))
            else:
                return dict(last_name = a[0],
                    first_name = ' '.join(a[1:]))
        else:
            if len(a) >= 4:
                pc = a[-3] + ' ' + a[-2] # prefix2 candidate
                if pc.upper() in name_prefixes2:
                    return dict(
                        last_name = pc + ' ' + a[-1],
                        first_name = ' '.join(a[:-3]))
            pc = a[-2] # prefix candidate
            if pc.upper() in name_prefixes1:
                return dict(
                    last_name = pc + ' ' + a[-1],
                    first_name = ' '.join(a[:-2]))
        return dict(
            last_name = a[-1],
            first_name = ' '.join(a[:-1]))
            
    return kw
    
def street2kw(s,**kw):
    """
Parse a string to extract the fields street, street_no and street_box.

Examples:
    
>>> street2kw(u"Limburger Weg")
{'street': u'Limburger Weg'}
>>> street2kw(u"Loten 3")
{'street_box': u'', 'street': u'Loten', 'street_no': u'3'}
>>> street2kw(u"Loten 3A")
{'street_box': u'A', 'street': u'Loten', 'street_no': u'3'}

>>> street2kw(u"In den Loten 3A")
{'street_box': u'A', 'street': u'In den Loten', 'street_no': u'3'}

>>> street2kw(u"Auf'm Bach")
{'street': u"Auf'm Bach"}
>>> street2kw(u"Auf'm Bach 3")
{'street_box': u'', 'street': u"Auf'm Bach", 'street_no': u'3'}
>>> street2kw(u"Auf'm Bach 3a")
{'street_box': u'a', 'street': u"Auf'm Bach", 'street_no': u'3'}
>>> street2kw(u"Auf'm Bach 3 A")
{'street_box': u'A', 'street': u"Auf'm Bach", 'street_no': u'3'}

>>> street2kw(u"rue des 600 Franchimontois 1")
{'street_box': u'', 'street': u'rue des 600 Franchimontois', 'street_no': u'1'}

>>> street2kw(u"Neustr. 1 (Referenzadr.)")
{'addr2': u'(Referenzadr.)', 'street': u'Neustr.', 'street_no': u'1'}

Edge cases:

>>> street2kw("")
{}
    
    """
    #~ m = re.match(r"(\D+),?\s*(\d+)\s*(\w*)", s)
    m = re.match(r"(.+),?\s+(\d+)\s*(\D*)$", s)
    if m:
        kw['street'] = m.group(1).strip()
        kw['street_no'] = m.group(2).strip()
        street_box = m.group(3).strip()
        if len(street_box) > 5:
            kw['addr2'] = street_box
        else:
            kw['street_box'] = street_box
    else:
        s = s.strip()
        if len(s):
            kw['street'] = s
    return kw



def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()




