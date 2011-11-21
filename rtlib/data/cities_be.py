## Copyright 2003-2010 Luc Saffre 
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

"""
"""

import csv
import os
import codecs

if __name__ == "__main__":
    print "zip_code name"
    f = codecs.open('belgzip.csv','r',"cp850")
    r = csv.reader(f)
    r.next()
    for (name,zip) in r:
        print zip, " ", name
    f.close()
    

    
