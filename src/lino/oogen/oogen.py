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
from ifiles import IFILES
#from styles import *


class Document:
	def __init__(self,name):
		self.name = name
		self.story = []
		self.tables = []
		self.fonts = elements.Fonts()
		self.styles = elements.Styles()
		self.autoStyles =elements.AutoStyles()
		self.masterStyles = elements.MasterStyles()
		self.populate()
		
	def addFont(self,**kw):
		x = elements.Font(**kw)
		self.fonts.append(x)
		return x
		
	#~ def toStory(self,elem):
		#~ assert hasattr(elem,'__xml__')
		#~ self.story.append(elem)
		
	def populate(self):
		
		self.addFont(
			name= "Tahoma1",
			fontFamily="Tahoma",
		)
		self.addFont(
			name= "Lucida Sans Unicode",
			fontFamily="&apos;Lucida Sans Unicode&apos;",
			fontPitch="variable",
		)
		self.addFont(
			name= "Tahoma",
			fontFamily="Tahoma",
			fontPitch="variable",
		)
		self.addFont(
			name="Courier New",
			fontFamily="'Courier New'",
			fontFamilyGeneric="modern",
			fontPitch="fixed",
		)
		self.addFont(
			name= "Times New Roman",
			fontFamily="&apos;Times New Roman&apos;",
			fontFamilyGeneric="roman",
			fontPitch="variable",
		)
		self.addFont(
			name= "Arial",
			fontFamily="Arial",
			fontFamilyGeneric="swiss",
			fontPitch="variable",
		)
		
		
		
#~ """
#~ <style:default-style style:family="paragraph">
#~ <style:properties style:use-window-font-color="true" style:font-name="Times New Roman" 
	#~ fo:font-size="12pt" fo:language="en" fo:country="US" 
		#~ style:font-name-asian="Lucida Sans Unicode" style:font-size-asian="12pt" style:language-asian="none" 
			#~ style:country-asian="none" 
		#~ style:font-name-complex="Tahoma" style:font-size-complex="12pt" style:language-complex="none" 
			#~ style:country-complex="none" 
		#~ fo:hyphenate="false" fo:hyphenation-remain-char-count="2" fo:hyphenation-push-char-count="2" 
		#~ fo:hyphenation-ladder-count="no-limit" 
			#~ style:text-autospace="ideograph-alpha" 
				#~ style:punctuation-wrap="hanging" 
					#~ style:line-break="strict" 
						#~ style:tab-stop-distance="1.251cm" 
							#~ style:writing-mode="page"/>
#~ </style:default-style>
#~ <style:style style:name="Standard" style:family="paragraph" style:class="text"/>
#~ -
	#~ <style:style style:name="Text body" style:family="paragraph" style:parent-style-name="Standard" style:class="text">
#~ <style:properties fo:margin-top="0cm" fo:margin-bottom="0.212cm"/>
#~ </style:style>		
#~ """
		
		s = elements.DefaultStyle(family="paragraph")
		s.append(elements.Properties(useWindowFontColor=True, 
			fontName="Times New Roman",
			fontSize="12pt",
			language="en", country="US",
			tabStopDistance="1.251cm",
			writingMode="page",
			hyphenate=False,
			hypenationRemainCharCount=2,
			hypenationPushCharCount=2,
			hypenationLadderCount="no-limit",
			textAutospace="ideograph-alpha",
			punctuationWrap="hanging",
			lineBreak="strict",
			))
		self.styles.append(s)
		
		s = elements.Style(name="Standard",family="paragraph",className="text")
		self.styles.append(s)
		s = elements.Style(name="Text body",family="paragraph",parentStyleName="Standard",className="text")
		s.append(elements.Properties(marginTop="0cm",marginBottom="0.212cm"))
		self.styles.append(s)

		#~ f.write("""\
#~ <style:default-style style:family="table-cell">
#~ <style:properties style:decimal-places="2" style:font-name="Arial" fo:language="en" fo:country="US" style:font-name-asian="Lucida Sans Unicode" style:language-asian="none" style:country-asian="none" style:font-name-complex="Tahoma" style:language-complex="none" style:country-complex="none" style:tab-stop-distance="1.25cm"/>
#~ </style:default-style>
#~ """)


		s = elements.DefaultStyle(family="table-cell")
		s.append(elements.Properties(decimalPlaces=2,fontName="Arial",language="en",country="US",tabStopDistance="1.25cm"))
		self.styles.append(s)
		
		#~ f.write("""\
