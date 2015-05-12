# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino_noi.lib.products`.

"""

from lino.api import dd
from lino.modlib.products.models import *


class ProductDetail(dd.DetailLayout):
    main = """
    id cat #sales_price vat_class
    name
    description
    tickets.TicketsByProduct
    """


def site_setup(site):
    site.modules.products.Products.set_detail_layout(ProductDetail())
