# from lino.misc.pset import PropertySet
"""

an attempt to create a universally usable datatype definition model.

"""


class Type:
	"base class for containers of data-type specific meta information"
	
	def __init__(self,label=None,doc=None):
		self.label = label
		self.doc = doc
		
	def child(self,**kw):
		return apply(self.__class__,[],kw)
	
	def __repr__(self):
		return "%s (%s)" % (self.__class__.__name__, repr(self.__dict__))

	def format(self,s):
		return repr(s)

## 	def render_value_html(self,value,renderer,fmt):
## 		return renderer.renderValue(request,value)
		
	
class StringType(Type):
	def __init__(self,width=50,**kw):
		Type.__init__(self,**kw)
		self.width = width

	def parse(self,s):
		return s
	
	def format(self,s):
		return str(s)
		
##		def expr2value(self,expr):
##			if(len(expr)==0) : return None;
##			return expr
##		def value2sql(self,value):
##			if len(value) == 0:
##				return 'NULL'
##			return '"' + value.replace('"',r'\"') + '"'

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
##		def expr2value(self,expr):
##			raise LinoError("Memo fields cannot be in header")

	

class DateType(Type):
	def parse(self,s):
		return ND(s)
##		def expr2value(self,expr):
##			if len(expr)==0 : return None
##			return expr
##		def value2sql(self,value):
##			return '"' + value + '"'


class IntType(Type):
	def __init__(self,width=5,**kw):
		Type.__init__(self,**kw)
		self.width = width
	def parse(self,s):
		return int(s)
##		def expr2value(self,expr):
##			if len(expr)==0 : return None
##			return int(expr)
##		def value2sql(self,value):
##			return str(value)

	

class AutoIncType(IntType):
	pass

class BoolType(IntType):
	pass


class AreaType(IntType):
	pass



## class QueryType(Type):
##		def expr2value(self,expr):
##			if len(expr)==0 : return None
##			return expr
##		def value2sql(self,value):
##			raise "value2sql"
	

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

