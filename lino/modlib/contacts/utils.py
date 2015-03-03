# -*- coding: UTF-8 -*-
# Copyright 2010-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Some utilities for parsing contact data. See also
:mod:`lino.mixins.human`.

- :func:`street2kw` to separate house number and optional
  flat number from street

"""

import re


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
