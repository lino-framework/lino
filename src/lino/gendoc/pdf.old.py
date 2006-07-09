## Copyright 2006 Luc Saffre 

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

import sys
import os
import types

from reportlab import platypus 
## from reportlab.platypus import \
##       SimpleDocTemplate, Paragraph,\
##       Spacer, Preformatted, \
##       Table, TableStyle, XPreformatted, Frame, Image, Flowable
      
from reportlab.lib.units import mm

#from lino.sdoc.pdf import PdfRenderer
#from lino.sdoc.environment import ParseError
#from lino.sdoc import commands

from lino.console.application import Application, UsageError


class Story:

    def __init__(self,stylesheet):
        self._elements = []
        self.stylesheet=stylesheet
        
    def append(self,elem):
        self._elements.append(elem)
        return elem
        
    def getDefaultParaStyle(self):
        return self._paraStyle


    def formatParagraph(self,**kw):
        # parent paragraph styles don't get updated by manual
        # formattings
        #self._paraStyle = self._paraStyle.child(**kw)
        s = self.getDefaultParaStyle()

        # print s
      
        # s is now usually equal to self._paraStyle, but not for
        # example in a TableRow where it could be the column's style
      
        for k,v in kw.items():
            setattr(s,k,v)

  
    def report(self,rpt):
        raise NotImplementedError

    def img(self,filename,
            width=None,height=None,
            style=None):
        if style is None:
            style = self.getDefaultParaStyle()
        elem = platypus.Image(filename,width,height)
        elem.style = style
        return self.append(elem)

    def table(self,*args,**kw):
        t = TableInstance(*args,**kw) 
        t = platypus.Table(rows,colWidths) #,repeatRows=repeatRows)
        # style of the flowable:
        # t.style = tableInstance._flowStyle.child()
        t.setStyle(TableStyle(cellFormats))


    def par(self,txt,style,wrap=True):
        try:
            txt.decode('utf8')
        except UnicodeDecodeError,e:
            print repr(txt)
            raise
        
        if wrap:
            elem = platypus.Paragraph(txt,style)
        else:
            elem = platypus.XPreformatted(txt,style)
            
        return self.append(elem)

    def pre(self,txt,style=None):
        if style is None:
            style = self.stylesheet.Code
        return self.append(platypus.Preformatted(txt,style))

    def heading(self,lvl,txt,**kw):
        self.par(txt,
                 style=self.getStyle["Heading"+str(lvl)],
                 **kw)

    def ul(self,*args,**kw):
        return self.append(UL(*args,**kw))
    
##     def li(self,*args,**kw):
##         return self.append(LI(*args,**kw))

    def getDocument(self):
        return None

    def beginStory(self):
        pass
    def endStory(self):
        pass
    


    

         
class Environment(Story):
   def __init__(self,
                doc,
                parent,
                width=None,
                flowStyle=None,
                paraStyle=None):
      """

      - parent : the environment to which this environment belongs

      - width : the outer width of this environment as a flowable.
      
      - flowStyle (or outer style) is the paragraph style of this
        Environment as a flowable inside its parent.
      
      - paraStyle (or inner style) is the default paragraph style for
        elements in this environment. Forwarded to BaseEnvironment.

      A ChildEnvironment dynamically inherits attributs from its
      parent. If somebody asks for some attribute from a
      ChildEnvironment, and if the ChildEnvironment does not have this
      attribut, then it will forward this request to its parent.
      
      """
      if paraStyle is None:
         paraStyle = parent.getDefaultParaStyle()
      BaseEnvironment.__init__(self,doc,paraStyle)
      
      self._parent = parent
      
      if flowStyle is None:
         flowStyle = parent.getDefaultParaStyle()
      self._flowStyle = flowStyle.child()
      self._flowStyle.setName("%s.flowStyle" % \
                              self.__class__.__name__)
      
      if width is None:
         width = parent.getTextWidth() \
                 - self._flowStyle.leftIndent \
                 - self._flowStyle.rightIndent # 20030417 - 20
      assert isnumber(width) 
      self.width = width

   
   def getFlowStyle(self):
      return self._flowStyle

   def getTextWidth(self):
      return self.width 
##       return self.width \
##              - self._flowStyle.leftIndent \
##              - self._flowStyle.rightIndent

#   def getRenderer(self):
#      # overridden by Story
#      return self._parent.getRenderer()


   def getParent(self):
      return self._parent
##       parent = self._parent
##       while True:
##          if parent is None or parent.__class__ == self.__class__:
##             return parent
##          parent = parent.getParent()

   def __getattr__(self,name):
      return getattr(self._parent,name)
   

