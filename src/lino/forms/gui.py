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
from lino.console import Application, syscon


## _toolkit = None

## def choose(wishlist=None):
##     #if console is None:
##     #    console=syscon.getSystemConsole()
##     global _toolkit
##     assert _toolkit is None, "cannot choose a second time"
##     _toolkit=createToolkit(wishlist)
##     return _toolkit
    

## def check():
##     if _toolkit is None:
##         choose()
##         #GuiConsole(toolkit=_toolkit)

    
## def run(app,*args,**kw):
##     check()
##     _toolkit.startApplication(app)
##     _toolkit.run_forever(*args,**kw)
    
## def run(sess):
##     check()
##     sess.setToolkit(_toolkit)
##     #print _toolkit
##     #_toolkit.addSession(sess)
##     _toolkit.run_forever(sess)
##     #_toolkit.main(app)
    
## def install():
##     check()
##     syscon.setToolkit(_toolkit)
    
## def runApplication(app):
##     check()
##     syscon.setToolkit(_toolkit)
##     syscon._session.app = app
##     _toolkit.run_forever(syscon._session)
    

class GuiApplication(Application):
    wishlist="wx tix cp console"

    def __init__(self,mainForm,*args,**kw):
        Application.__init__(self,*args,**kw)
        self.mainForm=mainForm
    

    def createToolkit(self):
        console=syscon.getSystemConsole()
        if console.isInteractive():
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

    
    

##     def main(self,*args,**kw):
##         kw['toolkit']=createToolkit(wishlist=self.wishlist)
##         Application.main(self,*args,**kw)

    def run(self,*args,**kw):
##         if self.mainForm is None:
##             self.mainForm=self.mainFormClass(*args,**kw)
        self.showForm(self.mainForm)
        self.toolkit.run_forever()
        


## def show(frm):#,*args,**kw):
##     app=GuiApplication(frm)
##     #toolkit=createToolkit(*args,**kw)
##     #app.main(*args,**kw)
##     #check()
##     app.main()
##     #toolkit.submit(frm)
##     #toolkit.run_forever(*args,**kw)
    

class DbApplication(GuiApplication):
    
    mainFormClass=None
    schemaClass=None

    def __init__(self,dbsess=None,mainForm=None,*args,**kw):
        
        if dbsess is None:
            dbsess=self.createContext()
        self.dbsess=dbsess
        if mainForm is None:
            mainForm=self.createMainForm()
        GuiApplication.__init__(self,mainForm)

    def quickStartup(self,*args,**kw):
        raise "use app.dbsess"
            
    def createContext(self):
        return self.schemaClass().quickStartup()
    
    def createMainForm(self):
        return self.mainFormClass(self.dbsess)
        
