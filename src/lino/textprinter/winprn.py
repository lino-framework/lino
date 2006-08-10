## Copyright 2004-2006 Luc Saffre 

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

#from math import sin, cos, radians

#from ctypes import WinError
import sys

import win32ui
import win32gui
import win32con
import win32print
import pywintypes
#import win32gui

from PIL import Image, ImageWin

#SUPPORT_LANDSCAPE = False

NEWCENTURY=True

"""
http://newcenturycomputers.net/projects/pythonicwindowsprinting.html

"""

            


"""
thanks to
http://starship.python.net/crew/theller/moin.cgi/PIL_20and_20py2exe
for the following trick to avoid "IOError: cannot identify image
file" when exefied with py2exe
"""

#from PIL import PngImagePlugin
from PIL import JpegImagePlugin
from PIL import BmpImagePlugin

Image._initialized=2

#OEM_CHARSET = win32con.OEM_CHARSET

charsets = {
    "cp850" : win32con.OEM_CHARSET,
    "cp437" : win32con.OEM_CHARSET
    }

# OEM_FIXED_FONT = win32con.OEM_FIXED_FONT
# http://msdn.microsoft.com/library/default.asp?url=/library/en-us/gdi/fontext_3pbo.asp

from lino.console import syscon
from lino.textprinter.textprinter import TextPrinter, \
     PrinterNotReady, ParserError

pt = 20
inch = 1440.0
mm = inch / 25.4
A4 = (210*mm, 297*mm)

RATIO=1.7

# Note that in all modes, the point 0,0 is the top left corner of
# the page, and the units increase as you go down and across the
# page.
# We work in twips: self.dc.SetMapMode(win32con.MM_TWIPS)

# A Twip is 1/20 of a typesetting Point. A typesetting Point is 1/72
# of an inch, so a Twip is 1/1440 of an inch. (0,0) is the bottom left
# corner.

# MS doc about SetMapMode() and MM_TWIPS: The mapping mode defines the
# unit of measure used to transform page-space units into device-space
# units, and also defines the orientation of the device's x and y
# axes.  [with MM_TWIPS] each logical unit is mapped to one twentieth
# of a printer's point (1/1440 inch, also called a twip). Positive x
# is to the right; positive y is up. (http://msdn.microsoft.com/library)

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
                 lpi=6,
                 fontName="Courier New",
                 coding=sys.stdin.encoding,
                 jobName="Win32PrinterDocument",
                 useWorldTransform=False,
                 **kw):
        
        TextPrinter.__init__(self,pageSize=A4,margin=5*mm,
                             coding=coding,**kw)

        self.fontDict = dict(
            name=fontName,
            orientation=50
            )
        
        try:
            self.fontDict['charset'] = charsets[coding]
        except KeyError,e:
            pass

        self.font = None
        self.useWorldTransform=useWorldTransform
        self.spoolFile=spoolFile
        self.jobName=jobName

        
        if printerName is None:
            printerName=win32print.GetDefaultPrinter()
        self.printerName=printerName
        
        #self.doc.dc.MoveTo(int(self.x),-int(self.y))
        #self.y = doc.pageHeight-(2*doc.margin)
        self.line = ""
        self.leading = 0
        
        #print "Viewport:",\
        #      self.dc.GetViewportOrg(), self.dc.GetViewportExt()
        #print "Window:", self.dc.GetWindowOrg(), self.dc.GetWindowExt()
        
        
        
##     def createTextObject(self):
##         textobject = TextObject(self)
##         #textobject.setFont("Courier", 10)
##         return textobject
        
    def onBeginDoc(self):
        #self.phandle=win32print.OpenPrinter(printerName)
        if NEWCENTURY:
            # open the printer.
            hprinter = win32print.OpenPrinter(self.printerName)

            # retrieve default settings.  this code has complications on
            # win95/98, I'm told, but I haven't tested it there.
            devmode = win32print.GetPrinter(hprinter,2)["pDevMode"]

            # change paper size and orientation
            # constants are available here:
            # http://msdn.microsoft.com/library/default.asp?\
            # url=/library/en-us/intl/nls_Paper_Sizes.asp
            devmode.PaperSize = 9 # DMPAPER_A4
            # 1 = portrait, 2 = landscape
            if self.isLandscape():
                devmode.Orientation = 2
            else:
                devmode.Orientation = 1

            # create dc using new settings.
            # first get the integer hDC value.
            # note that we need the name.
            hdc = win32gui.CreateDC("WINSPOOL",
                                    self.printerName,
                                    devmode)
            # next create a PyCDC from the hDC.
            self.dc = win32ui.CreateDCFromHandle(hdc)

        else:
            self.dc = win32ui.CreateDC()
            self.dc.CreatePrinterDC(self.printerName)

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
            self.dc.StartDoc(self.jobName,self.spoolFile)
        except win32ui.error,e:
            raise PrinterNotReady("StartDoc() failed")
        
        # using SetWorldTransform() requires advanced graphics mode
        if self.useWorldTransform: #SUPPORT_LANDSCAPE:
            self.dc.SetGraphicsMode(win32con.GM_ADVANCED)
        
        self.dc.SetMapMode(win32con.MM_TWIPS)
        
        #self.org = self.dc.GetViewportOrg()
        #self.ext = self.dc.GetViewportExt()
        self.org = self.dc.GetWindowOrg()
        self.ext = self.dc.GetWindowExt()
        #self.setCpi(cpi)
        #self.setLpi(lpi)


            
        
    def onBeginPage(self):
        self.x = self.org[0] + self.margin
        self.y = self.org[1] + self.margin
        self._images=[]

        if self.isLandscape():
            if self.useWorldTransform: # SUPPORT_LANDSCAPE:
                r=0
                # shifts to right:
                #r=self.dc.SetWorldTransform(1,0, 0,1, 200,0)
                #print "Landscape"
                r=self.dc.SetWorldTransform(
                    0,1, -1,0,
                    0, -int(self.pageWidth-2*self.margin))
                if r == 0:
                    raise PrinterNotReady("SetWorldTransform() failed")
