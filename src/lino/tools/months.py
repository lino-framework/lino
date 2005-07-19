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

from types import IntType

class Month:
    
    def __init__(self,year,month):
        #assert month > 0 and month < 13
        self.year=year
        self.month=month

    def __str__(self):
        return "%02d/%d" % (self.month, self.year)

    def __repr__(self):
        return "Month(%d,%d)" % (self.year,self.month)

    def __add__(self, other):
        assert type(other) == IntType
        self.month += other
        if self.month > 12:
            q,r = divmod(self.month,12)
            self.year += q
            self.month = r
        return self
    
    def __sub__(self, other):
        if type(other) == IntType:
            return self.__add__(-other)
        return (self.year-other.year)*12 + (self.month - other.month)
    
    def __cmp__(self, other):
        if self.year > other.year: return 1
        if self.year < other.year: return -1
        if  self.month > other.month: return 1
        if  self.month < other.month: return -1
        return 0
    
        
