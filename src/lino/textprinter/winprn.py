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
import win32print
import pywintypes
#import win32gui

from PIL import Image, ImageWin

#OEM_CHARSET = win32con.OEM_CHARSET

charsets = {
    "cp850" : win32con.OEM_CHARSET
    }

# OEM_FIXED_FONT = win32con.OEM_FIXED_FONT
# http://msdn.microsoft.com/library/default.asp?url=/library/en-us/gdi/fontext_3pbo.asp

from lino.ui import console
from lino.textprinter.textprinter import TextPrinter, PrinterNotReady, ParserError

pt = 20
inch = 1440.0
mm = inch / 25.4
A4 = (210*mm, 297*mm)

# Note that in all modes, the point 0,0 is the upper left corner of
# the page, and the units increase as you go down and across the
# page.
# We work in twips: self.dc.SetMapMode(win32con.MM_TWIPS)
# A Twip is 1/20 of a typesetting Point. A Point is 1/72 of an
# inch, so a Twip is 1/1440 of an inch.


# setLpi(6): 6 lines per inch means that leading must be 240.  If I
# ask height=240, then (for Courier New) I get a leading of 240+17=257
#
# leading = height * 257 / 240
# <=> height = leading * 240 / 257
#
# h = inch/lpi * 240 /257
# <=> h = (inch * 240 / 257) / lpi

LPIBASE = inch * 240 / 257 
        

## class TextObject:
##     def __init__(self,doc):
##         self.doc = doc
##         self.x = self.doc.org[0] + self.doc.margin
##         self.y = self.doc.org[1] + self.doc.margin
##         #self.doc.dc.MoveTo(int(self.x),-int(self.y))
##         #self.y = doc.pageHeight-(2*doc.margin)
##         self.line = ""
##         self.leading = 0
        
##     def write(self,text):
##         assert not "\n" in text, repr(text)
##         assert not "\r" in text, repr(text)
##         if self.doc.coding is not None:
##             #print "gonna code", repr(text)
##             #text = text.decode(self.coding)
##             text = text.encode(self.doc.coding)
##             #print "result:", repr(text)
##         self.line += text

##         font = win32ui.CreateFont(self.doc.fontDict)
        
##         # CreateFont: http://msdn.microsoft.com/library/default.asp?url=/library/en-us/gdi/fontext_8fp0.asp
        
##         self.doc.dc.SelectObject(font)
##         #console.debug(repr(tm))
## ##         console.info(repr(self.dc.GetTextFace()))
## ##         console.info(repr(self.dc.GetViewportExt()))
## ##         console.info(repr(self.dc.GetViewportOrg()))
## ##         console.info(repr(self.dc.GetWindowExt()))
## ##         console.info(repr(self.dc.GetWindowOrg()))
        
##         # http://msdn.microsoft.com/library/default.asp?url=/library/en-us/gdi/fontext_7ss2.asp
        
## ##         self.leading = tm['tmExternalLeading'] \
## ##                        + tm['tmHeight'] \
## ##                        #+ tm['tmInternalLeading'] \

##         # 
##         #self.leading = max(self.leading,self.doc.status.leading)
##         #self.doc.dc.TextOut(self.line)
##         console.debug("self.doc.dc.TextOut(%d,%d,%r)",
##                       int(self.x),-int(self.y),self.line)
##         self.doc.dc.TextOut(int(self.x),-int(self.y),self.line)
##         (dx,dy) = self.doc.dc.GetTextExtent(self.line)
        
##         # GetTextExtent() returns the dimensions of the string in
##         # logical units (twips)
        
##         self.x += dx
##         #console.debug("TextOut(%d,%d,%s)" % \
##         #              (int(self.x),-int(self.y),repr(self.line)))
##         if dy != 0:
##             self.leading = dy
##         self.line = ""
            
