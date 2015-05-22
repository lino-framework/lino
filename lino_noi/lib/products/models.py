# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino_noi.lib.products`.

"""

from lino.api import dd
from lino.mixins import Referrable
from lino.modlib.products.models import *


class Product(Product, Referrable):
    pass


class ProductDetail(dd.DetailLayout):
    main = """
    id ref cat #sales_price vat_class
    name
    description
    tickets.InterestsByProduct  tickets.TicketsByProduct
    """


class Products(Products):
    detail_layout = ProductDetail()
    insert_layout = """
    ref cat
    name
    """
    column_names = "ref name cat *"


# def site_setup(site):
#     site.modules.products.Products.set_detail_layout(ProductDetail())
