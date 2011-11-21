#coding: latin1
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

#import time
import datetime

from lino.adamo.datatypes import STRING
from lino.forms.wx.wxform import Form
from lino.ui import console

class Main:
    def __init__(self,datafile="arrivals.txt"):
        self.data = []
        self.datafile = datafile
        self.starttime = None

    def writedata(self,parent):
        f = file(self.datafile,"a")
        for line in self.data:
            f.write("\t".join(line)+"\n")
        f.close()
        parent.info("wrote %d lines to %s" % (len(self.data),
                                              self.datafile))
        self.data = []
        #parent.buttons.arrive.setFocus()
        parent.entries.dossard.setFocus()

    def arrive(self,frm):
        if self.starttime is None:
            frm.buttons.start.setFocus()
            frm.error("cannot arrive before start")
            return
        now = datetime.datetime.now()
        duration = now - self.starttime
        line = (
            frm.entries.dossard.getValue(),
            str(now), str(duration)
            )
        self.data.append(line)
        frm.info("%s arrived at %s after %s" % line)
        frm.entries.dossard.setValue('*')
        frm.entries.dossard.setFocus()
    
    def exit(self,parent):
        if len(self.data) > 0:
            if parent.confirm("write data to file?"):
                self.writedata(parent)
            else:
                parent.entries.dossard.setFocus()
                return
        parent.close(parent)

    def start(self,parent):
        self.starttime = datetime.datetime.now()
        parent.info("started at %s" %str(self.starttime))
        #parent.buttons.arrive.setFocus()
        parent.entries.dossard.setFocus()

    def run(self):
        
        frm = Form(label="Raceman arrivals",
                   doc="""\
Ankunftszeiten an der Ziellinie erfassen.
Beim Startschuss "Start" klicken!
Jedesmal wenn einer ankommt, ENTER drücken.
    """)
        
        frm.addEntry("dossard",STRING,
                     label="Dossard",
                     value="*",
                     doc="""Hier die Dossardnummer des ankommenden Läufers eingeben, oder '*' wenn sie später erfasst werden soll.""")

        
        #bbox = frm.addHPanel()
        bbox = frm
        bbox.addButton(name="start",
                      label="&Start",
                      onclick=self.start)
        bbox.addButton(name="arrive",
                      label="&Arrive",
                      onclick=self.arrive).setDefault()
        bbox.addButton("write",label="&Write",onclick=self.writedata)
        bbox.addButton("exit",label="&Exit",onclick=self.exit)

##         fileMenu  = frm.addMenu("&File")
##         fileMenu.addButton(frm.buttons.write,accel="Ctrl-S")
##         fileMenu.addButton(frm.buttons.exit,accel="Ctrl-Q")
        
##         fileMenu  = frm.addMenu("&Edit")
##         fileMenu.addButton(frm.buttons.start)
##         fileMenu.addButton(frm.buttons.arrive,accel="Ctrl-A")
        
        frm.show()
        
if __name__ == "__main__":
    console.parse_args()
    Main().run()
