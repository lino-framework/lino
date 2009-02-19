import types
from warnings import warn

from reportlab.lib import colors


from lino.sdoc.environment import ChildEnvironment, ElementContainer
from lino.sdoc.environment import ParseError
from lino.misc.pset import PropertySet
from lino.misc.etc import isnumber, issequence
#from lino.misc import debug

from reportlab.lib.enums import TA_LEFT, TA_RIGHT, \
	  TA_CENTER, TA_JUSTIFY

from lino.sdoc import PdsError

# from lino.sdoc import pds # .environment
# from pds import ParseError

epsilon = 0.001


colspecs = {
	'l' : TA_LEFT,
	'r' : TA_RIGHT,
	'c' : TA_CENTER,
	'j' : TA_JUSTIFY
	}


cellCommands = (
	'BACKGROUND',
	'GRID',
	'BOX',
	'OUTLINE',
	'INNERGRID',
	'LINEBELOW',
	'LINEABOVE',
	'LINEBEFORE',
	'LINEAFTER',
	'FONT',
	'FONTNAME', 'FACE',
	'SIZE', 'FONTSIZE',
	'LEADING',
	'TEXTCOLOR', 'COLOR',
	'ALIGN', 'ALIGNMENT',
	'VALIGN',
	'LEFTPADDING',
	'RIGHTPADDING',
	'TOPPADDING',
	'BOTTOMPADDING',
	)

def addCellFormats(formats,cmdName,tl,br,*params):
	if not cmdName in cellCommands:
		raise PdsError("Invalid cellformat '%s'" % cmdName)
	cmd = (cmdName,tl,br) + params
	formats.append(cmd)





class TableColumn:
	def __init__(self,
					 label=None,
					 width=None,
					 style=None,
					 **kw):
		#if label is None:
		#	 self.label = ""
		#else:
		self.label = label
		self.width = width
		self.style = style
##			if len(kw) > 0:
##				assert self.style is not None
##				for k,v in kw.items():
##					setattr(self.style,k,v)
	




class TableModel(PropertySet):
	defaults = {
		'columns' : [],
		'flowStyle' : None,
		'paraStyle' : None,
		'dataCellFormats' : [],
		'headerCellFormats' : [],
		'showHeaders' : False,
		'isgrowing' : True,
		}
	

	def addColumn(self,*args,**kw):
		col = apply(TableColumn,args,kw)
		# self.columns = list(self.columns)
		self.columns.append(col)
		if col.label is not None:
			self.showHeaders = True
			# print "true"
		# self.columns = columns


	def getColumnCount(self):
		return len(self.columns)
	
	def formatTable(self,cmdName,*params):
		# self.dataCellFormats = list(self.dataCellFormats)
		addCellFormats(self.dataCellFormats,
							cmdName,
							(0,0),
							(-1,-1),
							*params)
		
	def formatHeader(self,cmdName,*params):
		# self.headerCellFormats = list(self.headerCellFormats)
		addCellFormats(self.headerCellFormats,
							cmdName,
							(0,0),
							(-1,0),
							*params)
		
##		def beginTable(self,*args,**kw):
##			return document.beginTable(model=self,**kw)

##		def writeHeaders(self,ti):
##			if not self.showHeaders:
##				#print "don't"
##				return
##			ti.beginRow()
##			for col in self.columns:
##				if col.label is None:
##					ti.p("")
##				else:
##					ti.p(col.label)
##				ti.endCell()
##			#if document.getTableInstance().currentRow is not None:
##			ti.endRow()












