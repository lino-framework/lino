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
The :xfile:`models.py` module for the :mod:`lino.modlib.finan` app.
"""


import logging
logger = logging.getLogger(__name__)

import sys
import decimal

#~ from django import forms

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


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

#~ def _functionId(nFramesUp):
    #~ # thanks to:
    #~ # http://nedbatchelder.com/blog/200410/file_and_line_in_python.html
    #~ """ Create a string naming the function n frames up on the stack.
    #~ """
    #~ co = sys._getframe(nFramesUp+1).f_code
    #~ return "%s (%s:%d)" % (co.co_name, co.co_filename, co.co_firstlineno)
#~ 

#~ def todo_notice(msg):
    #~ print "[todo] in %s :\n       %s" % (_functionId(1),msg)
    
    
class VoucherStates(dd.Workflow):
    #~ label = _("State")
    pass
add = VoucherStates.add_item
add('10',_("Draft"),'draft',editable=True) 
add('20',_("Registered"),'registered',editable=False) 

    
  
class JournalEntry(ledger.Voucher):
    state = VoucherStates.field(default=VoucherStates.draft)
    
    class Meta: 
        verbose_name = _("Journal Entry")
        verbose_name_plural = _("Journal Entries")
        
    def register(self,ar):
        super(JournalEntry,self).register(ar)
        self.update_satisfied()
        
    def deregister(self,ar):
        super(JournalEntry,self).deregister(ar)
        self.update_satisfied()
        
    def update_satisfied(self):
        partners = set()
        #~ matches = dict()
        for i in self.items.all():
            if i.partner:
                partners.add(i.partner)
        for p in partners:
            ledger.update_partner_satisfied(p)
        
    def get_wanted_movements(self):
        amount, movements = self.get_finan_movements()
        if amount: raise Exception("Missing amount %s in movements" % amount)
        return movements
        
    def get_finan_movements(self):
        amount = decimal.Decimal(0)
        mvts = []
        for i in self.items.all():
            if i.dc == self.journal.dc:
                amount += i.amount
            else:
                amount -= i.amount
            if i.match:
                match = i.match
            elif i.partner:
                match = "%s#%s-%s" % (self.journal.ref,self.pk,i.seqno)
            else:
                match = ''
            b = self.create_movement(
              i.account,i.dc,i.amount,
              seqno=i.seqno,
              match=match,
              partner=i.partner)
            mvts.append(b)
            
        return amount, mvts
        
        
        
class PaymentOrder(JournalEntry):
    class Meta: 
        verbose_name = _("Payment Order")
        verbose_name_plural = _("Payment Orders")
        
    total = dd.PriceField(_("Total"),blank=True,null=True)
    
    def get_wanted_movements(self):
        a = self.journal.account
        if not a: raise Exception("No account in %s" % self.journal)
        amount, movements = self.get_finan_movements()
        self.total = amount
        for m in movements: 
            yield m
        yield self.create_movement(a,a.type.dc,amount)
        
class BankStatement(JournalEntry):
    
    class Meta: 
        verbose_name = _("Bank Statement")
        verbose_name_plural = _("Bank Statements")
        
    balance1 = dd.PriceField(_("Old balance"),blank=True,null=True)
    balance2 = dd.PriceField(_("New balance"),blank=True,null=True)
        
    def get_wanted_movements(self):
        a = self.journal.account
        if not a: raise Exception("No account in %s" % self.journal)
        amount, movements = self.get_finan_movements()
        if self.balance1 is not None:
            self.balance2 = self.balance1 + amount
        for m in movements: 
            yield m
        yield self.create_movement(a,a.type.dc,amount)
        
        
        
    
class DocItem(mixins.Sequenced,ledger.VoucherItem,ledger.Matchable):
    
    class Meta: 
        verbose_name = _("Item")
        verbose_name_plural = _("Items")
        
    voucher = dd.ForeignKey(BankStatement,related_name='items')
    #~ pos = models.IntegerField("Position")
    date = models.DateField(blank=True,null=True)
    amount = dd.PriceField(default=0)
    dc = ledger.DebitOrCreditField()
    #~ credit = dd.PriceField(default=0)
    remark = models.CharField(_("Remark"),max_length=200,blank=True)
    account = dd.ForeignKey('accounts.Account',blank=True)
    partner = dd.ForeignKey(partner_model,blank=True,null=True)
    #~ person = models.ForeignKey(Person,blank=True,null=True)
    #~ company = models.ForeignKey(Company,blank=True,null=True)
    
    debit = ledger.DcAmountField(accounts.DEBIT,_("Income"))
    credit = ledger.DcAmountField(accounts.CREDIT,_("Expense"))
    
    def get_default_match(self):
        return str(self.date)
    
    
    def get_siblings(self):
        return self.voucher.items.all()
    
    def match_changed(self,ar):
        if self.match:
            m = ledger.Match(self.voucher.journal.dc,self.partner,self.match)
            if m.balance > 0:
                self.dc = not self.voucher.journal.dc
                self.amount = m.balance
            else:
                self.dc = self.voucher.journal.dc
                self.amount = - m.balance
            #~ self.dc = not self.match.dc
            #~ self.account = self.match.account
            #~ self.partner = self.match.partner
    
    def full_clean(self,*args,**kw):
        if self.account_id is None:
            if self.match:
                if self.partner is not None:
                    match = ledger.Match(self.voucher.journal.dc,self.partner,self.match)
                    print match
                    if match.trade_type is not None:
                        self.account = match.trade_type.get_partner_account()
            if self.account_id is None:
                raise ValidationError("Could not guess account")
        return super(DocItem,self).full_clean(*args,**kw)
        
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
    
class BankStatementDetail(dd.FormLayout):
    main = "general ledger"
    general = dd.Panel("""
    date balance1 balance2 user workflow_buttons
    finan.ItemsByStatement
    """,label=_("General"))
    
    ledger = dd.Panel("""
    id journal year number narration
    ledger.MovementsByVoucher
    """,label=_("Ledger"))
        

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
    
    detail_layout = BankStatementDetail()
    
    @classmethod
    def get_request_queryset(cls,ar):
        qs = super(BankStatements,cls).get_request_queryset(ar)
        if not isinstance(qs,list):
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
    column_names = "date account partner match remark debit credit seqno *" 
    model = DocItem
    order_by = ["seqno"]
    

class ItemsByStatement(DocItems):
    master_key = 'voucher'
    auto_fit_column_widths = True
    hidden_columns = 'id amount dc seqno'
    
    

ledger.VoucherTypes.add_item(BankStatement,BankStatementsByJournal)

MODULE_LABEL = _("Financial")

def setup_main_menu(site,ui,profile,m): 
    m = m.add_menu('finan',MODULE_LABEL)
    
    for jnl in ledger.Journal.objects.filter(trade_type=''):
        m.add_action(jnl.voucher_type.table_class,
            label=unicode(jnl),
            params=dict(master_instance=jnl))

