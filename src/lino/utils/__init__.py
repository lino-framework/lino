## Copyright 2009 Luc Saffre
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
>>> constrain(-1,2,5)
2
>>> constrain(1,2,5)
2
>>> constrain(0,2,5)
2
>>> constrain(2,2,5)
2
>>> constrain(3,2,5)
3
>>> constrain(5,2,5)
5
>>> constrain(6,2,5)
5
>>> constrain(10,2,5)
5
"""
def constrain(value,lowest,highest):
    return min(highest,max(value,lowest))

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

