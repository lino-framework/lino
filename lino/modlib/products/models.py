## Copyright 2008-2010 Luc Saffre
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
from lino import fields
#journals = models.get_app('journals')
from lino import reports
#~ from lino import layouts
from lino.utils import perms


class ProductCat(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    def __unicode__(self):
        return self.name

class Product(models.Model):
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    cat = models.ForeignKey(ProductCat,verbose_name="Category")
    vatExempt = models.BooleanField(default=False)
    price = fields.PriceField(blank=True,null=True)
    #image = models.ImageField(blank=True,null=True,
    # upload_to=".")
    
    def __unicode__(self):
        return self.name

##
## report definitions
##        
        
class ProductCats(reports.Report):
    model = ProductCat
    order_by = "id"
    can_view = perms.is_staff

#~ class ProductDetail(layouts.DetailLayout):
  
    #~ datalink = 'products.Product'
    
    #~ main = """
    #~ g1:60
    #~ g2 g3:10
    #~ """
    
    #~ g1 = "name \n description"
    #~ g2 = "price \n cat"
    #~ g3 = "id \n vatExempt"

class Products(reports.Report):
    model = Product
    order_by = "id"
    column_names = "id:3 name description:30x1 cat vatExempt price:6"
