## Copyright 2012-2013 Luc Saffre
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
VAT (value-added tax) related logics.

This module defines some central ChoiceLists 
and Model mixins designed to work both with and without 
:mod:`lino.modlib.ledger` installed.

"""

import logging
logger = logging.getLogger(__name__)

import datetime
from decimal import Decimal

from django.db import models
from django.conf import settings

from lino import dd
from lino import mixins
from lino.utils import babel
#~ from lino.core.modeltools import full_model_name
#~ from lino.utils.choicelists import ChoiceList
#contacts = reports.get_app('contacts')
#~ from lino.modlib.journals import models as journals
#~ journals = reports.get_app('journals')
#from lino.modlib.contacts import models as contacts
#from lino.modlib.journals import models as journals
from django.utils.translation import ugettext_lazy as _
#~ from lino.modlib.accounts.utils import AccountTypes

from lino.modlib.ledger.utils import FiscalYears
#~ from lino.core.modeltools import models_by_base

ZERO = Decimal()
 
class VatClasses(dd.ChoiceList):
    """
    A VAT class is usually a direct or indirect property 
    of a trade object which determines the VAT *rate* to be used.
    The actual rates are not stored here, 
    they vary depending on your country, 
    the time and type of the operation, 
    and possibly other factors.
    """
    verbose_name = _("VAT Class")
add = VatClasses.add_item
add('0',_("Exempt"),'exempt')
add('1',_("Reduced"),'reduced')
add('2',_("Normal"),'normal')


class VatRegimes(dd.ChoiceList):
    """
    The VAT regime determines how the VAT is being handled,
    i.e. whether and how it is to be paid.
    """
    verbose_name = _("VAT Regime")
add = VatRegimes.add_item
add('10',_("Private person"),'private')
add('20',_("Subject to VAT"),'subject')
add('25',_("Co-contractor"),'cocontractor')
add('30',_("Intra-community"),'intracom')
add('40',_("Outside EU"),'outside')
add('50',_("Exempt"),'exempt')


    
class TradeTypes(dd.ChoiceList):
    verbose_name = _("Trade Type")
    
add = TradeTypes.add_item
add('S',_("Sales"),'sales')
add('P',_("Purchases"),'purchases')


from dateutil.relativedelta import relativedelta


class Periods(dd.ChoiceList):
    verbose_name = _("VAT Period")
    verbose_name_plural = _("VAT Periods")
    
    @classmethod
    def setup_field(cls,fld):
        def d(): return cls.from_date(datetime.date.today())
        fld.default = d
        
    @classmethod
    def from_date(cls,date):
        date -= relativedelta(months=1)
        return cls.from_int(date.month)
        
    @classmethod
    def from_int(cls,month):
        return cls.get_by_value('%02d' % month)
        
    
add = Periods.add_item

if settings.LINO.vat_quarterly:
  
  add('Q1',_("First Quarter (January-March)"),months=(1,2,3))
  add('Q2',_("Second Quarter (April-June)"),months=(4,5,6,))
  add('Q3',_("Third Quarter (July-August)"),months=(7,8,9))
  add('Q4',_("Fourth Quarter (September-December)"),months=(10,11,12))

else:
    
  add('01',_("January"),'january',months=(1,))
  add('02',_("February"),'february',months=(2,))
  add('03',_("March"),'march',months=(3,))
  add('04',_("April"),'april',months=(4,))
  add('05',_("May"),'may',months=(5,))
  add('06',_("June"),'june',months=(6,))
  add('07',_("July"),'july',months=(7,))
  add('08',_("August"),'august',months=(8,))
  add('09',_("September"),'september',months=(9,))
  add('10',_("October"),'october',months=(10,))
  add('11',_("November"),'november',months=(11,))
  add('12',_("December"),'december',months=(12,))

  

class DeclarationStates(dd.Workflow):
    pass
add = DeclarationStates.add_item
add("00",_("Draft"),"draft")
add("10",_("Registered"),"registered")
add("20",_("Submitted"),"submitted")



class DeclarationFields(dd.ChoiceList):
    
    @classmethod
    def amount_for_field(self,fld,dcl,item,tt):
        if not fld.name.startswith(tt.name):
            return
        #~ if tt.name == 'sales':
        if fld.name.endswith("_base"):
            return item.total_base
        if fld.name.endswith("_vat"):
            return item.total_vat
        #~ if fld.value == '80':
            #~ if item.vat_class == VatClasses.
            #~ if item.get_base_account().type == AccountTypes.invest
            #~ return item.total_base


add = DeclarationFields.add_item
add("00",_("Sales base"),"sales_base")
add("10",_("Sales VAT"),"sales_vat")
add("20",_("Purchases base"),"purchases_base")
add("30",_("Purchases VAT"),"purchases_vat")

declaration_fields_layout = dd.Panel("""
sales_base sales_vat
purchases_base purchases_vat
""")





class VatTotal(dd.Model):
    """
    Model mixin which defines the fields 
    `total_incl`, `total_base` and `total_vat`.
    Used for both the document header (:class:`VatDocument`) 
    and for each item (:class:`VatItemBase`).
    """
    class Meta:
        abstract = True
        
    #~ price = dd.PriceField(_("Total"),blank=True,null=True)
    total_incl = dd.PriceField(_("Total incl. VAT"),blank=True,null=True)
    total_base = dd.PriceField(_("Total excl. VAT"),blank=True,null=True)
    total_vat = dd.PriceField(_("VAT"),blank=True,null=True)
    
    
    _total_fields = set('total_vat total_base total_incl'.split())
    """
    For internal use.
    This is the list of field names to disable when `auto_compute_totals` is True.
    """
    
    auto_compute_totals = False
    """
    Set this to True on subclasses who compute their totals automatically.
    """
    
    #~ @classmethod
    #~ def site_setup(cls,site):
        #~ super(VatDocument,cls).site_setup(site)
        #~ cls._total_fields = set(dd.fields_list(cls,
            #~ 'total_vat total_base total_incl'))
        
    #~ def on_create(self,ar):
        #~ super(VatDocument,self).on_create(ar)
    
    def disabled_fields(self,ar):
        fields = super(VatTotal,self).disabled_fields(ar)
        if self.auto_compute_totals:
            fields = fields | self._total_fields
        return fields
    
    
    def reset_totals(self,ar):
        pass
        
    def get_vat_rate(self,*args,**kw):
        return None
        
    def total_base_changed(self,ar):
        #~ logger.info("20121204 total_base_changed %r",self.total_base)
        if self.total_base is None: 
            self.reset_totals(ar)
            if self.total_base is None: return
        #~ assert not isinstance(self.total_base,basestring)
        rate = self.get_vat_rate()
        #~ logger.info("20121206 total_base_changed %s",rate)
        if rate is None: 
            return
        self.total_vat = self.total_base * rate
        self.total_incl = self.total_base + self.total_vat
           
    def total_vat_changed(self,ar):
        if self.total_vat is None: 
            self.reset_totals(ar)
            if self.total_vat is None: return
        #~ assert not isinstance(self.total_vat,basestring)
        rate = self.get_vat_rate()
        if rate is None: return
        self.total_base = self.total_vat * rate
        self.total_incl = self.total_base + self.total_vat
        
    def total_incl_changed(self,ar):
        if self.total_incl is None: 
            self.reset_totals(ar)
            if self.total_incl is None: return
        #~ assert not isinstance(self.total_incl,basestring)
        rate = self.get_vat_rate()
        #~ logger.info("20121206 total_incl_changed %s",rate)
        if rate is None: return
        self.total_base = self.total_incl / (1 + rate)
        self.total_vat = self.total_incl - self.total_base
    
    #~ @dd.virtualfield(dd.PriceField(_("Total incl. VAT")))
    #~ def total_incl(self,ar=None):
        #~ """
        #~ Virtual field returning the sum of `total_base` and `total_vat`.
        #~ """
        #~ if self.total_base is None:
            #~ return None
        #~ return self.total_base + self.total_vat
        