##         else:
##             #print "Portrait"
##             r=self.dc.SetWorldTransform(1,0,0,1,0,0)
##             if r == 0:
##                 raise PrinterNotReady("SetWorldTransform() failed")
        
        r = self.dc.StartPage()
        # r seems to be always None
        # if r <= 0:
        #     raise PrinterNotReady("StartPage() returned %d",r)
    
    def onEndPage(self):
        for dib,destination in self._images:
            dib.draw(self.dc.GetHandleOutput(),destination)
                 
        #self.drawDebugRaster()
        
        r=self.dc.EndPage()
        # seems to be always None
        # if r <= 0:
        #    raise PrinterNotReady("EndPage() returned %d",r)

    def onSetPageSize(self):
        pass
            

    def onEndDoc(self):
        self.dc.EndDoc()
        #win32print.ClosePrinter(self.phandle)
        del self.dc
            
    def setLpi(self,lpi):
        pass
        #h = int(LPIBASE / lpi)
        #h = int(inch/lpi)
        #console.debug("%d lpi = %d twips" % (lpi,h))
        #self.fontDict['height'] = h
        #self.leading = int(inch/lpi)
        
    def setCpi(self,cpi):
        w = int(inch/cpi)
        #console.debug("%d cpi = %d twips" % (cpi,w))
        
        self.fontDict['width'] = w
        # see 20050602:
        self.fontDict['height'] = int(w*RATIO)
        # if RATIO changes, I must adapt TIM's prnprint.drv
        
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
            #print "CreateFont(%r)" % self.fontDict
            #print "CreateFont() returned %r" % self.font
        
            # CreateFont: http://msdn.microsoft.com/library/default.asp?url=/library/en-us/gdi/fontext_8fp0.asp
        
            self.dc.SelectObject(self.font)
            #print "select font",self.fontDict
            
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
        if len(self.line) == 0:
            (dx,dy) = self.dc.GetTextExtent(" ")
        else:
            print "self.dc.TextOut(%d,%d,%r)"%\
                  (int(self.x),-int(self.y),self.line)
            self.dc.TextOut(int(self.x),-int(self.y),self.line)
            (dx,dy) = self.dc.GetTextExtent(self.line)
            self.x += dx
        
        # GetTextExtent() returns the dimensions of the string in
        # logical units (twips)
        
        #console.debug("TextOut(%d,%d,%s)" % \
        #              (int(self.x),-int(self.y),repr(self.line)))
        #if dy != 0:
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
        #syscon.debug("self.y += %d" % self.leading)


    def length2i(self,s):
        try:
            if s.endswith("mm"):
                return int(float(s[:-2]) * mm)
            if s.endswith("ch"):
                self.flush()
                assert self.font is not None
                return int(float(s[:-2]) * self.fontDict['width'])
            if s.endswith("ln"):
                self.flush()
                return int(float(s[:-2]) * self.leading)
            return int(float(s) * mm)
        except ValueError,e:
            raise ParserError("invalid length: %r" % s)
        
        
    def insertImage(self,filename,
                    w=None,h=None,
                    dx=None,dy=None,
                    behindText=False):
        # picture size is given in mm
        # w = float(width) * mm 
        # h = float(height) * mm

        try:
            img = Image.open(filename)
        except OSError,e:
            syscon.error(str(e))
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
        
        VERTRES	: Hoehe des Bildschirms, angegeben in Rasterzeilen.
        
        LOGPIXELSX : Anzahl der Pixel pro logischen Inch ueber die
        Bildschirmbreite.
        
        LOGPIXELSY: Anzahl der Pixel pro logischen Inch ueber die
        Bildschirmhoehe.
        

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
        if behindText:
            dib.draw(self.dc.GetHandleOutput(),destination)
        else:
            self._add_image(dib,destination)

    def _add_image(self,dib,destination):
        self._images.append((dib,destination))


    def drawDebugRaster(self):
        fontDict=dict(name="Courier New",
                      height=100)
        font = win32ui.CreateFont(fontDict)
        self.dc.SelectObject(font)
        #print "CreateFont(%r)" % fontDict
        
        DELTA=10
        #print "org:", self.org
        #print "ext:", self.ext
        self.dc.MoveTo((self.org[0]+DELTA,-self.org[1]-DELTA))
        # to upper right
        self.dc.LineTo((self.ext[0]+DELTA,-self.org[1]-DELTA))
        
        # to lower right
        #self.dc.LineTo((0,-self.ext[1]))
        self.dc.LineTo((self.ext[0]-DELTA,-self.ext[1]-DELTA))

        # to lower left
        self.dc.LineTo((self.org[0],-(self.ext[1]-DELTA)))

        # to upper left
        self.dc.LineTo((self.org[0],-self.org[1]))
        
        CS=50 # Cross Size
        for x in range(self.org[0],self.ext[0],int(20*mm)):
            for y in range(self.org[1],self.ext[1],int(20*mm)):
                
                self.dc.MoveTo((x-CS,-y))
                self.dc.LineTo((x+CS,-y))
                
                self.dc.MoveTo((x,-y-CS))
                self.dc.LineTo((x,-y+CS))
                
                self.dc.TextOut(x,-y,"(%d,%d)"%(x,-y))
                #print (x,y)
        
        #self.dc.LineTo((0,5000))
        
        