class TableRow(ElementContainer,ChildEnvironment):
	def __init__(self, doc,
					 parent,
					 width=None,
					 flowStyle=None, paraStyle=None):
		#assert isinstance(parent,TableInstance)
		ChildEnvironment.__init__(self,doc,
										  parent,width,
										  flowStyle,paraStyle)
		self.cells = []
		self.currentCell = None
		self._colIndex = 0
		# _colIndex points to the column to be used for the next cell
		
	def __str__(self):
		return "TableRow(_colIndex=%d,cells=%s)" % \
				 (self._colIndex, repr(self.cells))
		
	def getCellCount(self):
		return len(self.cells)

	def getColIndex(self):
		return self._colIndex

	def beginCell(self):
		#debug.hello(self,'beginCell(%d)'%self._colIndex)
		if self.currentCell is not None:
			self.endCell()
		if self._colIndex >= self._parent.model.getColumnCount():
			if self._parent.model.isgrowing:
				self._parent.model.addColumn()
			else:
				raise "too many cells on this row"
		while self.getCellCount() <= self._colIndex:
			self.cells.append([]) 
		self.currentCell = self.cells[self._colIndex]
		
	def endCell(self):
		"""
		close this cell. next addElement() will call beginCell() 
		"""
		#debug.begin(self,"endCell()")
		if self.currentCell is None:
			self.beginCell()
		#if False:
		if len(self.currentCell) == 0:
			# empty cell : create at least one empty paragraph
			# to avoid reportlab.platypus.tables.py to make an
			# IndexError: list index out of range
			self.p("")
			assert len(self.currentCell) > 0
		# self.endEnvironment(self.currentCell)
		self.currentCell = None
		self._colIndex += 1
		
		# wrap back to the first column
		if not self._parent.model.isgrowing:
			if self._colIndex >= self._parent.getColumnCount():
				self._colIndex = 0
				#self._parent.endRow()
		#debug.end()
				

	def toStory(self,elem):
		# overrides ElementContainer.toStory
		"""
		sobald eine Table aktiv ist, wird die story abgefangen
		"""
		#debug.begin(self,'toStory(%s)' % str(elem))
		assert elem is not None
		if self.currentCell is None:
			self.beginCell()
			

		if type(elem) is types.ListType:
			self.currentCell += elem
		else:
			self.currentCell.append(elem)
		#debug.end()
			
	# overrides Environment
	def getTextWidth(self):
		"returns the textWidth of current column"
		self.computeColWidths()
		return self._parent.colWidths[self._colIndex] - 12

	def restartRow(self,toColumn=1):
		
		"""Alternative to endRow(). Skips back to the first column of
		the current row. Subsequent calls to addElement() will add into
		the same cells."""
		
		#assert self.currentRow is not None
		
##			if self.currentRow is None:
##				if len(self.rows) == 0:
##					# calling restartRow() at the very beginning of a Table
##					# makes not really sense but is tolerated.
##					self.currentRow = TableRow(self)
##				else:
##					# restartRow() after an endRow() is definitively
##					# tolerated. It undoes the endRow().
##					self.currentRow = self.rows.pop()
		
		self._colIndex = toColumn-1
		self.currentCell = None


	# overrides Environment
	def getDefaultParaStyle(self):
		"returns the default paragraph style in current cell"
		style = None
		if len(self._parent.model.columns) > self._colIndex:
			style = self._parent.model.columns[self._colIndex].style
		if style is None:
			# print "column style is None"
			return self._paraStyle # parent.getDefaultParaStyle()
		return style


	def beforeEnd(self):
		if self.currentCell is not None:
			self.endCell()


	def cell(self,txt):
		# ti = self.getTableInstance()
		self.beginCell()
		# txt = self.document.feeder(txt)
		self.p(txt)
		self.endCell()










## class TableCell(ChildEnvironment,ElementContainer):
##		def __init__(self,parent, width=None,
##						 flowStyle=None, paraStyle=None):
##			ChildEnvironment.__init__(self,parent,width,
##											  flowStyle,paraStyle)
##			ElementContainer.__init__(self)
	






class TableInstance(ElementContainer,ChildEnvironment):
	def __init__(self, doc,
					 parent,
					 columns, model, width,
					 flowStyle ):

		# TODO : make a copy of model.columns here so that
		# TableInstance.addColumn does not modify the model (?)
		# Currently this is done by child()ing the model...

		# self.rows = []
		self.currentRow = None
		self._rowIndex = -1

		if width is None:
			width = parent.getTextWidth()
			
		assert isnumber(width), "%s is not a number" % repr(width)
			
		assert isinstance(model,TableModel)
		
		# child() the model because updates to the table instance should
		# not update the TableModel
		self.model = model.child()
			
		if flowStyle is None:
			flowStyle = model.flowStyle

		ChildEnvironment.__init__(self, doc,
										  parent,width,
										  flowStyle,
										  self.model.paraStyle)
		
		if columns is not None:
			assert self.model.getColumnCount() is 0
			self.model.isgrowing = False
			# self.columns = []
			if issequence(columns):
				# it is a sequence of relative widths 
