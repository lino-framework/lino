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

from lino.adamo.ddl import Schema
from lino.forms import DbMainForm, DbApplication

import pinboard_tables as tables


    
class PinboardMainForm(DbMainForm):
    
    def setupMenu(self):
        m = self.addMenu("pinboard","&Pinboard")
        
        self.addReportItem(m,"authors",tables.AuthorsReport,
                        label="&Authors")
        self.addReportItem(m,"publications",tables.PublicationsReport,
                        label="&Publications")
        self.addReportItem(m,"nodes",tables.NodesReport,
                        label="&Nodes")
        self.addReportItem(m,"news",tables.NewsItemsReport,
                        label="&News")
        self.addReportItem(m,"newsgroups",tables.NewsgroupsReport,
                        label="&Newsgroups")
        
##         m = frm.addMenu("reports","&Reports")
##         m.addItem("s",label="&Static HTML").setHandler(
##             self.writeStaticSite,sess)
        
        self.addProgramMenu()



class Pinboard(DbApplication):
    name="Lino Pinboard"
    years='2005-2006'
    author="Luc Saffre"
    schemaClass=tables.PinboardSchema
    
    
    

if __name__ == '__main__':
    Pinboard().main()