class VatDocument(mixins.UserAuthored,VatTotal):
    """
    This is also used for Offers and other non-ledger documents
    """
    
    auto_compute_totals = True
    
    refresh_after_item_edit = False
    """
    See :doc:`/tickets/68`
    """
        
    class Meta:
        abstract = True
  
    partner = models.ForeignKey("contacts.Partner")
    item_vat = models.BooleanField(default=False,
      help_text=_("Whether price includes VAT or not."))
    vat_regime = VatRegimes.field(blank=True)
    declaration = models.ForeignKey("vat.Declaration",blank=True,null=True)
    
    
    def get_trade_type(self):
        raise NotImplementedError()
        
        
    def compute_totals(self):
        if self.pk is None:
            return
        base = Decimal()
        vat = Decimal()
        for i in self.items.order_by('seqno'):
            if i.total_base is not None:
                base += i.total_base
                vat += i.total_vat
        self.total_base = base
        self.total_vat = vat
        self.total_incl = vat + base
      
    def get_vat_sums(self):
        sums_dict = dict()
        def book(account,amount):
            if sums_dict.has_key(account):
                sums_dict[account] += amount
            else:
                sums_dict[account] = amount
        #~ if self.journal.type == JournalTypes.purchases:
        tt = self.get_trade_type()
        for i in self.items.order_by('seqno'):
            if i.total_base is not None:
                book(i.get_base_account(tt),i.total_base)
                vatacc = settings.LINO.get_vat_account(tt,i.vat_class,self.vat_regime)
                vatacc = self.journal.chart.get_account_by_ref(vatacc)
                book(vatacc,i.total_vat)
        return sums_dict
        
    def get_wanted_movements(self):
        sums_dict = self.get_vat_sums()
        #~ logger.info("20120901 get_wanted_movements %s",sums_dict)
        sum = Decimal()
        for a,m in sums_dict.items():
            if m:
                yield self.create_movement(a,a.type.dc,m)
                sum += m
        a = settings.LINO.get_partner_account(self)
        a = self.journal.chart.get_account_by_ref(a)
        yield self.create_movement(a,a.type.dc,sum,partner=self.partner)
        
    def full_clean(self,*args,**kw):
        self.compute_totals()
        super(VatDocument,self).full_clean(*args,**kw)
        
    def register(self,ar):
        self.compute_totals()
        super(VatDocument,self).register(ar)
        

