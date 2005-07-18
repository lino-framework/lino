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


from lino.forms import gui
from lino.console.application import Application

class MyApplication(Application):
    
    def showMainForm(self,sess):
        frm = sess.form(label="The First Lino Form")
    
        frm.addLabel("""\
Please enter your personal data.
Don't worry about your privacy.
You can trust us.
    """)
        firstName = frm.addEntry("firstName",label="First name")
        name = frm.addEntry("name",label="Name")
        frm.addOkButton()
        frm.addCancelButton()

        if frm.showModal():

            sess.message(
                "Hello %s %s. Thank you for registering.",
                firstName.getValue(),
                name.getValue())
        else:

            sess.message("You cancelled the form.")

            
gui.install()
MyApplication().main()
