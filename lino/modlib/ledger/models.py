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
General Ledger. 

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import datetime
from decimal import Decimal

from django.db import models
from django.conf import settings

from lino import dd
from lino import mixins
from django.utils.translation import ugettext_lazy as _
from lino.modlib.ledger.utils import FiscalYears
from lino.mixins.printable import model_group
from lino.utils.xmlgen.html import E
from lino.utils import iif
from lino.utils import join_elems

accounts = dd.resolve_app('accounts',strict=True)
vat = dd.resolve_app('vat',strict=True)
partner_model = settings.SITE.partners_app_label + '.Partner'

ZERO = Decimal()


vat.TradeTypes.purchases.update(
    #~ price_field_name='sales_price',
    #~ price_field_label=_("Sales price"),
    base_account_field_name='purchases_account',
    base_account_field_label=_("Purchases Base account"),
    vat_account_field_name='purchases_vat_account',
    vat_account_field_label=_("Purchases VAT account"),
    partner_account_field_name='suppliers_account',
    partner_account_field_label=_("Suppliers account"))

#~ TradeTypes.purchases.update(
    #~ partner_account_field_name='suppliers_account',
    #~ partner_account_field_label=_("Suppliers account"))




class VoucherType(dd.Choice):
    def __init__(self,model,table_class):
        self.table_class = table_class
        model = dd.resolve_model(model)
        self.model = model
        value = dd.full_model_name(model)
        text = model._meta.verbose_name + ' (%s.%s)' % (
            model.__module__,model.__name__)
        name = None
        super(VoucherType,self).__init__(value,text,name)
        
    def get_journals(self):
        return Journal.objects.filter(voucher_type=self)
        
class VoucherTypes(dd.ChoiceList):
    item_class = VoucherType
    #~ blank = False
    max_length = 100
    
    @classmethod
    def get_for_model(self,model):
        for o in self.objects():
            #~ o.model = dd.resolve_model(o.model) # TODO: resolve only once
            if o.model is model:
                return o
          
    @classmethod
    def add_item(cls,model,table_class):
        return cls.add_item_instance(VoucherType(model,table_class))
    



class DebitOrCreditField(models.BooleanField):
    pass
    
class MatchField(models.CharField):
    def __init__(self,verbose_name=None,**kw):
        if verbose_name is None:
            verbose_name = _("Match")
        kw.setdefault('max_length',20)
        models.CharField.__init__(self,verbose_name,**kw)
    
class DcAmountField(dd.VirtualField):
    """
    An editable virtual field to set both fields `amount` and `dc`
    """
    
    editable = True
    
    def __init__(self,dc,*args,**kw):
        self.dc = dc
        dd.VirtualField.__init__(self,dd.PriceField(*args,**kw),None)
        
    def set_value_in_object(self,request,obj,value):
        obj.amount = value
        obj.dc = self.dc
        
    def value_from_object(self,obj,ar):
        if obj.dc == self.dc: return obj.amount
        return None