#~ class DeclaredVatDocument(VatDocument):
    #~ class Meta:
        #~ abstract = True
    
        
class VatItemBase(mixins.Sequenced,VatTotal):
    """
    Abstract Base class for InvoiceItem and OrderItem.
    Subclasses must define a field called "voucher" 
    which must be a FK with related_name="items" to the 
    "owning document", 
    which in turn must be a subclass of :class:`VatDocument`).
    """
    class Meta:
        abstract = True
        #~ unique_together  = ('document','seqno')
    
    vat_class = VatClasses.field(blank=True)
    
    def get_vat_class(self,tt):
        name = settings.LINO.get_vat_class(tt,self)
        return VatClasses.get_by_name(name)
        
    def vat_class_changed(self,ar):
        #~ logger.info("20121204 vat_class_changed")
        if self.voucher.item_vat:
            self.total_incl_changed(ar)
        else:
            self.total_base_changed(ar)
              
    def get_base_account(self,tt):
        raise NotImplementedError
        
    #~ def unit_price_includes_vat(self):
        #~ return True
        
    def get_siblings(self):
        return self.voucher.items.all()
    
    def get_vat_rate(self,*args,**kw):
        tt = self.voucher.get_trade_type()
        if self.vat_class is None:
            self.vat_class = self.get_vat_class(tt)
        return settings.LINO.get_vat_rate(tt,
            self.vat_class,
            self.voucher.vat_regime)
        
    #~ def save(self,*args,**kw):
        #~ super(VatItemBase,self).save(*args,**kw)
        #~ self.voucher.full_clean()
        #~ self.voucher.save()
        
    def reset_totals(self,ar):
        #~ logger.info("20121204 reset_totals")
        if not self.voucher.auto_compute_totals:
            total = Decimal()
            for item in self.voucher.items.exclude(id=self.id):
                total += item.total_incl
            #~ if total != self.voucher.total_incl:
            self.total_incl = self.voucher.total_incl - total
            self.total_incl_changed(ar)
        
        super(VatItemBase,self).reset_totals(ar)
        
    def before_ui_save(self,ar):
        if self.total_incl is None:
            self.reset_totals(ar)
        super(VatItemBase,self).before_ui_save(ar)
        #~ super(VatItemBase,self).full_clean(*args,**kw)
    #~ before_save.alters_data = True
      
                    
    def after_ui_save(self,ar,**kw):
        """
        after edit of a grid cell automatically show new invoice totals 
        See :doc:`/tickets/68`
        """
        kw = super(VatItemBase,self).after_ui_save(ar,**kw)
        if self.voucher.refresh_after_item_edit:
            kw.update(refresh_all=True) 
            self.voucher.compute_totals()
            self.voucher.full_clean()
            self.voucher.save()
        return kw

    #~ def __unicode__(self):
        #~ return "%s object" % self.__class__.__name__
        #~ if self.voucher is None:
            #~ return dd.Model.__unicode__(self)
        #~ return u"DocItem %s.%d" % (self.voucher,self.pos)
        
