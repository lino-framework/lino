#coding: latin1

"""
prn2pdf converts a file containing text and simple formatting
printer control sequences into a PDF file.  

USAGE :
  prn2pdf [options] FILE

  where FILE is the .prn file to be converted 
  
OPTIONS :
  -o, --output FILE     write result to file FILE
  -b, --batch           don't start Acrobat Reader on the generated
                        pdf file
  -h, --help            display this text

"""

UNICODE_HACK = True
#UNICODE_HACK = False 

import sys, os
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch,mm
from reportlab.lib.pagesizes import letter, A4

from lino import copyleft
from lino.misc.console import getSystemConsole
from lino.misc.prndoc import Document, main

		
class PdfDocument(Document):
    def __init__(self,filename):
        Document.__init__(self,
                          pageSize=A4,
                          margin=5*mm)
        
        (root,ext) = os.path.splitext(filename)
        if ext.lower() != ".pdf":
            filename += ".pdf"
        
        self.canvas = canvas.Canvas(filename,
                                             pagesize=A4)

        self.filename = filename

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

            text = text.decode("cp850")
            text = text.encode("iso-8859-1","replace")
            
        else:
            text = text.decode("cp850")
            
        self.textobject.textOut(text)
        
    def writeln(self):
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
    

if __name__ == '__main__':
    print "prn2pdf" 
    print copyleft(year='2002-2004',author='Luc Saffre')

    doc = main(sys.argv[1:],docfactory=PdfDocument)
    
    if not getSystemConsole().isBatch():
        os.system("start %s" % doc.filename)
