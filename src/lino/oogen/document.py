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


import sys, os
import zipfile
import tempfile

#from lino.ui import console
from lino.oogen import elements
#from lino.oogen.generators import OoText, OoSpreadsheet
from lino.oogen.ifiles import IFILES

class Document:
    extension = NotImplementedError
    mimetype = NotImplementedError
    officeClass = NotImplementedError
    #bodyClass = NotImplementedError
    
    def __init__(self,filename):
        self.body = elements.Body() # self.bodyClass(self)
            
        self.fonts = elements.Fonts()
        self.styles = elements.Styles()
        self.autoStyles = elements.AutoStyles()
        self.masterStyles = elements.MasterStyles()
        
        self.createFonts()
        self.createStyles()
        self.createAutoStyles()
        self.createMasterStyles()
        self.elements = elements # used in pds scripts

        
        self.tempDir = tempfile.gettempdir()

        if not filename.lower().endswith(self.extension):
            filename += self.extension
        self.filename = filename
        
        self.ifiles = tuple([cl(self) for cl in IFILES])
        
        
        
    def addFont(self,**kw):
        x = elements.Font(**kw)
        self.fonts.append(x)
        return x
        
    def createFonts(self):
        
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

    def addStyle(self,**kw):
        s = elements.Style(**kw)
        self.styles.append(s)
        return s
        
    def addAutoStyle(self,**kw):
        s = elements.Style(**kw)
        self.autoStyles.append(s)
        return s

    def getStyle(self,name,family):
        try:
            return self.autoStyles.peek(name,family)
        except elements.InvalidRequest:
            return self.styles.peek(name,family)
        
    def createStyles(self):
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
        s.append(elements.Properties(marginTop="0cm",
                                     marginBottom="0.212cm"))
        self.styles.append(s)

        s = elements.DefaultStyle(family="table-cell")
        s.append(elements.Properties(decimalPlaces=2,
                                     fontName="Arial",
                                     language="en",country="US",
                                     tabStopDistance="1.25cm"))
        self.styles.append(s)
        
        s = elements.NumberStyle(name="N0",family="data-style")
        s.append(elements.Number(minIntegerDigits=1))
        self.styles.append(s)
        
        s = elements.CurrencyStyle(name="N106P0",
                                   family="data-style",
                                   volatile=True)
        s.append(elements.Number(decimalPlaces=2,minIntegerDigits=1,
                                 grouping=True))
        s.append(elements.Text("\n"))
        s.append(elements.CurrencySymbol("EUR",language="fr",country="BE"))
        self.styles.append(s)
        

        s = elements.CurrencyStyle(name="N106",
                                   family="data-style", volatile=True)
        s.append(elements.Number(decimalPlaces=2,
                                 minIntegerDigits=1,
                                 grouping=True))
        s.append(elements.Text(""))
        s.append(elements.CurrencySymbol(
            "EUR",language="fr",country="BE"))
        self.styles.append(s)
        

        self.styles.append(elements.Style(
            name="Default", family="table-cell", volatile=True))
        
        s = elements.Style(
            name="Result", family="table-cell",
            parentStyleName="Default")
        s.append(elements.Properties(
            fontStyle="italic",
            textUnderline="single",
            textUnderlineColor="font-color",
            fontWeight="bold"))
        self.styles.append(s)


        self.styles.append(elements.Style(
            name="Result2", family="table-cell",
            parentStyleName="Default", dataStyle="N106"))
        
        s = elements.Style(
            name="Heading", family="table-cell",
            parentStyleName="Default")
        s.append(elements.Properties(
            textAlign="center",textAlignSource="fix",
            fontSize="16pt",fontStyle="italic",
            fontWeight="bold"))
        self.styles.append(s)

        s = elements.Style(
            name="Heading1", family="table-cell",
            parentStyleName="Heading")
        s.append(elements.Properties(direction="ltr",
                                     rotationAngle=90))
        self.styles.append(s)

    def setPageProperties(self,**kw):
        self.pageProperties.setAttribs(**kw)

    def setHeaderProperties(self,**kw):
        self.headerProperties.setAttribs(**kw)

    def setFooterProperties(self,**kw):
        self.footerProperties.setAttribs(**kw)


    def createAutoStyles(self):
        
        pm = elements.PageMaster(name="pm1")
        self.autoStyles.append(pm)
        #pm.append(elements.Properties(writingMode="lr-tb"))
        
        self.pageProperties = elements.Properties(
            pageWidth="20.999cm",
            pageHeight="29.699cm",
            numFormat="1", 
            printOrientation="portrait", 
            marginTop="2cm",
            marginBottom="2cm",
            marginLeft="2cm",
            marginRight="2cm",
            footnoteMaxHeight="0cm",
            writingMode="lr-tb",
            )
            
        pm.append(self.pageProperties)
        pm.append(elements.FootnoteSep(
            width="0.018cm", distanceBeforeSep="0.101cm", 
            distanceAfterSep="0.101cm", adjustment="left",
            relWidth="25%", color="#000000"))
        
        h = elements.HeaderStyle()
        self.headerProperties = elements.Properties(
            minHeight="0.751cm",
            marginLeft="0cm",marginRight="0cm",
            marginBottom="0.25cm")
        h.append(self.headerProperties)
        pm.append(h)
        
        h = elements.FooterStyle()
        self.footerProperties = elements.Properties(
            minHeight="0.751cm",marginLeft="0cm",
            marginRight="0cm",marginBottom="0.25cm")
        h.append(self.footerProperties)
        pm.append(h)
        
        if False:
            pm = elements.PageMaster(name="pm2")
            self.autoStyles.append(pm)
            pm.append(elements.Properties(writingMode="lr-tb"))

            h = elements.HeaderStyle()
            pm.append(h)
            p = elements.Properties(
                minHeight="0.751cm",marginLeft="0cm",
                marginRight="0cm",marginBottom="0.25cm",
                border="0.088cm solid #000000",
                padding="0.018cm", backgroundColor="#c0c0c0")
            p.append(elements.BackgroundImage())
            h.append(p)

            h = elements.FooterStyle()
            pm.append(h)
            p = elements.Properties(
                minHeight="0.751cm",marginLeft="0cm",
                marginRight="0cm",marginBottom="0.25cm",
                border="0.088cm solid #000000",
                padding="0.018cm", backgroundColor="#c0c0c0")
            p.append(elements.BackgroundImage())
            h.append(p)

    def getHeader(self):
        """
        Examples:
         h = doc.getHeader()
         h.p("This is a simple paragraph in the header")
         
         
        writer ignores header if it contains regions!
        how to validate this?!
        
        """
        return self.headerContent
    
    def getFooter(self):
        return self.footerContent


    def createMasterStyles(self):
        
        mp = elements.MasterPage(name="Default",pageMasterName="pm1")
        self.masterStyles.append(mp)
        
        h = elements.Header()
        self.headerContent = h
        mp.append(h)
        #h.append(elements.P(elements.SheetName("???")))
