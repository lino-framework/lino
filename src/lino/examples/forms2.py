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
from lino.forms.wx.wxform import Form
from lino.ui import console

def privacy(parent):
    frm = parent.addForm(label="Privacy Statement",modal=False)
    frm.addLabel("""\

(imagine our privacy statement here)

Note that this form is a child of "%s".
It is not modal,
so you don't need to close it if you want to continue registering.
""" % parent.getLabel())
    btnPanel = frm.addPanel(frm.HORIZONTAL)
    btnPanel.addOkButton()
    btnPanel.addCancelButton()
    frm.show()
    
def main():
    frm = Form(label="my second form",
               modal=True)
    p = frm.addPanel(frm.VERTICAL)
    frm.addLabel("""\
Please enter your personal data.
Don't worry about your privacy.
You can trust us.
""")
    frm.addEntry("firstName",STRING,label="first name")
    frm.addEntry("name",STRING)
    
    btnPanel = frm.addPanel(frm.HORIZONTAL)
    btnPanel.addOkButton()
    btnPanel.addCancelButton()
    btnPanel.addButton(label="&Privacy statement").setHandler(privacy)
    if frm.show():
        print "Hello %s %s. Thank you for registering." % (
            frm.entries.firstName.value,
            frm.entries.name.value)
    else:
        print "You canceled the form."
        
if __name__ == "__main__":
    console.parse_args()
    main()
