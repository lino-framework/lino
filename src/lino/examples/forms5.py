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

from lino.ui import console

from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import *

def foo(frm,sess,tc):
    ds = sess.query(tc)
    frm = frm.addForm(label=ds.getLabel())
    frm.addTableEditor(ds)
    frm.show()

def main():
    sess = demo.startup(big=True)
    
    frm = sess.addForm(label="Main menu")
    frm.addLabel("""\
This is the main menu.                                           











""")

    m = frm.addMenu("&Stammdaten")
    m.addItem(label="&Partner").setHandler(foo,sess,Partners)
    m.addItem(label="&Nations").setHandler(foo,sess,Nations)
    m.addItem(label="&Cities").setHandler(foo,sess,Cities)
    m.addItem(label="&Quotes").setHandler(foo,sess,Quotes)
        
    m = frm.addMenu("&Programm")
    m.addItem(label="&Beenden",onclick=frm.close)
    
    frm.show()
        
    sess.shutdown()
        
if __name__ == "__main__":
    console.parse_args()
    main()
