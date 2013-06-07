# -*- coding: UTF-8 -*-
## Copyright 2009-2013 Luc Saffre
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
  
    vat_quarterly = False
    """
    Set this to True to support quarterly VAT declarations.
    """
    
    def get_vat_class(self,tt,item):
        return 'normal'
        
    def get_product_vat_class(self,tt,product):
        return 'normal'
        

    def get_product_base_account(self,tt,product):
        """
        Return the reference of the general account 
        to be used to book the product movement of 
        the specified trade type and product.
        
        The default implementation works with the accounts created by
        :mod:`lino.modlib.accounts.fixtures.mini`.
        """
        if tt.name == 'sales':
            #~ return '7000'
            return 'sales'
        elif tt.name == 'purchases':
        #~ elif item.voucher.journal.type == JournalTypes.purchases:
            return 'purchases'
            #~ return '6000'
        
    #~ def get_sales_item_account(self,item):
        #~ return self.modules.accounts.Account.objects.get(group__ref='704000')
        
    def get_partner_account(self,voucher):
        """
        Return the reference of the general account 
        where the partner movement of the given voucher should be booked.
        The default implementation works with the accounts created by
        :mod:`lino.modlib.accounts.fixtures.mini`.
        """
        tt = voucher.get_trade_type()
        if tt.name == 'sales':
            #~ return '4000'
            return 'customers'
        elif tt.name == 'purchases':
            #~ return '4400'
            return 'suppliers'
        
    def get_vat_account(self,tt,vc,vr):
        """
        Return the reference of the account where the VAT amount 
        for the specified trade operation should be booked.
        The operation is specified using its type `tt`, 
        its class `vc` and its regime `vr`
        `tt` is a :class:`TradeType` (usually either `sales` or `purchases`)
        `vc` is a :class:`VatClass`
        `vr` is a :class:`VatRegime`
        
        """
        if tt.name == 'sales':
            #~ return '4000'
            return 'vat_due'
        elif tt.name == 'purchases':
            #~ return '4400'
            return 'vat_deductible'
        
        #~ return '472100'

    def get_vat_rate(self,tt,vc,vr):
        VAT_RATES = dict(
          exempt=Decimal(),
          reduced=Decimal('0.07'),
          normal=Decimal('0.20')
        )
        return VAT_RATES[vc.name]

        
