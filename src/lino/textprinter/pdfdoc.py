#coding: latin1

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

import os
import sys

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch,mm
from reportlab.lib.pagesizes import letter, A4

#from lino.ui import console
from lino.textprinter.document import Document

UNICODE_HACK = True
#UNICODE_HACK = False


class Status:
    """
    could be used to save/restore the status of the textobject
    """
    def __init__(self,size=10,
                 psfontname="Courier",
                 bold=False,
                 ital=False,
                 leading=14.4):
        self.ital = ital
        self.bold = bold
        self.psfontname = psfontname
        self.size = size
        self.leading = leading
        self.lpi = None
        self.underline = False


        



		
class PdfDocument(Document):
    def __init__(self,filename,coding=None):
        Document.__init__(self,
                          pageSize=A4,
                          margin=5*mm)
        
        (root,ext) = os.path.splitext(filename)
        if ext.lower() != ".pdf":
            filename += ".pdf"
        
        self.canvas = canvas.Canvas(filename,
                                    pagesize=A4)
        self.coding = coding
        self.filename = filename
        self.status = Status()

        #self.canvas.setAuthor("Generated using prn2pdf")
        #self.canvas.setSubject("http://my.tele2.ee/lsaffre/comp/prn2pdf.htm")

        



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

    def createTextObject(self):
        textobject = self.canvas.beginText()
        textobject.setTextOrigin(self.margin,
                                 self.pageHeight-(2*self.margin))
        textobject.setFont("Courier", 10)
        return textobject
        
    def onBeginPage(self):
        #self.background()
        if self.pageHeight < self.pageWidth:
            # if landscape mode
            self.canvas.rotate(90)
            self.canvas.translate(0,-210*mm)
    
    def onEndPage(self):
        self.canvas.drawText(self.textobject)
        self.canvas.showPage()
        
    def onSetPageSize(self):
        self.canvas.setPageSize((self.pageHeight,self.pageWidth))
            

    def onEndDoc(self):
        try:
            self.canvas.save()
        except IOError,e:
            print "ERROR : could not save pdf file:"
            print e
            sys.exit(-1)
            
    def onSetFont(self):
        Document.onSetFont(self)
        if self.status.lpi is not None:
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

        if self.coding is not None:

            # Schade, dass PDF oder reportlab scheinbar nicht Unicode
            # unterstützt. Deshalb muss ich die Box-Character hier durch
            # Minusse & Co ersetzen...

            if UNICODE_HACK:

                text = text.replace(chr(179),"|")
                text = text.replace(chr(180),"+")
                text = text.replace(chr(185),"+")
                text = text.replace(chr(186),"|")
                text = text.replace(chr(187),"+")
                text = text.replace(chr(188),"+")
                text = text.replace(chr(191),"+")
                text = text.replace(chr(192),"+")
                text = text.replace(chr(193),"+")
                text = text.replace(chr(194),"+")
                text = text.replace(chr(195),"+")
                text = text.replace(chr(196),"-")
                text = text.replace(chr(197),"+")
                text = text.replace(chr(193),"+")
                text = text.replace(chr(200),"+")
                text = text.replace(chr(201),"+")
                text = text.replace(chr(202),"+")
                text = text.replace(chr(203),"+")
                text = text.replace(chr(204),"+")
                text = text.replace(chr(205),"-")
                text = text.replace(chr(206),"+")
                text = text.replace(chr(217),"+")
                text = text.replace(chr(218),"+")

                text = text.decode(self.coding) #"cp850")
                text = text.encode("iso-8859-1","replace")

            else:
                text = text.decode(self.coding) #"cp850")
                #text = text.decode("cp850")

        self.textobject.textOut(text)
        
    def newline(self):
        self.textobject.textLine()

        
        
    def insertImage(self,line):
        params = line.split(None,3)
        if len(params) < 3:
            raise "%s : need 3 parameters" % repr(params)
        # picture size must be givin in mm :
        w = float(params[0]) * mm #*self.status.size
        h = float(params[1]) * mm #*self.status.leading
        # position of picture is the current text cursor 
        (x,y) = self.textobject.getCursor()
        if x == 0 and y == 0:
            # print "no text has been processed until now"
            x = self.margin + x
            y = self.pageHeight-(2*self.margin)-h - y
        else:
            # but picture starts on top of charbox:
            y += self.status.leading
            
        filename = params[2]
        self.canvas.drawImage(filename,
                                     x,y-h,
                                     w,h)
        return len(params[0])+len(params[1])+len(params[2])+3
    
    def setCpi(self,cpi):
        "set font size in cpi (characters per inch)"
        if cpi == 10:
            self.status.size = 12
            self.status.leading = 14
        elif cpi == 12:
            self.status.size = 10
            self.status.leading = 12
        elif cpi == 15:
            self.status.size = 8
            self.status.leading = 10
        elif cpi == 17:
            self.status.size = 7
            self.status.leading = 8
        elif cpi == 20:
            self.status.size = 6
            self.status.leading = 8
        elif cpi == 5:
            self.status.size = 24
            self.status.leading = 28
        else:
            raise "%s : bad cpi size" % par
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
        
