# -*- coding: UTF-8 -*-
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
This package contains the **Debt Mediation** 
module 
(Schuldnerberatung, Médiation de dettes) 
for :mod:`lino.apps.pcsw`.
It enables social consultants to create :class:`Budgets`.
A :class:`Budget` collects financial 
information like monthly income, monthly expenses and debts 
of a household or a person, then print out a document which serves 
as base for the consultation and discussion with debtors.

"""

import logging
logger = logging.getLogger(__name__)

import os
import cgi
import datetime
import decimal


from django.db import models
from django.db.models import Q
from django.db.utils import DatabaseError
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.utils.encoding import force_unicode 
from django.utils.functional import lazy


#~ from lino import reports
from lino import dd
#~ from lino import layouts
#~ from lino.utils import printable
from lino import mixins
#~ from lino import actions
#~ from lino import fields
from lino.modlib.contacts import models as contacts
from lino.modlib.notes import models as notes
#~ from lino.modlib.links import models as links
from lino.modlib.uploads import models as uploads
from lino.modlib.cal import models as cal
#~ from lino.modlib.users import models as users
from lino.utils.choicelists import HowWell, Gender
from lino.utils.choicelists import ChoiceList
#~ from lino.modlib.properties.utils import KnowledgeField #, StrengthField
#~ from lino.modlib.uploads.models import UploadsByPerson
from lino.models import get_site_config
from lino.tools import get_field
from lino.tools import resolve_field
from lino.tools import range_filter
from lino.utils import babel 
from lino.core import actions
from lino.utils.choosers import chooser
from lino.utils import mti
from lino.mixins.printable import DirectPrintAction, Printable
#~ from lino.mixins.reminder import ReminderEntry
from lino.tools import obj2str

from lino.modlib.countries.models import CountryCity
from lino.modlib.properties import models as properties
#~ from lino.modlib.cal.models import DurationUnit, update_reminder
from lino.modlib.households import models as households
#~ from lino.modlib.contacts.models import Contact
#~ from lino.tools import resolve_model, UnresolvedModel


MAX_SUB_BUDGETS = 3


class AccountType(ChoiceList):
    u"""
    Lino has a hard-coded list of the five 
    basic "account types" or "top-level accounts".
    
    Note that the Belgian and French PCMN has 7+1 top-level accounts:
    
    |CLASSE 0 : Droits & engagements hors bilan
    |CLASSE 1 : Fonds propres, provisions pour risques & charges et Dettes à plus d'un an
    |CLASSE 2 : Frais d'établissement, actifs immobilisés et créances à plus d'un an
    |CLASSE 3 : Stock & commandes en cours d'exécution
    |CLASSE 4 : Créances et dettes à un an au plus
    |CLASSE 5 : Placements de trésorerie et valeurs disponibles
    |CLASSE 6 : Charges
    |CLASSE 7 : Produits
    
    TODO: explain the differences and understand how to solve this.
    See also 
    
    - http://code.gnucash.org/docs/help/acct-types.html
    - http://www.futureaccountant.com/accounting-process/study-notes/financial-accounting-account-types.php
    
    Provisions pour risques et charges : Gesetzliche Rücklagen.
    Créances et dettes : Kredite, Anleihen, Schulden.
    
    - "Assets = Liabilities + Capital"
    - "Passif = Actif"
    - A liability is capital acquired from others 
    - Passiva is synonym for "Liabilities + Capital" in this context


    """

    label = _("Account Type")
    
add = AccountType.add_item
add('A', _("Assets"),alias="asset")   # Aktiva, Anleihe, Vermögen, Anlage
add('L', _("Liabilities"),alias="liability") # Guthaben, Schulden, Verbindlichkeit
add('C', _("Capital"),alias="capital")  # Kapital owner's Equities
add('I', _("Incomes"),alias="income") # Gain/Revenue     Einnahmen  Produits
add('E', _("Expenses"),alias="expense") # Loss/Cost       Ausgaben   Charges



class PeriodsField(models.DecimalField):
    """
    Used for `Entry.periods` and `Account.periods`. 
    Where the latter is simply the default value for the former.
    It means: for how many months the entered amount counts.
    Default value is 1. For yearly amounts set it to 12.
    """
    def __init__(self, *args, **kwargs):
        defaults = dict(
            default=1,
            max_length=5,
            max_digits=5,
            decimal_places=0,
            )
        defaults.update(kwargs)
        super(PeriodsField, self).__init__(*args, **defaults)



class Budget(mixins.AutoUser,mixins.CachedPrintable):
    """
    Deserves more documentation.
    """
    
    #~ _lino_preferred_width = 30
    
    class Meta:
        verbose_name = _("Budget")
        verbose_name_plural = _("Budgets")
        
    #~ allow_cascaded_delete = True
    
    date = models.DateField(_("Date"),blank=True,default=datetime.date.today)
    partner = models.ForeignKey('contacts.Partner',blank=True,null=True)
    closed = models.BooleanField(verbose_name=_("Closed"))
    intro = dd.RichTextField(_("Introduction"),format="html",blank=True)
    
                
    def __unicode__(self):
        return force_unicode(_("Budget for %s") % self.partner)
        
    def get_actor(self,n):
        attname = "_actor%d_cached" % (n+1)
        if hasattr(self,attname):
            return getattr(self,attname)
        qs = self.actors.all()
        if qs.count() > n:
            a = qs[n]
            #~ a = qs[n].sub_budget.partner.get_mti_child('person','household')
        else:
            a = None
        setattr(self,attname,a)
        return a
        

                
    @property
    def actor1(self):
        return MainActor(self)
    @property
    def actor2(self):
        return self.get_actor(0)
    @property
    def actor3(self):
        return self.get_actor(1)
            
    #~ @property
    #~ def actor2(self):
        #~ qs = self.actor_set.all()
        #~ if qs.count() > 1:
            #~ return qs[1]
            
    def get_budget_pks(self):
        if not hasattr(self,'_budget_pks'):
            self._budget_pks = tuple([self.pk] + [a.sub_budget.pk for a in self.actors.filter(sub_budget__isnull=False)])
        return self._budget_pks
          
    def account_groups(self,types=None,**kw):
        """
        yield a list of all AccountGroups which have at least 
        one Entry in this Budget.
        """
        if types is not None:
            kw.update(account_type__in=[AccountType.items_dict[t] for t in types])
        #~ for t in types:
        #~ types = [AccountType.items_dict[t] for t in types]
        #~ types = [t for t in types]
        for g in AccountGroup.objects.filter(**kw).order_by('seqno'):
        #~ for g in AccountGroup.objects.filter(account_type__in=types).order_by('seqno'):
            #~ q = Account.objects.filter(group=g)
            if Entry.objects.filter(budget_id__in=self.get_budget_pks(),account__group=g).count():
            #~ if Entry.objects.filter(budget_id__in=self.get_budget_pks(),account__in=q).count():
                yield g
        
    def msum(self,fldname,types=None,**kw): 
        #~ kw.update(account__yearly=False)
        kw.update(periods=1)
        return self.sum(fldname,types,**kw)
        
    def ysum(self,fldname,types=None,**kw): 
        #~ kw.update(account__yearly=True)
        kw.update(periods=12)
        return self.sum(fldname,types,**kw)
        
    def sum(self,fldname,types=None,**kw): 
        if types is not None:
            kw.update(account_type__in=[AccountType.items_dict[t] for t in types])
        d = Entry.objects.filter(budget_id__in=self.get_budget_pks(),**kw).aggregate(models.Sum(fldname))
        v = d[fldname+'__sum']
        if v is None:
            return decimal.Decimal(0)
        return v
      
    def save(self,*args,**kw):
        super(Budget,self).save(*args,**kw)
        #~ if self.closed:
        if self.build_time:
            return
        if not self.partner:
            return
        fkw = dict()
        if self.partner.get_mti_child('household'):
            fkw.update(required_for_household=True)
        if self.partner.get_mti_child('person'):
            fkw.update(required_for_person=True)
        required = Account.objects.filter(**fkw)\
            .order_by('seqno').values_list('id',flat=True)
        missing = set(required)
        seqno = 1
        for e in Entry.objects.filter(budget=self).order_by('seqno'):
            #~ if e.item.pk in required:
            missing.discard(e.account.pk)
            seqno = max(seqno,e.seqno)
        #~ print 20120411, required, missing
        for pk in required:
            if pk in missing:
                seqno += 1
                e = Entry(account_id=pk,budget=self,seqno=seqno)
                e.full_clean()
                e.save()
                #~ print e
        if self.actors.all().count() == 0:
            try:
                hh = self.partner.household
            except households.Household.DoesNotExist:
                pass
            else:
                for m in hh.member_set.all():
                    qs = Budget.objects.filter(partner_id=m.person_id)
                    if qs.count():
                        a = Actor(budget=self,sub_budget=qs[qs.count()-1])
                        a.full_clean()
                        a.save()
            
        
      
class BudgetDetail(dd.DetailLayout):
    main = "general entries1 entries2 result"
    general = """
    date partner id user closed
    intro 
    ActorsByBudget
    """
    
    entries1 = """
    ExpensesByBudget 
    IncomesByBudget 
    """
    
    entries2 = """
    LiabilitiesByBudget 
    AssetsByBudget
    """
    
    result= """
    ExpensesSummaryByBudget IncomesSummaryByBudget 
    LiabilitiesSummaryByBudget AssetsSummaryByBudget
    """
    def setup_handle(self,h):
        h.general.label = _("General")
        h.entries1.label = _("Expenses & Income")
        h.entries2.label = _("Liabilities & Assets")
        h.result.label = _("Result")
    
class Budgets(dd.Table):
    model = Budget
    detail_layout = BudgetDetail()
    #~ master_key = 'person'
    #~ label = _("Language knowledge")
    #~ button_label = _("Languages")
    #~ column_names = "language native spoken written cef_level"

class MyBudgets(Budgets,mixins.ByUser):
    pass
    
class BudgetsByPartner(Budgets):
    master_key = 'partner'
    

class AccountGroup(mixins.Sequenced,babel.BabelNamed):
    class Meta:
        verbose_name = _("Budget Account Group")
        verbose_name_plural = _("Budget Account Groups")
        
    account_type = AccountType.field()
    help_text = dd.RichTextField(_("Introduction"),format="html",blank=True)
    
class AccountGroups(dd.Table):
    model = AccountGroup
    
class Account(mixins.Sequenced,babel.BabelNamed):
    class Meta:
        verbose_name = _("Budget Account")
        verbose_name_plural = _("Budget Accounts")
    group = models.ForeignKey(AccountGroup)
    type = AccountType.field()
    #~ account = models.ForeignKey(Account)
    required_for_household = models.BooleanField(
        _("Required for Households"),default=False)
    required_for_person = models.BooleanField(
        _("Required for Persons"),default=False)
    #~ optional = models.BooleanField(_("Optional"),default=False)
    #~ yearly = models.BooleanField(_("Yearly"),default=False)
    periods = PeriodsField(_("Periods"))
    help_text = dd.RichTextField(_("Introduction"),format="html",blank=True)
    
    #~ @chooser()
    #~ def account_choices(cls,account_type):
        #~ Account.objects.filter(type=account_type)
    
    def save(self,*args,**kw):
        if not self.type:
            self.type = self.group.account_type
        super(Account,self).save(*args,**kw)
        
    
class Accounts(dd.Table):
    model = Account
    
    

class ActorBase:
    ""
    @property
    def person(self):
        return self.partner.get_mti_child('person')
        
    @property
    def household(self):
        return self.partner.get_mti_child('household')        
        
class MainActor(ActorBase):
    "A volatile object that mimicks a 'real' Actor for actor1"
    def __init__(self,budget):
        self.budget = budget
        self.partner = budget.partner
        self.header = _("Common")
        
    
  
class Actor(mixins.Sequenced,ActorBase):
    """
    """
    class Meta:
        verbose_name = _("Budget Actor")
        verbose_name_plural = _("Budget Actors")
        
    #~ budget = models.ForeignKey(Budget,related_name="actors")
    budget = models.ForeignKey(Budget,related_name="actors")
    sub_budget = models.ForeignKey(Budget,
        verbose_name=_("Sub-Budgets"),
        related_name="used_by")
    header = models.CharField(_("Header"),max_length=20,blank=True)
    remark = dd.RichTextField(_("Remark"),format="html",blank=True)
    #~ remark = models.CharField(_("Remark"),max_length=200,blank=True)
    #~ closed = models.BooleanField(verbose_name=_("Closed"))
    
    def get_siblings(self):
        "Overrides :meth:`lino.mixins.Sequenced.get_siblings`"
        return self.__class__.objects.filter(budget=self.budget).order_by('seqno')
        
    @property
    def partner(self):
        return self.sub_budget.partner
        
    def save(self,*args,**kw):
        if not self.header:
            self.header = _("Actor") + " " + str(self.seqno)
        super(Actor,self).save(*args,**kw)
        
#~ class ActorDetail(dd.DetailLayout):
    #~ main = "general ExpensesByActor IncomesByActor DebtsByActor"
    #~ general = """
    #~ budget seqno child header
    #~ remark
    #~ """
    #~ def setup_handle(self,h):
        #~ h.general.label = _("General")
    
    
