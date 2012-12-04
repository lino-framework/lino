## Copyright 2012 Luc Saffre
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


class VatTotal(dd.Model):
    class Meta:
        abstract = True
        
    #~ price = dd.PriceField(_("Total"),blank=True,null=True)
    total_incl = dd.PriceField(_("Total incl. VAT"),blank=True,null=True)
    total_base = dd.PriceField(_("Total excl. VAT"),blank=True,null=True)
    total_vat = dd.PriceField(_("VAT"),blank=True,null=True)
    
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
    
    total_based_fields = set()
    
    compute_totals = False
    
    class Meta:
        abstract = True
  
    partner = models.ForeignKey("contacts.Partner")
    item_vat = models.BooleanField(default=False,
      help_text=_("Whether price includes VAT or not."))
    vat_regime = VatRegimes.field(blank=True)
    
    
    @classmethod
    def site_setup(cls,site):
        super(VatDocument,cls).site_setup(site)
        cls.total_based_fields = set(dd.fields_list(cls,'total_vat total_base'))
        
    #~ def on_create(self,ar):
        #~ super(VatDocument,self).on_create(ar)
    
    def disabled_fields(self,ar):
        fields = super(VatDocument,self).disabled_fields(ar)
        if not self.compute_totals:
            fields = fields | self.total_based_fields
        return fields
        
    def get_trade_type(self):
        return TradeTypes.sales
        
    def get_vat_sums(self):
        sums_dict = dict()
        def book(account,amount):
            if sums_dict.has_key(account):
                sums_dict[account] += amount
            else:
                sums_dict[account] = amount
        #~ if self.journal.type == JournalTypes.purchases:
        tt = self.get_trade_type()
        base = Decimal()
        vat = Decimal()
        for i in self.items.order_by('seqno'):
            #~ move(i.get_base_account(),i.total)
            book(i.get_base_account(tt),i.total_base)
            vatacc = settings.LINO.get_vat_account(tt,i.vat_class,self.vat_regime)
            vatacc = self.journal.chart.get_account_by_ref(vatacc)
            book(vatacc,i.total_vat)
            base += i.total_base
            vat += i.total_vat
        self.total_base = base
        self.total_vat = vat
        self.total_incl = vat + base
        return sums_dict
        
    def get_wanted_movements(self):
        sums_dict = self.get_vat_sums()
        #~ logger.info("20120901 get_wanted_movements %s",sums_dict)
        sum = Decimal()
        for a,m in sums_dict.items():
            if m:
                yield self.create_movement(a,m)
                sum += m
        a = settings.LINO.get_partner_account(self)
        a = self.journal.chart.get_account_by_ref(a)
        yield self.create_movement(a,sum,partner=self.partner)
        
        
class VatItemBase(mixins.Sequenced,VatTotal):
    """
    Abstract Base class for InvoiceItem and OrderItem.
    Subclasses must define a field called "voucher" 
    which must be a FK with related_name="items" to the owning document, 
    which in turn must be a subclass of :class:`VatDocument`).
    """
    class Meta:
        abstract = True
        #~ unique_together  = ('document','seqno')
    
    vat_class = VatClasses.field(blank=True)
    
    def get_vat_class(self,tt):
        name = settings.LINO.get_vat_class(tt,self)
        return VatClasses.get_by_name(name)
        
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
        
    #~ def full_clean(self,*args,**kw):
    def before_ui_save(self,ar):
        if self.total_incl is None:
            self.reset_totals(ar)
        super(VatItemBase,self).before_ui_save(ar)
        #~ super(VatItemBase,self).full_clean(*args,**kw)
    #~ before_save.alters_data = True
      
                    
    def reset_totals(self,ar):
        #~ logger.info("20121204 reset_totals")
        if not self.voucher.compute_totals:
            total = Decimal()
            for item in self.voucher.items.exclude(id=self.id):
                total += item.total_incl
            #~ if total != self.voucher.total_incl:
            self.total_incl = self.voucher.total_incl - total
            self.total_incl_changed(ar)
        
        super(VatItemBase,self).reset_totals(ar)
        

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
    
    def reset_totals(self,ar):
        super(QtyVatItemBase,self).reset_totals(ar)
        if not self.voucher.compute_totals:
            if self.qty:
                if self.voucher.item_vat: 
                    self.unit_price = self.total_incl / self.qty
                else:
                    self.unit_price = self.total_base / self.qty
        
        elif self.unit_price is not None and self.qty is not None:
            rate = self.get_vat_rate()
            if self.voucher.item_vat: # unit_price_includes_vat
                self.total_incl = self.unit_price * self.qty
                self.total_base = self.total_incl / (1 + rate)
                self.total_vat = self.total_incl - self.total_base
            else:
                self.total_base = self.unit_price * self.qty
                self.total_vat = self.total_base * rate
                self.total_incl = self.total_base + self.total_vat
                
        

MODULE_LABEL = _("VAT")

def site_setup(site): pass 
def setup_main_menu(site,ui,profile,m): pass
def setup_my_menu(site,ui,profile,m): pass
def setup_config_menu(site,ui,profile,m): pass
#~ def setup_explorer_menu(site,ui,profile,m): pass
  

def setup_explorer_menu(site,ui,profile,m):
    m  = m.add_menu("vat",MODULE_LABEL)
    m.add_action(VatClasses)
  
