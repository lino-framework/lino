## Copyright 2003-2005 Luc Saffre

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

from lino.adamo import *

from business import PartnerDocuments
from addrbook import Partners
from products import Products

class Invoices(PartnerDocuments):
    
    def init(self):
        PartnerDocuments.init(self)
        self.addField('zziel',DATE)
        self.addField('amount',AMOUNT)
        self.addField('inverted',BOOL)
        #self.addPointer('partner',Partners).setDetail('invoices')
        self.getRowAttr('partner').setDetail('invoices')

    class Instance(PartnerDocuments.Instance):
        
        def close(self):
            #print "Invoices.close() : %s lines" % len(self.lines)
            self.lock()
            total = 0
            for line in self.lines:
                total += (line.unitPrice * line.qty)
            self.amount = total
            self.unlock()
        

class InvoiceLines(Table):
    def init(self):
        self.addField('line',ROWID)
        self.addField('unitPrice',AMOUNT)
        self.addField('qty',INT)
        self.addField('remark',STRING)
        
        self.addPointer('invoice',Invoices).setDetail('lines')
        self.addPointer('product',Products).setDetail('invoiceLines')
        
        self.setPrimaryKey("invoice line")

    class Instance(Table.Instance):
        def after_product(self):
            self.unitPrice = self.product.price

