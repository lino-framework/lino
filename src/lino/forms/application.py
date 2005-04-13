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
from lino.forms import gui

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
        from lino import __copyright__,  __url__
        s += "\n\n" + __copyright__
        s += "\n\nHomepage:\n" + __url__
        s += "\n\nCredits:\n"
        s += "Python %d.%d.%d %s\n" % sys.version_info[0:4]

        if sys.modules.has_key('wx'):
            wx = sys.modules['wx']
            s += "wxPython " + wx.__version__ + "\n"
    
        if sys.modules.has_key('sqlite'):
            sqlite = sys.modules['sqlite']
            s += "PySQLLite " + sqlite.version + "\n"
    
        if sys.modules.has_key('reportlab'):
            reportlab = sys.modules['reportlab']
            s += "The Reportlab PDF generation library " + \
                           reportlab.Version + "\n"

        if sys.modules.has_key('win32print'):
            win32print = sys.modules['win32print']
            s += "Python Windows Extensions " + "\n"
        
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





