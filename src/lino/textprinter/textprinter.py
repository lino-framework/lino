## Copyright 2003-2006 Luc Saffre

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

import sys
import os
import codecs

from lino.console import syscon
from lino.adamo.exceptions import OperationFailed

from PIL import Image

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



class ParserError(Exception):
    pass

class PrinterNotReady(Exception):
    pass

class TextPrinter:
    def __init__(self,
                 pageSize=(0,0),
                 margin=0,
                 cpl=None,
                 cpi=12,
                 session=None,
                 encoding=None):

##         self.lineCommands = {
##             ".image" : "parse_image",
##             }
        self.commands = {
            chr(12) : self.formFeed,
            chr(27)+"l" : self.parse_l,
            chr(27)+"c" : self.parse_c,
            chr(27)+"b" : self.parse_b,
            chr(27)+"u" : self.parse_u,
            chr(27)+"i" : self.parse_i,
            chr(27)+"L" : self.parse_L,
            chr(27)+"I" : self.parse_I,
            chr(27)+"python " : self.parse_python,
            }

        if session is None:
            session=syscon.getMainSession()
        self.session=session
        self.encoding = encoding
        self.pageWidth,self.pageHeight = pageSize
        self.margin = margin 
        self.cpl=cpl
        self.cpi=cpi
        self.page=0
        #self.textobject = None
        self.fontChanged = True
        self._docStarted=False
        self._pageStarted=False
        self.session.debug("TextPrinter.__init__()")

    def getCpl(self):
        "characters per line"
        return self.cpl
    
    def lineWidth(self):
        return self.pageWidth - self.margin * 2
        
##     def createTextObject(self):
##         raise NotImplementedError
        
    def openImage(self,filename):
        try:
            return Image.open(filename)
        except OSError,e:
            raise OperationFailed(str(e))
            #syscon.error(str(e))
            #return
        
        
    def onBeginPage(self):
        pass
    def onEndPage(self):
        pass
    def onSetPageSize(self):
        pass
    def onBeginDoc(self):
        pass
    def onEndDoc(self):
        pass
            
    
    def write(self,text):
        raise NotImplementedError
    def newline(self,text):
        raise NotImplementedError

    def setCpi(self,cpi):
        pass
    def setItalic(self,ital):
        pass
    def setBold(self,bold):
        pass
    def setLpi(self,lpi):
        pass
    def setUnderline(self,ul):
        pass
        
    def beginPage(self):
        self.page += 1
        self.onBeginPage()
        assert not self._pageStarted
        self._pageStarted = True
        #assert self.textobject is None
        #self.textobject = self.createTextObject()

    def endPage(self):
        #if self.textobject is None:
        if not self._pageStarted:
            # formfeed without any preceding text generates blank page
            self.beginPage()
        self.onEndPage()
        self._pageStarted = False

    def beginDoc(self):
        if self._docStarted: return
        self.onBeginDoc()
        self._docStarted=True
        #self.setCpi(self.cpi)

    def close(self):
        #if not self.textobject is None:
        if self._pageStarted:
            self.endPage()
        if self._docStarted:
            self.onEndDoc()

##     def pageStarted(self):
##         return (self.textobject is not None)
        


    def findFirstCtrl(self,line):
        firstpos = None
        firstctrl = None
        for ctrl in self.commands.keys():
            pos = line.find(ctrl)
            if pos != -1 and (firstpos == None or pos < firstpos):
                firstctrl = ctrl
                firstpos = pos
        return (firstpos,firstctrl)
    

    def readfile(self,inputfile,encoding=None):
        if encoding is None:
            encoding = self.encoding
        f = codecs.open(inputfile,"r",encoding)
        cwd = os.getcwd()
        dirname = os.path.dirname(inputfile)
        if len(dirname) != 0:
            os.chdir(dirname)
            #print "chdir", dirname
        for line in f.readlines():
            #if encoding is not None:
            #    line = line.decode(encoding)
            #self.printLine(line.rstrip())
            self.writeln(line)
        os.chdir(cwd)


    def writeln(self,line):
        
        """Print a line of text after parsing it.

        The final newline is printed only if the line really has
        text.  Or if it is empty. For lines containing only
        instructions the final newline is ignored.

        """
        
        line = line.rstrip()
        
##         for k,v in self.lineCommands.items():
##             if line.startswith(k):
##                 m = getattr(self,v)
##                 m(line[len(k):])
##                 return
        if line.endswith("\r\n"):
            line=line[:-2]
        elif line.endswith("\n"):
            line=line[:-1]
            
        if len(line) > 0:

##             pos=line.find("#python ")
##             if pos != -1:
##                 if pos > 0:
##                     self.write(line[:pos])
##                     line=line[pos+1:]
##                 a=line.split(None,1)
##                 if len(a)==2:
##                     eval(a[1])
##                     return
##                 raise "foo, a=%r" % a
            
            hasText = False
            (pos,ctrl) = self.findFirstCtrl(line)
            while pos != None:
                if pos > 0:
                    self.writechars(line[0:pos])
                    hasText = True

                line = line[pos+len(ctrl):]
                meth = self.commands[ctrl]
                nbytes = meth(line)
                if nbytes > 0:
                    line = line[nbytes:]
                #print "len(%s) is %d" % (repr(ctrl),len(ctrl))
                (pos,ctrl) = self.findFirstCtrl(line)

            #if line == "\r\n": return
            if len(line) == 0 and not hasText:
                return
        
        self.writechars(line)
        self.newline()
                
        
        #self.c.drawString(self.xpos, self.ypos, line)
        #self.ypos -= self.linespacing 

    def printLine(self,line):
        """Deprecated alias for writeln().
        """
        self.writeln(line)

    def writechars(self,text):
        if not self._docStarted:
            self.beginDoc()
        if not self._pageStarted:
            self.beginPage()

        self.write(text)
        #self._lineHasText = True
        
    def flush(self):
        self.write("")

        
        
    def parse_L(self,line):
        self.setOrientationLandscape()
        return 0
    
    def setOrientationLandscape(self):
        #assert self.textobject is None, \
        #       'setLandscape after first text has been printed'
        if self.pageHeight > self.pageWidth:
            # only if not already
            (self.pageHeight, self.pageWidth) = \
                             (self.pageWidth,self.pageHeight)
            self.onSetPageSize()

    def isLandscape(self):
        return self.pageHeight < self.pageWidth
        

    def onSetFont(self):
        self.fontChanged = True
        #if self.textobject is None:
        #    self.beginPage()

    ## methods called if ctrl sequence is found :

    def parse_l(self,line):
        par = line.split(None,1)[0]
        self.setLpi(int(par))
        return len(par)+1
    
    def parse_c(self,line):
        par = line.split(None,1)[0]
        self.setCpi(int(par))
        return len(par)+1
        
    def parse_i(self,line):
        if line[0] == "0":
            self.setItalic(False)
        elif line[0] == "1":
            self.setItalic(True)
        return 1
            
    def parse_b(self,line):
        if line[0] == "0":
            self.setBold(False)
        elif line[0] == "1":
            self.setBold(True)
        else:
            raise ParserError("0 or 1 expected, but got '%s'" \
                              % line[0])
        return 1
    
    
    def parse_u(self,line):
        if line[0] == "0":
            self.setUnderline(False)
        elif line[0] == "1":
            self.setUnderline(True)
        else:
            raise ParserError("0 or 1 expected, but got '%s'" \
                              % line[0])
        return 1
        
    def parse_python(self,line):
        eval(line)
        return len(line)
##         a=line.split(None,1)
##         if len(a)==2:
##             eval(a[1])
##             return len(line)
##         raise ParseError, "a=%r" % a
    
    def parse_I(self,line):
        # deprecated, but still in use
        # use #python self.insertImage() instead
        params = line.split(None,3)
        #print params
        if len(params) < 3:
            raise ParserError("%r : need 3 parameters" % params)
        #width=self.length2i(params[0])
        #height=self.length2i(params[1])
        #filename = params[2]
        self.insertImage(filename=params[2],
                         w=params[0],
                         h=params[1])
        return len(params[0])+len(params[1])+len(params[2])+3

##     def parse_image(self,line):
##         x = "self.insertImage(%s)" % line
##         print x
##         eval(x)
        #assert type(d) == DictType
        #self.insertImage(**d)
    
    def formFeed(self,line):
        self.endPage()
        # self.beginPage()
        return 0


    def insertImage(self,filename,w,h):
        raise NotImplementedError


        
class FileTextPrinter(TextPrinter):
    extension=None
    def __init__(self,filename,**kw):
        (root,ext) = os.path.splitext(filename)
        if ext.lower() != self.extension:
            filename += self.extension
        self.filename = filename
        TextPrinter.__init__(self,**kw)

    def close(self):
        TextPrinter.close(self)
        self.session.showfile(self.filename)
            
		
