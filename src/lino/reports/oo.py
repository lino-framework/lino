## Copyright Luc Saffre 2003-2005

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

from lino.reports.base import BaseReport, ConfigError

class OoReport(BaseReport):
    
    def __init__(self,
                 document,
                 **kw):
        self.document = document
        BaseReport.__init__(self,**kw)
        
        #self.columnSep = columnSep
        #self.columnHeaderSep = columnHeaderSep
        
        
    def onBeginReport(self):
        self.table = self.document.table(name=self.name)
        for col in self.columns:
            self.table.addColumn()
        BaseReport.onBeginReport(self)


    def renderHeader(self):
        l = [ col.getLabel() for col in self.columns ]
        self.table.addRow(*l)
        

    def onEndRow(self):
        l = [ v for v in self.cellValues ]
        self.table.addRow(*l)
        
