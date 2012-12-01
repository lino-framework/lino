# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
My personal attempt to create a "universal account chart".
To be used for simple demo setups in different countries.

"""

from lino.utils.babel import babel_values
from lino import dd
accounts = dd.resolve_app('accounts')


def objects():
    chart  = accounts.Chart(name="Minimal Accounts Chart")
    yield chart
    #~ account = Instantiator(accounts.Account,"ref name").build
    def O(ref,type,fr,de,en):
        return accounts.Group(
          chart=chart,
          ref=ref,
          account_type=accounts.AccountTypes.get_by_name(type),
          **babel_values('name',de=de,fr=fr,en=en))
    yield O('10','capital',u"Capital",u"Kapital","Capital")
    yield O('40','asset',
        u"Créances commerciales",
        u"Forderungen aus Lieferungen und Leistungen",
        "Commercial receivable(?)")
    yield O('4000','asset',u"Clients",u"Kunden","Customers")
    yield O('4400','liability',u"Fournisseurs",u"Lieferanten","Suppliers")
    # todo: hackerzacker, gibt es da denn keine allgemein verständliche Formulierung?!
    yield O('451','asset',u"TVA à payer",u"Geschuldete MWSt","VAT to pay")
    yield O('4510','income',u"TVA due",u"MWSt zu regularisieren","VAT due")
    yield O('4512','asset',u"TVA déductible",u"Geschuldete MWSt","VAT receivable")
    yield O('6000','expense',u"Charges",u"Aufwendungen","Expenses")
    yield O('7','income',u"Produits",u"Erträge","Revenues")
    yield O('7000','income',u"Ventes",u"Verkäufe","Sales")
