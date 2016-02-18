# Copyright 2008-2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Database models for `lino.modlib.products`.

"""


from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd
from lino import mixins

vat = dd.resolve_app('vat')


class ProductCat(mixins.BabelNamed):

    class Meta:
        app_label = 'products'
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")
        abstract = dd.is_abstract_model(__name__, 'ProductCat')

    description = models.TextField(blank=True)


class ProductCats(dd.Table):
    model = 'products.ProductCat'
    required_roles = dd.required(dd.SiteStaff)
    order_by = ["id"]
    detail_layout = """
    id name
    description
    ProductsByCategory
    """


#class Product(mixins.BabelNamed, mixins.Referrable):
class Product(mixins.BabelNamed):

    class Meta:
        app_label = 'products'
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        abstract = dd.is_abstract_model(__name__, 'Product')

    description = dd.BabelTextField(
        verbose_name=_("Long description"),
        blank=True, null=True)
    cat = models.ForeignKey(
        ProductCat, verbose_name=_("Category"),
        blank=True, null=True)

    if vat:
        vat_class = vat.VatClasses.field(blank=True)
    else:
        vat_class = dd.DummyField()


class Products(dd.Table):
    model = 'products.Product'
    order_by = ["id"]
    column_names = "id name cat vat_class *"

    insert_layout = """
    cat
    name
    """

    detail_layout = """
    id cat #sales_price vat_class
    name
    description
    """

# note: a Site without sales will have to adapt the detail_layout and
# column_names of Products


class ProductsByCategory(Products):
    master_key = 'cat'


