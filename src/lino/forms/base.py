## Copyright 2005 Luc Saffre 

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

from lino.misc.descr import Describable
from lino.misc.attrdict import AttrDict

class BaseForm(Describable):

    def __init__(self,*args,**kw):
        Describable.__init__(self,*args,**kw)
        self.entries = AttrDict()
        self.buttons = []
        self.boxes = []
        self.components = []
    
    def addEntry(self,*args,**kw): 
        e = self.createEntry(*args,**kw)
        self.components.append(e)
        self.entries.define(e.name,e)
        return e
        
    def addButton(self,*args,**kw): 
        btn = self.createButton(*args,**kw)
        self.components.append(btn)
        self.buttons[btn.name] = btn
        return btn

    def addOkButton(self,*args,**kw):
        return self.addButton(name="ok",onclick=self.ok)

    def addAbortButton(self,*args,**kw):
        return self.addButton(name="abort",onclick=self.abort)

    def createEntry(self,name,type,label=None):
        raise NotImplementedError
    def createButton(self,name,onclick=None,label=None):
        raise NotImplementedError
    
    def show(self):
        raise NotImplementedError
    def showModal(self):
        raise NotImplementedError


    def ok(self,frm):
        self.close()

    def abort(self,frm):
        self.close()

    
class BaseButton(Describable):
    def __init__(self,onclick,*args,**kw):
        Describable.__init__(self,*args,**kw)
        self.onclick = onclick

    def setHandler(self,onclick,*args,**kw):
        self.onclick = onclick
        self.args = args
        self.kw = kw
        
    def click(self):
        self.onclick(self
