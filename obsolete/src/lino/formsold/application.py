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

import os

from lino.misc.descr import Describable
from lino.adamo.datasource import Datasource
from lino.adamo.schema import Schema
from lino.forms import gui
#from lino.ui.console import getSystemConsole
from lino.ui import console



class Application(Describable):

    def __init__(self,
                 toolkit=None,
                 years="",
                 version=None,
                 author=None,
                 tempDir=".",
                 #mainForm=None,
                 #console=None,
                 **kw):
        if toolkit is None:
            toolkit = gui.choose()
        self.toolkit = toolkit
        self.toolkit.addApplication(self)
        
        self.years = years
        self.version = version
        self.author = author
        self.tempDir = tempDir
        Describable.__init__(self,**kw)
        self.mainForm = None
##         if console is None:
##             console = getSystemConsole()
##         self.console = console
        

    def form(self,parent=None,*args,**kw):
        return self.toolkit.formFactory(self,parent,*args,**kw)
    
    def getOptionParser(self,**kw):
        parser = self.toolkit.getOptionParser(**kw)
        parser.add_option(
            "-t", "--tempdir",
            help="directory for temporary files",
            action="store",
            type="string",
            dest="tempDir",
            default=self.tempDir)
        return parser
        #return self.toolkit.getOptionParser(**kw)

    def parse_args(self,argv=None,**kw):
        parser = self.getOptionParser(**kw)
        (options, args) = parser.parse_args(argv)
        self.tempDir = options.tempDir
        return (options, args)

##     def setMainForm(self,frm):
##         self.mainForm = frm
        
##     def getMainForm(self,ui):
##         if self.mainForm is None:
##             self.mainForm = self.makeMainForm(ui)
##         assert self.mainForm.toolkit == ui
##         return self.mainForm 

##     def makeMainForm(self,ui):
##         "must call ui.form(), configure and return it"
##         raise NotImplementedError

    def addProgramMenu(self,frm):
        m = frm.addMenu("&Programm")
        m.addItem(label="&Beenden",action=frm.close)
        m.addItem(label="Inf&o").setHandler(self.showAbout)
        #m.addItem(label="show &Console").setHandler(self.showConsole)
        return m


    def showAbout(self):
        frm = self.form(label="About",doc=self.aboutString())
        frm.addOkButton()
        frm.show()
        
        
    def aboutString(self):
        s = self.name
        if self.version is not None:
            s += " version " + self.version
        if self.author is not None:
            s += "Copyright (c) %s %s." % self.years, self.author
        from lino import __copyright__, __credits__, __url__
        s += "\n\n" + __copyright__
        s += "\n\nCredits:\n" + __credits__
        s += "\n\nHomepage:\n" + __url__
        return s
    
    def showConsole(self):
        frm = self.form(label="Console",
                        halign=gui.RIGHT, valign=gui.BOTTOM)
        frm.addViewer()
        frm.show()

    def init(self):
        # supposed to show the application's main form
        pass

    def run(self):
        self.toolkit.start()

    def close(self):
        self.toolkit.closeApplication(self)
        
    
        
##     def main(self,frm=None):
##         if frm is None:
##             console.debug("app.main() explicit call")
##             #self.console.copyleft(name=self.name,
##             #                      years=self.years)
##             self.mainForm.show()
##             console.set(ui=self)
##         else:
##             console.debug("app.main() automagic call")
##             self.mainForm = frm
            
##         #self.ui.mainLoop()
        

## class GuiConsole(Application):
    
##     def write(self,s):
##         n = self.consoleEntry.getValue() + s
##         self.consoleEntry.setValue(n)

##     def init(self,toolkit):
##         frm self.form(None,label="Console")
##         self.consoleEntry = frm.addEntry(
##             type=MEMO(height=10,width=90))
##         self.mainForm = frm
##         console._syscon.redirect(stdout=self,stderr=self)
##         self.mainForm.show()





class AdamoApplication(Application):

    def __init__(self,filename=None,**kw):
        Application.__init__(self,**kw)
        self.schema = Schema()
        self.filename = filename
        self.sess = None
        
    def getSession(self):
        return self.sess

    def parse_args(self,
                   argv=None,
                   usage="usage: %prog [options] DBFILE",
                   description="""\
where DBFILE is the name of the sqlite database file""",
                   **kw):
        (options,args) = Application.parse_args(
            self,
            usage=usage,
            description=description,
            **kw)
        if len(args) == 1:
            self.filename = args[0]
        else:
            self.filename=os.path.join(self.tempDir,
                                       self.name+".db")
        return (options,args)


    def init(self): #,*args,**kw):
        # called from Toolkit.main()
        self.sess = self.schema.quickStartup(
            ui=self.toolkit.console,
            filename=self.filename)
##         return Application.init(self,
##                                 self.toolkit.console,
##                                 *args,**kw)
        
        
        
    def showTableGrid(self,ui,tc,*args,**kw):
        ds = self.sess.query(tc,*args,**kw)
        return ui.showDataGrid(ds)
    
    def showViewGrid(self,ui,tc,viewName="std",*args,**kw):
        ds = self.sess.view(tc,viewName,*args,**kw)
        return ui.showDataGrid(ds)
    

class MirrorLoaderApplication(AdamoApplication):

    def __init__(self,loadfrom=".",**kw):
        AdamoApplication.__init__(self,**kw)
        self.loadfrom = loadfrom
    
    def getOptionParser(self,**kw):
        parser = AdamoApplication.getOptionParser(self,**kw)
        
        parser.add_option("--loadfrom",
                          help="""\
                          directory for mirror source files""",
                          action="store",
                          type="string",
                          dest="loadfrom",
                          default=self.loadfrom)
        return parser
    
    def parse_args(self,argv=None):
        (options, args) = AdamoApplication.parse_args(self,argv)
        self.loadfrom = options.loadfrom
        return (options, args)

##     def getLoaders(self):
##         return []
    
##     def init(self,ui,*args,**kw):
##         self.schema.registerLoaders(self.getLoaders())
##         AdamoApplication.init(self,ui,*args,**kw)
