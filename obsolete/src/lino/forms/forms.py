## Copyright 2005-2007 Luc Saffre 

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

from lino.adamo.exceptions import InvalidRequestError
from lino.forms import gui

VERTICAL = 1
HORIZONTAL = 2

YES=True
NO=False


class MenuContainer:
    # also used by gendoc.html.HtmlDocument
    def __init__(self):
        self.menuBar = None
        self._menuController = None
        
    def addMenu(self,*args,**kw):
        if self.menuBar is None:
            self.menuBar = self.toolkit.menuBarFactory(
                self)
        return self.menuBar.addMenu(*args,**kw)

    def setMenuController(self,c):
        if self._menuController is None:
            self._menuController = c
        else:
            self.debug("ignored menuController %s" % str(c))

##     def setupMenu(self):
##         if self._menuController is not None:
##             self._menuController.setupMenu()
            


class Form(MenuContainer):
    
    title=None
    modal=False
    #doc=None
    returnValue=None
    enabled=True
    
    minWidth=None
    maxWidth=None
    minHeight=None
    maxHeight=None
    
    def __init__(self,
                 title=None,
                 halign=None, valign=None,
                 width=None,minWidth=None,maxWidth=None,
                 height=None,minHeight=None,maxHeight=None,
                 enabled=None): # *args,**kw):
        MenuContainer.__init__(self)
        if title is not None:
            self.title=title
        if enabled is not None:
            self.enabled=enabled
        self.accelerators=[]
        self._parent = None
        self.defaultButton = None
        self.valign = valign
        self.halign = halign
        self._boxes = []
        self.lastEvent = None
        self.ctrl=None
        self.session=None
        self.mainComp=None

        if width is not None:
            minWidth = maxWidth = width
        if maxWidth is not None:
            self.maxWidth = maxWidth
        if minWidth is not None:
            self.minWidth = minWidth
        if height is not None:
            minHeight = maxHeight = height
        if maxHeight is not None:
            self.maxHeight = maxHeight
        if minHeight is not None:
            self.minHeight = minHeight
        


    #def setup(self,sess):
    def show(self,sess):
        if self.ctrl is not None:
            raise InvalidRequestError("cannot setup() again")
        assert self.session is None
##         if self.session is not None:
##             assert self.session is sess
##         else:
        self.session=sess
        self.toolkit=sess.toolkit
        
        self._parent=self.toolkit.getActiveForm()
        self.mainComp = self.toolkit.vpanelFactory(self,weight=1)
        self.toolkit.setActiveForm(self)
            
        #if self.__doc__ is not None:
        #    self.mainComp.label(self.__doc__)
            
        self.layout(self.mainComp)
        self.setupMenu()
        self.mainComp.setup()
        self.ctrl = self.toolkit.createFormCtrl(self)
        self.onShow()
        self.toolkit.executeShow(self)
        return self.returnValue


    def __repr__(self):
        s = self.__class__.__name__
        s += '(title=%r)' % self.getTitle()
        s += ":\n"
##         if True:
##             s += str(self.__doc__)
##         elif self.mainComp is None:
##             s += str(self.__doc__)
        s += "\n  ".join(repr(self.mainComp).splitlines())
        #s += "\n)"
        return s
    
    
    def addAccelerator(self,hotkey,btn):
        self.accelerators.append((hotkey,btn))
        
        
##     def getComponents(self):
##         # implements Container
##         assert self.mainComp is not None, \
##                "Form %s was not setup()" % self.getTitle()
##         return ( self.mainComp, )

##     def addComponent(self,c):
##         # implements Container
##         return self.mainComp.addComponent(c)
        
    def getTitle(self):
        # may override to provide dynamic title
        assert self.title is not None,\
               "%s.title is None and getTitle() not defined" \
               % self.__class__
        return self.title

##     def configure(self,data=None,**kw):
##         if data is not None:
##             from lino.reports.reports import ReportRow
##             assert isinstance(data,ReportRow)
##         Describable.configure(self,data=data,**kw)

##     def getForm(self):
##         return self


##     def setupForm(self):
##         raise "replaced by layout()"

    def layout(self,panel):
        pass

    def setupMenu(self):
        pass
            
