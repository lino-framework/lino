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

import win32ui
import win32con

OEM_CHARSET = win32con.OEM_CHARSET

# OEM_FIXED_FONT = win32con.OEM_FIXED_FONT
# http://msdn.microsoft.com/library/default.asp?url=/library/en-us/gdi/fontext_3pbo.asp

from lino.ui import console
from lino.textprinter.document import Document

pt = 20
inch = 1440.0
mm = inch / 25.4
A4 = (210*mm, 297*mm)

# Note that in all modes, the point 0,0 is the upper left corner of
# the page, and the units increase as you go down and across the
# page. A Twip is 1/20 of a typesetting Point. A Point is 1/72 of an
# inch, so a Twip is 1/1440 of an inch.
        

class TextObject:
    def __init__(self,doc):
        self.doc = doc
        self.x = self.doc.org[0] + self.doc.margin
        self.y = self.doc.org[1] + self.doc.margin
        self.doc.dc.MoveTo(int(self.x),-int(self.y))
        #self.y = doc.pageHeight-(2*doc.margin)
        self.line = ""
        self.leading = 0
        
    def write(self,text):
        assert not "\n" in text, repr(text)
        assert not "\r" in text, repr(text)
        self.line += text

        font = win32ui.CreateFont(self.doc.fontDict)
        
        # CreateFont: http://msdn.microsoft.com/library/default.asp?url=/library/en-us/gdi/fontext_8fp0.asp
        
        self.doc.dc.SelectObject(font)
        tm = self.doc.dc.GetTextMetrics()
        #console.debug(repr(tm))
##         console.info(repr(self.dc.GetTextFace()))
##         console.info(repr(self.dc.GetViewportExt()))
##         console.info(repr(self.dc.GetViewportOrg()))
##         console.info(repr(self.dc.GetWindowExt()))
##         console.info(repr(self.dc.GetWindowOrg()))
        
        # http://msdn.microsoft.com/library/default.asp?url=/library/en-us/gdi/fontext_7ss2.asp
        
        self.leading = tm['tmExternalLeading'] \
                       + tm['tmHeight'] \
                       #+ tm['tmInternalLeading'] \

        # 
        #self.leading = max(self.leading,self.doc.status.leading)
        #self.doc.dc.TextOut(self.line)
        self.doc.dc.TextOut(int(self.x),-int(self.y),self.line)
        (dx,dy) = self.doc.dc.GetTextExtent(self.line)
        self.x += dx
        #console.debug("TextOut(%d,%d,%s)" % \
        #              (int(self.x),-int(self.y),repr(self.line)))
        self.line = ""

    def newline(self):
        #self.x = self.doc.margin
        self.x = self.doc.org[0] + self.doc.margin
        self.y += self.leading
        #self.doc.dc.MoveTo(int(self.x),-int(self.y))

class Win32PrinterDocument(Document):
    def __init__(self,printerName=None,
                 spoolFile=None,
                 cpi=12,
                 fontName="Courier New",
                 jobName="Win32PrinterDocument",
                 charset=None):
        Document.__init__(self,pageSize=A4,margin=5*mm)
        

        self.fontDict = {
            'name' : fontName
            }
        
        
        if charset is not None:
            self.fontDict['charset'] = charset

        
        self.dc = win32ui.CreateDC()
        self.dc.CreatePrinterDC(printerName)
        self.dc.StartDoc(jobName,spoolFile)
        self.dc.SetMapMode(win32con.MM_TWIPS)
        self.org = self.dc.GetWindowOrg()
        self.ext = self.dc.GetWindowExt()
        self.setCpi(cpi)
        
    def createTextObject(self):
        textobject = TextObject(self)
        #textobject.setFont("Courier", 10)
        return textobject
        
    def onBeginPage(self):
        self.dc.StartPage()
        if self.pageHeight < self.pageWidth:
            raise NotImplementedError
            #self.canvas.rotate(90)
            #self.canvas.translate(0,-210*mm)
    
    def onEndPage(self):
        self.dc.EndPage()
        
    def onSetPageSize(self):
        pass
            

    def onEndDoc(self):
        self.dc.EndDoc()
        del self.dc
            
    def setLpi(self,lpi):
        h = int(inch/lpi)
        #console.debug("%d lpi = %d twips" % (lpi,h))
        self.fontDict['height'] = h
        
    def setCpi(self,cpi):
        w = int(inch/cpi)
        #console.debug("%d cpi = %d twips" % (cpi,w))
        self.fontDict['width'] = w
        # self.fontDict['height'] = w
        self.width = int(
            (self.pageWidth-(self.margin*2))/inch*cpi)
        #print __name__, self.width
        
    def setItalic(self,ital):
        if ital:
            self.fontDict['italic'] = True
        else:
            self.fontDict['italic'] = None

    def setBold(self,bold):
        if bold:
            self.fontDict['weight'] = win32con.FW_BOLD
        else:
            self.fontDict['weight'] = win32con.FW_NORMAL
            
    def setUnderline(self,ul):
        if ul:
            self.fontDict['underline'] = True
        else:
            self.fontDict['underline'] = None
            
            
        # http://www.polyml.org/docs/Winref/Font.html
        ## name
        ## height
        #weight
        #italic
        #underline
        #pitch
        #family
        #charset
        
        #print self.status.leading
        #self.dc.SetTextFace("Courier")
        #self.textobject.setFont(psfontname,
        #                               self.status.size,
        #                               self.status.leading)

    def write(self,text):
        self.textobject.write(text)
            
        
    def newline(self):
        #self.textobject.flush()
        self.textobject.newline()
        #self.textobject = None
        
        
    def insertImage(self,line):
        raise NotImplementedError