class QtyVatItemBase(VatItemBase):
    class Meta:
        abstract = True
        
    unit_price = dd.PriceField(blank=True,null=True) 
    qty = dd.QuantityField(blank=True) # ,null=True)
    
    def unit_price_changed(self,ar):
        self.reset_totals(ar)
        
    def qty_changed(self,ar):
        self.reset_totals(ar)
        
    def reset_totals(self,ar):
        super(QtyVatItemBase,self).reset_totals(ar)
        #~ if not self.voucher.auto_compute_totals:
            #~ if self.qty:
                #~ if self.voucher.item_vat: 
                    #~ self.unit_price = self.total_incl / self.qty
                #~ else:
                    #~ self.unit_price = self.total_base / self.qty
        
        if self.unit_price is not None and self.qty is not None:
            rate = self.get_vat_rate()
            if self.voucher.item_vat: # unit_price_includes_vat
                self.total_incl = self.unit_price * self.qty
                self.total_base = self.total_incl / (1 + rate)
                self.total_vat = self.total_incl - self.total_base
            else:
                self.total_base = self.unit_price * self.qty
                self.total_vat = self.total_base * rate
                self.total_incl = self.total_base + self.total_vat
                

class Declaration(mixins.Registrable):
    class Meta:
        verbose_name = _("VAT declaration")
        verbose_name_plural = _("VAT declarations")
        
    year = FiscalYears.field()
    period = Periods.field()
    state = DeclarationStates.field(default=DeclarationStates.draft)
    
    def can_declare(self,doc):
        if doc.year == self.year:
            if doc.date.month in self.period.months:
                return True
            #~ logger.info("20121208 not %s in %s",doc.date.month,self.period.months)
        return False
        
    #~ def save(self,*args,**kw):
        #~ if self.state == DeclarationStates.draft:
            #~ if self.year and self.period:
                #~ self.compute_fields()
        #~ super(Declaration,self).save(*args,**kw)
    
    def full_clean(self,*args,**kw):
        self.compute_fields()
        super(Declaration,self).full_clean(*args,**kw)
        
    def register(self,ar):
        self.compute_fields()
        super(Declaration,self).register(ar)
        
    def deregister(self,ar):
        for m in dd.models_by_base(VatDocument):
            #~ logger.info("20121208 a model %s",m)
            for doc in m.objects.filter(declaration=self):
                doc.declaration = None
                doc.save()
        super(Declaration,self).deregister(ar)
        
    def compute_fields(self):
        ledger = dd.resolve_app('ledger')
        sums = dict()
        for fld in DeclarationFields.objects():
            sums[fld.name] = Decimal('0')
        
        item_models = []
        count = 0
        for m in dd.models_by_base(VatDocument):
            if issubclass(m,ledger.Voucher):
                item_models.append(m.items.related.model)
                #~ logger.info("20121208 a model %s",m)
                for doc in m.objects.filter(declaration__isnull=True):
                    #~ logger.info("20121208 a document %s",doc)
                    if self.can_declare(doc):
                        #~ logger.info("20121208 a can_declare %s",doc)
                        count += 1
                        doc.declaration = self
                        doc.save()

        #~ print 20121209, item_models
        for m in item_models:
        #~ for m in dd.models_by_base(VatDocument):
            for item in m.objects.filter(voucher__declaration=self):
                #~ logger.info("20121208 b document %s",doc)
                self.collect_item(sums,item)
                
        for fld in DeclarationFields.objects():
            setattr(self,fld.name,sums[fld.name])
            
                
    def collect_item(self,sums,item):
        tt = item.voucher.get_trade_type()
        for fld in DeclarationFields.objects():
            amount = DeclarationFields.amount_for_field(fld,self,item,tt)
            if amount:
                sums[fld.name] += amount
            
            #~ m = getattr(self,"collect_"+fld.name,None)
            #~ if m:
                #~ amount = m(self,tt,doc)
                #~ if amount:
                    #~ sums[fld.name] += amount
                    
                    
  