##     def set_parent(self,parent):
##         #assert self._parent is None
##         self._parent = parent

    def isShown(self):
        #return hasattr(self,'ctrl')
        return (self.ctrl is not None)

##     def show(self):
##         #assert not self.isShown(), \
##         #       "Form %s already isShown()" % self.getTitle()
##         self.toolkit.executeShow(self)
##         return self.returnValue
        
    
    def onShow(self): self.mainComp.onShow()
    def store(self): self.mainComp.store()
    def onClose(self): self.mainComp.onClose()
        
    def refresh(self):
        self.mainComp.refresh()
        self.toolkit.executeRefresh(self)
        
    def onIdle(self,evt):
        pass
    
    def onKillFocus(self,evt):
        pass
        #self.toolkit.setActiveForm(self._parent)
        
    def onSetFocus(self,evt):
        self.toolkit.setActiveForm(self)

    def close(self,evt=None):
        #if not self.isShown(): return
        #self.mainComp.onClose()
        self.toolkit.setActiveForm(self._parent)
        self.onClose()
        self.toolkit.closeForm(self,evt)
        self.ctrl=None
        #self.session=None
    
    # just forward to self.session:
    def showForm(self,frm):
        #frm.set_parent(self)
        return self.session.showForm(frm)
    def notice(self,*args,**kw):
        return self.session.notice(*args,**kw)
    def message(self,*args,**kw):
        return self.session.message(*args,**kw)
    def confirm(self,*args,**kw):
        return self.session.confirm(*args,**kw)

    def main(self,*args,**kw):
        app=gui.GuiApplication(self)
        app.main(*args,**kw)

##     def show(self):
##         assert self.session is None
##         return gui.getRoot().showForm(self)
        
        
##     def __xml__(self,xml):
##         xml.begin_tag("form",title=self.getTitle())
##         xml.end_tag("form")
        
    
##         for c in self.getComponents():
            
##     def render(self,doc):
##         self.mainComp.render(doc)
        
##     def store(self):
##         self.mainComp.store()

##     def showModal(self):
##         #if self.menuBar is not None:
##         #    raise "Form with menu cannot be modal!"
##         self.show(modal=True)
##         return self.lastEvent == self.defaultButton


class MemoViewer(Form):
    title="Text Editor"
    def __init__(self,txt,**kw):
        self.txt=txt
        Form.__init__(self,**kw)
                    
    def layout(self,add):
        add.entry(
            type=MEMO(width=80,height=10),
            value=self.txt)
                    
        
#class SimpleDbMainForm(DbMainForm):

        
class Dialog(Form):
    
    modal=True
    
    def ok(self):
        #self.store()
        self.returnValue=YES
        self.close()

    def cancel(self):
        self.returnValue=NO
        self.close()


class MessageDialog(Dialog):
    title="Message"
    def __init__(self,msg,**kw):
        Dialog.__init__(self,**kw)
        self.msg=msg
        
    def layout(self,p):
        p.label(self.msg)
        p.okButton()
        
class ConfirmDialog(Dialog):
    title="Confirmation"
    def __init__(self,prompt,default=YES,**kw):
        Dialog.__init__(self,**kw)
        self.prompt=prompt
        self.default=default
        
    def layout(self,panel):
        panel.label(self.prompt)
        
        #p=self.addPanel(HORIZONTAL)
        p=panel.hpanel()
        ok=p.okButton()
        cancel = p.cancelButton()
        if self.default == YES:
            ok.setDefault()
        else:
            cancel.setDefault()

class DecideDialog(Dialog):
    title="Decision"
    def __init__(self,prompt,answers,title=None,default=0,**kw):
        Dialog.__init__(self,**kw)
        self.prompt=prompt
        self.answers=answers
        self.default=default
        if title is not None:
            self.title=title
        
    def decide(self):
        self.returnValue=None
        for i in range(len(self.answers)):
            if self.lastEvent.getLabel() == self.answers[i]:
                self.returnValue=i
        
    def layout(self,panel):
        panel.label(self.prompt)
        
        p=panel.hpanel()
        for ans in self.answers:
            btn=p.button(label=ans,action=self.decide)
            
        ok=p.okButton()
        cancel = p.cancelButton()
        if self.default == YES:
            ok.setDefault()
        else:
            cancel.setDefault()

