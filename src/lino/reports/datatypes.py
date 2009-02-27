## Copyright 2003-2009 Luc Saffre 

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


import datetime
import copy
from time import mktime, ctime
import types
#import decimals

from lino.tools.months import Month
from lino.misc.etc import ispure, iif
#from lino.adamo.exceptions import DataVeto
from lino.reports.constants import *

class DataVeto(Exception):
    "Invalid data submitted"



ERR_FORMAT_NONE = "caller must handle None values"
ERR_PARSE_EMPTY = "caller must handle empty strings"

class Type:
    """ Base class for all datatypes.
    """
    
    allowedClasses=None # list of allowed classes for value (None means anything accepted)
    defaultValue=None
    parser=lambda x: x 
    formatter=str
    halign=LEFT
    valign=TOP
    

    # sizes are given in "characters" or "lines"
    
    minHeight = 1
    maxHeight = 1
    
    def __init__(self,**kw):
        self.configure(**kw)
        
    def configure(self,valign=None,halign=None):
        if valign is not None:
            self.valign=valign
        if halign is not None:
            self.halign=halign
        
##     def configure(self,**kw):
##         "make sure that no new attribute gets created"
##         for k,v in kw.items():
##             assert hasattr(self,k), \
##                    "invalid keyword "+k
##             #assert self.__dict__.has_key(k), \
##             #       "invalid keyword "+k
##             self.__dict__[k] = v
##             # setattr(self,k,v)

    def __call__(self,**kw):
        child=copy.copy(self)
        child.configure(**kw)
        return child
        #return apply(self.__class__,[],kw)
        
    def __repr__(self):
        return "%s (%s)" % (self.__class__.__name__,
                            repr(self.__dict__))

    def format(self,v):
        """Convert a value of this type to a string.
        """
        assert v is not None, ERR_FORMAT_NONE
        return self.formatter(v)

    def parse(self,s):
        assert len(s), ERR_PARSE_EMPTY
        return self.parser(s)

    def validate(self,value):
        if self.allowedClasses is None: return
        if value.__class__ in self.allowedClasses: return
        raise TypeError("%r is not a valid %s" % (value,self))
            
    
class WidthType(Type):
    defaultWidth=50
    minWidth=15
    maxWidth=50
    
    def configure(self,width=None,minWidth=None,maxWidth=None, **kw):
        Type.configure(self,**kw)
        if width is not None:
            minWidth = maxWidth = width
            
        if maxWidth is not None:
            self.maxWidth = maxWidth
        if minWidth is not None:
            self.minWidth = minWidth
                
        
class IntType(WidthType):
    defaultValue=0
    defaultWidth=5
    minWidth=3
    maxWidth=7
    parser=int
    halign=RIGHT
    allowedClasses=(types.IntType,)
    
##     def parse(self,s):
##         assert len(s), ERR_PARSE_EMPTY
##         return int(s)

##     def validate(self,value):
##         if value.__class__ is types.IntType:
##             return
##         raise DataVeto("not an integer")
    


class BoolType(IntType):
    defaultValue=False
    parser=bool
    formatter=lambda s,x: iif(x,'X','-')
    allowedClasses=(types.BooleanType,)

##     def validate(self,value):
##         #print __name__,value
##         Type.validate(self,value)
        
class AutoIncType(IntType):
    pass



    
class LongType(IntType):
    parser=long
    allowedClasses=(types.LongType,)
    
class AsciiType(WidthType):
    defaultValue=""
    defaultWidth=20
    minWidth=1
    maxWidth=50
    allowedClasses=(types.StringType,)
    
    def parse(self,s):
        assert len(s), ERR_PARSE_EMPTY
        return str(s)
    
    def format(self,v):
        assert v is not None, ERR_FORMAT_NONE
        return v
        
    def validate(self,value):
        Type.validate(self,value)
        if len(value) == 0:
            raise DataVeto("Cannot store empty string.")
        if value.endswith(' '):
            raise DataVeto("%r ends with a space" % value)
            
    
class StringType(AsciiType):
    defaultValue=""
    defaultWidth=50
    minWidth=15
    maxWidth=50
    allowedClasses=(types.StringType,types.UnicodeType)
    
    def parse(self,s):
        assert len(s), ERR_PARSE_EMPTY
        return s
    
    def format(self,v):
        assert v is not None, ERR_FORMAT_NONE
        #return v
        return unicode(v)
        #return v.encode("cp1252",'replace')
        
    def validate(self,value):
        AsciiType.validate(self,value)
        if not ispure(value):
            raise DataVeto("%r is not pure" % value)
            
        
    
