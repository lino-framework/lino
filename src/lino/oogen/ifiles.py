#coding: utf-8
"""
this module defines one class for each internal file of an oo document
"""
import os.path
opj = os.path.join

import elements

def writeXML(f,root,attribs={},children=[]):
	# this is completely useless
	f.write('<' + root)
	if len(attribs) > 0:
		for k,v in attribs.items():
			f.write(' %s=%s' % (k,v))
	f.write('>')
	for c in children:
		writeXML(f,c)
	f.write('</%s>' % root)


class InternalFile:
	def __init__(self,gen):
		#assert isinstance(gen,OoGenerator)
		self.gen = gen
		
	def writeFile(self):
		f = open(opj(self.gen.tempDir,self.filename),"w")
		self.writeInternalContent(f)
		f.close()
		
	def writeInternalContent(self,f):
		raise NotImplementedError
		
class MIMETYPE(InternalFile):
	filename = 'mimetype'
	def writeInternalContent(self,f):
		f.write(self.gen.mimetype+"\n")
		

class InternalXmlFile(InternalFile):
	def writeInternalContent(self,f):
		f.write("""\
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE %s PUBLIC "-//OpenOffice.org//DTD Manifest 1.0//EN" "Manifest.dtd">
""" % self.doctype)
		self.writeXmlContent(f)

	def writeXmlContent(self,f):
		raise NotImplementedError
		
		
		
	
class MANIFEST(InternalXmlFile):
	filename = 'manifest.xml'
	doctype = 'manifest:manifest'
	def writeXmlContent(self,f):
		f.write("""\
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
	doctype = 'office:document-meta'
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
	doctype = 'office:document-settings'
	def writeXmlContent(self,f):
		f.write("""\
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
	doctype = 'office:document-styles'
	def writeXmlContent(self,f):
		f.write("""\
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
		f.write("""\
<office:font-decls>
<style:font-decl style:name="Lucida Sans Unicode" fo:font-family="&apos;Lucida Sans Unicode&apos;" style:font-pitch="variable"/>
<style:font-decl style:name="Courier New" fo:font-family="'Courier New'" style:font-family-generic="modern" style:font-pitch="fixed"/>
<style:font-decl style:name="Tahoma" fo:font-family="Tahoma" style:font-pitch="variable"/>
<style:font-decl style:name="Times New Roman" fo:font-family="&apos;Times New Roman&apos;" style:font-family-generic="roman" style:font-pitch="variable"/>
<style:font-decl style:name="Arial" fo:font-family="Arial" style:font-family-generic="swiss" style:font-pitch="variable"/>
</office:font-decls>
""")
		f.write("""\
<office:styles>
<style:default-style style:family="table-cell">
<style:properties style:decimal-places="2" style:font-name="Arial" fo:language="en" fo:country="US" style:font-name-asian="Lucida Sans Unicode" style:language-asian="none" style:country-asian="none" style:font-name-complex="Tahoma" style:language-complex="none" style:country-complex="none" style:tab-stop-distance="1.25cm"/>
</style:default-style>
<number:number-style style:name="N0" style:family="data-style">
<number:number number:min-integer-digits="1"/>
</number:number-style>
<number:currency-style style:name="N106P0" style:family="data-style" style:volatile="true">
<number:number number:decimal-places="2" number:min-integer-digits="1" number:grouping="true"/>
<number:text> 
</number:text>
<number:currency-symbol number:language="fr" number:country="BE">EUR</number:currency-symbol>
</number:currency-style>
<number:currency-style style:name="N106" style:family="data-style">
<style:properties fo:color="#ff0000"/>
<number:text>-</number:text><number:number number:decimal-places="2" number:min-integer-digits="1" number:grouping="true"/><number:text> </number:text><number:currency-symbol number:language="fr" number:country="BE">EUR</number:currency-symbol><style:map style:condition="value()&gt;=0" style:apply-style-name="N106P0"/></number:currency-style><style:style style:name="Default" style:family="table-cell"/><style:style style:name="Result" style:family="table-cell" style:parent-style-name="Default"><style:properties fo:font-style="italic" style:text-underline="single" style:text-underline-color="font-color" fo:font-weight="bold"/></style:style><style:style style:name="Result2" style:family="table-cell" style:parent-style-name="Result" style:data-style-name="N106"/><style:style style:name="Heading" style:family="table-cell" style:parent-style-name="Default"><style:properties fo:text-align="center" style:text-align-source="fix" fo:font-size="16pt" fo:font-style="italic" fo:font-weight="bold"/></style:style><style:style style:name="Heading1" style:family="table-cell" style:parent-style-name="Heading"><style:properties fo:direction="ltr" style:rotation-angle="90"/></style:style>
</office:styles>
""")
		f.write("""\
<office:automatic-styles>
<style:page-master style:name="pm1">
	<style:properties style:writing-mode="lr-tb"/>
	<style:header-style>
		<style:properties fo:min-height="0.751cm" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-bottom="0.25cm"/>
	</style:header-style>
	<style:footer-style>
		<style:properties fo:min-height="0.751cm" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0.25cm"/>
	</style:footer-style>
</style:page-master>
<style:page-master style:name="pm2">
	<style:properties style:writing-mode="lr-tb"/>
	<style:header-style>
		<style:properties fo:min-height="0.751cm" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-bottom="0.25cm" 
			fo:border="0.088cm solid #000000" fo:padding="0.018cm" fo:background-color="#c0c0c0">
		<style:background-image/>
	</style:properties>
	</style:header-style>
<style:footer-style>
<style:properties fo:min-height="0.751cm" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0.25cm" 
	fo:border="0.088cm solid #000000" fo:padding="0.018cm" fo:background-color="#c0c0c0">
<style:background-image/>
</style:properties>
</style:footer-style>
</style:page-master>
</office:automatic-styles>
""")
		f.write("""\
<office:master-styles>
<style:master-page style:name="Default" style:page-master-name="pm1">
	<style:header>
		<text:p><text:sheet-name>???</text:sheet-name></text:p>
	</style:header>
	<style:header-left style:display="false"/>
	<style:footer><text:p>Page <text:page-number>1</text:page-number></text:p></style:footer>
	<style:footer-left style:display="false"/>
</style:master-page>
<style:master-page style:name="Report" style:page-master-name="pm2">
	<style:header>
		<style:region-left>
			<text:p>
				<text:sheet-name>???</text:sheet-name> (<text:title>???</text:title>)
			</text:p>
		</style:region-left>
		<style:region-right>
			<text:p>
				<text:date style:data-style-name="N2" text:date-value="0-00-00">20/05/2004</text:date>, 	<text:time>13:59:08</text:time></text:p></style:region-right></style:header><style:header-left style:display="false"/><style:footer><text:p>Page <text:page-number>1</text:page-number> / <text:page-count>99</text:page-count></text:p></style:footer><style:footer-left style:display="false"/>
</style:master-page>
</office:master-styles>
""")
		f.write("""\
</office:document-styles>
		""")
	
class CONTENT(InternalXmlFile):
	filename = 'content.xml'
	doctype = 'office:document-content'
	
	def writeXmlContent(self,f):
		f.write("""\
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
""" % self.gen.officeClass)
		f.write("""\
<office:automatic-styles>
</office:automatic-styles>
""")
		f.write("<office:body>")
		self.gen.writeBody(f.write)
		f.write("</office:body>")
		f.write("</office:document-content>")


IFILES = (MIMETYPE,MANIFEST,SETTINGS,META,STYLES,CONTENT)


