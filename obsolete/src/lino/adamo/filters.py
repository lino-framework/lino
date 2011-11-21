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

class Filter:
    def getLabel(self):
        raise NotImplementedError

class NotEmpty(Filter):
    
    def __init__(self,col):
        self.col=col
    
    def getLabel(self):
        return "'%s' not empty" % self.col.getLabel()

class IsEqual(Filter):
    def __init__(self,col,value):
        self.col=col
        self.value=value
    
    def getLabel(self):
        return "'%s' == %r" % (self.col.getLabel(),self.value)

class Contains(Filter):
    def __init__(self,col,value):
        self.col=col
        self.value=value
    
    def getLabel(self):
        return "'%s' contains %r" % (self.col.getLabel(),self.value)

class DateEquals(Filter):
    def __init__(self,col,year=None,month=None,day=None):
        self.col=col
        self.year=year
        self.month=month
        self.day=day
    
    def getLabel(self):
        return "'%s' == %s-%s-%s" % (
            self.col.getLabel(),
            self.year,self.month,self.day)

    

## class Master(Filter):
##     def __init__(self,col,slave):
##         self.col=col
##         self.slave=slave
    
