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

from models import *



#
# menu setup
#
def setup_menu(menu):
    m = menu.addMenu("contacts","~Contacts")
    m.addAction(Contacts().as_form())
    m.addAction(Companies().as_form())
    m.addAction(Persons().as_form())
    m = menu.addMenu("prods","~Products")
    m.addAction(Products().as_form())
    m.addAction(ProductCats().as_form())
    m = menu.addMenu("docs","~Documents")
    m.addAction(Orders().as_form())
    m.addAction(Invoices().as_form())
    m = menu.addMenu("config","~Configuration")
    m.addAction(ShippingModes().as_form())
    m.addAction(PaymentTerms().as_form())
    m.addAction(Languages().as_form())
    m.addAction(Countries().as_form())


#~ def setup_menu(menu):
    #~ m = menu.addMenu("~Contacts")
    #~ m.addAction("/edit/Contacts")
    #~ m.addAction("/edit/Companies")
    #~ m.addAction("/edit/Persons")
    #~ m = menu.addMenu("~Products")
    #~ m.addAction("/edit/Products")
    #~ m.addAction("/edit/ProductCats")
    #~ m = menu.addMenu("~Documents")
    #~ m.addAction("/edit/Orders")
    #~ m.addAction("/edit/Invoices")
    #~ m = menu.addMenu("~Configuration")
    #~ m.addAction("/edit/ShippingModes")
    #~ m.addAction("/edit/PaymentTerms")
    #~ m.addAction("/edit/Languages")
    #~ m.addAction("/edit/Countries")
