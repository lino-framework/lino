import os, types
from reportlab.platypus import \
	  SimpleDocTemplate, Paragraph,\
	  Spacer, Preformatted, \
	  Table, TableStyle, XPreformatted, Frame, Image, Flowable
	  
from reportlab.lib.units import mm

from lino.sdoc.document import Document
from lino.sdoc.renderer import Renderer
from lino.sdoc.environment import Body, Story
from lino.sdoc.tables import TableInstance, TableRow

from lino.sdoc.barcodes import BarcodeFlowable
from lino.sdoc.lists import ListInstance, ListStyle




class BackgroundPainter(Flowable):
	"""This is not actually drawn (i.e. it has zero height)
	but is executed when it would fit in the frame.	 Allows direct
	access to the canvas which is passed as first parameter.
	
	Instead of translating the canvas, storing it as an attribute of
	self and calling draw(), a user-defined function is called with the
	unmodified page canvas and x,y as arguments"""
		
	def __init__(self, func):
		self.func = func
	def __repr__(self):
		return "BackgroundPainter(%s)" % repr(self.func)
	def wrap(self, availWidth, availHeight):
		return (0,0)
	
	def draw(self):
		raise "don't call"

	def _drawOn(self,canv):
		raise "don't call"

	def drawOn(self, canvas, x, y, _sW=0):
		
		if _sW and hasattr(self,'hAlign'):
			a = self.hAlign
			if a in ['CENTER','CENTRE']:
				x = x + 0.5*_sW
			elif a == 'RIGHT':
				x = x + _sW
			elif a != 'LEFT':
				raise ValueError, "Bad hAlign value "+str(a)

		self.func(canvas,x,y)
		#canvas.saveState()
		#canvas.translate(x, y)
		#self._drawOn(canvas)
		#canvas.restoreState()




"""
Missing things in reportlab:

A "PageCount" field that returns the total number of pages in a
document. To be able to print "page 1 of 7"


"""



#IndexingFlowable
		
 
# from lino.sdoc import pds

# epsilon = 0.001



## class PdsDocTemplate(SimpleDocTemplate):

##		def afterInit(self):
##			"called from BaseDocTemplate.__init___()"
##			pass

##		def build(self):
##			SimpleDocTemplate.build(self,self.story)


## def myFirstPage(canvas, doc):
##		 canvas.saveState()
##		 #canvas.setStrokeColorRGB(1,0,0)
##		 #canvas.setLineWidth(5)
##		 #canvas.line(66,72,66,PAGE_HEIGHT-72)
##		 canvas.setFont('Times-Bold',16)
##		 canvas.drawString(108, doc.pagesize[1]-108, doc.title)
##		 # canvas.setFont('Times-Roman',9)
##		 # canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)
##		 canvas.restoreState()


class BulletListStyle(ListStyle):
	def getBulletText(self,listInstance):
		return '<font name="Symbol">'+chr(183)+'</font>'

## class Story:
##		def __init___(self,parent):
##			self._elements = []
##			self.parent = parent

##		def addElement(self,elem):
##			if elem is None:
##				return
##			if type(elem) is types.ListType:
##				self._elements += elem
##			else:
##				self._elements.append(elem)
	

## storyStack = []


class PdfRenderer(Renderer):

	outputExt = 'pdf'

	def __init__(self):
		self._story = []

##		def beginStory(self):
##			self._story = Story(self._story)

##		def endStory(e):
##			self._story = self._story.parent
##			#story = storyStack.pop()
##			#assert story.env is e
##			#return story

