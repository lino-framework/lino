#coding: latin1

## Copyright 2003-2005 Luc Saffre 

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


    # USER METHODS

    def report(self,rpt):
        raise NotImplementedError

    def getLineWidth(self):
        raise NotImplementedError
    
    def getColumnSepWidth(self):
        raise NotImplementedError
    
    def table(self,*args,**kw):
        raise NotImplementedError

    def p(self,*args,**kw):
        raise NotImplementedError

    def h(self,*args,**kw):
        raise NotImplementedError
        
    def form(self,frm):
        frm.gendoc_render(self)
        


class WriterDocument(GenericDocument):
    def __init__(self, writer=None):
        #if writer is None: writer=sys.stdout.write
        self.writer = writer

    
    def write(self,txt):
        self.writer(txt)
        



