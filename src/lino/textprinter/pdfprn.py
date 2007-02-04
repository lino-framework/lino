#coding: latin1

## Copyright 2004-2007 Luc Saffre

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

import os
import sys

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch,mm
from reportlab.lib.pagesizes import letter, A4

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont, TTFError


from lino.textprinter.textprinter import FileTextPrinter, \
     ParserError, OperationFailed



## HACK_BOXCHARS = {
    
##     # generated using tests/etc/3.py

##     u'\u250c': '+',
##     u'\u2500': '-',
##     u'\u252c': '+',
##     u'\u2510': '+',
##     u'\u2502': '|',
##     u'\u251c': '+',
##     u'\u253c': '+',
##     u'\u2524': '+',
##     u'\u2514': '+',
##     u'\u2534': '+',
##     u'\u2518': '+',
              
##     u'\u2554': '+',
##     u'\u2550': '-',
##     u'\u2566': '+',
##     u'\u2557': '+',
##     u'\u2551': '|',
##     u'\u2560': '+',
##     u'\u256c': '+',
##     u'\u2563': '+',
##     u'\u255a': '+',
##     u'\u2569': '+',
##     u'\u255d': '+',
##     }



class Status:
    """
    could be used to save/restore the status of the textobject
    """
    def __init__(self,size=10,
                 psfontname="Courier",
                 bold=False,
                 ital=False,
                 leading=12):
        self.ital = ital
        self.bold = bold
        self.psfontname = psfontname
        self.size = size
        self.leading = leading
        self.lpi = None
        self.underline = False


        

class PdfTextPrinter(FileTextPrinter):
    extension=".pdf"
    
    ratio_width2size=1.7   # fontsize = width * ratio_width2size
    ratio_size2leading=1.1 # leading = fontsize * ratio_size2leading
    charwidth=0.6
    def __init__(self,filename,margin=5*mm,**kw):
        FileTextPrinter.__init__(self,filename,
                                 pageSize=A4,
                                 margin=margin,
                                 **kw)
        

        try:
            font=TTFont("Courier", "cour.ttf")
##             print "pdfprn.py", font.face.bbox,\
##                   font.face.ascent, font.face.descent
##             minx,miny,maxx,maxy = font.face.bbox
##             boxheight=font.face.ascent-font.face.descent
##             #self.ratio_size2leading=float(maxy-miny) / font.face.defaultWidth
##             self.ratio_size2leading=float(boxheight) / font.face.defaultWidth
##             print "ratio_size2leading=",self.ratio_size2leading
            pdfmetrics.registerFont(font)
            pdfmetrics.registerFont(TTFont("Courier-Bold", "courbd.ttf"))
            pdfmetrics.registerFont(TTFont("Courier-Oblique",
                                           "couri.ttf"))
            pdfmetrics.registerFont(TTFont("Courier-BoldOblique",
                                           "courbi.ttf"))
        except TTFError,e:
            pass # continue with the Adobe builtin version
        
        
        self.canvas = canvas.Canvas(filename,pagesize=A4)
        self.textobject = None
        self.status = Status()


##      def background(self):
##          self.canvas.drawImage('logo2.jpg',
##                                       self.margin,
##                                       self.pageHeight-(2*self.margin)-25*mm,
##                                       25*mm,25*mm)
                                     
##          textobject = self.canvas.beginText()
##          textobject.setTextOrigin(self.margin+26*mm,
##                                           self.pageHeight-(2*self.margin))
##          textobject.setFont("Times-Bold", 12)
##          textobject.textLine("Rumma & Ko OÜ")
##          textobject.setFont("Times-Roman", 10)
##          textobject.textLine("Tartu mnt. 71-5")
##          textobject.textLine("10115 Tallinn")
##          textobject.textLine("Eesti")
##          self.canvas.drawText(textobject)

##     def createTextObject(self):
##         #textobject.setFont("Courier", 10)
##         return textobject
        
    def onBeginPage(self):
        #self.background()
        if self.pageHeight < self.pageWidth:
            # if landscape mode
            self.canvas.rotate(90)
            self.canvas.translate(0,-210*mm)
        self.textobject = self.canvas.beginText()
        self.textobject.setTextOrigin(
            self.margin, self.pageHeight-(2*self.margin))
    
    def onEndPage(self):
        self.canvas.drawText(self.textobject)
        self.canvas.showPage()
        self.textobject = None
        
    def onSetPageSize(self):
        self.canvas.setPageSize((self.pageHeight,self.pageWidth))
            

    def onEndDoc(self):
        try:
            self.canvas.save()
        except IOError,e:
            print "ERROR : could not save pdf file:"
            print e
            sys.exit(-1)
            