##		def addElement(elem):
##			self._story.addElement(elem) 

	def onBeginDocument(self,doc):
		self.document = doc
		self.rldoc = SimpleDocTemplate(self.getFilename())
		
		# overwrites the default UL 
		doc.stylesheet.UL = BulletListStyle(bulletWidth=12)

	def onEndDocument(self,doc):
		for k,v in doc.docstyle.items():
			setattr(self.rldoc,k,v)
		self.rldoc.build(self._story,
							  onFirstPage=self.drawPageHeader,
							  onLaterPages=self.drawPageHeader)
		# print "%d pages." % self.rldoc.page
		# del self._sdoc
	 


	def onBeginEnvironment(self,e):
		if isinstance(e,Body):
			pass # raise 'allowed only once'
		elif isinstance(e,TableInstance):
			assert not e.__dict__.has_key('_rows')
			e._rows = []
			#return 
		elif isinstance(e,TableRow):
			pass 
		elif isinstance(e,ListInstance):
			pass
		#elif isinstance(e,ListItem):
		#	 return 
		elif isinstance(e,BarcodeFlowable):
			pass
		elif isinstance(e,Story):
			pass
		else:
			raise '%s : unknown environment' % repr(e)

	def onEndEnvironment(self,e):
		if isinstance(e,Body):
			pass
			# self.render(e.getStory())
			# raise 'allowed only once'
			# return e.getStory()
		elif isinstance(e,TableInstance):
			e.getParent().toStory(self.compileTable(e))
		elif isinstance(e,TableRow):
			# print 'compileEndEnvironment.TableRow'
			table = e.getParent()
			assert table.__class__ is TableInstance
			row = e.cells
			table._rows.append(row)
		elif isinstance(e,ListInstance):
			pass
			#return None
		#elif isinstance(e,ListItem):
		#	 return self.compileListItem(e)
		elif isinstance(e,BarcodeFlowable):
			e.getParent().toStory(self.compileBarcode(e))
		elif isinstance(e,Story):
			pass
		else:
			raise '%s : unknown environment' % repr(e)

		
	def render(self,elem):
		if elem is None:
			return
		if type(elem) is types.ListType:
			self._story += elem
		else:
			self._story.append(elem)
			
		
	def getPageNumber(self):
		return self.rldoc.page


	def drawPageHeader(self, canvas, rldoc):
		assert rldoc == self.rldoc
		style = self.document.docstyle
		textWidth = self.document.getDocumentWidth()

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
		
	def drawFrame(self,canvas,func,
					  x,y,
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
		

	def setTitle(self,title):
		"Sets the document title. Does not print it."
		self.rldoc.title = title
		
	def getTitle(self):
		"Returns the document title."
		return self.rldoc.title


	def compilePara(self,txt,style):
		if style.wrap:
			elem = Paragraph(txt,style)
		else:
			elem = XPreformatted(txt,style)
		return elem



	def compileTable(self,tableInstance):

		colWidths = tableInstance.colWidths
		cellFormats = tableInstance.model.headerCellFormats \
						  + tableInstance.model.dataCellFormats
		rows = list(tableInstance._rows)
		
		if tableInstance.model.showHeaders:
			headerData = []
			for col in tableInstance.model.columns:
				if col.label is None:
					headerData.append("")
				else:
					headerData.append(col.label)
			rows.insert(0,headerData)

		if len(rows) == 0:
			return
	
		t = Table(rows,colWidths) #,repeatRows=repeatRows)
		# style of the flowable:
		t.style = tableInstance._flowStyle.child()
		t.setStyle(TableStyle(cellFormats))
		return t
			
	def compileImage(self,filename,width,height,paraStyle):
		elem = Image(filename,width,height)
		elem.style = style
		return elem

	def compileBarcode(self,barCodeSymbol,style):
		elem = BarcodeFlowable(barCodeSymbol)
		elem.style = style
		return elem

	def compileBackgroundPainter(self,func):
		elem = BackgroundPainter(func)
		#elem.style = style
		return elem


	# def compileTable(self,tableInstance):

	def compileListItem(self,txt,style,bulletText):
		if bulletText is None:
			return self.compilePara(txt,style)
		txt = '<bullet>' \
				+ bulletText \
				+ '</bullet>' + txt
		return self.compilePara(txt,style)

	def renderTag(self,tag):
		if tag == "tt":
			return '<font name="Courier">'
		elif tag == '/tt':
			return '</font>'


								 

##		def compileListItem(self,txt,style,bulletText):
##			txt = '<bullet>' \
##					+ bulletText \
##					+ '</bullet>' + txt
##			return self.compilePara(txt,style)

##		def compileEndList(self,listInstance):
##			return None # a listInstance is rendered by each item

##		def compileBeginList(self,listInstance):
##			return None # a listInstance is rendered by each item


