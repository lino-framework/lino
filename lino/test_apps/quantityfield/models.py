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

ur"""
Quantity Fields
===============

See also :mod:`lino.utils.quantity`.

Create some data:

>>> Item(name="Screw",price='2.49',qty='5').save()
>>> Item(name="Leather",price='24.95',qty='2.39').save()
>>> Item(name="Work",price='59.99',qty='0:40').save()

Here is our data:

>>> print '\n'.join([unicode(i) for i in Item.objects.all()])
5 x Screw at 2.49 = 12.45 EUR
2.39 x Leather at 24.95 = 59.6305 EUR
0:40 x Work at 59.99 = 39:60 EUR

Default value for `qty` is 1, while `discount` is "pseudo-nullable".

>>> Item(name="Thing",price='59.99').save()
>>> print unicode(Item.objects.get(pk=4))
1 x Thing at 59.99 = 59.99 EUR

>>> Item(name="Another thing",price='59.99',discount='10%').save()
>>> print unicode(Item.objects.get(pk=5))
1 x Another thing at 59.99 (-10%) = 53.991 EUR


"""

from django.db import models
from lino import dd

class Item(dd.Model):
    name = models.CharField(max_length=50)
    qty = dd.QuantityField(default='1')
    discount = dd.QuantityField()
    price = dd.PriceField()
    
    def __unicode__(self):
        if self.discount is None:
            return u"%s x %s at %s = %s EUR" % (self.qty,self.name,self.price,self.total())
        else:
            return u"%s x %s at %s (-%s) = %s EUR" % (self.qty,self.name,self.price,self.discount,self.total())
        
    def total(self):
        if self.discount is None:
            return self.qty * self.price
        else:
            return self.qty * (1 - self.discount) * self.price


