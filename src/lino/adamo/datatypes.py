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

from lino.misc.descr import Describable

ERR_FORMAT_NONE = "caller must handle None values"
ERR_PARSE_EMPTY = "caller must handle empty strings"


class Type(Describable):
    "base class for containers of data-type specific meta information"
    
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
    
        
    
class StringType(Type):
    def __init__(self,width=50,**kw):
        Type.__init__(self,**kw)
        self.width = width

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
    def __init__(self,width=50,height=4,**kw):
        Type.__init__(self,**kw)
        self.width = width
        self.height = height
    

class IntType(Type):
    def __init__(self,width=5,**kw):
        Type.__init__(self,**kw)
        self.width = width
        
    def parse(self,s):
        assert len(s), ERR_PARSE_EMPTY
        return int(s)

class DateType(Type):
    width = 8
    def parse(self,s):
        assert len(s), ERR_PARSE_EMPTY
        return ND(s)
    def format(self,v):
        assert v is not None, ERR_FORMAT_NONE
        return repr(v) # "[-]yyyymmdd"


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
TIME = StringType(width=8)
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
