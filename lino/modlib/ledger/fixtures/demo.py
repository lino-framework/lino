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

from lino.utils.babel import babel_values
from lino import dd

def objects():

    sales = dd.resolve_app('sales')
    ledger = dd.resolve_app('ledger')
    
    if sales:
        #~ yield sales.Orders.create_journal("VKR",'sales',name=u"Aufträge")
        yield sales.Invoice.create_journal('sales',**babel_values('name',
          de=u"Verkaufsrechnungen",fr=u"Factures vente",en="Sales invoices",et=u"Müügiarved"))
    else:
        yield ledger.AccountInvoice.create_journal('sales',**babel_values('name',
          de=u"Verkaufsrechnungen",fr=u"Factures vente",en="Sales invoices",et=u"Müügiarved"))
          
    yield ledger.AccountInvoice.create_journal('purchases',**babel_values('name',
      de=u"Einkaufsrechnungen",fr=u"Factures achat",en="Purchase invoices",et=u"Ostuarved"))

