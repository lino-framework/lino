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

from lino.forms import Application
from lino.adamo.datasource import Datasource
from lino.adamo.schema import Schema


class AdamoApplication(Application):

    usage="usage: %prog [options] DBFILE"
    description="""\
where DBFILE is the name of the sqlite database file"""
    
    def __init__(self,filename=None,**kw):
        Application.__init__(self,**kw)
        self.schema = Schema()
        self.filename = filename
        self.sess = None
        
    def getSession(self):
        return self.sess

    def applyOptions(self,options,args):
        Application.applyOptions(self,options,args)
        if len(args) == 1:
            self.filename = args[0]
        else:
            self.filename=os.path.join(self.tempDir,
                                       self.name+".db")

##     def parse_args(self,
##                    argv=None,
##                    usage="usage: %prog [options] DBFILE",
##                    description="""\
## where DBFILE is the name of the sqlite database file""",
##                    **kw):
##         (options,args) = Application.parse_args(
##             self,
##             usage=usage,
##             description=description,
##             **kw)
##         if len(args) == 1:
##             self.filename = args[0]
##         else:
##             self.filename=os.path.join(self.tempDir,
##                                        self.name+".db")
##         return (options,args)


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
    
    def setupOptionParser(self,parser):
        AdamoApplication.setupOptionParser(self,parser)
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

    


