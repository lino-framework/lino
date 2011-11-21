# Copyright 2005-2007 Luc Saffre 

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


import traceback
from cStringIO import StringIO

from lino.misc.descr import Describable
from lino.adamo.datatypes import STRING, MEMO
from lino.console.console import BaseToolkit 
#from lino.console.session import Session
from lino.gendoc.gendoc import GenericDocument

from lino.forms import keyboard
from lino.forms.forms import VERTICAL, HORIZONTAL,\
     Form, MessageDialog, ConfirmDialog, DecideDialog

from lino.forms.dbforms import ReportGridForm

#from lino.forms.forms import Container

def nop(x):
    pass




class Component:
    def __init__(self,form,
                 unusedName=None,label=None,doc=None,
                 enabled=True,
                 weight=0):
        self.form = form
        self._label=label
        self.doc=doc
        self.weight=weight
        self.enabled=enabled and form.enabled

    def getLabel(self):
        if self._label is None:
            return self.__class__.__name__
        return self._label
    
    def hasLabel(self):
        return self._label is not None

    def getDoc(self):
        return self.doc

    def __repr__(self):
        s=self.__class__.__name__+"("
        
        s += ', '.join([
            k+"="+repr(v) for k,v in self.interesting()])
            
        return s+")"
    
    def interesting(self,**kw):
        l=[]
        if self._label is not None:
            l.append(('label',self.getLabel().strip()))
        if not self.enabled:
            l.append( ('enabled',self.enabled))
        return l

    def setFocus(self):
        pass
##     def getForm(self):
##         return self.form.getForm()
    def refresh(self):
        pass
    
    def store(self):
        pass
    
    def onClose(self):
        pass
    
    def onShow(self):
        pass
    
    def setup(self):
        # overridden by toolkit implemetnations
        pass
    
    def render(self,doc):
        doc.p(self.getLabel())


class Adder:

    def __init__(self,frm,cnt):
        self.form=frm
        self.container=cnt



class Container(Component):

    def label(self,label,**kw):
        e = self.form.toolkit.labelFactory(self.form,
                                           label=label,**kw)
        return self.add_component(e)
        
    def entry(self,*args,**kw):
        e = self.form.toolkit.entryFactory(self.form,
                                           None,*args,**kw)
        return self.add_component(e)
    
    def dataentry(self,dc,*args,**kw):
        e = self.form.toolkit.dataEntryFactory(self.form,
                                               dc,*args,**kw)
        return self.add_component(e)

    def datagrid(self,rpt,name=None,*args,**kw):
        e = self.form.toolkit.dataGridFactory(self.form,
                                              rpt,*args,**kw)
        return self.add_component(e)
        
    def hpanel(self,**kw):
        c = self.form.toolkit.hpanelFactory(self.form,**kw)
        return self.add_component(c)
    
    def vpanel(self,**kw):
        c = self.form.toolkit.vpanelFactory(self.form,**kw)
        return self.add_component(c)
    
    def addViewer(self): 
        frm = self.getForm()
        c = frm.toolkit.viewerFactory(self.form)
        return self.add_component(c)
        #self._components.append(c)
        #return c
    
    def button(self,name=None,*args,**kw): 
        btn = self.form.toolkit.buttonFactory(
            self.form,name=name,*args,**kw)
        return self.add_component(btn)

    def formButton(self,frm,*args,**kw):
        b=self.button(label=frm.getTitle())
        b.setHandler(self.form.showForm,frm)
        return b
    
    def okButton(self,*args,**kw):
        b = self.button(name="ok",
                        label="&OK",
                        action=self.form.ok)
        b.setDefault()
        return b

    def cancelButton(self,*args,**kw):
        return self.button(name="cancel",
                           label="&Cancel",
                           hotkey=keyboard.ESCAPE,
                           action=self.form.cancel)

    def closeButton(self,*args,**kw):
        return self.button(name="close",
                           label="&Close",
                           hotkey=keyboard.ESCAPE,
                           action=self.form.close)



    
    
    def refresh(self):
        for c in self.getComponents():
            c.refresh()
        
    def store(self):
        for c in self.getComponents():
            c.store()
        
    def onClose(self):
        for c in self.getComponents():
            c.onClose()

    def onShow(self):
        for c in self.getComponents():
            c.onShow()

    def render(self,doc):
        # used by cherrygui. sorry for ugliness.
        for c in self.getComponents():
            c.render(doc)
            
    def validate(self):
        for e in self.getComponents():
            msg = e.validate()
            if msg is not None:
                return msg


