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
#from lino.forms import gui
from lino.ui.console import getSystemConsole


class Application(Describable):

    def __init__(self,
                 #toolkit=None,
                 years="",
                 version=None,
                 author=None,
                 tempDir=".",
                 console=None,
                 **kw):
        self.years = years
        self.version = version
        self.author = author
        self.tempDir = tempDir
        Describable.__init__(self,**kw)
        #if ui is None:
        #    ui = gui.choose(self)
        #self.toolkit = toolkit
        self.mainForm = None
        if console is None:
            console = getSystemConsole()
        self.console = console
        

    def getOptionParser(self,**kw):
        return self.console.getOptionParser(**kw)

    def parse_args(self,argv=None,**kw):
        parser = self.getOptionParser(**kw)
        parser.add_option(
            "-t", "--tempdir",
            help="directory for temporary files",
            action="store",
            type="string",
            dest="tempDir",
            default=self.tempDir)
    
        (options, args) = parser.parse_args(argv)
        self.tempDir = options.tempDir
        return (options, args)

    def setMainForm(self,frm):
        self.mainForm = frm
        
    def getMainForm(self,ui):
        if self.mainForm is None:
            self.mainForm = self.makeMainForm(ui)
        assert self.mainForm.toolkit == ui
        return self.mainForm 

    def makeMainForm(self,ui):
        "must call ui.form(), configure and return it"
        raise NotImplementedError
    

    def init(self,ui):
        pass
    
        
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
        





class AdamoApplication(Application):

    def __init__(self,schema,filename=None,**kw):
        self.schema = schema
        Application.__init__(self,**kw)
        self.filename = filename
        self.sess = None
        
    def addMasterTable(self,tc,**kw):
        """just an idea... for later when there is a default
        makeMainForm method."""
        pass

    def getSession(self):
        return self.sess

    def parse_args(self,
                   argv=None,
                   usage="usage: %prog [options] DBFILE",
                   description="""\
where DBFILE is the name of the sqlite database file""",
                   **kw):
        (options,args) = Application.parse_args(self,
                                                usage=usage,
                                                description=description,
                                                **kw)
        if len(args) == 1:
            self.filename = args[0]
        else:
            self.filename=os.path.join(self.tempDir,
                                       self.name+".db")
        return (options,args)


    def init(self,ui,*args,**kw):
        self.sess = self.schema.quickStartup(ui=ui,
                                             filename=self.filename)
        return Application.init(self,ui,*args,**kw)
        
        
        
    def showTableGrid(self,ui,tc,**kw):
        ds = self.sess.query(tc,**kw)
        return ui.showDataGrid(ds)
    

class MirrorLoaderApplication(AdamoApplication):

    def __init__(self,schema,loadfrom=".",**kw):
        AdamoApplication.__init__(self,schema,**kw)
        self.loadfrom = loadfrom
    
    def getOptionParser(self,**kw):
        parser = AdamoApplication.getOptionParser(self,**kw)
        
        parser.add_option("-l", "--loadfrom",
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

    def getLoaders(self):
        return []
    
    def init(self,ui,*args,**kw):
        self.schema.registerLoaders(self.getLoaders())
        AdamoApplication.init(self,ui,*args,**kw)
