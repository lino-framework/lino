# -*- coding: UTF-8 -*-
## Copyright 2009-2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino ; if not, see <http://www.gnu.org/licenses/>.

from decimal import Decimal
from django.conf import settings
from lino.utils import Cycler
from lino.utils.babel import babel_values
from lino import dd

sales = dd.resolve_app('sales')
ledger = dd.resolve_app('ledger')
contacts = dd.resolve_app('contacts')
products = dd.resolve_app('products')

REQUEST = None

def objects():

    
    yield sales.InvoicingMode(**babel_values('name',en='Default',de=u"Standard",fr=u"Standard"))
    
    if ledger: 
      
        vt = ledger.VoucherTypes.get_for_model(sales.Invoice)
        JOURNALS = Cycler(vt.get_journals())
        PARTNERS = Cycler(contacts.Partner.objects.all())
        USERS = Cycler(settings.LINO.user_model.objects.all())
        PRODUCTS = Cycler(products.Product.objects.all())
        ITEMCOUNT = Cycler(1,2,3)
        for i in range(20):
            jnl = JOURNALS.pop()
            invoice = sales.Invoice(journal=jnl,
              partner=PARTNERS.pop(),
              user=USERS.pop(),
              date=settings.LINO.demo_date(-30+i))
            yield invoice
            for j in range(ITEMCOUNT.pop()):
                item = sales.InvoiceItem(voucher=invoice,
                    #~ account=jnl.get_allowed_accounts()[0],
                    product=PRODUCTS.pop(),
                    )
                item.product_changed(REQUEST)
                item.before_ui_save(REQUEST)
                #~ if item.total_incl:
                    #~ print "20121208 ok", item
                #~ else:
                    #~ if item.product.price:
                        #~ raise Exception("20121208")
                yield item
            invoice.register(REQUEST)
            invoice.save()

    sales.Invoice