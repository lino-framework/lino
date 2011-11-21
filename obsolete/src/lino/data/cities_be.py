## Copyright 2003-2005 Luc Saffre 

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
import codecs

from lino.schemas.sprl.tables import Nations

dataDir = os.path.dirname(__file__)

def populate(q):
    #be = q.getColumnByName("nation").peek('be')
    be = q.getSession().peek(Nations,'be')
    #f = open(os.path.join(dataDir,'belgzip.csv'),'rb')
    f = codecs.open(os.path.join(dataDir,'belgzip.csv'),'rb',"cp850")
    r = csv.reader(f)
    r.next()
    #cities = be.cities
    #print cities
    for (name,zip) in r:
        q.appendRow(name=name,zipCode=zip,nation=be)
        #q.appendRow(name=name,zipCode=zip,nation_id='be')
        
    f.close()
    

    
