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

from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import Partners

gui.parse_args()
#sess = demo.startup(ui=gui)
sess = demo.startup()
ds = sess.query(Partners, orderBy="name")

frm = gui.form(label="The first DataGrid Form")
frm.addDataGrid(ds)
frm.show()

