#coding: latin1

## Copyright Luc Saffre 2004. This file is part of the Lino project.

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

import win32ui
import win32con

from lino import copyleft
from lino.ui import console
from lino.misc.prndoc import Document, main

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
        #self.x = doc.margin
        #self.y = doc.margin
        self.x = self.doc.org[0] + self.doc.margin
        self.y = self.doc.org[1] + self.doc.margin
        #self.y = doc.pageHeight-(2*doc.margin)
        self.line = ""
        
    def write(self,text):
        #text = text.strip()
        #if text.endswith('\n'):
        # text = text[:-1]
        # flush = True
        assert not "\n" in text, repr(text)
        assert not "\r" in text, repr(text)
        self.line += text
        #if flush:
        # self.flush()

    def flush(self):
        self.doc.dc.TextOut(int(self.x),-int(self.y),self.line)
        console.info("TextOut(%d,%d,%s)" % \
                     (int(self.x),-int(self.y),repr(self.line)))
        self.line = ""
        #self.x = self.doc.margin
        self.x = self.doc.org[0] + self.doc.margin
        self.y += self.doc.status.leading

class Win32PrinterDocument(Document):
    def __init__(self,printerName,
                 spoolFile=None,
                 charset=None):
        Document.__init__(self,pageSize=A4,margin=5*mm)
        

        self.fontDict = {
            'name' : 'Courier New'
            }
        
        
        if charset is not None:
            self.fontDict['charset'] = charset

        
        self.dc = win32ui.CreateDC()
        self.dc.CreatePrinterDC(printerName)
        self.dc.StartDoc("prn2printer",spoolFile)
        self.dc.SetMapMode(win32con.MM_TWIPS)
        self.org = self.dc.GetWindowOrg()
        self.ext = self.dc.GetWindowExt()
        
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
            
    def onSetFont(self):
        Document.onSetFont(self)
        self.fontDict['height'] = int(inch/self.status.size)

        # http://www.polyml.org/docs/Winref/Font.html
        ## name
        ## height
        #weight
        #italic
        #underline
        #pitch
        #family
        #charset
        
        font = win32ui.CreateFont(self.fontDict)
        self.dc.SelectObject(font)


        tm = self.dc.GetTextMetrics()
##         console.info(repr(tm))
##         console.info(repr(self.dc.GetTextFace()))
##         console.info(repr(self.dc.GetViewportExt()))
##         console.info(repr(self.dc.GetViewportOrg()))
##         console.info(repr(self.dc.GetWindowExt()))
##         console.info(repr(self.dc.GetWindowOrg()))
        
        # http://msdn.microsoft.com/library/default.asp?url=/library/en-us/gdi/fontext_7ss2.asp
        
        self.status.leading = tm['tmExternalLeading'] \
                              + tm['tmHeight']
                              # + tm['tmInternalLeading'] \
        #print self.status.leading
        #self.dc.SetTextFace("Courier")
        #self.textobject.setFont(psfontname,
        #                               self.status.size,
        #                               self.status.leading)

    def write(self,text):

##         if False:

##             text = text.replace(chr(179),"|")
##             text = text.replace(chr(180),"+")
##             text = text.replace(chr(185),"+")
##             text = text.replace(chr(186),"|")
##             text = text.replace(chr(187),"+")
##             text = text.replace(chr(188),"+")
##             text = text.replace(chr(191),"+")
##             text = text.replace(chr(192),"+")
##             text = text.replace(chr(193),"+")
##             text = text.replace(chr(194),"+")
##             text = text.replace(chr(195),"+")
##             text = text.replace(chr(196),"-")
##             text = text.replace(chr(197),"+")
##             text = text.replace(chr(193),"+")
##             text = text.replace(chr(200),"+")
##             text = text.replace(chr(201),"+")
##             text = text.replace(chr(202),"+")
##             text = text.replace(chr(203),"+")
##             text = text.replace(chr(204),"+")
##             text = text.replace(chr(205),"-")
##             text = text.replace(chr(206),"+")
##             text = text.replace(chr(217),"+")
##             text = text.replace(chr(218),"+")

##             text = text.decode("cp850")
##             text = text.encode("iso-8859-1","replace")
            
##         if False:
##             text = text.decode("cp850")
            
        self.textobject.write(text)
            
        
    def writeln(self):
        self.textobject.flush()
        #self.textobject = None
        
        
    def insertImage(self,line):
        raise NotImplementedError


def main(argv):

    parser = console.getOptionParser(
        usage="usage: %prog [options] FILE",
        description="""\
where FILE is the file to be printed on the Default Printer.
It may contain plain text and simple formatting printer control sequences. """ )
    
    parser.add_option("-p", "--printer",
                      help="""\
print on PRINTERNAME rather than on Default Printer.""",
                      action="store",
                      type="string",
                      dest="printerName",
                      default=None)
    
    parser.add_option("-o", "--output",
                      help="""\
write to SPOOLFILE rather than really printing.""",
                      action="store",
                      type="string",
                      dest="spoolFile",
                      default=None)
    
    (options, args) = parser.parse_args(argv)

    if len(args) == 0:
        parser.print_help() 
        sys.exit(-1)
    
    for inputfile in args:
        d = Win32PrinterDocument(options.printerName,
                                 options.spoolFile,
                                 charset=win32con.OEM_CHARSET)
        d.readfile(inputfile)
        d.endDoc()

    
        
if __name__ == '__main__':
    print copyleft(name="Lino/prn2printer", year='2004')
    main(sys.argv[1:])
    