##         if False:
##             h.append(elements.P("Here is a simple header"))
##         else:
##             h.append(elements.RegionLeft(elements.P("left header")))
##             h.append(elements.RegionCenter(elements.P("center header")))
##             h.append(elements.RegionRight(elements.P("right header")))
        
        mp.append(elements.HeaderLeft(display=False))
        
        f = elements.Footer()
        self.footerContent = f
        mp.append(f)
        #f.append(elements.P("Page ",elements.PageNumber("1")))
        
        mp.append(elements.FooterLeft(display=False))

        if False:
        
            mp = elements.MasterPage(name="Report",
                                     pageMasterName="pm2")
            self.masterStyles.append(mp)
            h = elements.Footer()
            mp.append(h)
            r = elements.RegionLeft(
                elements.P(elements.SheetName("???"),
                           "(",
                           elements.Title("???"),")"))
            h.append(r)
            r = elements.RegionRight(
                elements.P(
                    elements.Date("20/05/2004",
                                  dataStyleName="N2",
                                  dateValue="0-00-00"),
                    ",",
                    elements.Time("13:59:08")
                    ))
            h.append(r)
        
##     def report(self,**kw):
##         from lino.reports.oo import OoReport
##         return OoReport(self,**kw)

        
##     def generator(self,filename=None):
##         if filename is not None:
##             for cl in (OoText,OoSpreadsheet):
##                 if filename.lower().endswith(cl.extension):
##                     return cl(self,filename)
##         if len(self.tables) == len(self.children):
##             return OoSpreadsheet(self,filename)
##         return OoText(self,filename)
        
                
    def save(self,ui,showOutput=False):
        job = ui.job("Writing "+self.filename)
        for f in self.ifiles:
            f.writeFile()
        zf = zipfile.ZipFile(self.filename,'w', zipfile.ZIP_DEFLATED)
        for f in self.ifiles:
            zf.write(os.path.join(self.tempDir,f.filename),
                     f.filename)
        zf.close()
        job.done()

        if showOutput and ui.isInteractive():
            if sys.platform == "win32":
                os.system("start %s" % self.filename)
            else:
                ui.message("but how to start %s ?" % \
                           self.filename)

    
    def report(self,rpt,name=None,*args,**kw):
        if name is None: name=rpt.getLabel()
        rpt.beginReport(self)
        t = self.table(name=name)
        for col in rpt.columns:
            t.column()
        
        l = [ col.getLabel() for col in rpt.columns ]
        self.table.headerRow(*l)
        
        for row in rpt.iterator:
            cells = rpt.processRow(self,row)
            l = []
            for c in cells:
                if c.value is None:
                    l.append("")
                else:
                    l.append(c.col.format(c.value))
            self.table.row(*l)
        
        rpt.endReport(self)

    
        

class TextDocument(Document):
    
    extension = ".sxw"
    officeClass = "text"
    mimetype = "application/vnd.sun.xml.writer"
    #bodyClass = elements.TextBody
    
    def __init__(self,*args,**kw):
        Document.__init__(self,*args,**kw)
        self.tables = []
        
    def getTables(self):
        return self.tables
    
    def table(self,*args,**kw):
        t = self.body.table(self,*args,**kw)
        self.tables.append(t)
        return t

    def p(self,*args,**kw):
        return self.body.p(*args,**kw)
    def h(self,*args,**kw):
        return self.body.h(*args,**kw)
        

class SpreadsheetDocument(Document):
    
    extension = ".sxc"
    officeClass = "spreadsheet"
    mimetype = "application/vnd.sun.xml.calc"
    #bodyClass = elements.SpreadsheetBody
    

    def getTables(self):
        return self.body.children

    def table(self,*args,**kw):
        return self.body.table(self,*args,**kw)
        
    def p(self,*args,**kw):
        raise element.InvalidRequest(
            "Spreadsheet body contains only tables")
    
    def h(self,*args,**kw):
        raise elements.InvalidRequest(
            "Spreadsheet body contains only tables")
    