class Actors(dd.Table):
    model = Actor
    #~ detail_layout = ActorDetail()

class ActorsByBudget(Actors):
    master_key = 'budget'
    
class SequencedBudgetComponent(mixins.Sequenced):

    class Meta:
        abstract = True
        
    budget = models.ForeignKey(Budget)
    #~ actor = models.ForeignKey(Actor)
    #~ actor = models.ForeignKey(Actor,blank=True,null=True)
    
    #~ @chooser()
    #~ def actor_choices(cls,budget):
        #~ return Actor.objects.filter(budget=budget)
        
    def get_siblings(self):
        "Overrides :meth:`lino.mixins.Sequenced.get_siblings`"
        return self.__class__.objects.filter(budget=self.budget).order_by('seqno')
        


class Entry(SequencedBudgetComponent):
    class Meta:
        verbose_name = _("Budget Entry")
        verbose_name_plural = _("Budget Entries")
        #~ unique_together = ['budget','account','name']
        #~ unique_together = ['actor','account']
    
    #~ group = models.ForeignKey(AccountGroup)
    account_type = AccountType.field()
    account = models.ForeignKey(Account)
    partner = models.ForeignKey('contacts.Partner',blank=True,null=True)
    #~ name = models.CharField(_("Remark"),max_length=200,blank=True)
    #~ amount1 = dd.PriceField(_("Amount") + " 1",blank=True,null=True)
    #~ amount2 = dd.PriceField(_("Amount") + " 2",blank=True,null=True)
    #~ amount3 = dd.PriceField(_("Amount") + " 3",blank=True,null=True)
    amount = dd.PriceField(_("Amount"),default=0)
    circa = models.BooleanField(verbose_name=_("Circa"))
    todo = models.BooleanField(verbose_name=_("To Do"))
    remark = models.CharField(_("Remark"),max_length=200,blank=True)
    periods = PeriodsField(_("Periods"))
    monthly_rate = dd.PriceField(_("Monthly rate"),default=0,
    help_text="""
    The monthly_rate will be automatically added to the expenses 
    (in case of liabilities) or incomes (in case of assets).
    
    """)

    @chooser()
    def account_choices(cls,account_type):
        return Account.objects.filter(type=account_type)
        
    def save(self,*args,**kw):
        #~ if not self.name:
            #~ if self.partner:
                #~ self.name = unicode(self.partner.name)
            #~ else:
                #~ self.name = self.account.name
        self.account_type = self.account.type
        super(Entry,self).save(*args,**kw)
        
            
