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

another attempt to create a universal datatype definition model...

"""

import datetime

from lino.misc.descr import Describable
from lino.adamo.exceptions import DataVeto

ERR_FORMAT_NONE = "caller must handle None values"
ERR_PARSE_EMPTY = "caller must handle empty strings"


class Type(Describable):
    "base class for containers of data-type specific meta information"

    # sizes are given in "characters" or "lines"
    minHeight = 1
    maxHeight = 1
    
    minWidth = 5
    maxWidth = 40
    
    def __init__(self,
                 minHeight=None,
                 maxHeight=None,
                 minWidth=None,
                 maxWidth=None,
                 **kw):
        Describable.__init__(self,**kw)
        
        if minHeight is not None:
            self.minHeight = minHeight
        if maxHeight is not None:
            self.maxHeight = maxHeight
        if minWidth is not None:
            self.minWidth = minWidth
        if maxWidth is not None:
            self.maxWidth = maxWidth
        
    def __call__(self,**kw):
        return apply(self.__class__,[],kw)
    
    def __repr__(self):
        return "%s (%s)" % (self.__class__.__name__,
                            repr(self.__dict__))

    def format(self,v):
        assert v is not None, ERR_FORMAT_NONE
        return repr(v)

    def parse(self,s):
        assert len(s), ERR_PARSE_EMPTY
        return s

    def validate(self,value):
        pass
    
##     def getPreferredWidth(self):
##         #note: for StringType, self.width is an instance variable, for
##         #other classes it is a class variable.
##         return self.width

##     def getMinSize(self):
##         return (self.minWidth
        
    
        
    
class StringType(Type):
    def __init__(self,width=50,**kw):
        self.minWidth = self.maxWidth = width
        if width > 20:
            self.minWidth = 20
        Type.__init__(self,**kw)

    def parse(self,s):
        assert len(s), ERR_PARSE_EMPTY
        return s
    
    def format(self,v):
        assert v is not None, ERR_FORMAT_NONE
        return str(v)
        
    
class PasswordType(StringType):
    def format(self,v):
        assert v is not None, ERR_FORMAT_NONE
        return '*' * len(v)
        
    


class MemoType(StringType):
    def __init__(self,height=4,**kw):
        self.minHeight = self.maxHeight = height
        if height > 10:
            self.minHeight = 10
        elif height < 10:
            self.maxHeight = 10
        StringType.__init__(self,**kw)
        #self.width = width
        #self.height = height
    

class IntType(Type):
    def __init__(self,width=5,**kw):
        self.minWidth = self.maxWidth = width
        Type.__init__(self,**kw)
        #self.width = width
        
    def parse(self,s):
        assert len(s), ERR_PARSE_EMPTY
        return int(s)

    
class DateType(Type):
    maxWidth = 10
    minWidth = 10
    def parse(self,s):
        assert len(s), ERR_PARSE_EMPTY
        s = s.replace(".","-")
        l = s.split("-")
        if len(l) == 3:
            l = map(int,l)
            return datetime.date(*l)
        elif len(l) == 1:
            assert len(s) == 8, repr(s)
            y = int(s[0:4])
            m = int(s[4:6])
            d = int(s[6:8])
            return datetime.date(y,m,d)
        else:
            raise ValueError, repr(s)
    def format(self,v):
        assert v is not None, ERR_FORMAT_NONE
        #return repr(v) # "[-]yyyymmdd"
        return v.isoformat()
    
    def validate(self,value):
        if not isinstance(value,datetime.date):
            raise repr(value)+" is not a date"
            #raise DataVeto(repr(value)+" is not a date")

    
class TimeType(Type):
    maxWidth = 8
    minWidth = 8
    def parse(self,s):
        assert len(s), ERR_PARSE_EMPTY
        l = s.split(":")
        if len(l) != 3:
            raise ValueError, repr(s)
        l = map(int,l)
        return datetime.time(*l)
    
    def format(self,v):
        assert v is not None, ERR_FORMAT_NONE
        return str(v)[:self.maxWidth]

    def validate(self,value):
        if not isinstance(value,datetime.time):
            raise repr(value)+" is not a time"
            #raise DataVeto(repr(value)+" is not a time")
            
    
class DurationType(Type):
    minWidth = 8
    maxWidth = 8
    fmt = "hh.mm.ss" # currently only possible fmt
    def parse(self,s):
        assert len(s), ERR_PARSE_EMPTY
        l = s.split(".")
        if len(l) == 3:
            hours = int(l[0])
            minutes = int(l[1])
            seconds = int(l[2])
            return datetime.timedelta(0,seconds,0,0,minutes,hours)
        elif len(l) == 2:
            minutes = int(l[0])
            seconds = int(l[1])
            return datetime.timedelta(0,seconds,0,0,minutes)
        else:
            raise ValueError, repr(s)
    def format(self,v):
        assert v is not None, ERR_FORMAT_NONE
        h = v.seconds / 3600
        m = (v.seconds - h * 3600) / 60
        s = v.seconds - h * 3600 - m*60
        return "%02d.%02d.%02d" % (h,m,s)

    def validate(self,value):
        if not isinstance(value,datetime.timedelta):
            raise DataVeto(repr(value)+" is not a timedelta")

class AutoIncType(IntType):
    pass

class BoolType(IntType):
    pass


class AreaType(IntType):
    pass

class UrlType(StringType):
    pass

class ImageType(StringType):
    pass

class LogoType(StringType):
    pass

class EmailType(StringType):
    pass

class AmountType(IntType):
    pass

class PriceType(IntType):
    pass

STRING = StringType()
PASSWORD = PasswordType()
MEMO = MemoType()     
DATE = DateType()     
TIME = TimeType() # StringType(width=8)
DURATION = DurationType() 
INT = IntType() 
BOOL = BoolType()
AMOUNT = AmountType()
PRICE = PriceType()
ROWID = AutoIncType()
URL = UrlType(width=200)
EMAIL = EmailType(width=60)
AREA = AreaType()
IMAGE = ImageType()
LOGO = LogoType()

__all__ = [
    'STRING',
    'PASSWORD',
    'MEMO',
    'DATE',
    'TIME',
    'DURATION',
    'INT',
    'BOOL',
    'AMOUNT',
    'PRICE',
    'ROWID',
    'URL',
    'EMAIL',
    'AREA',
    'IMAGE',
    'LOGO',
    ]

def itod(i):
    return stod(str(i))

def stod(s):
    return DATE.parse(s)

