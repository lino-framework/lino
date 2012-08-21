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

"""
General Ledger. 

"""

import logging
logger = logging.getLogger(__name__)

from django.db import models
import datetime
from decimal import Decimal

from lino import dd
from lino import mixins
from lino.utils import babel
from lino.utils.choicelists import ChoiceList
#contacts = reports.get_app('contacts')
#~ from lino.modlib.journals import models as journals
#~ journals = reports.get_app('journals')
#from lino.modlib.contacts import models as contacts
#from lino.modlib.journals import models as journals
from django.utils.translation import ugettext_lazy as _
from lino.modlib.ledger.utils import FiscalYears
#~ from lino.modlib.accounts.utils import AccountTypes


DOCTYPES = []
DOCTYPE_CHOICES = []

def register_voucher_type(docclass,rptclass=None):
    #assert not docclass in DOCTYPE_CLASSES
    #~ i = 0
    #~ for cl in DOCTYPE_CLASSES:
        #~ if cl == docclass:
            #~ return i
        #~ i += 1
    type_id = len(DOCTYPE_CHOICES)
    DOCTYPE_CHOICES.append((type_id,docclass.__name__))
    DOCTYPES.append((docclass,rptclass))
    docclass.doctype = type_id
    return type_id

def get_doctype(cl):
    i = 0
    for c,r in DOCTYPES:
        if c is cl:
            return i
        i += 1
    return None






    
#~ def default_year():
    #~ return datetime.date.today().year
    
#~ def YearRef(**kw):
    #~ kw.setdefault('default',default_year)
    #~ return models.IntegerField(**kw)


    
    
#~ class Journal(dd.Model):
class Journal(mixins.Sequenced):
  
    id = models.CharField(max_length=4,primary_key=True)
    name = models.CharField(max_length=100)
    doctype = models.IntegerField() #choices=DOCTYPE_CHOICES)
    force_sequence = models.BooleanField(default=False)
    account = models.ForeignKey('accounts.Account',blank=True,null=True)
    #~ account = models.CharField(max_length=6,blank=True)
    #~ pos = models.IntegerField()
    #~ printed_name = models.CharField(max_length=100,blank=True)
    printed_name = babel.BabelCharField(max_length=100,blank=True)
    
    def get_doc_model(self):
        """The model of documents in this Journal."""
        #print self,DOCTYPE_CLASSES, self.doctype
        return DOCTYPES[self.doctype][0]

    def get_doc_report(self):
        return DOCTYPES[self.doctype][1]

    def get_document(self,year=None,number=None,**kw):
        cl = self.get_doc_model()
        kw.update(journal=self,year=year,number=number) 
        return cl.objects.get(**kw)
        
    def create_document(self,**kw):
        """Create an instance of this Journal's document model (:meth:`get_doc_model`)."""
        cl = self.get_doc_model()
        #~ kw.update(journal=self) # wouldn't work. See Django ticket #10808
        try:
            doc = cl(**kw)
        except TypeError,e:
            #~ print 20100804, cl
            raise
        doc.journal = self
        #~ doc.full_clean()
        #~ doc.save()
        return doc
        
    def get_next_number(self):
        self.save()
        cl = self.get_doc_model()
        d = cl.objects.filter(journal=self).aggregate(
            models.Max('number'))
        number = d['number__max']
        if number is None:
            return 1
        return number + 1
        
    def __unicode__(self):
        return self.id
        
    def save(self,*args,**kw):
        #~ self.before_save()
        r = super(Journal,self).save(*args,**kw)
        self.after_save()
        return r
        
    def after_save(self):
        pass
        
    def full_clean(self,*args,**kw):
        if not self.name:
            self.name = self.id
        #~ if not self.pos:
            #~ self.pos = self.__class__.objects.all().count() + 1
        super(Journal,self).full_clean(*args,**kw)
      
        
    def pre_delete_voucher(self,doc):
        #print "pre_delete_document", doc.number, self.get_next_number()
        if self.force_sequence:
            if doc.number + 1 != self.get_next_number():
                raise Exception(
                  "%s is not the last voucher in journal" % unicode(doc)
                  )



class Journals(dd.Table):
    model = Journal
    order_by = ["seqno"]
    column_names = "id name doctype force_sequence *"
    

                  
def JournalRef(**kw):
    #~ kw.update(blank=True,null=True) # Django Ticket #12708
    kw.update(related_name="%(app_label)s_%(class)s_set_by_journal")
    return models.ForeignKey(Journal,**kw)

def VoucherNumber(**kw):
    return models.IntegerField(**kw)
    


    
        