#~ <number:number-style style:name="N0" style:family="data-style">
#~ <number:number number:min-integer-digits="1"/>
#~ </number:number-style>
#~ """)
		s = elements.NumberStyle(name="N0",family="data-style")
		s.append(elements.Number(minIntegerDigits=1))
		self.styles.append(s)
		
		#~ f.write("""\
#~ <number:currency-style style:name="N106P0" style:family="data-style" style:volatile="true">
#~ <number:number number:decimal-places="2" number:min-integer-digits="1" number:grouping="true"/>
#~ <number:text> 
#~ </number:text>
#~ <number:currency-symbol number:language="fr" number:country="BE">EUR</number:currency-symbol>
#~ </number:currency-style>
#~ """)
		s = elements.CurrencyStyle(name="N106P0", family="data-style", volatile=True)
		s.append(elements.Number(decimalPlaces=2,minIntegerDigits=1,grouping=True))
		s.append(elements.Text("\n"))
		s.append(elements.CurrencySymbol("EUR",language="fr",country="BE"))
		self.styles.append(s)
		
		#~ f.write("""\
#~ <number:currency-style style:name="N106" style:family="data-style">
#~ <style:properties fo:color="#ff0000"/>
#~ <number:text>-</number:text><number:number number:decimal-places="2" number:min-integer-digits="1" number:grouping="true"/><number:text> </number:text><number:currency-symbol number:language="fr" number:country="BE">EUR</number:currency-symbol><style:map style:condition="value()&gt;=0" style:apply-style-name="N106P0"/>
#~ </number:currency-style>
#~ """)

		s = elements.CurrencyStyle(name="N106", family="data-style", volatile=True)
		s.append(elements.Number(decimalPlaces=2,minIntegerDigits=1,grouping=True))
		s.append(elements.Text(""))
		s.append(elements.CurrencySymbol("EUR",language="fr",country="BE"))
		self.styles.append(s)
		
		#~ f.write("""\
#~ <style:style style:name="Default" style:family="table-cell"/>
#~ <style:style style:name="Result" style:family="table-cell" style:parent-style-name="Default">
#~ <style:properties fo:font-style="italic" style:text-underline="single" style:text-underline-color="font-color" fo:font-weight="bold"/>
#~ </style:style>
#~ """)
		self.styles.append(elements.Style(name="Default", family="table-cell", volatile=True))
		s = elements.Style(name="Result", family="table-cell", parentStyleName="Default")
		s.append(elements.Properties(fontStyle="italic",textUnderline="single",textUnderlineColor="font-color",fontWeight="bold"))
		self.styles.append(s)

		#~ f.write("""\
#~ <style:style style:name="Result2" style:family="table-cell" style:parent-style-name="Result" style:data-style-name="N106"/>
#~ <style:style style:name="Heading" style:family="table-cell" style:parent-style-name="Default">
#~ <style:properties fo:text-align="center" style:text-align-source="fix" fo:font-size="16pt" fo:font-style="italic" fo:font-weight="bold"/>
#~ </style:style>
#~ """)

		self.styles.append(elements.Style(name="Result2", family="table-cell", parentStyleName="Default", dataStyle="N106"))
		s = elements.Style(name="Heading", family="table-cell", parentStyleName="Default")
		s.append(elements.Properties(textAlign="center",textAlignSource="fix",fontSize="16pt",fontStyle="italic",fontWeight="bold"))
		self.styles.append(s)

		#~ f.write("""\
#~ <style:style style:name="Heading1" style:family="table-cell" style:parent-style-name="Heading">
#~ <style:properties fo:direction="ltr" style:rotation-angle="90"/>
#~ </style:style>
#~ """)
		s = elements.Style(name="Heading1", family="table-cell", parentStyleName="Heading")
		s.append(elements.Properties(direction="ltr",rotationAngle=90))
		self.styles.append(s)


		
		#~ f.write("""\
#~ <style:page-master style:name="pm1">
	#~ <style:properties style:writing-mode="lr-tb"/>
	#~ <style:header-style>
		#~ <style:properties fo:min-height="0.751cm" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-bottom="0.25cm"/>
	#~ </style:header-style>
	#~ <style:footer-style>
		#~ <style:properties fo:min-height="0.751cm" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0.25cm"/>
	#~ </style:footer-style>