class Journal(dd.BabelNamed,mixins.Sequenced,mixins.PrintableType):
  
    class Meta:
        verbose_name = _("Journal")
        verbose_name_plural = _("Journals")
        
    #~ id = models.CharField(max_length=4,primary_key=True)
    ref = dd.NullCharField(max_length=20,unique=True)
    #~ name = models.CharField(max_length=100)
    trade_type = vat.TradeTypes.field(blank=True)
    #~ doctype = models.IntegerField() #choices=DOCTYPE_CHOICES)
    voucher_type = VoucherTypes.field() 
    force_sequence = models.BooleanField(default=False)
    #~ total_based = models.BooleanField(_("Voucher entry based on total amount"),default=False)
    chart = dd.ForeignKey('accounts.Chart')
    #~ chart = dd.ForeignKey('accounts.Chart',blank=True,null=True)
    account = dd.ForeignKey('accounts.Account',blank=True,null=True)
    #~ account = models.CharField(max_length=6,blank=True)
    #~ pos = models.IntegerField()
    #~ printed_name = models.CharField(max_length=100,blank=True)
    printed_name = dd.BabelCharField(max_length=100,blank=True)
    dc = DebitOrCreditField(default=None)
    
    @dd.chooser()
    def account_choices(self,chart):
        #~ fkw = dict()
        fkw = dict(type=accounts.AccountTypes.bank_accounts)
        return accounts.Account.objects.filter(chart=chart,**fkw)

    def get_doc_model(self):
        """The model of vouchers in this Journal."""
        #print self,DOCTYPE_CLASSES, self.doctype
        return self.voucher_type.model
        #~ return DOCTYPES[self.doctype][0]

    def get_doc_report(self):
        return self.voucher_type.table_class
        #~ return DOCTYPES[self.doctype][1]

    def get_voucher(self,year=None,number=None,**kw):
        cl = self.get_doc_model()
        kw.update(journal=self,year=year,number=number) 
        return cl.objects.get(**kw)
        
    def create_voucher(self,**kw):
        """
        Create an instance of this Journal's voucher model (:meth:`get_doc_model`).
        """
        cl = self.get_doc_model()
        kw.update(journal=self) 
        try:
            doc = cl() 
            #~ doc = cl(**kw) # wouldn't work. See Django ticket #10808
            #~ doc.journal = self
            for k,v in kw.items():
                setattr(doc,k,v)
            #~ print 20120825, kw
        except TypeError,e:
            #~ print 20100804, cl
            raise
        #~ doc.full_clean()
        #~ doc.save()
        return doc
        
    def get_allowed_accounts(self,**kw):
        if self.trade_type:
            kw[self.trade_type.name+'_allowed'] = True
        kw.update(chart=self.chart)
        return accounts.Account.objects.filter(**kw)
        
        
    def get_next_number(self,voucher):
        self.save()
        cl = self.get_doc_model()
        d = cl.objects.filter(journal=self,year=voucher.year).aggregate(
            models.Max('number'))
        number = d['number__max']
        #~ logger.info("20121206 get_next_number %r",number)
        if number is None:
            return 1
        return number + 1
        
    def __unicode__(self):
        s = super(Journal,self).__unicode__()
        if self.ref:
            s += " (%s)" % self.ref
            #~ return '%s (%s)' % (d.BabelNamed.__unicode__(self),self.ref or self.id)
        return s
            #~ return self.ref +'%s (%s)' % dd.BabelNamed.__unicode__(self)
            #~ return self.id +' (%s)' % dd.BabelNamed.__unicode__(self)
        
    def save(self,*args,**kw):
        #~ self.before_save()
        r = super(Journal,self).save(*args,**kw)
        self.after_save()
        return r
        
    def after_save(self):
        pass
        
    def full_clean(self,*args,**kw):
        if self.dc is None:
            if self.trade_type:
                self.dc = self.trade_type.dc
            elif self.account:
                self.dc = self.account.type.dc
                
        if not self.name:
            self.name = self.id
        #~ if not self.pos:
            #~ self.pos = self.__class__.objects.all().count() + 1
        super(Journal,self).full_clean(*args,**kw)
      
        
    #~ def pre_delete_voucher(self,doc):
    def disable_voucher_delete(self,doc):
        #print "pre_delete_voucher", doc.number, self.get_next_number()
        if self.force_sequence:
            if doc.number + 1 != self.get_next_number(doc):
                return _("%s is not the last voucher in journal" % unicode(doc))

    def get_templates_group(self):
        return model_group(self.voucher_type.model)


class Journals(dd.Table):
    model = Journal
    order_by = ["seqno"]
    column_names = "ref:5 trade_type voucher_type force_sequence name * seqno id"
    detail_layout = """
    ref trade_type voucher_type 
    force_sequence account seqno id
    name
    build_method  printed_name
    """
    insert_layout = dd.FormLayout("""
    ref name
    trade_type 
    voucher_type 
    """,window_size=(60,'auto'))
    

                  
def JournalRef(**kw):
    #~ kw.update(blank=True,null=True) # Django Ticket #12708
    kw.update(related_name="%(app_label)s_%(class)s_set_by_journal")
    return models.ForeignKey(Journal,**kw)

def VoucherNumber(**kw):
    return models.IntegerField(**kw)
    


