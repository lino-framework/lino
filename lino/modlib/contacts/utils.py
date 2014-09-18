# -*- coding: UTF-8 -*-
# Copyright 2010-2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Some utilities for parsing contact data.

- :func:`name2kw` to separate first name from last name

- :func:`street2kw` to separate house number and optional 
  flat number from street

"""

import re


name_prefixes1 = ("HET", "'T", 'VAN', 'DER', 'TER', 'DEN',
                  'VOM', 'VON', 'OF', "DE", "DU", "EL", "AL", "DI")
name_prefixes2 = ("VAN DEN", "VAN DER", "VAN DE",
                  "IN HET", "VON DER", "DE LA")


def name2kw(s, last_name_first=True):
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
>>> name2kw("Den Tandt Marc Antoine Bernard")
{'first_name': 'Marc Antoine Bernard', 'last_name': 'Den Tandt'}

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
>>> name2kw("Marc Antoine Bernard Den Tandt",False)
{'first_name': 'Marc Antoine Bernard', 'last_name': 'Den Tandt'}

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
    """
Examples:

>>> print(parse_name("luc saffre"))
{'first_name': 'Luc', 'last_name': 'Saffre'}

But careful with name prefixes:

>>> print(parse_name("herman van veen"))
{'first_name': 'Herman', 'last_name': 'van veen'}
>>> print(parse_name("jean van den bossche"))
{'first_name': 'Jean', 'last_name': 'van den bossche'}


    """
    kw = name2kw(text, last_name_first=False)
    if len(kw) != 2:
        raise Warning(
            "Cannot find first and last names in %r", text)
    for k in ('last_name', 'first_name'):
        if kw[k] and not kw[k].isupper():
            kw[k] = upper1(kw[k])
    return kw


def street2kw(s, **kw):
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

Some rather special cases:

>>> street2kw(u"rue des 600 Franchimontois 1")
{'street_box': u'', 'street': u'rue des 600 Franchimontois', 'street_no': u'1'}

>>> street2kw(u"Eupener Strasse 321 /A")
{'street_box': u'/A', 'street': u'Eupener Strasse', 'street_no': u'321'}


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
