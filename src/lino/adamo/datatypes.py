## Copyright Luc Saffre 2003-2005.

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


class Type:
    "base class for containers of data-type specific meta information"
    
    def __init__(self,label=None,doc=None):
        self.label = label
        self.doc = doc
        
    def child(self,**kw):
        return apply(self.__class__,[],kw)
    
    def __repr__(self):
        return "%s (%s)" % (self.__class__.__name__,
                            repr(self.__dict__))

    def format(self,s):
        return repr(s)

        
    
class StringType(Type):
    def __init__(self,width=50,**kw):
        Type.__init__(self,**kw)
        self.width = width

    def parse(self,s):
        return s
    
    def format(self,s):
        return str(s)
        
##      def expr2value(self,expr):
##          if(len(expr)==0) : return None;
##          return expr
##      def value2sql(self,value):
##          if len(value) == 0:
##              return 'NULL'
##          return '"' + value.replace('"',r'\"') + '"'

class PasswordType(StringType):
    def format(self,s):
        if s is None:
            return "None"
        return '*' * len(s)
    


class MemoType(StringType):
    def __init__(self,width=50,height=4,**kw):
        Type.__init__(self,**kw)
        self.width = width
        self.height = height
##      def expr2value(self,expr):
##          raise LinoError("Memo fields cannot be in header")

    

class IntType(Type):
    def __init__(self,width=5,**kw):
        Type.__init__(self,**kw)
        self.width = width
    def parse(self,s):
        return int(s)
##      def expr2value(self,expr):
##          if len(expr)==0 : return None
##          return int(expr)
##      def value2sql(self,value):
##          return str(value)


class DateType(Type):
    width = 8
    def parse(self,s):
        return ND(s)
##      def expr2value(self,expr):
##          if len(expr)==0 : return None
##          return expr
##      def value2sql(self,value):
##          return '"' + value + '"'


    

class AutoIncType(IntType):
    pass

class BoolType(IntType):
    pass


class AreaType(IntType):
    pass



## class QueryType(Type):
##      def expr2value(self,expr):
##          if len(expr)==0 : return None
##          return expr
##      def value2sql(self,value):
##          raise "value2sql"
    

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



class StartupDelay(Exception):
    pass

class InvalidRequestError(Exception):
    "The requested action was refused"
    #pass

class DataVeto(Exception):
    "Invalid data submitted"
    #pass

class DatabaseError(Exception):
    "dbd-specific exception was raised"

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

