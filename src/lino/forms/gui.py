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

#from lino.ui.console import ConsoleApplication
from lino.console import syscon

_toolkit = None
#_app = None



def choose(wishlist="tix"):
    global _toolkit
    
    assert _toolkit is None, "cannot choose a second time"
    
    for tkname in wishlist.split():
        if tkname == "tix": 
            from lino.forms.tix.tixform import Toolkit
            _toolkit = Toolkit()
            return _toolkit
        if tkname == "wx": 
            from lino.forms.wx.wxform import Toolkit
            _toolkit = Toolkit()
            return _toolkit
        if tkname == "testkit": 
            from lino.forms.testkit import Toolkit
            _toolkit = Toolkit()
            return _toolkit
        if tkname == "console": 
            from lino.forms.console import Toolkit
            _toolkit = Toolkit()
            return _toolkit
        if tkname == "cherrypy": 
            from lino.forms.cherrygui import Toolkit
            _toolkit = Toolkit()
            return _toolkit
        
        if tkname == "htmlgen":
            from lino.console.htmlgen_toolkit import Toolkit
            #from lino.forms.cherrypy import Toolkit
            _toolkit = Toolkit()
            return _toolkit
    raise "no toolkit found"

def check():
    if _toolkit is None:
        choose()
        #GuiConsole(toolkit=_toolkit)

    
## def form(*args,**kw):
##     check()
##     global _app
##     if _app is None:
##         from lino.forms.application import BaseApplication
##         _app = BaseApplication(toolkit=_toolkit)
##         #from lino.forms.application import AutomagicApplication
##         #_app = AutomagicApplication(toolkit=_toolkit,*args,**kw)
##         #return _app._form
##     return _app.form(None,*args,**kw)
## ##     frm = _app.form(None,*args,**kw)
## ##     _app.mainForm = frm
## ##     return frm

## def parse_args(*args,**kw):
##     check()
##     #assert _app is not None, "only for use with automagicApp"
##     return _toolkit.parse_args(*args,**kw)

def run(sess):
    check()
    sess.setToolkit(_toolkit)
    #print _toolkit
    #_toolkit.addSession(sess)
    _toolkit.run_forever(sess)
    #_toolkit.main(app)
    
def install():
    check()
    syscon.setToolkit(_toolkit)
    
def runApplication(app):
    check()
    syscon.setToolkit(_toolkit)
    syscon._session.app = app
    _toolkit.run_forever(syscon._session)
    
## def main(*args,**kw):
##     check()
##     return _toolkit.main(*args,**kw)

## def run(app,*args,**kw):
##     check()
##     _toolkit.setApplication(app)
##     return _toolkit.main(*args,**kw)
##     #return _toolkit.main(*args,**kw)



## class GuiApplication(ConsoleApplication):

##     def __init__(self, toolkit,**kw):
##         if toolkit is None:
##             toolkit = choose()
##         self.toolkit = toolkit
##         self.toolkit.addApplication(self)
##         ConsoleApplication.__init__(self,**kw)
        
##     def form(self,parent=None,*args,**kw):
##         return self.toolkit.formFactory(self,parent,*args,**kw)
    
##     def setupOptionParser(self,parser):
##         self.toolkit.setupOptionParser(parser)

##     def applyOptions(self,options,args):
##         return self.toolkit.applyOptions(options,args)
    
##     def init(self):
##         # supposed to show the application's main form
##         pass

##     def run(self):
##         self.toolkit.run_forever()

##     def close(self):
##         self.toolkit.closeApplication(self)



## class AutomagicApplication(GuiApplication):
    
##     def __init__(self, toolkit,*args,**kw):
##         GuiApplication.__init__(self,toolkit)
##         self._form = self.form(*args,**kw)
        
##     def init(self):
##         self._form.show()
        



## class GUI:
##     def __init__(self):
##         self.app = None

##     def form(self,*args,**kw):
##         if self.app is None:
##             self.app = Application()
##         return self.app.form(*args,**kw)

##     def textprinter(self):
##         from lino.textprinter.plain import PlainTextPrinter
##         return PlainDocument(self.out)
        
##     def report(self,**kw):
##         from lino.reports.plain import Report
##         return Report(writer=self.out,**kw)

