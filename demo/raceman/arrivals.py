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

import time

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

    def arrive(self,parent):
        if self.starttime is None:
            parent.error("cannot arrive before start")
            return
        line = (parent.entries.dossard.get(),
                str(time.time() - self.starttime))
        self.data.append( line)
        parent.info("%s arrived at %s" % line)
    
    def exit(self,parent):
        if len(self.data) > 0:
            if parent.confirm("write data to file?"):
                self.writedata(parent)
        parent.close()

    def start(self,parent):
        self.starttime = time.time()
        parent.info("started at %s" %str(self.starttime))

    def run(self):
        
        frm = Form(label="Raceman arrivals")
        frm.addLabel("""\
Raceman arrivals        
    """)
        frm.addEntry("dossard",STRING, label="Dossard", value="*")
        self.startButton = frm.addButton(label="&Start",
                                         onclick=self.start)
        self.arriveButton = frm.addButton(label="&Arrive",
                                          onclick=self.arrive)
        frm.addButton(label="&Write",onclick=self.writedata)
        frm.addButton(label="&Exit",onclick=self.exit)
        frm.show()
        
if __name__ == "__main__":
    console.parse_args()
    Main().run()