##     def onSetFont(self):
##         TextPrinter.onSetFont(self)

    def prepareFont(self):
        if not self.fontChanged: return
        self.fontChanged=False
        if self.status.lpi is None:
            self.status.leading = self.status.size * self.ratio_size2leading
        else:
            self.status.leading = 72 / self.status.lpi

        psfontname = self.status.psfontname
        if self.status.bold:
            psfontname += "-Bold"
            if self.status.ital:
                psfontname += "Oblique"
        elif self.status.ital:
            psfontname += "-Oblique"
            
        self.textobject.setFont(psfontname,
                                self.status.size,
                                self.status.leading)
        

    def write(self,text):
        self.session.debug("write(%r)",text)
        self.prepareFont()

##         if self.coding is not None:
##             text = text.encode(self.coding)
##         self.textobject.textOut(text)
##         return

            
        #for k,v in HACK_BOXCHARS.items():
        #    text = text.replace(k,v)

        if False: # reportlab version 1.x
            try:
                text = text.encode("iso-8859-1","strict")
            except UnicodeError, e:
                print e
                print repr(text)
                text = text.encode("iso-8859-1","replace")

        self.textobject.textOut(text)
        
    def newline(self):
        self.write("") # see http://lino.saffre-rumma.ee/news/463.html
        self.textobject.textLine()

        
    def length2i(self,s):
        try:
            if s.endswith("mm"):
                return float(s[:-2]) * mm
            if s.endswith("ch"):
                #print "1ch=%s"%self.status.size
                return float(s[:-2]) * self.status.size * self.charwidth
            if s.endswith("ln"):
                #print "1ln=%s"%self.status.leading
                return float(s[:-2]) * self.status.leading 
            return float(s) * mm
        except ValueError,e:
            raise ParserError("invalid length: %r" % s)
        
        
    def insertImage(self,filename,
                    w=None,h=None,
                    x=None,y=None,
                    dx=None,dy=None):
        """
        
        w and h are the width and height of the image. At least one of
        these parameters must be specified. If the other parameter is
        not specified, it will be calculated to keep the image's
        aspect ratio.

        x and y to specify an absolute position of the top left corner
        of the image. (0,0) is the lower left corner of the page.  If
        x or y or both are missing, the image gets inserted at the
        current text cursor position (more precisely the top left
        corner of the charbox)

        dx and dy are optional distances to be added to x and y.
        
        """
        self.flush()
        width = height = None
        if w is not None:
            width = self.length2i(w)
        if h is not None:
            height = self.length2i(h)


        if height is None:
            img=self.openImage(filename)
            height = int(width * img.size[1] / img.size[0])
            del img
            #print "width,height=",width,height
        if width is None:
            img=self.openImage(filename)
            width = int(height * img.size[0] / img.size[1])
            del img


        # position of picture is the current text cursor 
        (cx,cy) = self.textobject.getCursor()
        if cx == 0 and cy == 0:
            # print "no text has been processed until now"
            cx = self.margin
            cy = self.pageHeight-(2*self.margin)-height
        else:
            # but picture starts on top of charbox:
            cy += self.status.leading
            
        if x is None: x=cx
        else: x = self.length2i(x)
        if y is None: y=cy
        else: y = self.length2i(y)
            
        if dx is not None:
            x += self.length2i(dx)
        if dy is not None:
            y -= self.length2i(dy)
        #print filename,(x,y-height, width,height)
        self.canvas.drawImage(filename,
                              x,y-height, width,height)



    def setCpi(self,cpi):
        "set font size in cpi (characters per inch)"
        w=int(inch/cpi)
        self.status.size = int(w*self.ratio_width2size)
##         if cpi == 10:
##             self.status.size = 12
##             #self.status.leading = 14
##         elif cpi == 12:
##             self.status.size = 10
##             #self.status.leading = 12
##         elif cpi == 15:
##             self.status.size = 8
##             #self.status.leading = 10
##         elif cpi == 17:
##             self.status.size = 7
##             #self.status.leading = 8
##         elif cpi == 20:
##             self.status.size = 6
##             #self.status.leading = 8
##         elif cpi == 5:
##             self.status.size = 24
##             #self.status.leading = 28
##         else:
##             raise ParserError("%s : bad cpi size" % par)
        #self.width = int(self.lineWidth()/inch*cpi)
        self.cpl = int(self.lineWidth()/inch*cpi)
        #print __name__, self.width
        self.onSetFont()
         
    def setItalic(self,ital):
        self.status.ital = ital
        self.onSetFont()
    
    def setBold(self,bold):
        #console.debug("setBold(%s)"%str(bold))
        self.status.bold = bold
        self.onSetFont()
        
    def setUnderline(self,ul):
        #console.debug("setUnderline(%s)"%str(ul))
        self.status.underline = ul
        self.onSetFont()
        
    def setLpi(self,lpi):
        self.status.lpi = lpi
        self.onSetFont()
        
    def drawDebugRaster(self):
        self.write("drawDebugRaster() not implemented for PdfTextPrinter")