class Panel(Container):
    
    def __init__(self,*args,**kw):
        Component.__init__(self,*args,**kw)
        self._components = []

    def getComponents(self):
        return self._components

    def add_component(self,c):
        self._components.append(c)
        return c

    def __repr__(self):
        s = self.__class__.__name__
        s += ":"
        for c in self._components:
            s += "\n- " + ("\n  ".join(repr(c).splitlines()))
        return s

class VPanel(Panel):
    direction=VERTICAL
    
class HPanel(Panel):
    direction=HORIZONTAL
    


            
            
        
        
        
class Button(Component):
    def __init__(self,form,name=None,label=None,
                 action=None,hotkey=None,
                 *args,**kw):
        #if hotkey is not None:
        #    label += " [" + hotkey.__name__ + "]"
        Component.__init__(self,form,name,label,*args,**kw)
        self.action=action
        self.hotkey=hotkey
        if hotkey is not None:
            form.addAccelerator(hotkey,self)
        self._args = []
        self._kw = {}

    def setHandler(self,action,*args,**kw):
        """set a handler with optional args and keyword parameters.

        """
        self.action = action
        self._args = args
        self._kw = kw

    def setDefault(self):
        """set this as the default button for its form.

        """
        self.form.defaultButton = self
        return self
        
    def click(self):
        """execute this button's handler.

        """
        self.form.store()
        self.form.lastEvent = self
        self.action(*(self._args),**(self._kw))
##         try:
##             self.action(*(self._args),**(self._kw))
##         except InvalidRequestError,e:
##             frm.session.status(str(e))
##         except Exception,e:
##             frm.session.exception(
##                 e,"after clicking '%s' in '%s'" % (
##                 self.getLabel(),frm.getLabel()))

        
    def render(self,doc):
        doc.renderButton(self)

class TextViewer(Component):
    
    def addText(self,v):
        raise NotImplementedError

class TypedMixin:    
    def __init__(self,type):
        if type is None:
            type = STRING
        self._type = type
        
    def format(self,v):
        return self._type.format(self._value)
    
    def getType(self):
        return self._type
    
    def parse(self,s):
        return self._type.parse(s)

    def getMinWidth(self):
        return self._type.minWidth
    def getMaxWidth(self):
        return self._type.maxWidth
    def getMinHeight(self):
        return self._type.minHeight
    def getMaxHeight(self):
        return self._type.maxHeight



class Label(Component,TypedMixin):
    
    def __init__(self,form, type=None,*args,**kw):
        Component.__init__(self,form,*args,**kw)
        TypedMixin.__init__(self,type)

    def render(self,doc):
        doc.renderLabel(self)


    

class BaseEntry(Component):

    def store(self):
        "store data from widget"
        pass
    
    def getValue(self):
        "return current raw value"
        raise NotImplementedError
    
    def setValue(self,v):
        "store raw value"
        raise NotImplementedError
    
##     def format(self,v):
##         "convert raw value to string"
##         raise NotImplementedError

    def render(self,doc):
        doc.renderEntry(self)
    
##     def parse(self,s):
##         "convert the non-empty string to a raw value"
##         raise NotImplementedError
        

class Entry(BaseEntry,TypedMixin):
    def __init__(self,form, name=None, type=None,
                 value=None,
                 *args,**kw):

        Component.__init__(self,form, name, *args,**kw)
        TypedMixin.__init__(self,type)
        self.setValue(value)

    def getValue(self):
        return self._value
    
    def setValue(self,v):
        if v is not None:
            self._type.validate(v)
        self._value = v
        self.refresh()
        
    def refresh(self):
        self.enabled = self.form.enabled
        

