#coding: utf-8

## Copyright Luc Saffre 2004-2005.

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
oogen : generate OpenOffice documents programmatically

Bibliography:
-   http://books.evc-cit.info
    Using OpenOffice.org's XML Data Format
-   http://www.oooforum.org/forum/viewtopic.php?t=13861
    Opening 2 csv text files into OOo Calc as separate sheets
-   http://udk.openoffice.org/python/python-bridge.html
    Python-UNO bridge

"""

import sys, os
from lino.ui import console
from lino.oogen import elements
from lino.oogen.generators import OoText, OoSpreadsheet


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
        
        s = elements.Style(name="Standard",
                           family="paragraph",className="text")
        self.styles.append(s)
        s = elements.Style(name="Text body",
                           family="paragraph",
                           parentStyleName="Standard",
                           className="text")
        s.append(elements.Properties(marginTop="0cm",marginBottom="0.212cm"))
        self.styles.append(s)

        s = elements.DefaultStyle(family="table-cell")
        s.append(elements.Properties(decimalPlaces=2,fontName="Arial",language="en",country="US",tabStopDistance="1.25cm"))
        self.styles.append(s)
        
        s = elements.NumberStyle(name="N0",family="data-style")
        s.append(elements.Number(minIntegerDigits=1))
        self.styles.append(s)
        
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
        
    def report(self,**kw):
        from lino.reports.oo import OoReport
        return OoReport(self,**kw)
        
    def table(self,name=None,style=None,**kw):
        if name is None:
            name = "Table"+str(len(self.tables)+1)
        if style is None:
            style = name
        t = elements.Table(name,style,**kw)
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

    def generator(self,filename=None):
        if filename is not None:
            for cl in (OoText,OoSpreadsheet):
                if filename.lower().endswith(cl.extension):
                    return cl(self,filename)
        if len(self.tables) == len(self.story):
            return OoSpreadsheet(self,filename)
        return OoText(self,filename)
        
                
    def save(self,filename=None,showOutput=False):
        g = self.generator(filename)
        g.save()
        if showOutput and console.isInteractive():
            if sys.platform == "win32":
                os.system("start %s" % g.outputFilename)
            else:
                console.warning("but how to start %s ?" % \
                                g.outputFilename)

    
        

