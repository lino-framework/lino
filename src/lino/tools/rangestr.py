## Copyright 2005 Luc Saffre 

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

This module defines a single function rangestr() which expects a
sorted list of integers and returns a list of strings.

>>> rangestr([1,2,3,4,5])
['1-5']

>>> rangestr([1,2,3,5,6,7,8,9,10])
['1-3', '5-10']

>>> rangestr([])
[]

>>> rangestr([1])
['1']


TODO: Special cases with invalid input:

>>> rangestr([1,None,2])
['1', '2']

"""
def rangestr(l):
    r=[]
    n1=None
    n2=None
    for n in l:
        if n2 is None:
            if n1 is None: n1=n
            n2=n
        elif n == n2 + 1:
            n2=n
        else:
            r.append(n1n2(n1,n2))
            n1=n
            n2=None
    if n2 is not None:
        r.append(n1n2(n1,n2))
    return r

def n1n2(n1,n2):
    if n1 == n2:
        return str(n1)
    return "%s-%s" % (n1,n2)
            
    
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
