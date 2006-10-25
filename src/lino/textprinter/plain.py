## Copyright 2005-2006 Luc Saffre 

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

from lino.textprinter.textprinter import TextPrinter
from lino.console import syscon

class PlainTextPrinter(TextPrinter):
    def __init__(self,writer=None,cpl=72,frameStyle="+-+|+-+|",**kw):
        TextPrinter.__init__(self,pageSize=(cpl,0),cpl=cpl,**kw)
        if writer is None:
            """
            
            tests/75.py fails if I take stdout from
            self.session.toolkit because TestCase.setUp() only does
            setSystemConsole() while self.session remains the RunTests
            instance.
            
            """
            writer=syscon.getSystemConsole()
            #writer=syscon.getSystemConsole().stdout
            #writer=self.session.toolkit.stdout
            #writer=sys.stdout
        self._writer = writer
        assert len(frameStyle) == 8
        self.topLeft = frameStyle[0]
        self.topBorder = frameStyle[1]
        self.topRight = frameStyle[2]
        self.rightBorder = frameStyle[3]
        self.bottomRight = frameStyle[4]
        self.bottomBorder = frameStyle[5]
        self.bottomLeft = frameStyle[6]
        self.leftBorder = frameStyle[7]
        
        
    def onBeginPage(self):
        self._writer.write(
            self.topLeft+
            self.topBorder*self.getCpl()
            +self.topRight
            +"\n")
        self.textobject=""
        
    def onEndPage(self):
        self._writer.write(
            self.bottomLeft+
            self.bottomBorder*self.getCpl()+
            self.bottomRight+
            "\n")
    
    def write(self,text):
        #self.writer(text)
        self.textobject += text
            
    def newline(self):
        ln = self.textobject.ljust(self.getCpl())
        ln = ln[:self.getCpl()]
        self._writer.write(self.leftBorder+ln+self.rightBorder+"\n")
        self.textobject = ""
        
    def insertImage(self,*args,**kw):
        pass

