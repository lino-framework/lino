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

from lino.forms.base import Application
from lino.adamo.datasource import Datasource

class AdamoApplication(Application):

    def __init__(self,filename=None,**kw):
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
                   description="where DBFILE is the name of the sqlite database file",
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


    def startup(self,schema):
        self.sess = schema.quickStartup(filename=self.filename)
        
    def showTableGrid(self,tc,**kw):
        ds = self.sess.query(tc,**kw)
        return self.showDataGrid(ds)
    
    def showDataGrid(self,ds,**kw):
        assert isinstance(ds,Datasource)
        frm = self.mainForm.addForm(label=ds.getLabel(),**kw)
        frm.addDataGrid(ds)
        frm.show()


class MirrorLoaderApplication(AdamoApplication):

    def __init__(self,loadfrom=None,**kw):
        AdamoApplication.__init__(self,**kw)
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
    
    def startup(self,schema):
        schema.registerLoaders(self.getLoaders())
        return AdamoApplication.startup(self,schema)
