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


from lino.forms import base

class Label(base.Label):
    pass
                
class Button(base.Button):
    pass
    
class DataGrid(base.DataGrid):
    pass
        
class DataForm(base.DataForm):
    pass
        
    def getStatus(self):
        return "%d/%d" % (self.currentPos,len(self.ds))
    

class TextViewer(base.TextViewer):

    def addText(self,s):
        self.getForm().notice(s)
    
class Panel(base.Panel):

    pass
            
class Entry(base.Entry):
    pass

class DataEntry(base.DataEntry):
    pass


class Form(base.Form):

    def __init__(self,*args,**kw):
        self._isShown = False
        base.Form.__init__(self,*args,**kw)

    
    def status(self,msg,*args,**kw):
        self.app.toolkit.console.status(msg,*args,**kw)


##     def onJobInit(self,job):
##         pass


##     def onJobRefresh(self,job):
##         pass

##     def onJobDone(self,job,msg):
##         pass

##     def onJobAbort(self,*args,**kw):
##         pass

    def isShown(self):
        return self._isShown
    
    def onShow(self):
        self._isShown=True
            
##     def show(self,modal=False):
        
##         if self.isShown():
##             raise InvalidRequestError("form is already open")

##         self._isShown=True
            
##         self.modal = modal
##         #print "show(modal=%s) %s" % (modal, self.getLabel())
##         self.session.notice(
##             "show(modal=%s) %s", modal, self.getLabel())
##         self.session.notice(repr(self.mainComp))
##         self.onShow()



class Toolkit(base.Toolkit):
    labelFactory = Label
    entryFactory = Entry
    dataEntryFactory = DataEntry
    buttonFactory = Button
    viewerFactory = TextViewer
    panelFactory = Panel
    dataGridFactory = DataGrid
    navigatorFactory = DataForm
    formFactory = Form
    
##     def __init__(self,*args,**kw):
##         base.Toolkit.__init__(self,*args,**kw)
##         self._running = False

##     def running(self):
##         return self._running 

##     def run_awhile(self):
##         assert self.running()
##         pass
    
##     def run_forever(self):
##         assert not self.running()
##         self._running = True
##         self.init()
        
##     def addApplication(self,app):
##         base.Toolkit.addApplication(self,app)
##         app.init()