class Entries(dd.Table):
    model = Entry

#~ class EntriesByType(Entries):
    #~ master_key = 'account_type'
    
#~ class EntriesByGroup(Entries):
    #~ master_key = 'budget'
    

class EntriesByType(Entries):
    _account_type = None
  
    @classmethod
    def class_init(self):
        super(EntriesByType,self).class_init()
        if self._account_type is not None:
            self.label = self._account_type.text
            #~ print 20120411, unicode(self.label)
            self.known_values = dict(account_type=self._account_type)
            
class EntriesByBudget(Entries):
    master_key = 'budget'
    column_names = "account partner remark amount periods circa todo"

class ExpensesByBudget(EntriesByBudget,EntriesByType):
    _account_type = AccountType.expense
        
class IncomesByBudget(EntriesByBudget,EntriesByType):
    _account_type = AccountType.income
    
class LiabilitiesByBudget(EntriesByBudget,EntriesByType):
    _account_type = AccountType.liability
    column_names = "account partner remark amount monthly_rate circa todo"
    
class AssetsByBudget(EntriesByBudget,EntriesByType):
    _account_type = AccountType.asset
    
    

class SummaryByBudget(dd.Table):
    """
    Abstract base for 
    """
    master_key = 'budget'
    column_names = "summary_description:20 amount1 amount2 amount3 total"
  
    @classmethod
    def override_column_headers(self,ar):
        d = dict()
        d.update(amount1=ar.master_instance.actor1.header)
        d.update(amount2=ar.master_instance.actor2.header)
        d.update(amount3=ar.master_instance.actor3.header)
        return d
        
    @dd.virtualfield(dd.PriceField(_("Amount")+" 1"))
    def amount1(self,row,ar): return row.amounts[0]
        
    @dd.virtualfield(dd.PriceField(_("Amount")+" 2"))
    def amount2(self,row,ar): return row.amounts[1]
    #~ def amount2(self,entry,ar):
        #~ if entry.seqno == 2: return entry.amount
        #~ return 0
        
    @dd.virtualfield(dd.PriceField(_("Amount")+" 3"))
    def amount3(self,row,ar): return row.amounts[2]
    #~ def amount3(self,entry,ar):
        #~ if entry.seqno == 3: return entry.amount
        #~ return 0
        
    @dd.virtualfield(dd.PriceField(_("Total")))
    def total(self,row,ar):
        return sum(row.amounts)
        #~ return sum([e.amount for e in entry.budget.entry_set()])
        #~ return entry.budget.entry_set.aggregate(models.Sum('amount'))
        
    @dd.displayfield(_("Description"))
    def summary_description(self,row,ar):
        #~ chunks = [row.account]
        #~ if row.name:
        #~ if row.partner:
            #~ chunks.append(row.partner)
            #~ return "%s/%s" join_words(unicode(row.account),unicode(row.partner),row.name)
            #~ return '/'.join([unicode(x) for x in words if x])
        #~ return join_words(unicode(row.account),row.name)
        parts = [row.remark,row.partner,row.account]
        return ' / '.join([unicode(x) for x in parts if x])

  
