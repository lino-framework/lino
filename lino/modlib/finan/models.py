## Copyright 2008-2011 Luc Saffre
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


import logging
logger = logging.getLogger(__name__)

import sys
import decimal
#import logging ; logger = logging.getLogger('lino.apps.finan')

from django import forms

from lino import reports
#~ from lino import layouts
from lino.utils import perms

from django.db import models
from lino import fields
from lino.tools import resolve_model

contacts = reports.get_app('contacts')
#~ ledger = reports.get_app('ledger')
from lino.modlib.ledger import models as ledger
journals = reports.get_app('journals')

Person = resolve_model('contacts.Person')
Company = resolve_model('contacts.Company')

def _functionId(nFramesUp):
    # thanks to:
    # http://nedbatchelder.com/blog/200410/file_and_line_in_python.html
    """ Create a string naming the function n frames up on the stack.
    """
    co = sys._getframe(nFramesUp+1).f_code
    return "%s (%s:%d)" % (co.co_name, co.co_filename, co.co_firstlineno)


def todo_notice(msg):
    print "[todo] in %s :\n       %s" % (_functionId(1),msg)
  
class BankStatement(ledger.Booked,models.Model):
    
    #~ # implements Journaled:
    #~ journal = journals.JournalRef()
    #~ number = journals.DocumentRef()
    
    #~ # implements Booked:
    #~ value_date = models.DateField(auto_now=True)
    #~ ledger_remark = models.CharField("Remark for ledger",
      #~ max_length=200,blank=True)
    #~ booked = models.BooleanField(default=False)
    
    date = fields.MyDateField()
    balance1 = fields.PriceField()
    balance2 = fields.PriceField()
    
    def full_clean(self,*args,**kw):
    #~ def before_save(self):
        if not self.booked:
            if self.value_date is None:
                self.value_date = self.date
            #journals.AbstractDocument.before_save(self)
            #ledger.LedgerDocumentMixin.before_save(self)
            balance = self.balance1
            if self.id is not None:
                for i in self.docitem_set.all():
                    balance += i.debit - i.credit
            self.balance2 = balance
        super(BankStatement,self).full_clean(*args,**kw)
        
    #~ def after_save(self):
        #~ logger.info("Saved document %s (balances=%r,%r)",self,self.balance1,self.balance2)
        
    def collect_bookings(self):
        sum_debit = 0 # decimal.Decimal(0)
        for i in self.docitem_set.all():
            b = self.create_booking(
              pos=i.pos,
              account=i.account,
              person=i.person,
              company=i.company,
              date=i.date,
              debit=i.debit,
              credit=i.credit)
            sum_debit += i.debit - i.credit
            yield b
        #todo_notice("BankStatement.balance1 and 2 are strings?!")
        #http://code.google.com/p/lino/issues/detail?id=1
        #logger.info("finan.BankStatement %r %r",self.balance1, sum_debit)
        self.balance2 = self.balance1 + sum_debit
        #jnl = self.get_journal()
        #~ acct = ledger.Account.objects.get(id=self.journal.account)
        #~ b = self.create_booking(account=acct)
        b = self.create_booking(account=self.journal.account)
        if sum_debit > 0:
            b.debit = sum_debit
        else:
            b.credit = - sum_debit
        yield b
        
    def add_item(self,account=None,company=None,person=None,**kw):
        pos = self.docitem_set.count() + 1
        if account is not None:
            if not isinstance(account,ledger.Account):
                account = ledger.Account.objects.get(match=account)
        if person is not None:
            if not isinstance(person,Person):
                person = Person.objects.get(pk=person)
        if company is not None:
            if not isinstance(company,Company):
                company = Company.objects.get(pk=company)
        kw['account'] = account
        kw['person'] = person
        kw['company'] = company
        for k in ('debit','credit'):
            v = kw.get(k,None)
            if isinstance(v,basestring):
                kw[k] = decimal.Decimal(v)
        #~ return self.docitem_set.create(**kw)
        kw['document'] = self
        return DocItem(**kw)
        #~ return self.docitem_set.create(**kw)
    
  
class DocItem(models.Model):
    document = models.ForeignKey(BankStatement) 
    pos = models.IntegerField("Position")
    date = fields.MyDateField(blank=True,null=True)
    debit = fields.PriceField(default=0)
    credit = fields.PriceField(default=0)
    remark = models.CharField(max_length=200,blank=True)
    account = models.ForeignKey(ledger.Account)
    person = models.ForeignKey(Person,blank=True,null=True)
    company = models.ForeignKey(Company,blank=True,null=True)
    
    def full_clean(self,*args,**kw):
        if self.pos is None:
            self.pos = self.document.docitem_set.count() + 1
        return super(DocItem,self).full_clean(*args,**kw)
        
    def __unicode__(self):
        return u"DocItem %s.%d" % (self.document,self.pos)
        
#~ class Booking(models.Model):
    #~ #journal = models.ForeignKey(journals.Journal)
    #~ #number = models.IntegerField()
    #~ document = models.ForeignKey(LedgerDocument) 
    #~ pos = models.IntegerField("Position")
    #~ date = fields.MyDateField() 
    #~ account = models.ForeignKey(Account)
    #~ contact = models.ForeignKey(contacts.Contact,blank=True,null=True)
    #~ debit = fields.PriceField(default=0)
    #~ credit = fields.PriceField(default=0)
    

##
## report definitions
##        
        

#~ class FinDocDetail(layouts.DetailLayout):
    #~ datalink = 'finan.BankStatement'
    #~ box1 = """
    #~ date value_date
    #~ ledger_remark
    #~ """
    
    #~ balance = """
    #~ balance1
    #~ balance2
    #~ """
    
    #~ main = """
            #~ box1 balance
            #~ finan.ItemsByDocument
            #~ """
    
class BankStatements(journals.DocumentsByJournal):
    model = BankStatement
    column_names = "number date balance1 balance2 ledger_remark value_date"
    
    
    
class DocItems(reports.Report):
    column_names = "document pos:3 "\
                  "date account company person remark debit credit" 
    model = DocItem
    order_by = ["pos"]

class ItemsByDocument(DocItems):
    column_names = "pos:3 date account company person remark debit credit" 
    #master = BankStatement
    fk_name = 'document'
    
BankStatement.content = ItemsByDocument

journals.register_doctype(BankStatement,BankStatements)