class DataEntry(BaseEntry):
    
    def __init__(self,frm,col,*args,**kw):
        BaseEntry.__init__(self,frm, col.name,*args,**kw)
        self.col = col
        
    def interesting(self,**kw):
        l=Component.interesting(self)
        l.insert(0,('name',self.col.name))
        return l
    
    def setValue(self,v):
        row=self.form.getCurrentRow()
        self.col.setCellValue(row,v)
        #print "toolkit:setValue()",v,row
        
    def parse(self,s):
        return self.col.datacol.parse(s)
    
    def format(self,v):
        return self.col.format(v)

    def getType(self):
        return self.col.getType()

    def getMaxWidth(self):
        return self.col.datacol.getMaxWidth()
    def getMinWidth(self):
        return self.col.datacol.getMinWidth()
    def getMaxHeight(self):
        return self.col.datacol.getMaxHeight()
    def getMinHeight(self):
        return self.col.datacol.getMinHeight()
    
    def getValue(self):
        return self.col.getCellValue(self.form.getCurrentRow())

    def refresh(self):
        frm = self.form
        self.enabled = frm.enabled and self.col.canWrite(
            frm.getCurrentRow())
        


class MenuItem(Button):
    pass
##     def __init__(self,form,name,accel,*args,**kw):
##         Button.__init__(self,form,name,*args,**kw)
##         self.accel = accel

class Menu(Component):
    def __init__(self,*args,**kw):
        Component.__init__(self,*args,**kw)
        self.items = []

    def addItem(self,name,**kw):
        i = MenuItem(self.form,name,**kw)
        self.items.append(i)
        return i
    
    def addButton(self,btn,**kw):
        kw.setdefault("label",btn.getLabel())
        kw.setdefault("action",btn.action)
        return self.addItem(**kw)
    
    def addLink(self,htdoc,**kw):
        # used by gendoc.html
        kw.setdefault("label",htdoc.title)
        kw.setdefault("action",self.form.urlto(htdoc))
        return self.addItem(htdoc.name,**kw)
    
    def findItem(self,name):
        for mi in self.items:
            if mi.name == name: return mi













class MenuBar(Component):
    
    def __init__(self,*args,**kw):
        Component.__init__(self,*args,**kw)
        self.menus = []

    def addMenu(self,*args,**kw):
        i = Menu(self.form,*args,**kw)
        self.menus.append(i)
        return i
    
    def findMenu(self,name):
        for mnu in self.menus:
            if mnu.name == name: return mnu


class DataGrid(Component):
    def __init__(self,form,rpt,pageNum=1,*args,**kw):
        Component.__init__(self,form,*args,**kw)
        #ReportMixin.__init__(self,rpt)
        self.rpt = rpt # a Query or a Report
        self.choosing = False
        self.chosenRow = None
        self.pageNum=pageNum

    def __repr__(self):
        s=Component.__repr__(self)
        s += " of " + self.form.rpt.__class__.__name__
        if self.enabled:
            s += " with %d rows" % len(self.form.rpt)
        return s

    def __len__(self):
        return len(self.rpt)
                  
    def setModeChoosing(self):
        self.choosing = True

    def getChosenRow(self):
        return self.chosenRow
    
    def setChosenRow(self,row):
        self.chosenRow = row
        
    def getSelectedRows(self):
        raise NotImplementedError




    

class Toolkit(BaseToolkit):
    
    labelFactory = Label
    entryFactory = Entry
    dataEntryFactory = DataEntry
    buttonFactory = Button
    vpanelFactory = VPanel
    hpanelFactory = HPanel
    viewerFactory = TextViewer
    dataGridFactory = DataGrid
    menuBarFactory = MenuBar
    
    def __init__(self,console=None):
        self.root=None
        self._running=False
        if console is None:
            from lino.console import syscon
            console=syscon.getSystemConsole()
        self.console = console
        self._activeForm=None

    def setActiveForm(self,frm):
        #assert frm is not None
        #print "setActiveForm()",frm
        self._activeForm = frm

    def getActiveForm(self):
        return self._activeForm

