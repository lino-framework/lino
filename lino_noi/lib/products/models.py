# -*- coding: UTF-8 -*-
# Copyright 2015-2016 Luc Saffre
#
# This file is part of Lino Noi.
#
# Lino Noi is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Noi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Noi.  If not, see
# <http://www.gnu.org/licenses/>.

"""Database models for `lino_noi.lib.products`.

"""

from lino.api import dd
from lino_xl.lib.products.models import *
from lino.mixins import Referrable


class Product(Product, Referrable):

    class Meta(Product.Meta):
        app_label = 'products'
        abstract = dd.is_abstract_model(__name__, 'Product')




class ProductDetail(dd.DetailLayout):
    main = """
    id ref cat
    name
    description
    tickets.InterestsByProduct  tickets.TicketsByProduct
    """


class Products(Products):
    detail_layout = ProductDetail()
    column_names = "ref name cat *"


# def site_setup(site):
#     site.modules.products.Products.set_detail_layout(ProductDetail())
