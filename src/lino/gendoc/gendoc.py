#coding: latin1

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


#import sys

class GenericDocument:
    
    def beginDocument(self):
        pass
    
    def endDocument(self):
        pass

    def renderLabel(self,lbl):
        if lbl.enabled:
            self.p(lbl.getLabel())
        
    def renderButton(self,btn):
        if btn.enabled:
            self.p("["+btn.getLabel()+"]")
            
    def renderEntry(self,e):
        raise
        if e.enabled:
            v=e.getValue()
            if v is None:
                self.p(e.getLabel()+": [None]")
            else:
                self.p(e.getLabel()+": ["+e.format(v)+"]")
        
    def renderDataGrid(self,grid):
        if grid.enabled:
            self.report(grid.rpt)
            
    def renderForm(self,frm):
        frm.render(self)
        
    


#class DocumentContext:

    def report(self,rpt):
        raise NotImplementedError

    def getLineWidth(self):
        raise NotImplementedError
    
    def getColumnSepWidth(self):
        raise NotImplementedError
    
    def table(self,*args,**kw):
        raise NotImplementedError

    def par(self,*args,**kw):
        raise NotImplementedError, repr(self)

    def pre(self,*args,**kw):
        raise NotImplementedError, repr(self)

    def header(self,*args,**kw):
        raise NotImplementedError
        
    def ul(self,*args,**kw):
        raise NotImplementedError
        


class WriterDocument(GenericDocument):
    def __init__(self, writer=None):
        #if writer is None: writer=sys.stdout.write
        self.writer = writer

    
    def write(self,txt):
        self.writer(txt)
        

        