class SummaryRow(actions.VirtualRow):
    """
    Abstract base for :class:`EntriesSummaryRow` and :class:`DebtsSummaryRow`
    """
    def __init__(self,seqno):
        self.id = seqno
        self.pk = seqno
        self.amounts = [0] * MAX_SUB_BUDGETS
        
class EntriesSummaryRow(SummaryRow):
    "Virtual Row used by :class:`EntriesSummaryByBudget`"
    def __init__(self,seqno,account,partner,remark):
        self.account = account
        self.partner = partner
        self.remark = remark
        SummaryRow.__init__(self,seqno)

class EntriesSummaryByBudget(EntriesByType,SummaryByBudget):
    """
    Summary table of Entries in this Budget and all Actors,
    using three (`MAX_SUB_BUDGETS`) columns with amounts.
    """
    
    order_by = ('account','partner', 'remark', 'seqno')
    
    @classmethod
    def get_filter_kw(self,master,**kw):
        self._cols_dict = dict()
        if master is None:
            return kw
        #~ print 20120429, master
        budget_pks = master.get_budget_pks()
        assert len(budget_pks) <= MAX_SUB_BUDGETS
        for i,pk in enumerate(budget_pks):
            self._cols_dict[pk] = i
        kw.update(budget_id__in=budget_pks)
        #~ fkw = dict(budget_id__in=budget_pks)
        return kw
        
    @classmethod
    def get_data_rows(self,ar):
        if not self._cols_dict:
            return
        #~ master = ar.master_instance
        #~ if master is None:
            #~ return
        #~ budget_pks = tuple([master.pk] + [a.sub_budget.pk for a in master.actors.filter(sub_budget__isnull=False)])
        #~ assert len(budget_pks) <= MAX_SUB_BUDGETS
        #~ cols_dict = dict()
        #~ for i,pk in enumerate(budget_pks):
            #~ cols_dict[pk] = i
        row = None
        i = 0
        #~ fkw = dict(budget_id__in=budget_pks)
        #~ if self._account_type is not None:
            #~ fkw.update(account_type=self._account_type)
        #~ for e in self.model.objects.filter(**fkw).order_by('account','seqno'):
        #~ for e in super(EntriesSummaryByBudget,self).get_request_queryset(ar):
        for e in self.get_request_queryset(ar):
            if row is not None and (
                row.account != e.account 
                    or row.partner != e.partner 
                    or row.remark != e.remark):
                yield row
                row = None
            if row is None:
                i += 1
                row = EntriesSummaryRow(i,e.account,e.partner,e.remark)
            row.amounts[self._cols_dict[e.budget.pk]] += e.amount
        if row is not None:
            yield row
    
    
