#coding: latin1
## Copyright 2004-2005 Luc Saffre 

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

import sys
import os
opj = os.path.join

from lino.ui import console

#from lino.apps.raceman.schema import makeSchema

from lino.apps.raceman import races, loaders

from lino.apps.raceman.races import 
     Categories, Participants, Persons, Clubs

from lino.forms.application import MirrorLoaderApplication

import datetime

from lino.adamo.datatypes import STRING

## class Arrivals:
##     def __init__(self,app,race=None,
##                  datafile="arrivals.txt"):
##         self.app = app
##         self.race = race
##         self.data = []
##         self.datafile = datafile
##         self.starttime = None
##         self.frm = None

##     def writedata(self):
##         f = file(self.datafile,"a")
##         for line in self.data:
##             f.write("\t".join(line)+"\n")
##         f.close()
##         self.frm.info("wrote %d lines to %s" % (len(self.data),
##                                                 self.datafile))
##         self.data = []
##         #parent.buttons.arrive.setFocus()
##         self.frm.entries.dossard.setFocus()

##     def arrive(self):
##         if self.starttime is None:
##             self.frm.buttons.start.setFocus()
##             self.frm.info("cannot arrive before start")
##             return
##         now = datetime.datetime.now()
##         duration = now - self.starttime
##         line = (
##             self.frm.entries.dossard.getValue(),
##             str(now), str(duration)
##             )
##         self.data.append(line)
##         self.frm.info("%s arrived at %s after %s" % line)
##         self.frm.entries.dossard.setValue('*')
##         self.frm.entries.dossard.setFocus()
    
##     def exit(self):
##         if len(self.data) > 0:
##             if self.app.confirm("write data to file?"):
##                 self.writedata()
##             else:
##                 self.frm.entries.dossard.setFocus()
##                 return
##         self.frm.close()

##     def start(self):
##         self.starttime = datetime.datetime.now()
##         self.frm.info("started at %s" %str(self.starttime))
##         #parent.buttons.arrive.setFocus()
##         self.frm.entries.dossard.setFocus()

##     def __call__(self):
##         frm = self.app.addForm(
##             label="Raceman arrivals",
##             doc="""\
## Ankunftszeiten an der Ziellinie erfassen.
## Beim Startschuss "Start" klicken!
## Jedesmal wenn einer ankommt, ENTER drücken.
##     """)
        
##         frm.addEntry("dossard",STRING,
##                      label="Dossard",
##                      value="*",
##                      doc="""Hier die Dossardnummer des ankommenden Läufers eingeben, oder '*' wenn sie später erfasst werden soll.""")

        
##         #bbox = frm.addHPanel()
##         bbox = frm
##         bbox.addButton(name="start",
##                       label="&Start",
##                       action=self.start)
##         bbox.addButton(name="arrive",
##                       label="&Arrive",
##                       action=self.arrive).setDefault()
##         bbox.addButton("write",label="&Write",action=self.writedata)
##         bbox.addButton("exit",label="&Exit",action=self.exit)

## ##         fileMenu  = frm.addMenu("&File")
## ##         fileMenu.addButton(frm.buttons.write,accel="Ctrl-S")
## ##         fileMenu.addButton(frm.buttons.exit,accel="Ctrl-Q")
        
## ##         fileMenu  = frm.addMenu("&Edit")
## ##         fileMenu.addButton(frm.buttons.start)
## ##         fileMenu.addButton(frm.buttons.arrive,accel="Ctrl-A")
##         self.frm = frm
##         frm.show()
    

class Raceman(MirrorLoaderApplication):
        
    def makeMainForm(self):
        self.arrivals = Arrivals(self)
        frm = self.addForm(
            label="Main menu",
            doc="""\
This is the Raceman main menu.                                     
"""+("\n"*10))

        m = frm.addMenu("&Stammdaten")
        m.addItem(label="&Races").setHandler(
            self.showTableGrid,
            Races,
            columnNames="id name1 date startTime status tpl type name2")
        m.addItem(label="&Clubs").setHandler(self.showTableGrid,
                                             Clubs)
        m.addItem(label="&Personen").setHandler(self.showTableGrid,
                                                Persons)
    
        #m = frm.addMenu("&Arrivals")
        #m.addItem(label="&Erfassen").setHandler(self.arrivals)
        
        m = frm.addMenu("&Programm")
        m.addItem(label="&Beenden",action=frm.close)
        m.addItem(label="Inf&o",action=self.showAbout)

        return frm

        

def main(argv):

    app = Raceman(name="Raceman",
                  years='2005',
                  tempDir=r'c:\temp',
                  loadfrom=r'c:\temp\timrun')
    (options, args) = app.parse_args(argv)


    #workdir = options.tempDir
    #schema = makeSchema(app.loadfrom)
    schema = adamo.Schema()
    races.setupSchema(schema)
    app.setMirrorLoaders(loaders)
    #loaders.setupSchema(schema)
    app.startup(schema)
    #filename=opj(workdir,"raceman.db")
    #sess = schema.quickStartup(filename=filename)
    app.main()
    




if __name__ == '__main__':
    #console.copyleft(name="Lino/Raceman", years='2002-2005')
    main(sys.argv[1:])




