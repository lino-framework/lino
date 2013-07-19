## Copyright 2008-2013 Luc Saffre
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
Deserves documentation
"""


import logging
logger = logging.getLogger(__name__)

import sys
import decimal

#~ from django import forms

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


from lino import dd
from lino import mixins


#~ from lino import fields
#~ from lino.core.dbutils import resolve_model

partners = dd.resolve_app(settings.SITE.partners_app_label)
ledger = dd.resolve_app('ledger')
#~ from lino.modlib.ledger import models as ledger
#~ journals = dd.resolve_app('journals')
accounts = dd.resolve_app('accounts')

partner_model = settings.SITE.partners_app_label + '.Partner'


#~ Contact = dd.resolve_model('contacts.Contact')
#~ Person = resolve_model('contacts.Person')
#~ Company = resolve_model('contacts.Company')

def _functionId(nFramesUp):
    # thanks to:
    # http://nedbatchelder.com/blog/200410/file_and_line_in_python.html
    """ Create a string naming the function n frames up on the stack.
    """
    co = sys._getframe(nFramesUp+1).f_code
    return "%s (%s:%d)" % (co.co_name, co.co_filename, co.co_firstlineno)


def todo_notice(msg):
    print "[todo] in %s :\n       %s" % (_functionId(1),msg)
    
    
class VoucherStates(dd.Workflow):
    #~ label = _("State")
    pass
add = VoucherStates.add_item
add('10',_("Draft"),'draft',editable=True) 
add('20',_("Registered"),'registered',editable=False) 

    
  
class BankStatement(mixins.Registrable,ledger.Voucher):
    
    balance1 = dd.PriceField(_("Old balance"),blank=True,null=True)
    balance2 = dd.PriceField(_("New balance"),blank=True,null=True)
    
    state = VoucherStates.field(default=VoucherStates.draft)
    
    
    def unused_full_clean(self,*args,**kw):
    #~ def before_save(self):
        if not self.booked:
            if self.value_date is None:
                self.value_date = self.date
            #journals.AbstractDocument.before_save(self)
            #ledger.LedgerDocumentMixin.before_save(self)
            balance = self.balance1
            if self.id is not None:
                for i in self.items.all():
                    balance += i.debit - i.credit
            self.balance2 = balance
        super(BankStatement,self).full_clean(*args,**kw)
        
    #~ def after_save(self):
        #~ logger.info("Saved document %s (balances=%r,%r)",self,self.balance1,self.balance2)
        
        
    def get_wanted_movements(self):
        #~ a = self.journal.chart.get_account_by_ref(a)
        
        a = self.journal.account
        if not a: return 
        sum = decimal.Decimal(0)
        for i in self.items.all():
            if i.dc == a.type.dc:
                sum += i.amount
            else:
                sum -= i.amount
            b = self.create_movement(
              i.account,i.dc,i.amount,
              seqno=i.seqno,
              partner=i.partner)
              #~ person=i.person,
              #~ company=i.company,
              #~ date=i.date)
            #~ sum_debit += i.debit - i.credit
            yield b
        #todo_notice("BankStatement.balance1 and 2 are strings?!")
        #http://code.google.com/p/lino/issues/detail?id=1
        #logger.info("finan.BankStatement %r %r",self.balance1, sum_debit)
        if self.balance1 is not None:
            self.balance2 = self.balance1 + sum
        #jnl = self.get_journal()
        #~ acct = ledger.Account.objects.get(id=self.journal.account)
        #~ b = self.create_booking(account=acct)
        yield self.create_movement(a,a.type.dc,sum)
        
    def unused_add_item(self,account=None,**kw):
        #~ pos = self.items.count() + 1
        #~ if account is not None:
            #~ if not isinstance(account,ledger.Account):
                #~ account = ledger.Account.objects.get(match=account)
        kw['account'] = account
        kw['contact'] = contact
        #~ kw['person'] = person
        #~ kw['company'] = company
        for k in ('debit','credit'):
            v = kw.get(k,None)
            if isinstance(v,basestring):
                kw[k] = decimal.Decimal(v)
        #~ return self.items.create(**kw)
        kw['document'] = self
        return DocItem(**kw)
        #~ return self.items.create(**kw)
    
  
class DocItem(mixins.Sequenced,ledger.VoucherItem):
    voucher = models.ForeignKey(BankStatement,related_name='items')
    #~ pos = models.IntegerField("Position")
    date = models.DateField(blank=True,null=True)
    amount = dd.PriceField(default=0)
    dc = ledger.DebitOrCreditField()
    #~ credit = dd.PriceField(default=0)
    remark = models.CharField(max_length=200,blank=True)
    account = models.ForeignKey('accounts.Account')
    partner = models.ForeignKey(partner_model,blank=True,null=True)
    #~ person = models.ForeignKey(Person,blank=True,null=True)
    #~ company = models.ForeignKey(Company,blank=True,null=True)
    
    debit = ledger.DcAmountField(accounts.DEBIT,_("Income"))
    credit = ledger.DcAmountField(accounts.CREDIT,_("Expense"))
    
    def get_siblings(self):
        return self.voucher.items.all()
    
    #~ def full_clean(self,*args,**kw):
        #~ if self.pos is None:
            #~ self.pos = self.document.items.count() + 1
        #~ return super(DocItem,self).full_clean(*args,**kw)
        
    #~ def __unicode__(self):
        #~ return u"DocItem %s.%d" % (self.document,self.pos)
        
#~ class Booking(dd.Model):
    #~ #journal = models.ForeignKey(journals.Journal)
    #~ #number = models.IntegerField()
    #~ document = models.ForeignKey(LedgerDocument) 
    #~ pos = models.IntegerField("Position")
    #~ date = fields.MyDateField() 
    #~ account = models.ForeignKey(Account)
    #~ contact = models.ForeignKey(contacts.Contact,blank=True,null=True)
    #~ debit = fields.PriceField(default=0)
    #~ credit = fields.PriceField(default=0)
    

        

class BankStatements(dd.Table):
    parameters = dict(
        pyear=ledger.FiscalYears.field(blank=True),
        #~ ppartner=models.ForeignKey('contacts.Partner',blank=True,null=True),
        pjournal=ledger.JournalRef(blank=True))
    model = BankStatement
    order_by = ["date","id"]
    column_names = "date id number balance1 balance2 user *" 
    params_layout = "pjournal pyear"
    #~ detail_layout = InvoiceDetail()
    insert_layout = dd.FormLayout("""
    date 
    balance1 
    balance2
    """,window_size=(40,'auto'))
    
    detail_layout = """
    date narration balance1 balance2 
    journal year number user id workflow_buttons
    finan.ItemsByStatement
    """
    
    @classmethod
    def get_request_queryset(cls,ar):
        qs = super(BankStatements,cls).get_request_queryset(ar)
        if ar.param_values.pyear:
            qs = qs.filter(year=ar.param_values.pyear)
        if ar.param_values.pjournal:
            qs = qs.filter(journal=ar.param_values.pjournal)
        return qs
    
    
    
class BankStatementsByJournal(BankStatements,ledger.ByJournal):
    #~ order_by = ["number"]
    #~ master_key = 'journal' # see django issue 10808
    params_panel_hidden = True
                  
   
    
    
class DocItems(dd.Table):
    column_names = "date account partner remark debit credit seqno *" 
    model = DocItem
    order_by = ["seqno"]

class ItemsByStatement(DocItems):
    master_key = 'voucher'
    
#~ BankStatement.content = ItemsByDocument

#~ journals.register_doctype(BankStatement,BankStatements)

ledger.VoucherTypes.add_item(BankStatement,BankStatementsByJournal)

MODULE_LABEL = _("Financial")

def setup_main_menu(site,ui,profile,m): 
    m = m.add_menu('finan',MODULE_LABEL)
    
    for jnl in ledger.Journal.objects.filter(trade_type=''):
        m.add_action(jnl.voucher_type.table_class,
            label=unicode(jnl),
            params=dict(master_instance=jnl))