#~ </style:page-master>
#~ """)
		pm = elements.PageMaster(name="pm1")
		self.autoStyles.append(pm)
		pm.append(elements.Properties(writingMode="lr-tb"))
		
		pm.append(elements.Properties(
			pageWidth="20.999cm", pageHeight="29.699cm", numFormat="1", 
			printOrientation="portrait", 
			marginTop="2cm",
			marginBottom="2cm",
			marginLeft="2cm",
			marginRight="2cm",
			writingMode="lr-tb",
			footnoteMaxHeight="0cm"))
		pm.append(elements.FootnoteSep(
			width="0.018cm", distanceBeforeSep="0.101cm", 
			distanceAfterSep="0.101cm", adjustment="left", relWidth="25%", color="#000000"))
		
		h = elements.HeaderStyle()
		h.append(elements.Properties(minHeight="0.751cm",marginLeft="0cm",marginRight="0cm",marginBottom="0.25cm"))
		pm.append(h)
		
		h = elements.FooterStyle()
		h.append(elements.Properties(minHeight="0.751cm",marginLeft="0cm",marginRight="0cm",marginBottom="0.25cm"))
		pm.append(h)
		
		#~ f.write("""\
#~ <style:page-master style:name="pm2">
	#~ <style:properties style:writing-mode="lr-tb"/>
	#~ <style:header-style>
		#~ <style:properties fo:min-height="0.751cm" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-bottom="0.25cm" 
			#~ fo:border="0.088cm solid #000000" fo:padding="0.018cm" fo:background-color="#c0c0c0">
		#~ <style:background-image/>
		#~ </style:properties>
	#~ </style:header-style>
	#~ <style:footer-style>
		#~ <style:properties fo:min-height="0.751cm" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0.25cm" 
			#~ fo:border="0.088cm solid #000000" fo:padding="0.018cm" fo:background-color="#c0c0c0">
			#~ <style:background-image/>
		#~ </style:properties>
		#~ </style:footer-style>
#~ </style:page-master>
#~ """)
		pm = elements.PageMaster(name="pm2")
		self.autoStyles.append(pm)
		pm.append(elements.Properties(writingMode="lr-tb"))
		
		h = elements.HeaderStyle()
		pm.append(h)
		p = elements.Properties(minHeight="0.751cm",marginLeft="0cm",marginRight="0cm",marginBottom="0.25cm",
			border="0.088cm solid #000000", padding="0.018cm", backgroundColor="#c0c0c0")
		p.append(elements.BackgroundImage())
		h.append(p)
		
		h = elements.FooterStyle()
		pm.append(h)
		p = elements.Properties(minHeight="0.751cm",marginLeft="0cm",marginRight="0cm",marginBottom="0.25cm",
			border="0.088cm solid #000000", padding="0.018cm", backgroundColor="#c0c0c0")
		p.append(elements.BackgroundImage())
		h.append(p)
		
		"""
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
				<text:date style:data-style-name="N2" text:date-value="0-00-00">20/05/2004</text:date>, 	
				<text:time>13:59:08</text:time>
			</text:p>
		</style:region-right>
	</style:header>
	<style:header-left style:display="false"/>
	<style:footer>
		<text:p>Page <text:page-number>1</text:page-number> / <text:page-count>99</text:page-count></text:p>
	</style:footer>
	<style:footer-left style:display="false"/>
</style:master-page>
"""
		mp = elements.MasterPage(name="Default",pageMasterName="pm1")
		self.masterStyles.append(mp)
		h = elements.Header()
		mp.append(h)
		h.append(elements.P(elements.SheetName("???")))
		mp.append(elements.HeaderLeft(display=False))
		f = elements.Footer()
		mp.append(f)
		f.append(elements.P("Page ",elements.PageNumber("1")))
		mp.append(elements.FooterLeft(display=False))
		
		mp = elements.MasterPage(name="Report",pageMasterName="pm2")
		self.masterStyles.append(mp)
		h = elements.Footer()
		mp.append(h)
		r = elements.RegionLeft(elements.P(elements.SheetName("???"),"(",elements.Title("???"),")"))
		h.append(r)
		r = elements.RegionRight(
			elements.P(
				elements.Date("20/05/2004",dataStyleName="N2",dateValue="0-00-00"),
				",",
				elements.Time("13:59:08")
				))
		h.append(r)
		
		
		
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
		
	def h(self,level,text,**kw):
		h = elements.H(level,text,**kw)
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
		self.ifiles = tuple([cl(self) for cl in IFILES])
		
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