## ##         tm = self.doc.dc.GetTextMetrics()
## ##         console.debug(
## ##             "dy=%d, leading=%d, extLeading=%d, height=%d, intLeading=%d",
## ##             dy, self.leading,
## ##             tm['tmExternalLeading'],tm['tmHeight'],
## ##             tm['tmInternalLeading'])
                      

##     def flush(self):
##         self.write("")

##     def newline(self):
##         #self.x = self.doc.margin
##         self.x = self.doc.org[0] + self.doc.margin
##         self.y += self.leading
##         #self.doc.dc.MoveTo(int(self.x),-int(self.y))
##         console.debug("self.y += %d" % self.leading)

class Win32TextPrinter(TextPrinter):
    
    def __init__(self,printerName=None,
                 spoolFile=None,
                 cpi=12,
                 lpi=6,
                 fontName="Courier New",
                 jobName="Win32PrinterDocument",
                 coding=None):
        
        TextPrinter.__init__(self,pageSize=A4,margin=5*mm)

        self.fontDict = {
            'name' : fontName
            }
        
        
        if coding is not None:
            self.fontDict['charset'] = charsets[coding]

        self.coding = coding
        self.font = None
        
        self.dc = win32ui.CreateDC()
        self.dc.CreatePrinterDC(printerName)



##         while True:
##             h = win32print.OpenPrinter(win32print.GetDefaultPrinter())
##             t = win32print.GetPrinter(h)
##             win32print.ClosePrinter(h)


##             if t[18]:
##                 break
##             print t
##             if not console.confirm("not ready. retry?"):
##                 raise PrinterNotReady
        
##             # structure of t:
##             # http://msdn.microsoft.com/library/default.asp?\
##             #   url=/library/en-us/gdi/prntspol_9otu.asp

##             """
##             ('\\\\KYLLIKI',
##              '\\\\KYLLIKI\\Samsung ML-1200 Series',
##              'ML-1200',
##              'LPT1:',
##              'Samsung ML-1200 Series',
##              'Samsung ML-1210/ML-1220M',
##              '', None, '', 'WinPrint',
##              'RAW', '', None, 24, 1, 0, 0, 0, 0, 1, 0)
##              """

##         only on win95:
##         try:
##             h = win32print.EnumPrinters(win32print.PRINTER_ENUM_DEFAULT)
##         except pywintypes.error,e:
##             raise PrinterNotReady

        try:
            self.dc.StartDoc(jobName,spoolFile)
        except win32ui.error,e:
            raise PrinterNotReady
        self.dc.SetMapMode(win32con.MM_TWIPS)
        self.org = self.dc.GetWindowOrg()
        self.ext = self.dc.GetWindowExt()
        self.setCpi(cpi)
        #self.setLpi(lpi)

        self.x = self.org[0] + self.margin
        self.y = self.org[1] + self.margin
        #self.doc.dc.MoveTo(int(self.x),-int(self.y))
        #self.y = doc.pageHeight-(2*doc.margin)
        self.line = ""
        self.leading = 0
        
        
        
##     def createTextObject(self):
##         textobject = TextObject(self)
##         #textobject.setFont("Courier", 10)
##         return textobject
        
    def onBeginPage(self):
        self.dc.StartPage()
        #self.drawDebugRaster()
        if self.pageHeight < self.pageWidth:
            console.warning("Portrait orientation not yet supported!")
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
        h = int(LPIBASE / lpi)
        #h = int(inch/lpi)
        #console.debug("%d lpi = %d twips" % (lpi,h))
        #self.fontDict['height'] = h
        #self.leading = int(inch/lpi)
        
    def setCpi(self,cpi):
        w = int(inch/cpi)
        #console.debug("%d cpi = %d twips" % (cpi,w))
        self.fontDict['width'] = w
        # self.fontDict['height'] = w
        self.cpl = int(self.lineWidth()/inch*cpi)
            #(self.pageWidth-(self.margin*2))/inch*cpi)
        #print __name__, self.width
        self.font = None
        
    def setItalic(self,ital):
        if ital:
            self.fontDict['italic'] = True
        else:
            self.fontDict['italic'] = None
        self.font = None

    def setBold(self,bold):
        if bold:
            self.fontDict['weight'] = win32con.FW_BOLD
        else:
            self.fontDict['weight'] = win32con.FW_NORMAL
        self.font = None
            
    def setUnderline(self,ul):
        if ul:
            self.fontDict['underline'] = True
        else:
            self.fontDict['underline'] = None
        self.font = None
            
            
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