class ExpensesSummaryByBudget(EntriesSummaryByBudget,EntriesByType):
    _account_type = AccountType.expense
        
class IncomesSummaryByBudget(EntriesSummaryByBudget,EntriesByType):
    _account_type = AccountType.income

class LiabilitiesSummaryByBudget(EntriesSummaryByBudget,EntriesByType):
    _account_type = AccountType.liability

class AssetsSummaryByBudget(EntriesSummaryByBudget,EntriesByType):
    _account_type = AccountType.asset



#~ class DebtType(babel.BabelNamed):
    #~ class Meta:
        #~ verbose_name = _("Debt Type")
        #~ verbose_name_plural = _("Debt Types")
        
    
#~ class DebtTypes(dd.Table):
    #~ model = DebtType
    

#~ class Debt(SequencedBudgetComponent):
    #~ class Meta:
        #~ verbose_name = _("Debt")
        #~ verbose_name_plural = _("Debts")
        
    #~ account = models.ForeignKey(Account)
    #~ # type = models.ForeignKey(DebtType)
    #~ partner = models.ForeignKey('contacts.Partner',blank=True,null=True)
    #~ name = models.CharField(_("Description"),max_length=200,blank=True)
    #~ amount = dd.PriceField(_("Remaining"),blank=True,null=True)
    #~ # remark = models.CharField(_("Remark"),max_length=200,blank=True)

    #~ def save(self,*args,**kw):
        #~ if not self.name and self.partner:
            #~ self.name = unicode(self.partner)
        #~ super(Debt,self).save(*args,**kw)
        
    #~ @chooser()
    #~ def account_choices(cls):
        #~ return Account.objects.filter(type=AccountType.asset)
  
        
        
