# -*- coding: iso-8859-1 -*-

## Copyright 2004-2008 Luc Saffre

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

# name: (regular, bold, italic, bolditalic)
FONTFILES={
    "Courier": ("cour.ttf", "courbd.ttf","couri.ttf","courbi.ttf"),
    
    "LucidaSansTypewriter": ("ltype.ttf","ltypeb.ttf","ltypeo.ttf","ltypebo.ttf"),
    "LucidaConsole": ("lucon.ttf",),
    "VeraMono": ("VeraMono.ttf", "VeraMoBd.ttf","VeraMoIt.ttf","VeraMoBI.ttf"),
    "DejaVu": ( "DejaVuSansMono.ttf","DejaVuSansMono-Bold.ttf",
               "DejaVuSansMono-Oblique.ttf","DejaVuSansMono-BoldOblique.ttf"),
    # http://dejavu.sourceforge.net
    
    "Liberation": ("LiberationMono-Regular.ttf","LiberationMono-Bold.ttf",
                   "LiberationMono-Italic.ttf","LiberationMono-BoldItalic.ttf"),
    # https://www.redhat.com/promo/fonts/
    }


class Status:
    """
    could be used to save/restore the status of the textobject
    """
    def __init__(self,size=10.0,
                 fontName="Courier",
                 bold=False,
                 ital=False):
        self.ital = ital
        self.bold = bold
        self.fontName = fontName
        self.size = size
        #self.leading = None #leading
        #self.lpi = None
        self.underline = False


        

class PdfTextPrinter(FileTextPrinter):
    "http://lino.saffre-rumma.ee/src/299.html"
    
    extension=".pdf"
    ratio_width2size=1.7   # fontsize = width * ratio_width2size
    ratio_size2leading=1.1 # leading = fontsize * ratio_size2leading
    charwidth=0.6
    
    def __init__(self,filename,fontName="Courier",**kw):
        FileTextPrinter.__init__(self,filename,pageSize=A4,**kw)

        fontfiles=FONTFILES[fontName]
        pdfmetrics.registerFont(TTFont(fontName, fontfiles[0]))
        if len(fontfiles) == 1:
            self._can_bold=False
        else:
            self._can_bold=True
            pdfmetrics.registerFont(TTFont(fontName+"-Bold", fontfiles[1]))
            pdfmetrics.registerFont(TTFont(fontName+"-Oblique", fontfiles[2]))
            pdfmetrics.registerFont(TTFont(fontName+"-BoldOblique", fontfiles[3]))
        

##         try:
## ##             font=TTFont("Courier", "cour.ttf")
## ##             print "pdfprn.py", font.face.bbox,\
## ##                   font.face.ascent, font.face.descent
## ##             minx,miny,maxx,maxy = font.face.bbox
## ##             boxheight=font.face.ascent-font.face.descent
## ##             #self.ratio_size2leading=float(maxy-miny) / font.face.defaultWidth
## ##             self.ratio_size2leading=float(boxheight) / font.face.defaultWidth
## ##             print "ratio_size2leading=",self.ratio_size2leading
##             pdfmetrics.registerFont(TTFont("Courier", "cour.ttf"))
##             pdfmetrics.registerFont(TTFont("Courier-Bold", "courbd.ttf"))
##             pdfmetrics.registerFont(TTFont("Courier-Oblique", "couri.ttf"))
##             pdfmetrics.registerFont(TTFont("Courier-BoldOblique", "courbi.ttf"))
##         except TTFError,e:
##             pass # continue with the Adobe builtin version
        
        
        self.canvas = canvas.Canvas(filename,pagesize=A4)
        self.textobject = None
        self.status = Status(fontName=fontName)
        self.leading=None
        self.lpi = None
        self.setCpi(self.cpi)


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
        if self.isLandscape():
            # if landscape mode
            self.canvas.rotate(90)
            self.canvas.translate(0,-210.0*mm)
        self.textobject = self.canvas.beginText()
        self.textobject.setTextOrigin(self.margin,self.pageHeight-self.margin)
        #FileTextPrinter.onBeginPage(self)
    
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
        if self.lpi is None:
            self.leading = self.status.size * self.ratio_size2leading
        else:
            self.leading = 72.0 / self.lpi

        fontname = self.status.fontName
        if self._can_bold:
            if self.status.bold:
                fontname += "-Bold"
                if self.status.ital:
                    fontname += "Oblique"
            elif self.status.ital:
                fontname += "-Oblique"
            
        self.textobject.setFont(fontname,
                                self.status.size,
                                self.leading)
        if False and not self._can_bold:
            # disabled because that doesn't look satisfying either
            if self.status.bold:
                self.textobject.setFillGray(0.0)
            else:
                self.textobject.setFillGray(0.2)
        

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
        # self.session.debug("PdfTextPrinter.newline()")
        self.write("") # see http://lino.saffre-rumma.ee/news/463.html
        self.textobject.textLine()

        
    def length2i(self,s):
        "http://lino.saffre-rumma.ee/src/328.html"
        try:
            if s.endswith("mm"):
                return float(s[:-2]) * mm
            if s.endswith("ch"):
                #print "1ch=%s"%self.status.size
                return float(s[:-2]) * self.status.size * self.charwidth
            if s.endswith("ln"):
                #print "1ln=%s"%self.leading
                return float(s[:-2]) * self.leading 
            return float(s) * mm
        except ValueError,e:
            raise ParserError("invalid length: %r" % s)
        
        
    def insertImage(self,filename,
                    w=None,h=None,
                    x=None,y=None,
                    dx=None,dy=None,
                    behindText=False):
        "http://lino.saffre-rumma.ee/src/334.html"
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
            cy = self.pageHeight-self.margin-height
        else:
            # but picture starts on top of charbox:
            cy += self.leading
            
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
        "http://lino.saffre-rumma.ee/src/330.html"
        w=inch/cpi
        self.status.size = w*self.ratio_width2size
        self.cpl=self.lineWidth() / inch * cpi
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
        self.lpi = lpi
        self.onSetFont()
        
    def drawDebugRaster(self):
        self.flush()

        LEFT=0
        RIGHT=self.pageWidth
        TOP=self.pageHeight
        BOTTOM=0
        WIDTH=self.pageWidth
        HEIGHT=self.pageHeight
        CS=9.0*mm # Cross Size

        self.canvas.setFont("Helvetica",6)
        self.canvas.setLineWidth(0.01)
        
        self.canvas.rect(LEFT,TOP,WIDTH,HEIGHT)

        x=LEFT
        while x <= RIGHT:
            y=BOTTOM
            while y <= TOP:
                self.canvas.line(x-CS,y,x+CS,y)
                self.canvas.line(x,y-CS,x,y+CS)
                self.canvas.drawString(x,y,"(%d,%d)"%(round(x/mm),round(y/mm)))
                y += 20.0*mm
            x += 20.0*mm
        

        