class PasswordType(StringType):
    def format(self,v):
        assert v is not None, ERR_FORMAT_NONE
        return '*' * len(v)
        
    


class MemoType(StringType):
    def configure(self,
                 height=None,
                 minHeight=4,maxHeight=10,
                 **kw):
        if height is not None:
            minHeight = maxHeight = height
        self.minHeight = minHeight
        self.maxHeight = maxHeight
        StringType.configure(self,**kw)

        
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
            #raise repr(value)+" is not a date"
            raise DataVeto("not a date")

class MonthType(Type):
    maxWidth = 7
    minWidth = 7
    
    def parse(self,s):
        assert len(s), ERR_PARSE_EMPTY
        return Month.parse(s)
##         s = s.replace(".","-")
##         s = s.replace("/","-")
##         l = s.split("-")
##         if len(l) == 2:
##             l = map(int,l)
##             return Month(*l)
##         elif len(l) == 1:
##             assert len(s) == 6, repr(s)
##             y = int(s[0:4])
##             m = int(s[4:6])
##             return Month(y,m)
##         else:
##             raise ValueError, repr(s)
    
    def format(self,v):
        assert v is not None, ERR_FORMAT_NONE
        return str(s)
    
    def validate(self,value):
        if not isinstance(value,datetime.date):
            #raise repr(value)+" is not a date"
            raise DataVeto("not a date")

    
class TimeType(Type):
    maxWidth = 8
    minWidth = 8
    def parse(self,s):
        assert len(s), ERR_PARSE_EMPTY
        l = s.split(":")
        if len(l) > 4:
            raise ValueError, repr(s)
        if len(l) < 1:
            return stot(s)
        l = map(int,l)
        return datetime.time(*l)
    
    def format(self,v):
        assert v is not None, ERR_FORMAT_NONE
        return str(v)[:self.maxWidth]

    def validate(self,value):
        if not isinstance(value,datetime.time):
            #raise repr(value)+" is not a time"
            raise DataVeto("not a time")


class TimeStampType(Type):
    maxWidth = 10
    minWidth = 10
    def parse(self,s):
        assert len(s), ERR_PARSE_EMPTY
        l=s.split()
        if len(l) == 2:
            d=DateType.parse(None,l[0])
            t=TimeType.parse(None,l[1])
            dt=datetime.datetime.combine(d,t)
            ts_tuple=dt.timetuple()
            return mktime(ts_tuple)
        raise ValueError, repr(s)
    
    def format(self,v):
        assert v is not None, ERR_FORMAT_NONE
        return ctime(v)
    
    def validate(self,value):
        if value.__class__ in (types.FloatType, types.IntType):
            return
        raise DataVeto("not a date")
##         if not isinstance(value,types.FloatType):
##             #raise repr(value)+" is not a date"
##             raise DataVeto("not a date")

    
        
            
    
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
            #raise DataVeto(repr(value)+" is not a timedelta")
            raise DataVeto("not a timedelta")



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


def itot(i):
    return stot(str(i))

def stot(s):
    if len(s) == 4:
        return datetime.time(int(s[0:2]),int(s[2:]))
    elif len(s) == 3:
        return datetime.time(int(s[0:1]),int(s[1:]))
    elif len(s) <= 2:
        return datetime.time(i)
    else:
        raise ValueError, repr(s)

def itod(i):
    return DATE.parse(str(i))
##     s=str(i)
##     assert len(s) == 8, repr(i)
##     y = int(s[0:4])
##     m = int(s[4:6])
##     d = int(s[6:8])
##     return datetime.date(y,m,d)

def stod(s):
    return DATE.parse(s)

def itom(i):
    return MONTH.parse(str(i))

def stom(s):
    return MONTH.parse(s)


ASTRING = AsciiType()
STRING = StringType()
PASSWORD = PasswordType()
MEMO = MemoType()     
DATE = DateType()     
MONTH = MonthType()
TIME = TimeType() # StringType(width=8)
TIMESTAMP = TimeStampType() 
DURATION = DurationType() 
INT = IntType() 
LONG = LongType() 
BOOL = BoolType()
AMOUNT = AmountType()
PRICE = PriceType()
ROWID = AutoIncType()
URL = UrlType(width=200)
EMAIL = EmailType(width=60)
IMAGE = ImageType()
LOGO = LogoType()
LANG = AsciiType(width=2)

__all__ = filter(lambda x: x[0] != "_", dir())