#~ class Debts(dd.Table):
    #~ model = Debt
    
   
#~ class DebtsByBudget(Debts):
    #~ master_key = 'budget'
    #~ column_names = 'partner account name amount'
    

#~ class DebtsSummaryRow(SummaryRow):
    #~ "Virtual Row used by :class:`DebtsSummaryByBudget`"
    #~ def __init__(self,seqno,name,account):
        #~ self.name = name
        #~ self.account = account
        #~ SummaryRow.__init__(self,seqno)

#~ class DebtsSummaryByBudget(Debts,SummaryByBudget):
    #~ """
    #~ Summary table of Debts in this Budget and all Actors,
    #~ using three (`MAX_SUB_BUDGETS`) columns with amounts.
    #~ """
    
    #~ column_names = "name amount1 amount2 amount3 total"
    
    #~ @classmethod
    #~ def get_data_rows(self,ar):
        #~ master = ar.master_instance
        #~ if master is None:
            #~ return
        # print 20120429, master
        #~ budget_pks = tuple([master.pk] + [a.sub_budget.pk for a in master.actors.filter(sub_budget__isnull=False)])
        #~ assert len(budget_pks) <= MAX_SUB_BUDGETS
        #~ cols_dict = dict()
        #~ for i,pk in enumerate(budget_pks):
            #~ cols_dict[pk] = i
        #~ row = None
        #~ i = 0
        #~ fkw = dict(budget_id__in=budget_pks)
        #~ # if self._account_type is not None:
            #~ # fkw.update(account_type=self._account_type)
        #~ for d in self.model.objects.filter(**fkw).order_by('seqno'):
            #~ if row is not None and (row.name != d.name or row.account != d.account):
                #~ yield row
                #~ row = None
            #~ if row is None:
                #~ i += 1
                #~ row = DebtsSummaryRow(i,d.name,d.account)
            #~ row.amounts[cols_dict[d.budget.pk]] += d.amount
        #~ if row is not None:
            #~ yield row
    



if settings.LINO.user_model:
  
    USER_MODEL = dd.resolve_model(settings.LINO.user_model)

    dd.inject_field(USER_MODEL,
        'is_debts',
        models.BooleanField(
            verbose_name=_("is Debts user")
        ),"""Whether this user is responsible for Debts Mediation.
        """)


def site_setup(site):
    site.modules.contacts.Partners.add_detail_tab('debts.BudgetsByPartner')
    site.modules.contacts.AllPersons.add_detail_tab('debts.BudgetsByPartner')
    site.modules.households.Households.add_detail_tab('debts.BudgetsByPartner')

def setup_main_menu(site,ui,user,m):  pass
  
def setup_master_menu(site,ui,user,m): pass

def setup_my_menu(site,ui,user,m): 
    m  = m.add_menu("debts",_("Debts"))
    m.add_action(MyBudgets)
  
def setup_config_menu(site,ui,user,m): 
    m  = m.add_menu("debts",_("Debts"))
    #~ m.add_action(Accounts)
    m.add_action(AccountGroups)
    #~ m.add_action(DebtTypes)
    m.add_action(Accounts)
  
def setup_explorer_menu(site,ui,user,m):
    m  = m.add_menu("debts",_("Debts"))
    m.add_action(Budgets)
    m.add_action(Entries)
    #~ m.add_action(Debts)
