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

from lino.textprinter.textprinter import TextPrinter

from lino.ui import console

HACK_BOXCHARS = {
    
    # generated using tests/etc/3.py

    u'\u250c': '+',
    u'\u2500': '-',
    u'\u252c': '+',
    u'\u2510': '+',
    u'\u2502': '|',
    u'\u251c': '+',
    u'\u253c': '+',
    u'\u2524': '+',
    u'\u2514': '+',
    u'\u2534': '+',
    u'\u2518': '+',
              
    u'\u2554': '+',
    u'\u2550': '-',
    u'\u2566': '+',
    u'\u2557': '+',
    u'\u2551': '|',
    u'\u2560': '+',
    u'\u256c': '+',
    u'\u2563': '+',
    u'\u255a': '+',
    u'\u2569': '+',
    u'\u255d': '+',
    }



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


        



		
class PdfTextPrinter(TextPrinter):

    def __init__(self,filename,cpi=12):
        TextPrinter.__init__(self,
                             pageSize=A4,
                             margin=5*mm)
        (root,ext) = os.path.splitext(filename)
        if ext.lower() != ".pdf":
            filename += ".pdf"
        
        self.canvas = canvas.Canvas(filename,
                                    pagesize=A4)
        self.filename = filename
        self.status = Status()
        self.setCpi(cpi)


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
        #textobject.setFont("Courier", 10)
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
            
##     def onSetFont(self):
##         TextPrinter.onSetFont(self)

    def prepareFont(self):
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

        if self.fontChanged:
            self.prepareFont()

        for k,v in HACK_BOXCHARS.items():
            text = text.replace(k,v)
            
        console.debug("write(%s)",repr(text))
        #text = text.encode("iso-8859-1","replace")
        try:
            text = text.encode("iso-8859-1","strict")
        except UnicodeError, e:
            print e
            print repr(text)
            #print HACK_BOXCHARS
            text = text.encode("iso-8859-1","replace")

        self.textobject.textOut(text)
        
    def newline(self):
        self.textobject.textLine()

        
        
##     def insertImage(self,line):
##         params = line.split(None,3)
##         if len(params) < 3:
##             raise "%s : need 3 parameters" % repr(params)
##         # picture size must be givin in mm :
##         w = float(params[0]) * mm #*self.status.size
##         h = float(params[1]) * mm #*self.status.leading
##         # position of picture is the current text cursor 
##         (x,y) = self.textobject.getCursor()
##         if x == 0 and y == 0:
##             # print "no text has been processed until now"
##             x = self.margin + x
##             y = self.pageHeight-(2*self.margin)-h - y
##         else:
##             # but picture starts on top of charbox:
##             y += self.status.leading
            
##         filename = params[2]
##         self.canvas.drawImage(filename,
##                                      x,y-h,
##                                      w,h)
##         return len(params[0])+len(params[1])+len(params[2])+3
    
    def insertImage(self,width,height,filename):
        # picture size must be givin in mm :
        w = float(width) * mm 
        h = float(height) * mm 
        # position of picture is the current text cursor 
        (x,y) = self.textobject.getCursor()
        if x == 0 and y == 0:
            # print "no text has been processed until now"
            x = self.margin + x
            y = self.pageHeight-(2*self.margin)-h - y
        else:
            # but picture starts on top of charbox:
            y += self.status.leading
            
        self.canvas.drawImage(filename, x,y-h, w,h)
    
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
        self.width = int(
            (self.pageWidth-(self.margin*2))/inch*cpi)
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
        
