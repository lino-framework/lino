#coding: utf-8

def quote(text):
	assert not '"' in text
	return '"'+text+'"'

class CDATA:
	def __init__(self,text):
		self.text = text
	def __xml__(self,wr):
		wr(self.text)
		
class Element:
	elementname = None
	def __init__(self,**kw):
		self.attribs = kw
		assert self.elementname is not None, "tried to instanciate abstract class Element"
		
	def __xml__(self,wr):
		wr("<"+self.elementname)
		if len(self.attribs) > 0:
			for k,v in self.attribs.items():
				wr(' %s=%s' % (k,v))
		wr('/>')
		
class Container(Element):
	allowedChildren = (CDATA,Element)
	def __init__(self,content=None,**kw):
		Element.__init__(self,**kw)
		self.children = []
		if content is not None:
			if type(content) == type(''):
				self.append(self.allowedChildren[0](content))	
			else:
				for elem in content:
					self.append(elem)	
		
	def append(self,elem):
		#print self.allowedChildren
		for cl in self.allowedChildren:
			if isinstance(elem,cl):
				self.children.append(elem)
				return
		raise "%s not allowed in %s" % (str(elem.__class__),repr(self))
		
	def __xml__(self,wr):
		wr("<"+self.elementname)
		if len(self.attribs) > 0:
			for k,v in self.attribs.items():
				wr(' %s=%s' % (k,v))
		wr('>')
		for child in self.children:
			child.__xml__(wr)
		wr("</"+self.elementname+">" )
		

class Span(Container):
	elementname = "text:span"
	allowedChildren = (CDATA,)
		
		
class P(Container):
	allowedChildren = (Span,CDATA)
	elementname = "text:p"
	def __init__(self,content,style=None,**kw):
		if style is None:
			style = "Default"
		kw['text:style-name']=quote(style)
		Container.__init__(self,content,**kw)
		
		
class H(P):
	allowedChildren = (CDATA,)
	elementname = "text:h"
	def __init__(self,level,content,style=None,**kw):
		if style is None:
			style = "Heading "+str(level)
		kw['text:level']=quote(str(level))
		self.level = level
		P.__init__(self,content,style,**kw)
	
		
		
class TableColumn(Element):
	elementname = "table:table-column"
	
class TableCell(Container):
	allowedChildren = (P,Span,CDATA,Container)
	elementname = "table:table-cell"
	
class TableRow(Container):
	allowedChildren = (TableCell,)
	elementname = "table:table-row"

class Table(Container):
	allowedChildren = (TableColumn,TableRow)
	elementname = "table:table"
	def __init__(self,name,style,**kw):
		self.columns = []
		kw['table:name'] = quote(name)
		kw['table:style-name'] = quote(style)
		kw['style:family'] = quote("table")
		Container.__init__(self,**kw)

	def addColumn(self,*args,**kw):
		col = TableColumn(*args,**kw)
		self.columns.append(col)
		self.append(col)
		
	def addRow(self,cells,*args,**kw):
		assert len(cells) == len(self.columns)
		row = TableRow(*args,**kw)
		self.append(row)
		for cell in cells:
			if isinstance(cell,TableCell):
				row.append(cell)
			else:
				row.append(TableCell(cell))
		
	