class ListInstance(ChildEnvironment):
    def __init__(self,doc,
                 parent,width,listStyle,itemStyle):
      
        Environment.__init__(self,doc,parent,width,itemStyle)
        self.itemCount = 0
        self.listStyle = listStyle

        # dynamically create ParagraphStyle with the indentation
        # depending on the nesting level of the list:
        # TODO : manage _paraStyle for ListItem
        level = self.getListLevel()
        self._paraStyle = self._paraStyle.child(
            leftIndent=level * listStyle.bulletWidth,
            bulletIndent=(level-1)* listStyle.bulletWidth)
      

    def getListLevel(self):
        lvl = 1
        parent = self
        while True:
            parent = parent.getParent()
            if parent is None:
                return lvl
            elif parent.__class__ == self.__class__:
                lvl += 1


    def getBulletText(self):
        return self.listStyle.getBulletText(self)
      
    def li(self,txt):
        txt = self.document.feeder(txt)
        self.itemCount += 1
        bulletText = self.getBulletText()
        elem = self.document.renderer.compileListItem(
            txt,
            self._paraStyle,
            bulletText)
        self.toStory(elem)

##    def onBegin(self):
##       pass
##       #return self.getRenderer().compileBeginList(self)
   
##    def onEnd(self):
##       pass
##       #return self.getRenderer().compileEndList(self)

        



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












class TableRow(ElementContainer,Environment):
	def __init__(self, doc,
					 parent,
					 width=None,
					 flowStyle=None, paraStyle=None):
		#assert isinstance(parent,TableInstance)
		Environment.__init__(self,doc,
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
	






class TableInstance(ElementContainer,Environment):
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

		Environment.__init__(self, doc,
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

		



class Document:

    def __init__(self,
                 title="Untitled",
                 date=None,
                 stylesheet=None):

        self.title = title
        self.date = date
        #self.stylesheet = stylesheet
        if stylesheet is None:
            stylesheet=
        self.body=Story(self,stylesheet)
        
        
    def saveas(self,filename):
        self.rldoc = platypus.SimpleDocTemplate(filename)
        
        # overwrites the default UL 
        self.stylesheet.UL = BulletListStyle(bulletWidth=12)


        for k,v in self.body.stylesheet.Document.items():
            setattr(self.rldoc,k,v)
        self.rldoc.build(self.body,
                         onFirstPage=self.onEveryPage,
                         onLaterPages=self.onEveryPage)
        

    def getPageNumber(self):
        return self.rldoc.page


	def getDocumentWidth(self):
		return self.docstyle.pagesize[0] \
				 - self.docstyle.rightMargin \
				 - self.docstyle.leftMargin \
				 - 12
		""" -12 because Frame takes 6 pt padding on each side
		"""


    def onEveryPage(self, canvas, rldoc):
        assert rldoc == self.rldoc
        style = self.docstyle
        textWidth = self.getDocumentWidth()
        hs=Story(self.stylesheet)
        header=self.header(story)

        x = style.leftMargin
        y = style.pagesize[1] - style.topMargin # headerHeight
            
        # x and y are the bottom left corner of the frame. The
        # canvas' (0,0) is not the paper's (0,0) but the bottom left
        # corner of the printable area
            
        self.drawFrame(canvas, style.header,
                       x, y,
                       textWidth, style.topMargin, vAlign="BOTTOM")
        
        y = style.bottomMargin 
        self.drawFrame(canvas, style.footer,
                       x, y,
                       textWidth, style.bottomMargin, vAlign="TOP")
        
    def drawFrame(self,canvas,func,x,y,
                  textWidth,availableHeight,vAlign="TOP"):
        story = self.document.makeStory(func, textWidth)
        if story is not None:
            height = 0
            for e in story:
                unused,h = e.wrap(textWidth,availableHeight)
                height += h
                availableHeight -= h

            if vAlign == "BOTTOM":
                pass
            elif vAlign == "MIDDLE":
                y -= (height/2)
            elif vAlign == "TOP":
                y -= height

            canvas.saveState()
            f = Frame(x,y,
                         textWidth,height,
                         leftPadding=0,
                         rightPadding=0,
                         bottomPadding=0,
                         topPadding=0)
                         #showBoundary=True)
            f.addFromList(story,canvas)
            canvas.restoreState() 
        
    


class PdfMake(Application):

    name="Lino/PdfMake"

    copyright="""\
Copyright (c) 2006 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    
    url="http://lino.saffre-rumma.ee/pdfmake.html"
    
    usage="usage: lino pdfmake [options] [FILE]"
    
    description="""\

PdfMake creates a PDF file named FILE and then runs Acrobat Reader to
view it. Default for FILE is "tmp.pdf".

"""

    

    def run(self,body,ofname=None):
        if ofname is None:
            if len(self.args) > 0:
                ofname=self.args[0]
            else:
                ofname="tmp.pdf"
            
        renderer=PdfRenderer()

        try:
            commands.beginDocument(ofname,renderer)
            self.status(
                "Writing %s...",commands.getOutputFileName())
            try:
                body()
                commands.endDocument(
                    showOutput=self.isInteractive())
                self.notice("%d pages." % commands.getPageNumber())
            except ParseError,e:
                raise
                #traceback.print_exc(2)
                # print document
                # print e
                # showOutput = False


        except IOError,e:
            print e
            return -1

