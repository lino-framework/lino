#coding: latin1
## Copyright 2004-2006 Luc Saffre 

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

from lino.forms.gui import DbApplication
from lino.forms.forms import DbMainForm

from lino.apps.raceman import loaders
from lino.apps.raceman.raceman_tables import *

class RacemanMainForm(DbMainForm):
    """\
This is the Raceman main menu.                                     
    """
    
    def setupMenu(self):

        m = self.addMenu("master","&Stammdaten")
        
        m.addReportItem("events",races.EventsReport,
                        label="&Events")
        
        m.addReportItem("races",races.RacesReport,
                        label="&Races")
        
        m.addReportItem("clubs",races.ClubsReport,
                        label="&Clubs")
        
        m.addReportItem("persons",races.PersonsReport,
                        label="&Persons")
        
        self.addProgramMenu()
        


    
class Raceman(DbApplication):
    
    name="Raceman"
    years='2005-2006'
    #tables = races.TABLES
    schemaClass=RacemanSchema
    mainFormClass=RacemanMainForm
    loadMirrorsFrom="."
    

    def setupApplication(self):
        l=[lc(self.loadfrom) for lc in loaders.LOADERS]
        self.registerLoaders(l)


    def registerLoaders(self,loaders):
        for l in loaders:
            it = self.dbsess.schema.findImplementingTables(
                l.tableClass)
            assert len(it) == 1
            it[0].setMirrorLoader(l)

    def setupOptionParser(self,parser):
        DbApplication.setupOptionParser(self,parser)
        parser.add_option("--loadfrom",
                          help="""\
directory containing mirror source files""",
                          action="store",
                          type="string",
                          dest="loadfrom",
                          default=".")
        
        

if __name__ == '__main__':
    Raceman().main()




