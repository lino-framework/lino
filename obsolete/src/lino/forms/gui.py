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

import lino
from lino.console import Application
from lino.console import syscon

## _toolkit=None

## def start_toolkit(wishlist=None):
##     global _toolkit
##     assert _toolkit is None
##     _toolkit=create_toolkit(*args,**kw)
##     _toolkit.run_forever()
    
## def create_toolkit(*args,**kw):
##     if wishlist is None:
##         if syscon.getSystemConsole().isInteractive():
##             wishlist="wx tix cp console"
##             wishlist=self.wishlist
##         else:
##             wishlist="testkit"
            
##         #if wishlist is None:
##         #    wishlist=lino.config.get('forms','wishlist')

##         for tkname in wishlist.split():
##             #print tkname
##             if tkname == "tix": 
##                 from lino.forms.tix.tixform import Toolkit
##                 return Toolkit()
##             if tkname == "wx": 
##                 from lino.forms.wx.wxtoolkit import Toolkit
##                 return Toolkit()
##             if tkname == "testkit": 
##                 from lino.forms.testkit import Toolkit
##                 return Toolkit()
##             if tkname == "console":
##                 return console
##                 #from lino.forms.console import Toolkit
##                 #return Toolkit()
##             if tkname == "cp": 
##                 from lino.forms.cherrygui import Toolkit
##                 return Toolkit()
##             if tkname == "htmlgen":
##                 from lino.console.htmlgen_toolkit import Toolkit
##                 return Toolkit()

##         raise "no toolkit found for wishlist %r" % wishlist



class GuiApplication(Application):
    """An Application that runs in a GUI and has a main form.

    wishlist is a space-separated list of GUI toolkits, in order of
    preference.

    If mainFormClass is not None, this class will be used to
    instanciate the main form.
    
    """
    wishlist="qt wx tix cp console"
    mainFormClass=None

    def __init__(self,mainForm=None,*args,**kw):
        Application.__init__(self,*args,**kw)
        self.mainForm=mainForm
        self.console=None

    def start_running(self):
        self.console=self.toolkit
        self.toolkit=self.createToolkit()
        self.toolkit.start_running(self)

    def run(self,*args,**kw):
        #assert self.console is None
        if self.mainForm is None:
            self.mainForm=self.createMainForm()
        #self.createMainForm()
        #print self.mainForm
        self.showForm(self.mainForm)
        self.toolkit.run_forever()
        
    def createToolkit(self):
        if self.console.isInteractive():
            wishlist=self.wishlist
        else:
            wishlist="testkit"
            
        #if wishlist is None:
        #    wishlist=lino.config.get('forms','wishlist')

        for tkname in wishlist.split():
            #print tkname
            if tkname == "tix": 
                from lino.forms.tix.tixform import Toolkit
                return Toolkit()
            if tkname == "qt": 
                from lino.forms.qt.qttoolkit import Toolkit
                return Toolkit()
            if tkname == "wx": 
                from lino.forms.wx.wxtoolkit import Toolkit
                return Toolkit()
            if tkname == "testkit": 
                from lino.forms.testkit import Toolkit
                return Toolkit()
            if tkname == "console":
                return console
                #from lino.forms.console import Toolkit
                #return Toolkit()
            if tkname == "cp": 
                from lino.forms.cherrygui import Toolkit
                return Toolkit()
            if tkname == "htmlgen":
                from lino.console.htmlgen_toolkit import Toolkit
                return Toolkit()

        raise "no toolkit found for wishlist %r" % wishlist

    def createMainForm(self):
        #if self.mainForm is None:
        #    self.mainForm=self.mainFormClass()
        return self.mainFormClass()
    


## def show(frm):#,*args,**kw):
##     app=GuiApplication(frm)
##     #toolkit=createToolkit(*args,**kw)
##     #app.main(*args,**kw)
##     #check()
##     app.main()
##     #toolkit.submit(frm)
##     #toolkit.run_forever(*args,**kw)
    

## class DbApplication(GuiApplication):
    
##     schemaClass=None

##     def __init__(self,dbc=None,mainForm=None,*args,**kw):
##         self.dbsess=dbc
##         GuiApplication.__init__(self,mainForm)

##     def createMainForm(self):
##         return self.mainFormClass(self.dbsess)

##     def run(self,dbc=None,*args,**kw):
##         if dbc is None:
##             dbc=self.createContext()
##         self.dbsess=dbc
##         GuiApplication.run(self,*args,**kw)
        