##     def write(self,text):
##         self.textobject.write(text)
            
        
##     def newline(self):
##         #self.textobject.flush()
##         self.textobject.newline()
##         #self.textobject = None

        
    def write(self,text):
        assert not "\n" in text, repr(text)
        assert not "\r" in text, repr(text)
        if self.coding is not None:
            #print "gonna code", repr(text)
            #text = text.decode(self.coding)
            text = text.encode(self.coding)
            #print "result:", repr(text)
        self.line += text

        if self.font is None:
            self.font = win32ui.CreateFont(self.fontDict)
        
            # CreateFont: http://msdn.microsoft.com/library/default.asp?url=/library/en-us/gdi/fontext_8fp0.asp
        
            self.dc.SelectObject(self.font)
            console.debug("select font %s",self.fontDict)
            
        #console.debug(repr(tm))
##         console.info(repr(self.dc.GetTextFace()))
##         console.info(repr(self.dc.GetViewportExt()))
##         console.info(repr(self.dc.GetViewportOrg()))
##         console.info(repr(self.dc.GetWindowExt()))
##         console.info(repr(self.dc.GetWindowOrg()))
        
        # http://msdn.microsoft.com/library/default.asp?url=/library/en-us/gdi/fontext_7ss2.asp
        
##         self.leading = tm['tmExternalLeading'] \
##                        + tm['tmHeight'] \
##                        #+ tm['tmInternalLeading'] \

        # 
        #self.leading = max(self.leading,self.doc.status.leading)
        #self.doc.dc.TextOut(self.line)
        console.debug("self.dc.TextOut(%d,%d,%r)",
                      int(self.x),-int(self.y),self.line)
        self.dc.TextOut(int(self.x),-int(self.y),self.line)
        (dx,dy) = self.dc.GetTextExtent(self.line)
        
        # GetTextExtent() returns the dimensions of the string in
        # logical units (twips)
        
        self.x += dx
        #console.debug("TextOut(%d,%d,%s)" % \
        #              (int(self.x),-int(self.y),repr(self.line)))
        if dy != 0:
            self.leading = dy
        self.line = ""
            
##         tm = self.doc.dc.GetTextMetrics()
##         console.debug(
##             "dy=%d, leading=%d, extLeading=%d, height=%d, intLeading=%d",
##             dy, self.leading,
##             tm['tmExternalLeading'],tm['tmHeight'],
##             tm['tmInternalLeading'])
                      

    def flush(self):
        self.write("")

    def newline(self):
        #self.x = self.doc.margin
        self.x = self.org[0] + self.margin
        self.y += self.leading
        #self.doc.dc.MoveTo(int(self.x),-int(self.y))
        console.debug("self.y += %d" % self.leading)


    def length2i(self,s):
        try:
            if s.endswith("mm"):
                return float(s[:-2]) * mm
            if s.endswith("ch"):
                self.flush()
                assert self.font is not None
                return float(s[:-2]) * self.fontDict['width']
            if s.endswith("ln"):
                self.flush()
                return float(s[:-2]) * self.leading
            return float(s) * mm
        except ValueError,e:
            raise ParserError("invalid length: %r" % s)
        
        
    def insertImage(self,filename,w=None,h=None,dx=None,dy=None):
        # picture size is given in mm
        # w = float(width) * mm 
        # h = float(height) * mm

        try:
            img = Image.open(filename)
        except OSError,e:
            console.error(str(e))
            return
        
        self.flush() # make sure that self.x and self.y are correct

        

        
        