##					s = 0
##					for w in columns:
##						s += w
				s = reduce(lambda x, y: x+y, columns)
				# print s
				for w in columns:
					self.addColumn(width=w * self.width / s)
			elif type(columns) is types.StringType:
				# string of colspecs characters
				for c in columns:
					s = self._paraStyle.child(alignment=colspecs[c])
					s.setName("%s.defaultParaStyle" % \
								 c.__class__.__name__)
					
					self.addColumn(style=s)
			else:
				raise "%s : invalid colSpecs" % repr(columns)
		#else:
		#	 self.columns = list(self.model.columns)

		if self.model.getColumnCount() > 0:
			self.computeColWidths()
		#else:
		#	 print 'foo'
		#		  "beginTable() must specify the number of columns"
			
		
		"""make a copy using list() so that adding cell formats won't
		affect the style definition..."""
		#print cellFormats 
		# self.cellFormats = list(model.cellFormats)
		# self._colCount = 0


	def computeColWidths(self):

		# distribute free space to all columns whose width is None
		remainingWidth = self.width
		# print 'table width is %d' % self.width
		
		freeCount = 0	# number of columns whose width is None
		for col in self.model.columns:
			if col.width is None:
				freeCount += 1
			else:
				remainingWidth -= col.width
		if remainingWidth < 0:
			raise "remainingWidth %s is < 0" % repr(remainingWidth)
		
		if freeCount > 0:
			w = remainingWidth / freeCount
			
		self.colWidths = [] 
		for col in self.model.columns:
			if col.width is None:
				assert freeCount > 0
				self.colWidths.append(w-epsilon)
				# colWidths.append(w)
			else:
				self.colWidths.append(col.width-epsilon)

		self.model.isgrowing = False
					
		#return colWidths

##	  def getTextWidth(self):
##			try:
##				w = self.model.columns[self._colIndex].width
##			except IndexError:
##				w = None
##			if w is None:
##				if self.getColumnCount() > 0:
##					if self.currentCell is None:
##						self.beginCell()
##					w = self.width / self.getColumnCount()
			
		# what about cellPadding & Co? w should perhaps further be
		# modified... but okay for this time...
##			return w

		

	def __str__(self):
		return "TableInstance(_rowIndex=%d, currentRow=%s)" % \
				 (self._rowIndex,str(self.currentRow))
	
	def addColumn(self,*args,**kw):
		if self._rowIndex != -1:
			raise PdsError(
				"Cannot addColumn() when table data has started")
		self.model.addColumn(*args,**kw)
		# print self.model.showHeaders
		# ? self.computeColWidths()
		
	def formatTable(self,cmdName,*params):
		self.model.formatTable(cmdName,*params)
		
	def formatHeader(self,cmdName,*params):
		self.model.formatHeader(cmdName,*params)
		
	def beginRow(self):
		#debug.begin(self,'beginRow()')
		if self.currentRow is not None:
			self.endRow()
		assert self.currentRow is None
		
		self.currentRow = TableRow(
			self.document,
			self,
			paraStyle=self.getParent().getDefaultParaStyle())
		#self._colIndex = 0
		self._rowIndex += 1
		self.document.beginEnvironment(self.currentRow)
		#debug.end()
		
	def endRow(self):
		assert self.currentRow is not None
		if self.currentRow.currentCell is not None:
			self.currentRow.endCell()
			assert self.currentRow.currentCell is None
		#if self._colCount == 0:
		#	 self._colCount = self.currentRow.getCellCount()
		# assert self.getColumnCount() > 0, "table is empty"
		if self.model.isgrowing:
			self.computeColWidths()
			assert self.model.isgrowing is False
			assert self.currentRow.getCellCount() \
						 == self.model.getColumnCount()
		elif self.currentRow.getCellCount() \
				  != self.model.getColumnCount():
			raise ParseError, \
					"found %d instead of %d columns in row %d" \
					% (self.currentRow.getCellCount(), \
						self.getColumnCount(), self._rowIndex)
		#self.rows.append(self.currentRow)
		self.currentRow = None
		#self.currentCell = None
		self.document.endEnvironment(TableRow)


	def beginCell(self):
		"""It is allowed to make an explicit beginCell() in a table environment when no row has been started
		"""
		# note: This beginCell() is not necessary'
		assert self.currentRow is None
		# otherwise the beginCell would have been processed by the
		# currentRow
		self.beginRow()
		self.currentRow.beginCell()

	#def endCell(self):
	#	 assert self.currentRow is not None
	#	 self.currentRow.endCell()

