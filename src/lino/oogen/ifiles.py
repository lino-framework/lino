#coding: utf-8

## Copyright 2004-2005 Luc Saffre

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
this module defines one class for each internal file of an oo document
"""
import os.path
opj = os.path.join

class InternalFile:
	filename = NotImplementedError
	def __init__(self,doc):
		#assert isinstance(gen,OoGenerator)
		self.doc = doc
		
	def writeFile(self):
		f = open(opj(self.doc.tempDir,self.filename),"w")
		self.writeInternalContent(f)
		f.close()
		
	def writeInternalContent(self,f):
		raise NotImplementedError
		

class InternalXmlFile(InternalFile):
	#doctype=NotImplementedError
	def writeInternalContent(self,f):
		f.write("""\
<?xml version="1.0" encoding="utf-8"?>
""")
		self.writeXmlContent(f)

	def writeXmlContent(self,f):
		raise NotImplementedError
		
		
class MIMETYPE(InternalFile):
	filename = 'mimetype'
	def writeInternalContent(self,f):
		f.write(self.doc.mimetype+"\n")
		
	
class MANIFEST(InternalXmlFile):
	filename = 'manifest.xml'
	#doctype = 'manifest:manifest'
	def writeXmlContent(self,f):
		f.write("""\
<!DOCTYPE %s PUBLIC "-//OpenOffice.org//DTD Manifest 1.0//EN" "Manifest.dtd">
<manifest:manifest xmlns:manifest="http://openoffice.org/2001/manifest">
	<manifest:file-entry manifest:media-type="application/vnd.sun.xml.writer" manifest:full-path="/" />
	<manifest:file-entry manifest:media-type=""manifest:full-path="Pictures/" />
	<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml" />
	<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="styles.xml" />
	<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="meta.xml" />
	<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="settings.xml" />
</manifest:manifest>
""")

class META(InternalXmlFile):
	filename = 'meta.xml'
	#doctype = 'office:document-meta'
	def writeXmlContent(self,f):
		f.write("""\
<office:document-meta 
xmlns:office="http://openoffice.org/2000/office" xmlns:xlink="http://www.w3.org/1999/xlink" 
xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:meta="http://openoffice.org/2000/meta" office:version="1.0">
<office:meta>
<meta:generator>lino.oogen</meta:generator>
<meta:initial-creator>Luc Saffre</meta:initial-creator>
<meta:creation-date>2004-02-03T11:22:46</meta:creation-date>
<dc:creator>Luc Saffre</dc:creator>
<dc:date>2004-05-20T13:59:07</dc:date>
<dc:language>en-US</dc:language>
<meta:editing-cycles>26</meta:editing-cycles>
<meta:editing-duration>PT5H35M34S</meta:editing-duration>
<meta:user-defined meta:name="Info 1"/>
<meta:user-defined meta:name="Info 2"/>
<meta:user-defined meta:name="Info 3"/>
<meta:user-defined meta:name="Info 4"/>
<meta:document-statistic meta:table-count="3" meta:cell-count="188"/>
</office:meta>
</office:document-meta>
		""")
		
		
		
class SETTINGS(InternalXmlFile):
	filename = 'settings.xml'
	#doctype = 'office:document-settings'
	def writeXmlContent(self,f):
		f.write("""\
<!DOCTYPE office:document-settings PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "office.dtd">
<office:document-settings 
	xmlns:office="http://openoffice.org/2000/office" 
		xmlns:xlink="http://www.w3.org/1999/xlink" 
		xmlns:config="http://openoffice.org/2001/config" 
	office:version="1.0">
<office:settings>
</office:settings>
</office:document-settings>
		""")
		
		
class STYLES(InternalXmlFile):
	filename = 'styles.xml'
	#doctype = 'office:document-styles'
	def writeXmlContent(self,f):
		f.write("""\
<!DOCTYPE office:document-styles PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "office.dtd">		
<office:document-styles 
xmlns:office="http://openoffice.org/2000/office" 
xmlns:style="http://openoffice.org/2000/style" 
xmlns:text="http://openoffice.org/2000/text" 
xmlns:table="http://openoffice.org/2000/table" 
xmlns:draw="http://openoffice.org/2000/drawing" 
xmlns:fo="http://www.w3.org/1999/XSL/Format" 
xmlns:xlink="http://www.w3.org/1999/xlink" 
xmlns:number="http://openoffice.org/2000/datastyle" 
xmlns:svg="http://www.w3.org/2000/svg" 
xmlns:chart="http://openoffice.org/2000/chart" 
xmlns:dr3d="http://openoffice.org/2000/dr3d" 
xmlns:math="http://www.w3.org/1998/Math/MathML" 
xmlns:form="http://openoffice.org/2000/form" 
xmlns:script="http://openoffice.org/2000/script" 
office:version="1.0">
""")

		self.doc.fonts.__xml__(f.write)
		self.doc.styles.__xml__(f.write)
		self.doc.autoStyles.__xml__(f.write)
		self.doc.masterStyles.__xml__(f.write)
		
		f.write("""\n</office:document-styles>""")
		

	
class CONTENT(InternalXmlFile):
	filename = 'content.xml'
	#doctype = 'office:document-content'
	
	def writeXmlContent(self,f):
		f.write("""\
<!DOCTYPE office:document-content PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "office.dtd">
<office:document-content 
xmlns:office="http://openoffice.org/2000/office" 
xmlns:style="http://openoffice.org/2000/style" 
xmlns:text="http://openoffice.org/2000/text" 
xmlns:table="http://openoffice.org/2000/table" 
xmlns:draw="http://openoffice.org/2000/drawing" 
xmlns:fo="http://www.w3.org/1999/XSL/Format" 
xmlns:xlink="http://www.w3.org/1999/xlink" 
xmlns:number="http://openoffice.org/2000/datastyle" 
xmlns:svg="http://www.w3.org/2000/svg" 
xmlns:chart="http://openoffice.org/2000/chart" 
xmlns:dr3d="http://openoffice.org/2000/dr3d" 
xmlns:math="http://www.w3.org/1998/Math/MathML" 
xmlns:form="http://openoffice.org/2000/form" 
xmlns:script="http://openoffice.org/2000/script" 
office:class="%s"
office:version="1.0">
""" % self.doc.officeClass)
		self.doc.fonts.__xml__(f.write)
		self.doc.autoStyles.__xml__(f.write)
		self.doc.body.__xml__(f.write)
		#f.write("\n<office:body>")
		#self.gen.writeBody(f.write)
		#f.write("\n</office:body>")
		f.write("\n</office:document-content>")




IFILES = (MIMETYPE,MANIFEST,SETTINGS,META,STYLES,CONTENT)
