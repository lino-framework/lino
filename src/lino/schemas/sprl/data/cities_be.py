## Copyright Luc Saffre 2003-2004.

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
"""

import csv
import os

from lino.adamo.datatypes import DataVeto
from lino.schemas.sprl.tables import Nations


dataDir = os.path.dirname(__file__)

def populate(sess):
    be = sess.query(Nations).peek('be')
    f = file(os.path.join(dataDir,'belgzip.csv'),'rb')
    r = csv.reader(f)
    r.next()
    cities = be.cities
    #print cities
    for (name,zip) in r:
        cities.appendRow(name=name,zipCode=zip)

    

    