#~ class Voucher(mixins.Controllable):
#~ class Voucher(mixins.UserAuthored,mixins.ProjectRelated):
class Voucher(mixins.UserAuthored,mixins.Registrable):
    """
    A Voucher is a document that represents a monetary transaction.
    Subclasses must define a field `state`.
    This model is subclassed by sales.Invoice, ledger.AccountInvoice, 
    finan.Statement etc...
    
    It is *not* abstract because we have a ForeignKey to Voucher in 
    Movement and we want one Movement model for all ledger movements.
    
    """
    class Meta:
        verbose_name = _("Voucher")
        verbose_name_plural = _("Vouchers")
        #~ abstract = True
        
    #~ required_to_deregister = dict(states='registered paid')
        
    #~ controller_is_optional = False
    
    date = models.DateField(_("Date"),default=datetime.date.today)
    
    journal = JournalRef()
    year = FiscalYears.field(blank=True)
    number = VoucherNumber(blank=True,null=True)
    #~ ledger_remark = models.CharField("Remark for ledger",
      #~ max_length=200,blank=True)
    narration = models.CharField(_("Narration"),max_length=200,blank=True)
    
    #~ @classmethod
    #~ def create_journal(cls,id,**kw):
        #~ doctype = get_doctype(cls)
        #~ jnl = Journal(doctype=doctype,id=id,**kw)
        #~ return jnl
        
    def get_due_date(self):
        return self.date
        
    def get_trade_type(self):
        return self.journal.trade_type
        
    @classmethod
    def create_journal(cls,trade_type=None,account=None,chart=None,**kw):
    #~ def create_journal(cls,jnl_id,trade_type,**kw):
        #~ doctype = get_doctype(cls)
        #~ jnl = Journal(doctype=doctype,id=jnl_id,*args,**kw)
        if isinstance(account,basestring):
            account = chart.get_account_by_ref(account)
            #~ account = account.Account.objects.get(chart=chart,ref=account)
        if isinstance(trade_type,basestring):
            trade_type = vat.TradeTypes.get_by_name(trade_type)
        vt = VoucherTypes.get_by_value(dd.full_model_name(cls))
        kw.update(chart=chart)
        if account is not None:
            kw.update(account=account)
        #~ jnl = Journal(trade_type=tt,voucher_type=vt,id=jnl_id,**kw)
        return Journal(trade_type=trade_type,voucher_type=vt,**kw)
        
    @classmethod
    def get_journals(cls):
        vt = VoucherTypes.get_by_value(dd.full_model_name(cls))
        #~ doctype = get_doctype(cls)
        return Journal.objects.filter(voucher_type=vt).order_by('seqno')
            
        
    def __unicode__(self):
        if self.number is None:
            return "%s #%s (not registered)" % (
                unicode(self.journal.voucher_type.model._meta.verbose_name),self.id)
        if self.journal.ref:
            return "%s#%s" % (self.journal.ref,self.number)
        return "#%s (%s %s)" % (self.number,self.journal,self.year)
        
    def get_default_match(self):
        #~ return "%s#%s" % (self.journal.ref,self.number)
        return "%s%s" % (self.id,self.journal.ref)
        
    #~ def on_create(self,*args,**kw):
        #~ super(Voucher,self).on_create(*args,**kw)
        #~ settings.SITE.on_create_voucher(self)
                
    def register(self,ar):
        """
        delete any existing movements and re-create them
        """
        if self.year is None:
            self.year = FiscalYears.from_date(self.date)
        if self.number is None:
            self.number = self.journal.get_next_number(self)
        assert self.number is not None
        self.movement_set.all().delete() 
        for m in self.get_wanted_movements():
            m.full_clean()
            m.save()
        super(Voucher,self).register(ar)
        
    def deregister(self,ar):
        self.number = None
        self.movement_set.all().delete() 
        super(Voucher,self).deregister(ar)
        
        
        
    def disable_delete(self,ar):
        msg = self.journal.disable_voucher_delete(self)
        if msg is not None:
            return msg
        return super(Voucher,self).disable_delete(ar)
            
        
    #~ def delete(self):
        #~ self.journal.pre_delete_voucher(self)
        #~ return super(Voucher,self).delete()
        
    #~ def get_child_model(self):
        #~ ## overrides Typed
        #~ return DOCTYPES[self.journal.doctype][0]
        
        
    def get_wanted_movements(self):
        """
        Subclasses must implement this. 
        Supposed to return or yield a list 
        of unsaved :class:`Movement` instances.
        """
        raise NotImplementedError()
        #~ return []
        
    #~ def create_movement_credit(self,account,amount,**kw):
        #~ kw.update(is_credit=True)
        #~ return self.create_movement(account,amount,**kw)
        
    #~ def create_movement_debit(self,account,amount,**kw):
        #~ kw.update(is_credit=False)
        #~ return self.create_movement(account,amount,**kw)
        
    def create_movement(self,account,dc,amount,**kw):
        assert isinstance(account,accounts.Account)
        kw['voucher'] = self
        #~ account = accounts.Account.objects.get(group__ref=account)
        #~ account = self.journal.chart.get_account_by_ref(account)
        kw['account'] = account
        if amount < 0:
            amount = - amount
            dc = not dc
        kw['amount'] = amount
        kw['dc'] = dc
        
        #~ kw['journal'] = self.journal
        #~ kw['year'] = self.year
        #~ kw['number'] = self.number
        #~ kw['voucher'] = self
        #kw['number'] = self.number
        #~ kw.setdefault('date',self.date)
        #~ if not kw.get('date',None):
            #~ kw['date'] = self.value_date
        b = Movement(**kw)
        #print b.date
        #b.save()
        return b
        
    #~ def get_row_permission(self,ar,state,ba):
        #~ """
        #~ Only invoices in an editable state may be edited.
        #~ """
        #~ if not ba.action.readonly and self.state is not None and not self.state.editable:
            #~ return False
        #~ return super(Voucher,self).get_row_permission(ar,state,ba)

    def get_mti_child(self):
        return self.journal.voucher_type.model.objects.get(
            journal=self.journal,number=self.number,year=self.year)
        #~ m = self.journal.voucher_type.model
        #~ return m.objects.get(pk=self.pk)
        
    def obj2html(self,ar):
        return ar.obj2html(self.get_mti_child())
        
    
    #~ def add_voucher_item(self,account=None,**kw):
        #~ if account is not None:
            #~ if not isinstance(account,accounts.Account):
            #~ if isinstance(account,basestring):
                #~ account = self.journal.chart.get_account_by_ref(account)
            #~ kw['account'] = account
        
    def add_voucher_item(self,account=None,**kw):
        if account is not None:
            if isinstance(account,basestring):
                account = self.journal.chart.get_account_by_ref(account)
            kw['account'] = account
        kw.update(voucher=self)
        return self.items.model(**kw)
        #~ return super(AccountInvoice,self).add_voucher_item(**kw)
        
        
