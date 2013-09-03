# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
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

from decimal import Decimal

class SiteMixin(object):
    """
    Mixin to add to your Site class if you use :mod:`lino.modlib.vat`.
    """

    vat_quarterly = False
    """
    Set this to True to support quarterly VAT declarations.
    Used by :mod:`lino.modlib.declarations`
    """
    
    #~ def get_item_vat(self,voucher):
        #~ """
        #~ Expected to return the default value for the `item_vat` field.
        #~ Called on every new voucher whose model is subclass of 
        #~ `lino.modlib.vat.models.VatDocument`.
        #~ """
        #~ return True
        

    def get_vat_class(self,tt,item):
        return 'normal'
        
    #~ def get_product_vat_class(self,tt,product):
        #~ return 'normal'
        

    VAT_CLASS_TO_RATE = dict(
      exempt=Decimal(),
      reduced=Decimal('0.07'),
      normal=Decimal('0.20')
    )
    
    def get_vat_rate(self,tt,vc,vr):
        return self.VAT_CLASS_TO_RATE[vc.name]

        
