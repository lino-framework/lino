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
and Model mixins 
designed to work both *with* and *without* 
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
from lino.utils.choicelists import ChoiceList, Choice
#contacts = reports.get_app('contacts')
#~ from lino.modlib.journals import models as journals
#~ journals = reports.get_app('journals')
#from lino.modlib.contacts import models as contacts
#from lino.modlib.journals import models as journals
from django.utils.translation import ugettext_lazy as _
#~ from lino.modlib.ledger.utils import FiscalYears
#~ from lino.modlib.accounts.utils import AccountTypes

ZERO = Decimal()
 
class VatClasses(ChoiceList):
    """
    A VAT class is usually a direct or indirect property 
    of a trade object which determines the VAT *rate* to be used.
    The actual rates are not stored here, 
    they vary depending on your country, 
    the time and type of the operation, 
    and possibly other factors.
    """
    label = _("VAT Rate")
add = VatClasses.add_item
add('0',_("Exempt"),'exempt')
add('1',_("Reduced"),'reduced')
add('2',_("Normal"),'normal')


class VatRegimes(ChoiceList):
    """
    The VAT regime determines how the VAT is being handled,
    i.e. whether and how it is to be paid.
    """
    label = _("VAT Regime")
add = VatRegimes.add_item
add('10',_("Private person"),'private')
add('20',_("Subject to VAT"),'subject')
add('25',_("Co-contractor"),'cocontractor')
add('30',_("Intra-community"),'intracom')
add('40',_("Outside EU"),'outside')
add('50',_("Exempt"),'exempt')


    
class TradeTypes(ChoiceList):
    label = _("Trade Type")
add = TradeTypes.add_item
add('S',_("Sales"),'sales')
add('P',_("Purchases"),'purchases')


class VatTotal(dd.Model):
    class Meta:
        abstract = True
        
    total_excl = dd.PriceField(_("Total excl. VAT"),blank=True,null=True)
    total_vat = dd.PriceField(_("VAT"),blank=True,null=True)
    
    @dd.virtualfield(dd.PriceField(_("Total incl. VAT")))
    def total_incl(self,ar=None):
        """
        Virtual field returning the sum of `total_excl` and `total_vat`.
        """
        if self.total_excl is None:
            return None
        return self.total_excl + self.total_vat
        
class VatDocument(mixins.UserAuthored,VatTotal):
    """
    This is also used for Offers and other non-ledger documents
    """
    class Meta:
        abstract = True
  
    partner = models.ForeignKey("contacts.Partner")
    item_vat = models.BooleanField(default=False,
      help_text=_("Whether item unit price includes VAT or not."))
    vat_regime = VatRegimes.field(blank=True)
    def get_trade_type(self):
        return TradeTypes.sales
        
    def get_sums(self):
        sums_dict = dict()
        def move(account,amount):
            if sums_dict.has_key(account):
                sums_dict[account] += amount
            else:
                sums_dict[account] = amount
        #~ if self.journal.type == JournalTypes.purchases:
        tt = self.get_trade_type()
        for i in self.items.order_by('seqno'):
            #~ move(i.get_base_account(),i.total)
            move(i.get_base_account(tt),i.total_excl)
            move(
                settings.LINO.get_vat_account(tt,i.vat_class,self.vat_regime),
                i.total_vat)
        return sums_dict
        
    def get_wanted_movements(self):
        sums_dict = self.get_sums()
        #~ logger.info("20120901 get_wanted_movements %s",sums_dict)
        sum = ZERO
        for a,m in sums_dict.items():
            if m:
                yield self.create_movement(a,m)
                sum += m
        a = settings.LINO.get_partner_account(self)
        yield self.create_movement(a,sum,partner=self.partner)
        
        
class VatItemBase(mixins.Sequenced,VatTotal):
    """
    Abstract Base class for InvoiceItem and OrderItem.
    Subclasses MUST define a field called "document" 
    which MUST be a FK with related_name="items" to the owning document, which in turn MUST be a subclass of :class:`VatDocument`).
    """
    class Meta:
        abstract = True
        #~ unique_together  = ('document','seqno')
    
    vat_class = VatClasses.field(blank=True)
    unit_price = dd.PriceField(blank=True,null=True) 
    qty = dd.QuantityField(blank=True) # ,null=True)
    #~ total = dd.PriceField(blank=True,null=True)
    
    
    #~ def total_excl(self):
        #~ if self.unitPrice is not None:
            #~ qty = self.qty or 1
            #~ return self.unitPrice * qty
        #~ elif self.total is not None:
            #~ return self.total
        #~ return 0
        
    #~ def save(self, *args, **kwargs):
        #~ self.before_save()
        #~ super(DocItem,self).save(*args,**kwargs)
                    
    def get_base_account(self,tt):
        raise NotImplementedError
        
    #~ def unit_price_includes_vat(self):
        #~ return True
        
    def get_siblings(self):
        return self.document.items.all()
    
    def full_clean(self,*args,**kw):
        tt = self.document.get_trade_type()
        if self.vat_class is None:
            #~ self.vat_class = VatClasses.normal
            self.vat_class = self.get_vat_class(tt)
            
        if self.unit_price is not None and self.qty is not None:
            rate = settings.LINO.get_vat_rate(tt,
                self.vat_class,
                self.document.vat_regime)
            if self.document.item_vat: # unit_price_includes_vat
                total_incl = self.unit_price * self.qty
                self.total_excl = total_incl / (1 + rate)
                self.total_vat = total_incl - self.total_excl
            else:
                self.total_excl = self.unit_price * self.qty
                self.total_vat = self.total_excl * rate
        super(VatItemBase,self).full_clean(*args,**kw)
    #~ before_save.alters_data = True

    #~ def __unicode__(self):
        #~ return "%s object" % self.__class__.__name__
        #~ if self.document is None:
            #~ return dd.Model.__unicode__(self)
        #~ return u"DocItem %s.%d" % (self.document,self.pos)
        
        

MODULE_LABEL = _("VAT")

def site_setup(site): pass 
def setup_main_menu(site,ui,user,m): pass
def setup_my_menu(site,ui,user,m): pass
def setup_config_menu(site,ui,user,m): pass
def setup_explorer_menu(site,ui,user,m): pass
  
