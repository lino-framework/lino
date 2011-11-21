#coding: latin1

## Copyright 2003-2006 Luc Saffre

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""
Sources:

ISO 639 : Code for the representation of names of languages
ISO 3166 : alpha-2 country codes

http://www.loc.gov/standards/iso639-2/

http://www.loc.gov/standards/iso639-2/ISO-639-2_values_8bits.txt

To read this file, please note that one line of text contains one
entry. An alpha-3 (bibliographic) code, an alpha-3 (terminologic) code
(when given), an alpha-2 code (when given), an English name, and a
French name of a language are all separated by pipe (|)
characters. The Line terminator is the LF character.
"""

import os
import codecs

from lino.adamo.exceptions import DataVeto

dataDir = os.path.dirname(__file__)

def populate(q):
    q.setBabelLangs('en fr')
    #f = file(os.path.join(dataDir,'ISO-639-2_values_8bits.txt'))
    f = codecs.open(
        os.path.join(dataDir,'ISO-639-2_values_8bits.txt'),
        "r", "latin1")
    for line in f.readlines():
        #print line
        a = line.split('|')
        if len(a) > 2:
            bibliographic = a[0]
            terminologic = a[1]
            alpha2 = a[2]
            name_en = a[3]

            #if len(a) > 4:
            name_fr = a[4]
            #print (name_en,name_fr)
            if len(alpha2):
                #try:
                q.appendRow(id=alpha2.encode('ascii'),
                            name=(name_en,name_fr))
                #except DataVeto,e:
                #    print e
        elif len(line.strip()):
            print "ignored:", line

    f.close()
