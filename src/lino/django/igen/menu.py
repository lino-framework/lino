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

from models import Contact, Country

#
# reports definition
#        
        
from lino.django.tom import reports

class Contacts(reports.Report):
    queryset=Contact.objects.order_by("id")
    columnNames="id companyName firstName lastName title country"
    can_delete=True

class Companies(reports.Report):
    #queryset=Contact.objects.order_by("companyName")
    columnNames="companyName country title firstName lastName"
    queryset=Contact.objects.exclude(companyName__exact=None)\
      .order_by("companyName")

class Persons(reports.Report):
    queryset=Contact.objects.filter(companyName__exact=None)\
      .order_by("lastName","firstName")
    columnNames="title firstName lastName country"

class Countries(reports.Report):
    queryset=Country.objects.order_by("isocode")
    columnNames="isocode name"
    columnWidths="3 30"


#
# menu setup
#
def setup_menu(menu):
    m = menu.addMenu("contacts","Contacts")
    m.addAction(Contacts())
    m.addAction(Companies())
    m.addAction(Persons())
    m.addAction(Countries())
