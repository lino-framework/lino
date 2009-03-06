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

from models import Unit, Entry

#
# reports definition
#

from lino.django.tom import reports

class Units(reports.Report):
    queryset=Unit.objects.order_by("id")
    columnNames="id title name parent seq format"
    columnWidths="3 20 10 20 3 6"

class UnitsPerParent(reports.Report):
    columnNames="id title name seq format parent"
    columnWidths="3 30 10 3 6 30"
    
    def __init__(self,parent,**kw):
        self.parent=parent
        reports.Report.__init__(self,**kw)
        
    def get_queryset(self):
        return Unit.objects.filter(parent=self.parent).order_by("seq")
    queryset=property(get_queryset)
    

#
# menu setup
#
def setup_menu(menu):
    m = menu.addMenu("voc","Vocabulary")
    m.addAction(Units(),label="List of All Units",)
    m.addAction(UnitsPerParent(None),name="tree",label="Table of Contents")
