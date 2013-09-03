## Copyright 2008-2012 Luc Saffre
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


from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import dd

vat = dd.resolve_app('vat')


class ProductCat(dd.BabelNamed):
    """
    """
    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")

    #~ name = dd.BabelCharField(max_length=200)
    description = models.TextField(blank=True)
    #~ def __unicode__(self):
        #~ return self.name

class ProductCats(dd.Table):
    model = ProductCat
    required = dd.required(user_level='manager')
    order_by = ["id"]
    detail_layout = """
    id name
    description
    ProductsByCategory
    """

class Product(dd.BabelNamed):
  
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
    
    description = dd.BabelTextField(
        verbose_name=_("Long description"),
        blank=True,null=True)
    cat = models.ForeignKey(ProductCat,
        verbose_name=_("Category"),
        blank=True,null=True)
        
    if vat:
        vat_class = vat.VatClasses.field(blank=True)
    else:
        vat_class = dd.DummyField()
    
    #~ vatExempt = models.BooleanField(verbose_name=_("VAT exempt"),default=False)
    #~ price = dd.PriceField(verbose_name=_("Price"),blank=True,null=True)
    #image = models.ImageField(blank=True,null=True,
    # upload_to=".")
    
    #~ def __unicode__(self):
        #~ return self.name


class Products(dd.Table):
    required = dd.required(auth=True)
    model = Product
    order_by = ["id"]
    column_names = "id:3 name cat vat_class sales_price:6 *"
    detail_layout = """
    id cat sales_price vat_class 
    name 
    description
    """
    
# note: a Site without sales will have to adapt the detail_layout and 
# column_names of Products 
    
class ProductsByCategory(Products):
    master_key = 'cat'
    
    
MODULE_LABEL = _("Products")

#~ def setup_master_menu(site,ui,profile,m): 
def setup_main_menu(site,ui,profile,m): 
    m  = m.add_menu("products",MODULE_LABEL)
    m.add_action(Products)
    m.add_action(ProductCats)

#~ def setup_my_menu(site,ui,profile,m): 
    #~ pass
  
def setup_config_menu(site,ui,profile,m): 
    pass
  
def setup_explorer_menu(site,ui,profile,m):
    pass
      