##         # position of picture is the current text cursor
##         if self.textobject:
##             self.textobject.flush()
##             x = self.textobject.x
##             y = self.textobject.y
##         else:
##             #print "no text has been processed until now"
##             x = self.org[0] + self.margin
##             y = self.org[1] + self.margin
##             #x = self.margin
##             #y = self.pageHeight-(2*self.margin)-h - y
##             #y = self.margin
##         else:
##             # but picture starts on top of charbox:
##             y += self.status.leading

        #print "x,y", x, y


        # thanks to http://dbforums.com/t944137.html
        # and
        # http://www.activevb.de/rubriken/apikatalog/deklarationen/getdevicecaps.html
        """
        HORZRES	: Breite des Bildscchirms, angegeben in Pixeln.
        
        VERTRES	: Höhe des Bildschorms, angegeben in Rasterzeilen.
        
        LOGPIXELSX : Anzahl der Pixel pro logischen Inch über die
        Bildschirmbreite.
        
        LOGPIXELSY: Anzahl der Pixel pro logischen Inch über die
        Bildschirmhöhe.
        

        """
##         printer_resolution = self.dc.GetDeviceCaps(win32con.HORZRES),\
##                              self.dc.GetDeviceCaps(win32con.VERTRES)
##         print "printer resolution =", printer_resolution

        
##         print "twips:", x,y,w,h
##         # convert to inch
##         x /= inch
##         y /= inch
##         w /= inch
##         h /= inch
##         print "inch:", x,y,w,h
        
##         # convert to pixels
##         x *= self.dc.GetDeviceCaps(win32con.LOGPIXELSX)
##         y *= self.dc.GetDeviceCaps(win32con.LOGPIXELSY)
##         w *= self.dc.GetDeviceCaps(win32con.LOGPIXELSX)
##         h *= self.dc.GetDeviceCaps(win32con.LOGPIXELSY)

        x = int(self.x)
        y = int(self.y)
        if dx is not None:
            x += self.length2i(dx)
        if dy is not None:
            y += self.length2i(dy)
        
        width = height = None
        if w is not None:
            width = self.length2i(w)
        if h is not None:
            height = self.length2i(h)
            
        if height is None:
            height = int(width * img.size[0] / img.size[1])
        if width is None:
            width = int(height * img.size[1] / img.size[0])
        
        #print "pixels:", x,y,w,h


##         print "image size =", img.size

##         #
##         # Resize the image to fit the page but not to overflow
##         #
##         ratios = [1.0 * printer_resolution[0] / img.size[0],
##                   1.0 * printer_resolution[1] / img.size[1]]
##         print "ratios =", ratios
##         scale = min(ratios)
##         print "scale =", scale

        dib = ImageWin.Dib(img)
##         scaled_size = [int(scale * i) for i in img.size]
##         print "scaled_size =", scaled_size
##         destination = [x, y] + scaled_size
        
        #y = 500
        # destination is a 4-tuple topx,topy, botx,boty
        destination = ( x, -y, x+width, -(y+height) )
        #destination = [int(x) for x in destination]
        #destination = [x, y, 500, 500]
        #print "destination:", destination
        dib.draw(self.dc.GetHandleOutput(),destination)
                 

    def drawDebugRaster(self):
        DELTA=10
        self.dc.MoveTo(self.org)
        # to upper right
        self.dc.LineTo((self.ext[0],-self.org[1]))
        
        # to lower right
        #self.dc.LineTo((0,-self.ext[1]))
        self.dc.LineTo((self.ext[0]-DELTA,-(self.ext[1]-DELTA)))

        # to lower left
        self.dc.LineTo((self.org[0],-(self.ext[1]-DELTA)))

        # to upper left
        self.dc.LineTo((self.org[0],-self.org[1]))
        
        #self.dc.LineTo((0,-self.ext[1]))
        #self.dc.MoveTo(self.org)
        #self.dc.LineTo((0,5000))
        
