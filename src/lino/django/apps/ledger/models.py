## Copyright 2008-2009 Luc Saffre.
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

from django.db import models
#from lino.django.plugins import fields, journals
#from lino.django.apps.igen.models import Contact
#from .. import Model
from . import contacts, fields, journals

__app_label__ = "ledger"

class FinancialDocument(journals.AbstractDocument):
    creation_date = fields.MyDateField()
    value_date = fields.MyDateField() 
    remark = models.CharField("Remark for internal use",
      max_length=200,blank=True)
    balance1 = fields.PriceField(blank=True,null=True)
    balance2 = fields.PriceField(blank=True,null=True)
    
    def save(self,*args,**kw):
        if self.value_date is None:
            self.value_date = self.creation_date
        return super(FinancialDocument,self).save(*args,**kw)
        
    def add_item(self,account=None,contact=None,**kw):
        pos = self.docitem_set.count() + 1
        if account is not None:
            if not isinstance(account,Account):
                account = Account.objects.get(pk=account)
        if contact is not None:
            if not isinstance(contact,contacts.Contact):
                contact = contacts.Contact.objects.get(pk=contact)
        kw['account'] = account
        kw['contact'] = contact        
        return self.docitem_set.create(**kw)
    
journals.register_doctype(FinancialDocument)
  
class Account(models.Model):
    name = models.CharField(max_length=200,blank=True)

class DocItem(models.Model):
    document = models.ForeignKey(FinancialDocument) 
    pos = models.IntegerField("Position")
    debit = fields.PriceField(blank=True,null=True)
    credit = fields.PriceField(blank=True,null=True)
    remark = models.CharField(max_length=200,blank=True)
    account = models.ForeignKey(Account)
    contact = models.ForeignKey(contacts.Contact,blank=True,null=True)
    
    def save(self,*args,**kw):
        if self.pos is None:
            self.pos = self.document.docitem_set.count() + 1
        return super(DocItem,self).save(*args,**kw)
        
    

##
## report definitions
##        
        
from django import forms

from lino.django.utils import reports
from lino.django.utils import layouts
from lino.django.utils import perms

class FinDocPageLayout(layouts.PageLayout):
    
    balance = """
    balance1
    balance2
    """
    
    box1 = """
    creation_date value_date
    remark
    """
    
    main = """
            box1 balance
            content
            """
    def inlines(self):
        return dict(content=ItemsByDocument())
            

class Accounts(reports.Report):
    model = Account
    
class FinancialDocuments(reports.Report):
    page_layouts = (FinDocPageLayout, )
    model = FinancialDocument
    order_by = "number"

class ItemsByDocument(reports.Report):
    columnNames = "pos:3 account contact remark debit credit" 
    model = DocItem
    master = FinancialDocument
    order_by = "pos"

def lino_setup(lino):
    m = lino.add_menu("ledger","~Ledger",
      can_view=perms.is_authenticated)
    m.add_action(FinancialDocuments())
    m.add_action(Accounts())