class Vouchers(dd.Table):
    """
    List of all vouchers
    """
    model = Voucher
    editable = False
    order_by = ["date","number"]
    column_names = "date number *"


#~ class VouchersByJournal(dd.Table):
class ByJournal(dd.Table):
    order_by = ["number"]
    master_key = 'journal' # see django issue 10808
    #master = journals.Journal
    
    @classmethod
    def get_title_base(self,ar):
        """
        Without this override we would have a title like "Invoices of journal <Invoices>"
        """
        return unicode(ar.master_instance)
                  






        
class Matchable(dd.Model):
    
    class Meta: 
        abstract = True
        
    match = MatchField(blank=True)
    #~ match = dd.ForeignKey('ledger.Movement',verbose_name=_("Match"),blank=True,null=True)
    
    #~ @dd.chooser()
    #~ def match_choices(cls,partner):
        #~ d = {}
        #~ qs = Movement.objects.filter(partner=partner,satisfied=False)
        #~ for m in qs:
            #~ i = d.setdefault(m.get_match(),[])
            #~ i.append(m)
        #~ choices = []
        #~ for k,lst in d.items():
            #~ amount = ZERO
            #~ text = ", ".join([i.select_text() for i in lst])
            #~ for i in lst:
                #~ amount += iif(i.dc,1,-1) * i.amount
            #~ text += ' ' + unicode(amount)
            #~ choices.append((k,text))
        #~ return choices
        
        
        
    @dd.chooser(simple_values=True)
    def match_choices(cls,partner):
        #~ DC = voucher.journal.dc
        #~ choices = []
        qs = Movement.objects.filter(partner=partner,satisfied=False)
        qs = qs.order_by('voucher__date')
        #~ qs = qs.distinct('match')
        return qs.values_list('match',flat=True)
        
        for mvt in qs:
            choices.append(Match(DC,partner,mvt.match))
        return choices
        
    #~ def get_match_display(self,m):
        #~ return repr(m)
    


    
