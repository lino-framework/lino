#coding: utf-8
"""
oogen : generate OpenOffice documents programmatically

Bibliography:
-	http://books.evc-cit.info
	Using OpenOffice.org's XML Data Format
-	http://www.oooforum.org/forum/viewtopic.php?t=13861
	Opening 2 csv text files into OOo Calc as separate sheets
-	http://udk.openoffice.org/python/python-bridge.html
	Python-UNO bridge

"""
import zipfile
import os.path
opj = os.path.join

import elements
import ifiles

class Document:
	def __init__(self,name):
		self.name = name
		self.story = []
		self.tables = []
		
	#~ def toStory(self,elem):
		#~ assert hasattr(elem,'__xml__')
		#~ self.story.append(elem)
		
	def table(self,name=None,style=None,**kw):
		if name is None:
			name = "Table"+str(len(self.tables)+1)
		if style is None:
			style = name
		t = elements.Table(name,style)
		self.story.append(t)
		self.tables.append(t)
		return t
		
	def p(self,*args,**kw):
		p = elements.P(*args,**kw)
		self.story.append(p)
		return p
		
	def h(self,*args,**kw):
		h = elements.H(*args,**kw)
		self.story.append(h)
		return h
		


class OoGenerator:
	"base clase for OoText,OoSpreadsheet,..."
	extension = NotImplementedError
	mimetype = NotImplementedError
	
	def __init__(self,doc=None,filename=None):
		if doc is None:
			doc = Document()
		self.doc = doc
		
		if filename is None:
			filename = doc.name
		if not filename.endswith(self.extension):
			filename += self.extension
		self.tempDir = r'c:\temp'
		self.outputFilename = filename
		self.ifiles = tuple([cl(self) for cl in ifiles.IFILES])
		
	def save(self):
		for f in self.ifiles:
			f.writeFile()
		zf = zipfile.ZipFile(self.outputFilename,'w',zipfile.ZIP_DEFLATED)
		for f in self.ifiles:
			zf.write(opj(self.tempDir,f.filename),f.filename)
		zf.close()
		


class OoText(OoGenerator):
	extension = ".sxw"
	officeClass = "text"
	mimetype = "application/vnd.sun.xml.writer"
	
	def writeBody(self,wr):
		for elem in self.doc.story:
			elem.__xml__(wr)

class OoSpreadsheet(OoGenerator):
	extension = ".sxc"
	officeClass = "spreadsheet"
	mimetype = "application/vnd.sun.xml.calc"
		
	def writeBody(self,wr):
		for elem in self.doc.tables:
			elem.__xml__(wr)