##		def getDefaultParaStyle(self):
##			if self.currentRow is None:
##				# otherwise the beginCell is processed by the currentRow
##				self.beginRow()
##			return self.currentRow.getDefaultParaStyle()
		


	def toStory(self,elems):
		#debug.begin(self,'toStory(%s)' % str(elems))
		if self.currentRow is None:
			# otherwise the beginCell is processed by the currentRow
			self.beginRow()
		self.currentRow.toStory(elems)
##			else:
##				self.getParent().toStory(elems)
		#debug.end()
		
	def cell(self,txt):
		if self.currentRow is None:
			# otherwise the beginCell is processed by the currentRow
			self.beginRow()
		self.currentRow.cell()
		

	def tr(self,*args):
		if self.currentRow is not None:
			self.endRow()
		self.beginRow()
		for a in args:
			self.currentRow.cell(str(a))
		# self.endRow()
		
		
	def formatRow(self,cmdName,*params):
		if self._rowIndex == -1:
			raise PdsError(
				"Cannot formatRow() before the first row")
		rowIndex = self._rowIndex
		if self.model.showHeaders: rowIndex += 1
		addCellFormats(self.model.dataCellFormats,
							cmdName,
							(0,rowIndex),
							(-1,rowIndex),
							*params)
	def formatCell(self,cmdName,*params):
		rowIndex = self._rowIndex
		if self.model.showHeaders: rowIndex += 1
		addCellFormats(self.model.dataCellFormats,
							cmdName,
							(self.currentRow.getColIndex(),rowIndex),
							(self.currentRow.getColIndex(),rowIndex),
							*params)
		
	def formatColumn(self,cmdName,*params):
		addCellFormats(self.model.dataCellFormats,
							cmdName,
							(self.currentRow.getColIndex(),0),
							(self.currentRow.getColIndex(),-1),
							*params)

	def formatTable(self,cmdName,*params):
		self.model.formatTable(cmdName,*params)
##			addCellFormats(self.model.dataCellFormats,
##								cmdName,
##								(0,0),
##								(-1,-1),
##								*params)

	def getColumnCount(self):
		return len(self.colWidths)
	
	def getRowIndex(self):
		return self._rowIndex
		
	def onBegin(self):
		# self.model.writeHeaders(self)
		pass


	def beforeEnd(self):
		if self.currentRow is not None:
			self.currentRow.beforeEnd()
			self.endRow()
		if not hasattr(self,'colWidths'):
			self.computeColWidths()

		



class TablesMixin:
	"mix-in class for Document"

	def setupStyleSheet(self,sheet):
		sheet.define("DefaultTable", TableModel(dataCellFormats=[
			('ALIGN',(0,0),(-1,-1),'LEFT'),
			('VALIGN',(0,0),(-1,-1),'TOP'),
			('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
			('BOX', (0,0), (-1,-1), 0.25, colors.black),
			]))

		sheet.define("EmptyTable", TableModel( dataCellFormats=[
			('ALIGN',(0,0),(-1,-1),'LEFT'),
			('VALIGN',(0,0),(-1,-1),'TOP'),
			]))
		
		sheet.define("DataTable",TableModel(dataCellFormats=[
			('ALIGN',(0,0),(-1,-1),'LEFT'),
			('VALIGN',(0,0),(-1,-1),'TOP'),
			('LINEBELOW', (0,0), (-1,-1), 0.25, colors.black),
			('BOX', (0,0), (-1,-1), 0.25, colors.black),
			# ('BACKGROUND', (0,0), (-1,-1), colors.grey),
			]))


	def getTableInstance(self):
		return self.getEnvironment(TableInstance)
	
	def getDefaultTableModel(self):
		return self.stylesheet.DefaultTable #.child()
	
		

	def beginTable(self,columns=None,model=None,
						width=None,
						flowStyle=None):
		"""Starts a table instance.
		$model$ is an optional TableModel object.
		$columns$ is an optional column descriptor.
		$width$ defaults to getTextWidth()
		
		returns True so that you can put it in an if statement to
		to create indentation::
		
		  if beginTable():
			  ...
			  endTable()
		"""
		if model is None:
			model = self.getDefaultTableModel()
		# print "beginTable() : width is %s" % repr(width)
		ti = TableInstance(self,
								 self.getenv(),
								 columns,model,width,flowStyle)
		self.beginEnvironment(ti)
		return True

	def endTable(self):
		self.getTableInstance().beforeEnd()
		self.endEnvironment(TableInstance)

		