##     def setupOptionParser(self,p):
##         self.console.setupOptionParser(p)
        
    def shutdown(self):
        pass
    
    def show_verbose(self,*args,**kw):
        self.console.show_verbose(*args,**kw)
    def show_status(self,*args,**kw):
        self.console.show_status(*args,**kw)
        
    def show_debug(self,*args,**kw):
        self.console.show_debug(*args,**kw)
        
        
    def onTaskBegin(self,*args,**kw):
        return self.console.onTaskBegin(*args,**kw)
    def onTaskDone(self,*args,**kw):
        return self.console.onTaskDone(*args,**kw)
    def onTaskAbort(self,*args,**kw):
        return self.console.onTaskAbort(*args,**kw)
    def onTaskIncrement(self,*args,**kw):
        return self.console.onTaskIncrement(*args,**kw)
    def onTaskBreathe(self,*args,**kw):
        return self.console.onTaskBreathe(*args,**kw)
    

    
    def showException(self,sess,e,details=None):
        print details
        raise
        msg = str(e)
        #msg = e.getMessage()
        out = StringIO()
        traceback.print_exc(None,out)
        s = out.getvalue()
        del out
        if details is not None:
            msg += "\n" + details
        while True:
            i = sess.decide(
                msg,
                title="Oops, an error occured!",
                answers=("&End",
                         "&Ignore",
                         "&Details",
                         "&Send"))
            if i == 0:
                sess.critical(s)
                return
            
            elif i == 1:
                return
            elif i == 2:
                frm = sess.form(label="Details")
                frm.addEntry(type=MEMO,value=s)
                frm.showModal()
                #return
                

    def show_report(self,sess,rpt,**kw):
        raise DeprecationError("")
        return sess.showForm(ReportGridForm(rpt))
        

    def show_notice(self,sess,*args,**kw):
        self.console.show_notice(sess,*args,**kw)
        #assert app.mainForm is not None
##         if self._activeForm is not None:
##             self._activeForm.status(*args,**kw)
##         else: self.show_message(sess,*args,**kw)
        

    def show_message(self,sess,msg,*args,**kw):
        msg=sess.buildMessage(msg,*args)
        return sess.showForm(MessageDialog(msg,**kw))
        

    def show_confirm(self,sess,*args,**kw):
        return sess.showForm(ConfirmDialog(*args,**kw))
        


    def show_decide(self,sess,*args,**kw):
        return sess.showForm(DecideDialog(*args,**kw))
    
##     def show_decide(self,sess,prompt,answers,
##                title="Decision",
##                default=0):
##         raise "must be converted like message and confirm"
##         frm = sess.form(label=title,doc=prompt)
##         #p = frm.addPanel(HORIZONTAL)
##         p = frm.addHPanel()
##         buttons = []
##         for i in range(len(answers)):
##             btn = p.addButton(label=answers[i])
##             btn.setHandler(frm.close)
##             buttons.append(btn)
##         frm.showModal()
##         for i in range(len(answers)):
##             if frm.lastEvent == buttons[i]:
##                 return i
##         raise "internal error: no button clicked?"
        
    
    def createFormCtrl(self,frm):
        return 1

    def executeShow(self,frm):
        raise NotImplementedError

    def executeRefresh(self,frm):
        pass

        
        

        
    def running(self):
        #return self._running # self.wxapp is not None
        return self.root is not None

    def run_forever(self):
        pass
    
    def run_awhile(self):
        pass
        #raise NotImplementedError

    def stop_running(self):
        pass
    
    #def start_running(self):
    def start_running(self,app):
        assert not self.running()
        self.root=app
        #self.onTaskBegin(app)
        #self._running=true
        