class Movement(mixins.Sequenced,Matchable):
  
    allow_cascaded_delete = ['voucher']
    
    class Meta:
        verbose_name = _("Movement")
        verbose_name_plural = _("Movements")
        
    voucher = models.ForeignKey(Voucher)
    #~ pos = models.IntegerField("Position",blank=True,null=True)
    account = dd.ForeignKey(accounts.Account)
    partner = dd.ForeignKey(partner_model,blank=True,null=True)
    amount = dd.PriceField(default=0)
    dc = DebitOrCreditField()
    satisfied = models.BooleanField(_("Satisfied"),default=False)
    #~ match = dd.ForeignKey('self',verbose_name=_("Match"),blank=True,null=True)
    #~ is_credit = models.BooleanField(_("Credit"),default=False)
    #~ debit = dd.PriceField(default=0)
    #~ credit = dd.PriceField(default=0)
    
    #~ def full_clean(self,*args,**kw):
        #~ if not self.match:
            #~ self.match = self.voucher.get_default_match()
        #~ super(Matchable,self).full_clean(*args,**kw)
    
    #~ def get_default_match(self):
        #~ return unicode(self.voucher)
        
    def select_text(self):
        v = self.voucher.get_mti_child()
        return "%s (%s)" % (v,v.date)
    
    @dd.virtualfield(dd.PriceField(_("Debit")))
    def debit(self,ar):
        if self.dc: 
            #~ return ZERO
            return None
        return self.amount
    
    @dd.virtualfield(dd.PriceField(_("Credit")))
    def credit(self,ar):
        if self.dc: 
            return self.amount
        #~ return ZERO
        return None
            
    @dd.displayfield(_("Voucher"))
    def voucher_link(self,ar):
        #~ return self.voucher.get_mti_child().obj2html(ar)
        return ar.obj2html(self.voucher.get_mti_child())
        
    #~ @dd.displayfield(_("Matched by"))
    #~ def matched_by(self,ar):
        #~ elems = [obj.voucher_link(ar) for obj in Movement.objects.filter(match=self)]
        #~ return E.div(*elems)
        
    
    def get_siblings(self):
        return self.voucher.movement_set.order_by('seqno')
        #~ return self.__class__.objects.filter().order_by('seqno')
        
    def __unicode__(self):
        return "%s.%d" % (unicode(self.voucher),self.seqno)
        

class Movements(dd.Table): 
    model = Movement
    column_names = 'voucher_link account debit credit *'
    editable = False
    
class MovementsByVoucher(Movements):
    master_key = 'voucher'
    column_names = 'seqno account debit credit match satisfied'
    #~ editable = False
    auto_fit_column_widths = True
    
class MovementsByPartner(Movements):
    master_key = 'partner'
    order_by = ['-voucher__date']
    column_names = 'voucher__date voucher_link debit credit account match satisfied'
    #~ editable = False
    auto_fit_column_widths = True
    
class Match(object):
    """
    Volatile object representing a group of movements
    """
    def __init__(self,dc,partner,match):
        self.dc = dc
        self.partner = partner
        self.match = match
        self.debts = []
        self.received = []
        self.balance = ZERO
        self.due_date = None
        self.trade_type = None
        self.has_unsatisfied_movement = False
        self.has_satisfied_movement = False
        
        qs = Movement.objects.filter(partner=partner,match=match)
        for mvt in qs.order_by('voucher__date'):
            self.collect(mvt)
    
    def collect(self,mvt):
        if mvt.satisfied:
            self.has_satisfied_movement = True
        else:
            self.has_unsatisfied_movement = True
        if self.trade_type is None:
            voucher = mvt.voucher.get_mti_child()
            self.trade_type = voucher.get_trade_type()
        if mvt.dc == self.dc:
            self.debts.append(mvt)
            self.balance += mvt.amount
            voucher = mvt.voucher.get_mti_child()
            due_date = voucher.get_due_date()
            if self.due_date is None or due_date < self.due_date:
                self.due_date = due_date
        else:
            self.received.append(mvt)
            self.balance -= mvt.amount
    
    def update_satisfied(self):
        satisfied = self.balance != ZERO
        if satisfied:
            if not self.has_unsatisfied_movement: return 
        else:
            if not self.has_satisfied_movement: return 
        for m in self.debts + self.received:
            if m.satisfied != satisfied:
                m.satisfied = satisfied
                m.save()
                
def get_partner_matches(partner,dc,**flt):
    qs = Movement.objects.filter(partner=partner,**flt)
    qs = qs.order_by('voucher__date')
    if False: # DISTINCT ON fields not supported
        qs = qs.distinct('match') 
        for mvt in qs:
            yield Match(cls.DUE_DC,partner,mvt.match)
    else:
        #~ logger.info("20130921 %s %s",partner,qs)
        found = set()
        for mvt in qs:
            if not mvt.match in found:
                found.add(mvt.match)
                yield Match(dc,partner,mvt.match)
        
    