class DocumentsByDeclaration(dd.VirtualTable):
#~ class DocumentsByDeclaration(dd.Table):
    master = Declaration
    column_names = 'date partner voucher total_base total_vat total_incl'
    #~ model = VatDocument
    #~ master_key = 'declaration'
  
    @classmethod
    def get_data_rows(self,ar):
    #~ def get_request_queryset(self,ar):
        docs = []
        for m in dd.models_by_base(VatDocument):
            for doc in m.objects.filter(declaration=ar.master_instance):
                docs.append(doc)
                
        def f(a,b): return cmp(a.date,b.date)
        docs.sort(f)
        return docs
        
    @dd.virtualfield(models.DateField(_("Date")))
    def date(self,obj,ar=None): return obj.date
        
    @dd.virtualfield(models.ForeignKey('contacts.Partner'))
    def partner(self,obj,ar=None): return obj.partner
    
    @dd.virtualfield(dd.PriceField(_("Total incl. VAT")))
    def total_incl(self,obj,ar=None): return obj.total_incl
      
    @dd.virtualfield(dd.PriceField(_("Total excl. VAT")))
    def total_base(self,obj,ar=None): return obj.total_base
      
    @dd.virtualfield(dd.PriceField(_("Total VAT")))
    def total_vat(self,obj,ar=None): return obj.total_vat
      
    @dd.displayfield(_("Voucher"))
    def voucher(self,obj,ar): return obj.href_to(ar)
      

for fld in DeclarationFields.objects():
    dd.inject_field(Declaration,fld.name,dd.PriceField(fld.text,default=Decimal))

    
class Declarations(dd.Table):
    model = Declaration
    column_names = 'year period workflow_buttons * state id'
    insert_layout = dd.FormLayout("""
    date 
    year 
    period
    """,window_size=(40,'auto'))
    detail_layout = dd.FormLayout("""
    date year period workflow_buttons
    fields
    DocumentsByDeclaration
    """,fields=declaration_fields_layout)
    
    
        

MODULE_LABEL = _("VAT")

def site_setup(site): pass 
def setup_main_menu(site,ui,profile,m): pass
def setup_my_menu(site,ui,profile,m): pass
  
def setup_reports_menu(site,ui,profile,m):
    m  = m.add_menu("vat",MODULE_LABEL)
    m.add_action(Declarations)
    
def setup_config_menu(site,ui,profile,m): pass
#~ def setup_explorer_menu(site,ui,profile,m): pass
  

def setup_explorer_menu(site,ui,profile,m):
    m  = m.add_menu("vat",MODULE_LABEL)
    m.add_action(VatRegimes)
    m.add_action(TradeTypes)
    m.add_action(VatClasses)
  
