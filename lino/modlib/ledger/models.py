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


from django.db import models
from lino import fields


from django import forms

from lino import reports
from lino.utils import perms

#contacts = reports.get_app('contacts')
from lino.modlib.journals import models as journals
#~ journals = reports.get_app('journals')
#from lino.modlib.contacts import models as contacts
#from lino.modlib.journals import models as journals

#~ from lino.tools import resolve_model
#~ Person = resolve_model('contacts.Person')
#~ Company = resolve_model('contacts.Company')


class Account(models.Model):
    #~ id = models.CharField(max_length=8,primary_key=True)
    match = models.CharField(max_length=50,blank=True)
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        if self.match:
            return "%s (%s)" % (self.match,self.name)
        return self.name
        #~ if self.name:
            #~ return self.name
        #~ return self.id
        #return super(Account,self).__unicode__()


#~ class LedgerJournal(journals.Journal):
  
    #~ def __init__(self,docclass,id,account_id=None,**kw):
        #~ assert type(account_id) == type('')
        #~ self.account_id = account_id
        #~ journals.Journal.__init__(self,docclass,id,**kw)
        
    #~ account = models.ForeignKey(Account)
    
    
class Booked(models.Model):
    """
    A model that subclasses Booked must also 
    subclass :class:`lino.modlib.journals.models.Journaled`::
    
      value_date = models.DateField(auto_now=True)
      ledger_remark = models.CharField("Remark for ledger",
        max_length=200,blank=True)
      booked = models.BooleanField(default=False)
    
    """
    
    class Meta:
        abstract = True
        
    value_date = models.DateField(auto_now=True)
    ledger_remark = models.CharField("Remark for ledger",
      max_length=200,blank=True)
    booked = models.BooleanField(default=False)
    
    def unbook(self):
        for b in self.booking_set.all():
            b.delete()
        self.booked = False
            
    def book(self):
        self.full_clean()
        self.save()
        bookings = [b for b in self.collect_bookings()]
        for b in bookings:
            b.full_clean()
            b.save()
        self.booked = True
        #self.save()
        
    def collect_bookings(self):
        pass
        
    def create_booking(self,**kw):
        kw['journal'] = self.journal
        kw['number'] = self.number
        #~ kw['document'] = self
        #kw['number'] = self.number
        if not kw.get('date',None):
            kw['date'] = self.value_date
        b = Booking(**kw)
        #print b.date
        #b.save()
        return b
        
        

#~ ACCOUNTS = dict(
  #~ #providers='4400',
  #~ #customers='4000',
  #~ sales_base='7000',
  #~ sales_vat='4510',
#~ )

#~ def set_accounts(**kw):
    #~ for k,v in kw.items():
        #~ if not ACCOUNTS.has_key(k):
            #~ raise RuntimeError("invalid account name %s" % k)
        #~ ACCOUNTS[k] = v

#~ def get_account(name):
    #~ x = ACCOUNTS[name]
    #~ a = Account.objects.get(pk=x)
    #~ if a is None:
        #~ raise ConfigurationError("No account %s defined" % x)
    #~ return a
    
        
class Booking(models.Model):
    journal = journals.JournalRef()
    number = journals.DocumentRef()
    #~ document = models.ForeignKey(LedgerDocument)
    pos = models.IntegerField("Position",blank=True,null=True)
    date = models.DateField()
    account = models.ForeignKey(Account)
    contact = models.ForeignKey('contacts.Contact',blank=True,null=True)
    #~ person = models.ForeignKey(Person,blank=True,null=True)
    #~ company = models.ForeignKey(Company,blank=True,null=True)
    debit = fields.PriceField(default=0)
    credit = fields.PriceField(default=0)
    
    def __unicode__(self):
        return u"%s.%d" % (self.document,self.pos)
        
    def document(self,request):
        return "%s-%s" % (self.journal,self.number)
    document.return_type = models.CharField(max_length=30)
    

##
## report definitions
##        
        

class Accounts(reports.Report):
    model = Account
    #column_names = "id name:50"

    
#~ class LedgerJournals(journals.Journals):
    #~ model = LedgerJournal
    #~ column_names = journals.Journals.column_names + " account"
    

