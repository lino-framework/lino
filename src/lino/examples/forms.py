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

from lino.adamo.datatypes import STRING
#from lino.adamo import center
from lino.forms.wx import Form

from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import Partners

center.setFormFactory(Form)

def clickme(parent):
    frm = parent.addForm(label="click!")
    frm.addLabel("""\
This is a child form. It is not modal,
so you don't need to close it if you want to continue with "%s".
""" % parent.getLabel())
    frm.addOkButton()
    frm.addAbortButton()
    frm.show()
    
def main():
    sess = demo.beginSession()
    ds = sess.query(Partners)
    
    frm = sess.addForm(label="my first form")
    box = frm.addBox(frm.VERTICAL)
    box.addLabel("""\
Please enter your personal data.
We won't store it. You can trust us.
""")
    box.addEntry("firstName",STRING,label="first name")
    box.addEntry("name",STRING)
    btnBox = box.addBox(frm.HORIZONTAL)
    btnBox.addOkButton()
    btnBox.addAbortButton()
    btnBox.addButton(name="click &Me").setHandler(clickme)
    btnBox.addButton(label=ds.getLabel()).setHandler(ds.showGridForm)
    if frm.showModal():
        print "Hello %s %s. Thank you for registering." % (
            frm.entries.firstName.getValue(),
            frm.entries.name.getValue())
    else:
        print """You pressed ESC, clicked "Abort" or closed the form."""
        
    sess.shutdown()
