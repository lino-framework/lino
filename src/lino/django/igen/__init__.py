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


"""
lino.django.igen


"igen" stands for "invoice generator" and is a simple, 
web-based program to write invoices either manually or 
periodically based on contracts.

It should become the first Lino Django application. 

There is even an early 
`demo site <http://igen.saffre-rumma.ee>`_ 


"""


#
# menu setup
#
def lino_setup(lino):
    import models as reports
    m = lino.addMenu("contacts","~Contacts")
    m.addAction(reports.Contacts())
    m.addAction(reports.Companies())
    m.addAction(reports.Persons())
    m = lino.addMenu("prods","~Products")
    m.addAction(reports.Products())
    m.addAction(reports.ProductCats())
    m = lino.addMenu("docs","~Documents")
    m.addAction(reports.Orders())
    m.addAction(reports.Invoices())
    m = lino.addMenu("config","~Configuration")
    m.addAction(reports.ShippingModes())
    m.addAction(reports.PaymentTerms())
    m.addAction(reports.Languages())
    m.addAction(reports.Countries())


