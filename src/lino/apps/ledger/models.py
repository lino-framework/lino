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
from lino.apps import fields
from lino.apps.contacts import models as contacts
from lino.apps.journals import models as journals


class Account(models.Model):
    id = models.CharField(max_length=8,primary_key=True)
    name = models.CharField(max_length=200,blank=True)
    
    def __unicode__(self):
        if len(self.name):
            return self.name
        return self.id
        #return super(Account,self).__unicode__()


#~ class LedgerJournal(journals.Journal):
  
    #~ def __init__(self,docclass,id,account_id=None,**kw):
        #~ assert type(account_id) == type('')
        #~ self.account_id = account_id
        #~ journals.Journal.__init__(self,docclass,id,**kw)
        
    #~ account = models.ForeignKey(Account)
    
    
class LedgerDocument(journals.AbstractDocument):
  
    #journal_class = LedgerJournal
    #journal = models.ForeignKey(journals.Journal)
    #journal = journals.JournalRef()
    """
    django.core.exceptions.FieldError: Local field 'journal' in class 'LedgerDocument' clashes with field of similar name from base class 'AbstractDocument'
    """
    
    value_date = fields.MyDateField(auto_now=True) 
    ledger_remark = models.CharField("Remark for ledger",
      max_length=200,blank=True)
    booked = models.BooleanField(default=False)
    
    def unbook(self):
        for b in self.booking_set.all():
            b.delete()
        self.booked = False
            
    def book(self):
        bookings = [b for b in self.collect_bookings()]
        for b in bookings:
            b.save()
        self.booked = True
        #self.save()
        
    def collect_bookings(self):
        pass
        
    def create_booking(self,**kw):
      #kw['journal'] = self.idjnl
      kw['document'] = self
      #kw['number'] = self.number
      if not kw.get('date',None):
          kw['date'] = self.value_date
      b = Booking(**kw)
      #print b.date
      #b.save()
      return b
        
        

ACCOUNTS = dict(
  #providers='4400',
  #customers='4000',
  sales_base='7000',
  sales_vat='4510',
)

def set_accounts(**kw):
    for k,v in kw.items():
        if not ACCOUNTS.has_key(k):
            raise RuntimeError("invalid account name %s" % k)
        ACCOUNTS[k] = v

def get_account(name):
    x = ACCOUNTS[name]
    a = Account.objects.get(pk=x)
    if a is None:
        raise ConfigurationError("No account %s defined" % x)
    return a
    
#~ def customers_account():
    #~ a = Account.objects.get(pk="4000")
    #~ if a is None:
        #~ raise ConfigurationError("No account 4000 defined")
    #~ return a

#~ def sales_base():
    #~ a = Account.objects.get(pk="7000")
    #~ if a is None:
        #~ raise ConfigurationError("No account 7000 defined")
    #~ return a

#~ def vat_base():
    #~ a = Account.objects.get(pk="4510")
    #~ if a is None:
        #~ raise ConfigurationError("No account 7000 defined")
    #~ return a
    
        
class Booking(models.Model):
    #journal = journals.JournalRef()
    #number = models.IntegerField()
    document = models.ForeignKey(LedgerDocument)
    pos = models.IntegerField("Position",blank=True,null=True)
    date = fields.MyDateField()
    account = models.ForeignKey(Account)
    partner = models.ForeignKey(contacts.Partner,blank=True,null=True)
    debit = fields.PriceField(default=0)
    credit = fields.PriceField(default=0)
    
    def __unicode__(self):
        return u"%s.%d" % (self.document,self.pos)
    

##
## report definitions
##        
        
from django import forms

from lino.utils import reports
from lino.utils import layouts
from lino.utils import perms


class Accounts(reports.Report):
    model = Account
    #columnNames = "id name:50"

    
#~ class LedgerJournals(journals.Journals):
    #~ model = LedgerJournal
    #~ columnNames = journals.Journals.columnNames + " account"
    