#~ class Voucher(mixins.Controllable):
class Voucher(mixins.UserAuthored):
    """
    A Voucher is a document that represents a monetary transaction.
    This model is subclassed by sales.Invoice, purchases.Invoice, finan.Statement etc...
    """
    #~ class Meta:
        #~ abstract = True
        
    #~ controller_is_optional = False
    
    journal = JournalRef()
    year = FiscalYears.field()
    number = VoucherNumber(blank=True)
    date = models.DateField()
    #~ ledger_remark = models.CharField("Remark for ledger",
      #~ max_length=200,blank=True)
    narration = models.CharField(_("Narration"),max_length=200,blank=True)
    
    @classmethod
    def create_journal(cls,id,**kw):
        doctype = get_doctype(cls)
        jnl = Journal(doctype=doctype,id=id,**kw)
        return jnl
        
    @classmethod
    def get_journals(cls):
        doctype = get_doctype(cls)
        return Journal.objects.filter(doctype=doctype).order_by('seqno')
            
        
    def __unicode__(self):
        return "%s-%s/%s" % (self.journal,self.year,self.number)
        
    def full_clean(self,*args,**kw):
        #~ logger.info('Voucher.full_clean')
        if self.number is None:
            self.number = self.journal.get_next_number()
        #~ logger.info('Voucher.full_clean : number is %r',self.number)
        super(Voucher,self).full_clean(*args,**kw)
        
    def save(self,*args,**kw):
        super(Voucher,self).save(*args,**kw)
        if self.number is not None:
            """
            delete any existing movements and re-create them
            """
            self.movement_set.all().delete() 
            for m in self.get_wanted_movements():
                m.full_clean()
                m.save()
        
    def delete(self):
        #jnl = self.get_journal()
        self.journal.pre_delete_document(self)
        return super(Voucher,self).delete()
        
    def get_child_model(self):
        ## overrides Typed
        return DOCTYPES[self.journal.doctype][0]
        
        
    def get_wanted_movements(self):
        return []
        
    #~ def create_movement_credit(self,account,amount,**kw):
        #~ kw.update(is_credit=True)
        #~ return self.create_movement(account,amount,**kw)
        
    #~ def create_movement_debit(self,account,amount,**kw):
        #~ kw.update(is_credit=False)
        #~ return self.create_movement(account,amount,**kw)
        
    def create_movement(self,account,amount,**kw):
        kw['voucher'] = self
        kw['account'] = account
        kw['amount'] = amount
        #~ kw['journal'] = self.journal
        #~ kw['year'] = self.year
        #~ kw['number'] = self.number
        #~ kw['document'] = self
        #kw['number'] = self.number
        #~ kw.setdefault('date',self.date)
        #~ if not kw.get('date',None):
            #~ kw['date'] = self.value_date
        b = Movement(**kw)
        #print b.date
        #b.save()
        return b
        
        
ZERO = Decimal()        
    
class Movement(mixins.Sequenced):
    voucher = models.ForeignKey(Voucher)
    #~ pos = models.IntegerField("Position",blank=True,null=True)
    account = models.ForeignKey('accounts.Account')
    partner = models.ForeignKey('contacts.Partner',blank=True,null=True)
    amount = dd.PriceField(default=0)
    #~ is_credit = models.BooleanField(_("Credit"),default=False)
    #~ debit = dd.PriceField(default=0)
    #~ credit = dd.PriceField(default=0)
    
    @dd.virtualfield(dd.PriceField(_("Debit")))
    def debit(self,ar):
        if self.account.type.dc: 
            return ZERO
        return self.amount
    
    @dd.virtualfield(dd.PriceField(_("Credit")))
    def credit(self,ar):
        if self.account.type.dc: 
            return self.amount
        return ZERO
            
    
    def get_siblings(self):
        return self.voucher.movement_set.order_by('seqno')
        #~ return self.__class__.objects.filter().order_by('seqno')
        
    def __unicode__(self):
        return u"%s.%d" % (unicode(self.voucher),self.pos)
        
    #~ def document(self,request):
        #~ return "%s-%s/%s" % (self.journal,self.year,self.number)
    #~ document.return_type = models.CharField(max_length=30)
    

class Movements(dd.Table): 
    model = Movement
    column_names = 'voucher account debit credit *'
    
class MovementsByVoucher(Movements):
    master_key = 'voucher'
    column_names = 'seqno account debit credit'
    
#~ class BookingsByBookable(Movements):
    #~ master = Bookable
    #~ column_names = 'pos date account partner'
    
    #~ @classmethod
    #~ def get_filter_kw(self,master_instance,**kw):
        #~ kw['journal'] = master_instance.journal
        #~ kw['year'] = master_instance.year
        #~ kw['number'] = master_instance.number
        #~ return kw

      
    
#~ class LedgerJournals(journals.Journals):
    #~ model = LedgerJournal
    #~ column_names = journals.Journals.column_names + " account"
    

