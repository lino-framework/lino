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

import random

from lino.ui import console

from lino.forms.application import AdamoApplication

from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import * # Nations,  Quotes


class MyApplication(AdamoApplication):
    
    def makeMainForm(self):
        
        frm = self.addForm(label="Main menu")

        ds = self.sess.query(Quotes)
        q = random.choice(ds)
        fortune = q.abstract.strip()
        if q.author is not None:
            fortune += " ("+str(q.author)+")"
        frm.addLabel(label="Random Quote:",
                     doc=fortune+('\n'*10))
        
        m = frm.addMenu("&File")
        m.addItem(label="&Quit",action=frm.close)

        m = frm.addMenu("&Contacts")
        m.addItem(label="&Partners").setHandler(self.showTableGrid,
                                                Partners)
        m.addItem(label="&Cities").setHandler(self.showTableGrid,
                                              Cities)
        m.addItem(label="&Nations").setHandler(self.showTableGrid,
                                               Nations)
        m = frm.addMenu("&Sales")
        OUT = self.getSession().peek(Journals,'OUT')
        m.addItem(label="&Invoices").setHandler(self.showTableGrid,
                                                Invoices,
                                                jnl=OUT)
        m = frm.addMenu("&?")
        m.addItem(label="&About",action=self.showAbout)
        return frm


def main():
    schema = demo.makeSchema(big=True)
    app = MyApplication()
    app.startup(schema)
    app.main()
    
        

if __name__ == "__main__":
    console.parse_args()
    main()
