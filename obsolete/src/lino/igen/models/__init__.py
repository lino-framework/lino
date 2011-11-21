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

#~ from lino.django.utils import perms
#~ from . import countries, auth, ledger, sales, contacts, products, journals
#~ from lino.django.igen import models as igen
#~ from lino.django.utils import sysadm
#~ from lino.django.ledger import models as ledger

#~ def lino_setup(lino):
    #~ m = lino.add_menu("contacts","~Contacts")
    #~ m.add_action(contacts.Companies())
    #~ m.add_action(contacts.Persons())
    #~ m.add_action(sales.Contacts(),label="All")
    #~ m = lino.add_menu("prods","~Products")
    #~ m.add_action(products.Products())
    #~ m.add_action(products.ProductCats())
    #~ m = lino.add_menu("sales","~Sales",
      #~ can_view=perms.is_authenticated)
    #~ m.add_action(sales.Orders())
    #~ m.add_action(sales.Invoices())
    #~ m.add_action(sales.DocumentsToSign())
    #~ m.add_action(sales.PendingOrders())
    
    #~ m = lino.add_menu("ledger","~Ledger",
      #~ can_view=perms.is_authenticated)
    #~ m.add_action(ledger.FinancialDocuments())
    #~ m.add_action(ledger.Accounts())

#~ m = lino.add_menu("admin","~Administration",
      #~ can_view=perms.is_staff)
    #~ m.add_action(MakeInvoicesDialog())
    
    #~ m = lino.add_menu("config","~Configuration",
      #~ can_view=perms.is_staff)
    #~ m.add_action(sales.InvoicingModes())
    #~ m.add_action(sales.ShippingModes())
    #~ m.add_action(sales.PaymentTerms())
    #~ m.add_action(countries.Languages())
    #~ m.add_action(contacts.Countries())

    #~ m = lino.add_menu("system","~System")
    #~ m.add_action(auth.Permissions())
    #~ m.add_action(auth.Users())
    #~ m.add_action(auth.Groups())
    #~ m.can_view = perms.is_staff