class DuePaymentsByPartner(dd.VirtualTable):
    """
    Due Payements is the table to print in a Payment Reminder.
    Usually this table has one row per sales invoice which is not completely paid.
    But several invoices ("debts") may be grouped by match.
    """
    
    master = 'contacts.Partner'
    column_names = 'match due_date balance debts received'
    auto_fit_column_widths = True
    
    DUE_DC = accounts.DEBIT
    
    
    @classmethod
    def get_data_rows(cls,ar):
        partner = ar.master_instance
        if partner is None: return 
        return get_partner_matches(cls.DUE_DC,partner,satisfied=False)
        
    @dd.displayfield(_("Match"))
    def match(self,row,ar):
        return row.match
            
    @dd.displayfield(_("Due date"))
    def due_date(self,row,ar):
        return row.due_date
            
    @dd.displayfield(_("Due"))
    def debts(self,row,ar):
        #~ return ", ".join([ar.obj2html(i,i.select_text()) for i in row.debts])
        #~ return join_elems([ar.obj2html(i.voucher,i.select_text()) for i in row.debts])
        return join_elems([ar.obj2html(i.voucher.get_mti_child()) for i in row.debts])
            
    @dd.displayfield(_("Received"))
    def received(self,row,ar):
        #~ return ", ".join([ar.obj2html(i,i.select_text()) for i in row.received])
        #~ return join_elems([ar.obj2html(i.voucher,i.select_text()) for i in row.received])
        return join_elems([ar.obj2html(i.voucher.get_mti_child()) for i in row.received])
        
    @dd.virtualfield(dd.PriceField(_("Balance")))
    def balance(self,row,ar):
        return row.balance
            



class InvoiceStates(dd.Workflow):
    #~ label = _("State")
    pass
add = InvoiceStates.add_item
add('10',_("Draft"),'draft',editable=True) 
add('20',_("Registered"),'registered',editable=False) 
#~ add('20',_("Signed"),'signed')
#~ add('30',_("Sent"),'sent')
add('40',_("Paid"),'paid',editable=False)

#~ InvoiceStates.draft.add_transition(_("Deregister"),states='registered paid')
#~ InvoiceStates.registered.add_transition(_("Register"),states='draft')
    
class AccountInvoice(vat.VatDocument,Voucher,Matchable):
    
    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
    
    your_ref = models.CharField(_("Your reference"),
        max_length=200,blank=True)
    
    due_date = models.DateField(_("Due date"),blank=True,null=True)
    
    state = InvoiceStates.field(default=InvoiceStates.draft)
    
    workflow_state_field = 'state'
    
    def get_due_date(self):
        return self.due_date or self.date
        
        
    


class VoucherItem(dd.Model):
    """
    Subclasses must define a field `voucher` which must 
    be a FK with related_name='items'
    """
    
    allow_cascaded_delete = ['voucher']
    
    class Meta:
        abstract = True
        verbose_name = _("Voucher item")
        verbose_name_plural = _("Voucher items")
        
    title = models.CharField(_("Description"),max_length=200,blank=True)
    
    def get_row_permission(self,ar,state,ba):
        """
        Items of registered invoices may not be edited
        """
        #~ logger.info("VoucherItem.get_row_permission %s %s %s",self.voucher,state,ba)
        if not self.voucher.state.editable:
            #~ if not ar.bound_action.action.readonly:
            if not ba.action.readonly:
                return False
        #~ if not self.voucher.get_row_permission(ar,self.voucher.state,ba):
            #~ return False
        return super(VoucherItem,self).get_row_permission(ar,state,ba)
        
        

class InvoiceDetail(dd.FormLayout):
    main = "general ledger"
    
    totals = """
    total_base
    total_vat
    total_incl
    workflow_buttons
    """
    
    general = dd.Panel("""
    id date partner user 
    due_date your_ref vat_regime #item_vat
    ItemsByInvoice:60 totals:20
    """,label=_("General"))
    
    ledger = dd.Panel("""
    journal year number narration
    MovementsByVoucher
    """,label=_("Ledger"))
    
