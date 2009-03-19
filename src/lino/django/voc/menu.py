## Copyright 2009 Luc Saffre.
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

from models import Units, UnitsPerParent, Entries


#
# menu setup
#
def setup_menu(menu):
    m = menu.addMenu("voc","Vocabulary")
    m.addAction(Units().as_form(),label="List of All Units",)
    m.addAction(UnitsPerParent(None).as_form(),name="tree",label="Table of Contents")
    m.addAction(Entries().as_form(),label="List of Entries",)

#~ def setup_menu(menu):
    #~ m = menu.addMenu("Vocabulary")
    #~ m.addAction("/edit/Units")
    #~ m.addAction("/edit/UnitsPerParent")
    #~ m.addAction("/edit/Entries")