class Invoices(dd.Table):
    parameters = dict(
        pyear=FiscalYears.field(blank=True),
        ppartner=models.ForeignKey(partner_model,blank=True,null=True),
        pjournal=JournalRef(blank=True))
    model = AccountInvoice
    order_by = ["date","id"]
    column_names = "date id number partner total_incl user *" 
    params_layout = "pjournal pyear ppartner"
    detail_layout = InvoiceDetail()
    insert_layout = dd.FormLayout("""
    partner
    date total_incl
    """,window_size=(60,'auto'))
    
    @classmethod
    def get_request_queryset(cls,ar):
        qs = super(Invoices,cls).get_request_queryset(ar)
        if ar.param_values.ppartner:
            qs = qs.filter(partner=ar.param_values.ppartner)
        if ar.param_values.pyear:
            qs = qs.filter(year=ar.param_values.pyear)
        if ar.param_values.pjournal:
            qs = qs.filter(journal=ar.param_values.pjournal)
        return qs
    
    


class InvoicesByJournal(ByJournal,Invoices):
    column_names = "number date due_date " \
                  "partner " \
                  "total_incl " \
                  "total_base total_vat user workflow_buttons *"
                  #~ "ledger_remark:10 " \
    params_panel_hidden = True
                  
                  

    

class InvoicesByPartner(Invoices):
    label = _("Unregistered invoices")
    order_by = ["date"]
    master_key = 'partner'
    column_names = "date total_incl total_base total_vat *"
    filter = models.Q(state=InvoiceStates.draft)
    


VoucherTypes.add_item(AccountInvoice,InvoicesByJournal)


class InvoiceItem(VoucherItem,vat.VatItemBase):
    #~ document = models.ForeignKey(AccountInvoice,related_name='items') 
    voucher = models.ForeignKey(AccountInvoice,related_name='items') 
    
    #~ account = models.ForeignKey('accounts.Account',blank=True,null=True)
    account = models.ForeignKey('accounts.Account')
    
    def get_base_account(self,tt):
        return self.account
        
    @dd.chooser()
    def account_choices(self,voucher):
        if voucher and voucher.journal:
            fkw = {voucher.journal.trade_type.name+'_allowed':True}
            return accounts.Account.objects.filter(chart=voucher.journal.chart,**fkw)
        return []


class ItemsByInvoice(dd.Table):
    model = InvoiceItem
    column_names = "account title vat_class total_base total_vat total_incl seqno"
    master_key = 'voucher'
    order_by = ["seqno"]
    
    
    


#~ MODULE_LABEL = _("Ledger")
MODULE_LABEL = accounts.MODULE_LABEL

def unused_site_setup(site):
    if site.is_installed(settings.SITE.partners_app_label):
        app = site.modules[settings.SITE.partners_app_label]
        for t in (app.Partners,app.Persons,app.Organisations):
            t.add_detail_tab("ledger",
                """
                ledger.InvoicesByPartner
                ledger.MovementsByPartner
                """,
                label=MODULE_LABEL)


def setup_main_menu(site,ui,profile,main): 
    for tt in vat.TradeTypes.objects():
        m = main.add_menu(tt.name,tt.text)
        for jnl in Journal.objects.filter(trade_type=tt):
            m.add_action(jnl.voucher_type.table_class,
                label=unicode(jnl),
                params=dict(master_instance=jnl))


#~ def setup_main_menu(site,ui,user,m): 
    #~ m = m.add_menu("ledger",MODULE_LABEL)
    #~ for jnl in Journal.objects.all():
        #~ m.add_action(jnl.voucher_type.table_class,
            #~ label=unicode(jnl),
            #~ params=dict(master_instance=jnl))
    
def setup_config_menu(site,ui,profile,m): 
    #~ m = m.add_menu("ledger",MODULE_LABEL)
    m = m.add_menu("accounts",MODULE_LABEL)
    m.add_action(Journals)
    
    
def setup_explorer_menu(site,ui,profile,m):
    #~ m = m.add_menu("ledger",MODULE_LABEL)
    m = m.add_menu("accounts",MODULE_LABEL)
    m.add_action(Invoices)
    m.add_action(Vouchers)
    m.add_action(VoucherTypes)
    m.add_action(Movements)
    m.add_action(FiscalYears)
  


def customize_accounts():

    for tt in vat.TradeTypes.objects():
        dd.inject_field('accounts.Account',
            tt.name+'_allowed',
            models.BooleanField(verbose_name=tt.text))

customize_accounts()



def update_partner_satisfied(p):
    for m in get_partner_matches(accounts.DEBIT,p):
        m.update_satisfied()
        
