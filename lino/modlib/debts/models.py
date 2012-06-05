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
This package contains the **Debt Mediation** module 
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
from django.utils.translation import pgettext_lazy 
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
from lino.utils.choicelists import HowWell, Gender, UserLevel
from lino.utils.choicelists import ChoiceList
#~ from lino.modlib.properties.utils import KnowledgeField #, StrengthField
#~ from lino.modlib.uploads.models import UploadsByPerson
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
    Used for `Entry.periods` and `Account.periods`
    (which holds simply the default value for the former).
    It means: for how many months the entered amount counts.
    Default value is 1. For yearly amounts set it to 12.
    """
    def __init__(self, *args, **kwargs):
        defaults = dict(
            default=1,
            #~ max_length=3,
            max_digits=3,
            decimal_places=0,
            )
        defaults.update(kwargs)
        super(PeriodsField, self).__init__(*args, **defaults)

#~ class PeriodsField(models.IntegerField):
    #~ """
    #~ Used for `Entry.periods` and `Account.periods`
    #~ (which holds simply the default value for the former).
    #~ It means: for how many months the entered amount counts.
    #~ Default value is 1. For yearly amounts set it to 12.
    #~ """
    #~ def __init__(self, *args, **kwargs):
        #~ defaults = dict(
            #~ max_length=3,
            # max_digits=3,
            #~ blank=True,
            #~ null=True
            #~ )
        #~ defaults.update(kwargs)
        #~ super(PeriodsField, self).__init__(*args, **defaults)


#~ class DebtsUserTable(dd.Table):
    #~ """
    #~ Abstract base class for tables that are visible only to 
    #~ Debt Mediation Agents (users with a non-empty `debts_level`).
    #~ """
    #~ @classmethod
    #~ def get_permission(self,action,user,obj):
        #~ if user.debts_level < UserLevel.user:
            #~ return False
        #~ return super(DebtsUserTable,self).get_permission(action,user,obj)
        



class AccountGroup(mixins.Sequenced,babel.BabelNamed):
  
    class Meta:
        verbose_name = _("Budget Account Group")
        verbose_name_plural = _("Budget Account Groups")
        
    account_type = AccountType.field()
    #~ entries_columns = models.CharField(_("Columns in Entries tables"),max_length=200,blank=True)
    help_text = dd.RichTextField(_("Introduction"),format="html",blank=True)
    
class AccountGroups(dd.Table):
    model = AccountGroup
    required_user_groups = ['debts']
    required_user_level = UserLevel.manager
    


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
    required_user_level = UserLevel.manager
    required_user_groups = ['debts']
    


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
    #~ closed = models.BooleanField(verbose_name=_("Closed"))
    intro = dd.RichTextField(_("Introduction"),format="html",blank=True)
    conclusion = dd.RichTextField(_("Conclusion"),format="html",blank=True)
    dist_amount = dd.PriceField(_("Disposable amount"),default=100)
    
                
    def __unicode__(self):
        return force_unicode(_("Budget for %s") % self.partner)
        
    def get_actors(self):
        attname = "_cached_actors"
        if hasattr(self,attname):
            return getattr(self,attname)
        l = []
        l.append(MainActor(self))
        l += [a for a in self.actor_set.all()]
        setattr(self,attname,l)
        return l
        
    def get_actor_index(self,actor):
        for i,a in enumerate(self.get_actors()):
            if actor == a:
                return i 
        raise Exception("No actor %r in %s" % (actor,self))
        
    def get_actor(self,n):
        l = self.get_actors()
        if len(l) > n:
            return l[n]
        else:
            return None
        

    @property
    def actor1(self):
        return self.get_actor(0)
        #~ return MainActor(self)
    @property
    def actor2(self):
        return self.get_actor(1)
    @property
    def actor3(self):
        return self.get_actor(2)
        
            
    #~ @property
    #~ def actor2(self):
        #~ qs = self.actor_set.all()
        #~ if qs.count() > 1:
            #~ return qs[1]
            
    #~ def get_budget_pks(self):
        #~ if not hasattr(self,'_budget_pks'):
            #~ self._budget_pks = tuple([self.pk] + [a.sub_budget.pk for a in self.actors.filter(sub_budget__isnull=False)])
        #~ return self._budget_pks
          
    def account_groups(self,types=None,**kw):
        """
        Yield all AccountGroups which have at least one Entry in this Budget.
        """
        if types is not None:
            kw.update(account_type__in=[AccountType.items_dict[t] for t in types])
        #~ for t in types:
        #~ types = [AccountType.items_dict[t] for t in types]
        #~ types = [t for t in types]
        for g in AccountGroup.objects.filter(**kw).order_by('seqno'):
            if Entry.objects.filter(budget=self,account__group=g).count():
                yield g
        
    #~ def msum(self,fldname,types=None,**kw): 
        #~ # kw.update(account__yearly=False)
        #~ kw.update(periods=1)
        #~ return self.sum(fldname,types,**kw)
        
    #~ def ysum(self,fldname,types=None,**kw): 
        #~ # kw.update(account__yearly=True)
        #~ kw.update(periods=12)
        #~ return self.sum(fldname,types,**kw)
        
    def sum(self,fldname,types=None,**kw): 
        """
        Compute and return the sum of `fldname` (either ``amount`` or `monthly_rate`
        """
        fldnames = [fldname]
        if types is not None:
            kw.update(account_type__in=[AccountType.items_dict[t] for t in types])
        #~ d = Entry.objects.filter(budget=self,**kw).aggregate(models.Sum(*fldnames))
        sa = [models.Sum(n) for n in fldnames]
        rv = decimal.Decimal(0)
        #~ for e in Entry.objects.filter(budget=self,**kw).annotate(*sa):
        for e in Entry.objects.filter(budget=self,**kw).annotate(models.Sum(fldname)):
            amount = decimal.Decimal(0)
            for n in fldnames:
                amount += getattr(e,n+'__sum',0)
            if e.periods is not None:
                amount = amount / decimal.Decimal(e.periods)
            rv += amount
        return rv
      
    #~ @dd.displayfield(_("Summary"))
    #~ def summary(self,rr):
        #~ return 'Not <b>yet</b> written.'
      
    def save(self,*args,**kw):
        super(Budget,self).save(*args,**kw)
        #~ if self.closed:
        if self.build_time:
            return
        if not self.partner:
            return
        flt = models.Q(required_for_household=True)
        flt = flt | models.Q(required_for_person=True)
        required = Account.objects.filter(flt)\
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
        household = self.partner.get_mti_child('household')
        if household and self.actor_set.all().count() == 0:
            mr = False
            mrs = False
            for m in household.member_set.all():
                if m.person.gender == Gender.male and not mr:
                    header = unicode(_("Mr."))
                    mr = True
                elif m.person.gender == Gender.female and not mrs:
                    header = unicode(_("Mrs."))
                    mrs = True
                else:
                    header = ''
                a = Actor(budget=self,partner=m.person,header=header)
                a.full_clean()
                a.save()
            
    def entries_by_group(self,ar,group,**kw):
        """
        Return a TableRequest showing the Entries of this Budget, 
        using the table layout depending on AccountType.
        Shows all Entries of the specified `AccountGroup`.
        """
        t = entries_table_for_group(group)
        return ar.spawn(t,master_instance=self,account__group=group,**kw)
        
    def BudgetSummary(self,ar):
        return ar.spawn(BudgetSummary,master_instance=self)
        
    def DistByBudget(self,ar):
        return ar.spawn(DistByBudget,master_instance=self)
        
    @dd.action(_("Duplicate"))
    def duplicate_row(self,ar):
        dup = mixins.duplicate_row(self)
        kw = dict()
        kw.update(refresh=True)
        kw.update(message="Duplicated %s to %s." % (self,dup))
        return ar.ui.success_response(**kw)
        
      
class BudgetDetail(dd.DetailLayout):
    """
    Defines the Detail form of a :class:`Budget`.
    
    The following four screenshots were obsolete 
    already a few hours after their publication...
    
    .. image:: /screenshots/debts.Budget.Detail.1.jpg
      :scale: 50
      
    .. image:: /screenshots/debts.Budget.Detail.2.jpg
      :scale: 50

    .. image:: /screenshots/debts.Budget.Detail.3.jpg
      :scale: 50

    .. image:: /screenshots/debts.Budget.Detail.4.jpg
      :scale: 50

    
    
    """
    main = "general entries1 entries2 summary_tab tmp_tab"
    general = """
    date partner id user 
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
    
    tmp_tab = """
    PrintExpensesByBudget 
    PrintIncomesByBudget 
    """
    
    
    conclusion_panel = """
    conclusion
    dist_amount spacer
    """
    summary_tab = """
    BudgetSummary:30 conclusion_panel:30
    DistByBudget
    """
    
    #~ ExpensesSummaryByBudget IncomesSummaryByBudget 
    #~ LiabilitiesSummaryByBudget AssetsSummaryByBudget
    
    def setup_handle(self,h):
        h.general.label = _("General")
        h.entries1.label = _("Expenses & Income")
        h.entries2.label = _("Liabilities & Assets")
        h.summary_tab.label = pgettext_lazy("debts","Summary")
        h.tmp_tab.label = _("Preview")
        
    
  
class Budgets(dd.Table):
    """
    Base class for lists of :class:`Budgets <Budget>`.
    Serves as base for :class:`MyBudgets` and :class:`BudgetsByPartner`,
    but is directly used by :menuselection:`Explorer --> Debts -->Budgets`.
    """
    model = Budget
    required_user_groups = ['debts']
    detail_layout = BudgetDetail()
    
    @dd.constant()
    def spacer(self,ui):  return '<br/>'


class MyBudgets(Budgets,mixins.ByUser):
    """
    """
    pass
    
class BudgetsByPartner(Budgets):
    master_key = 'partner'
    

    

class ActorBase:
    ""
    @property
    def person(self):
        return self.partner.get_mti_child('person')
        
    @property
    def household(self):
        return self.partner.get_mti_child('household')        
        
    def __unicode__(self):
        return self.header
        
class MainActor(ActorBase):
    "A volatile object that represents the budget partner as actor"
    def __init__(self,budget):
        self.budget = budget
        self.partner = budget.partner
        self.header = _("Common")
        
    
class SequencedBudgetComponent(mixins.Sequenced):

    class Meta:
        abstract = True
        
    budget = models.ForeignKey(Budget)
        
    def get_siblings(self):
        "Overrides :meth:`lino.mixins.Sequenced.get_siblings`"
        return self.__class__.objects.filter(budget=self.budget).order_by('seqno')
        
  
class Actor(mixins.Sequenced,ActorBase):
    """
    """
    class Meta:
        verbose_name = _("Budget Actor")
        verbose_name_plural = _("Budget Actors")
        
    allow_cascaded_delete = True
        
    #~ budget = models.ForeignKey(Budget,related_name="actors")
    budget = models.ForeignKey(Budget)
    partner = models.ForeignKey('contacts.Partner',blank=True)
    #~ sub_budget = models.ForeignKey(Budget,
        #~ verbose_name=_("Linked Budget"),
        #~ related_name="used_by")
    header = models.CharField(_("Header"),max_length=20,blank=True)
    remark = dd.RichTextField(_("Remark"),format="html",blank=True)
    #~ remark = models.CharField(_("Remark"),max_length=200,blank=True)
    #~ closed = models.BooleanField(verbose_name=_("Closed"))
    
    def get_siblings(self):
        "Overrides :meth:`lino.mixins.Sequenced.get_siblings`"
        return self.__class__.objects.filter(budget=self.budget).order_by('seqno')
        
    #~ @property
    #~ def partner(self):
        #~ return self.partner
        
        
    def save(self,*args,**kw):
        if not self.header:
            self.header = _("Actor") + " " + str(self.seqno)
        super(Actor,self).save(*args,**kw)
        
    
class Actors(dd.Table):
    required_user_groups = ['debts']
    model = Actor
    column_names = "budget seqno partner header remark *"

class ActorsByBudget(Actors):
    master_key = 'budget'
    column_names = "seqno partner header remark *"
    


class Entry(SequencedBudgetComponent):
    class Meta:
        verbose_name = _("Budget Entry")
        verbose_name_plural = _("Budget Entries")
        #~ unique_together = ['budget','account','name']
        #~ unique_together = ['actor','account']
        
    allow_cascaded_delete = True
    
    #~ group = models.ForeignKey(AccountGroup)
    account_type = AccountType.field()
    account = models.ForeignKey(Account)
    partner = models.ForeignKey('contacts.Partner',blank=True,null=True)
    #~ name = models.CharField(_("Remark"),max_length=200,blank=True)
    amount = dd.PriceField(_("Amount"),default=0)
    actor = models.ForeignKey(Actor,blank=True,null=True)
    #~ amount = dd.PriceField(_("Amount"),default=0)
    circa = models.BooleanField(verbose_name=_("Circa"))
    dist = models.BooleanField(verbose_name=_("Distribute"))
    todo = models.CharField(verbose_name=_("To Do"),max_length=200,blank=True)
    remark = models.CharField(_("Remark"),max_length=200,blank=True)
    description = models.CharField(_("Description"),max_length=200,blank=True)
    periods = PeriodsField(_("Periods"))
    monthly_rate = dd.PriceField(_("Monthly rate"),default=0,
    help_text="""
    The monthly_rate will be automatically added to the expenses 
    (in case of liabilities) or incomes (in case of assets).
    
    """)

    @chooser()
    def account_choices(cls,account_type):
        return Account.objects.filter(type=account_type)
        
    @chooser()
    def actor_choices(cls,budget):
        return Actor.objects.filter(budget=budget).order_by('seqno')
        
    @dd.displayfield(_("Description"))
    def summary_description(row,ar):
        #~ chunks = [row.account]
        if row.description:
            desc = row.description
        #~ if row.partner:
            #~ chunks.append(row.partner)
            #~ return "%s/%s" join_words(unicode(row.account),unicode(row.partner),row.name)
            #~ return '/'.join([unicode(x) for x in words if x])
        #~ return join_words(unicode(row.account),row.name)
        else:
            #~ parts = [row.remark,row.partner,row.account]
            parts = [row.account,row.partner]
            desc = ' / '.join([unicode(x) for x in parts if x])
        if row.todo:
            desc += " [%s]" % row.todo
        return desc
          
          
    def account_changed(self,ar):
        if self.account_id:
            self.periods = self.account.periods
            self.description = unicode(self.account)

    def save(self,*args,**kw):
        #~ if not self.name:
            #~ if self.partner:
                #~ self.name = unicode(self.partner.name)
            #~ else:
                #~ self.name = self.account.name
        self.account_type = self.account.type
        if not self.description:
            self.description = unicode(self.account)
        #~ if self.periods is None:
            #~ self.periods = self.account.periods
        super(Entry,self).save(*args,**kw)
        
            
class Entries(dd.Table):
    model = Entry
    required_user_groups = ['debts']
    required_user_level = UserLevel.manager


class EntriesByType(Entries):
    _account_type = None
    required_user_level = None
  
    @classmethod
    def class_init(self):
        super(EntriesByType,self).class_init()
        if self._account_type is not None:
            self.label = self._account_type.text
            #~ print 20120411, unicode(self.label)
            self.known_values = dict(account_type=self._account_type)
            
class EntriesByBudget(Entries):
    master_key = 'budget'
    column_names = "account description amount actor periods remark todo seqno"
    required_user_level = None
    order_by = ['seqno']

        
class ExpensesByBudget(EntriesByBudget,EntriesByType):
    _account_type = AccountType.expense
        
class IncomesByBudget(EntriesByBudget,EntriesByType):
    _account_type = AccountType.income
    
class LiabilitiesByBudget(EntriesByBudget,EntriesByType):
    _account_type = AccountType.liability
    column_names = "account partner remark amount actor monthly_rate dist todo seqno"
    
class AssetsByBudget(EntriesByBudget,EntriesByType):
    _account_type = AccountType.asset
    column_names = "account remark amount actor monthly_rate todo seqno"



class PrintEntriesByBudget(EntriesByBudget,EntriesByType):
  
    slave_grid_format = 'html'
    
    @classmethod
    def get_handle_name(self,ar):
        hname = ar.ui._handle_attr_name
        #~ hname = super(PrintEntriesByBudget,self).get_handle_name(ar)
        hname += str(len(ar.master_instance.get_actors()))
        return hname
        
    @classmethod
    def get_column_names(self,ar):
        """
        Builds columns dynamically by request. Called once per UI handle.
        """
        if 'amounts ' in self.column_names:
            #~ todo
            amounts = ''
            if ar.master_instance is not None:
                for i,a in enumerate(ar.master_instance.get_actors()):
                    amounts += 'amount'+str(i) + ' '
            return self.column_names.replace('amounts ',amounts)
        return self.column_names
        
    @classmethod
    def override_column_headers(self,ar):
        d = dict()
        #~ d.update(amount0='')
        if ar.master_instance is not None:
            for i,a in enumerate(ar.master_instance.get_actors()):
                d['amount'+str(i)] = a.header
        return d
        
    
    @classmethod
    def come_together(self,budget,row,prev):
        if prev is not None:
            if row.description == prev.description:
                if row.account == prev.account:
                    return prev
        for i,a in enumerate(budget.get_actors()):
            setattr(row,'amount'+str(i),decimal.Decimal(0))
        row.total = decimal.Decimal(0)
        return row
        
    @classmethod
    def get_data_rows(self,ar):
        """
        """
        budget = ar.master_instance
        if budget is None: 
            return
        qs = self.get_request_queryset(ar)
        current = None
        for row in qs:
            current = self.come_together(budget,row,current)
            if row.actor is None:
                name = 'amount0'
            else:
                name = 'amount' + str(budget.get_actor_index(row.actor))
            am = getattr(current,name)
            setattr(current,name,am+row.amount)
            current.total += row.amount
            if current is not row:
                yield current
            
        
    @dd.virtualfield(dd.PriceField(_("Amount")))
    def total(self,obj,ar):
        return obj.total
        
    # TODO: generate them dynamically:
    
    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount0(self,obj,ar):
        return obj.amount0
        
    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount1(self,obj,ar):
        return obj.amount1
        
    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount2(self,obj,ar):
        return obj.amount2
        
    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount3(self,obj,ar):
        return obj.amount3
        
    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount4(self,obj,ar):
        return obj.amount4
        
        
  
  
  
class PrintExpensesByBudget(PrintEntriesByBudget):
    _account_type = AccountType.expense
    column_names = "summary_description amounts total"
        
class PrintIncomesByBudget(PrintEntriesByBudget):
    _account_type = AccountType.income
    column_names = "summary_description amounts total"
    
class PrintLiabilitiesByBudget(PrintEntriesByBudget):
    _account_type = AccountType.liability
    column_names = "partner remark total monthly_rate todo"
    
class PrintAssetsByBudget(PrintEntriesByBudget):
    _account_type = AccountType.asset
    column_names = "summary_description total monthly_rate"

ENTRIES_BY_TYPE_TABLES = (
  PrintExpensesByBudget,
  PrintIncomesByBudget,
  PrintLiabilitiesByBudget,
  PrintAssetsByBudget)

def entries_table_for_group(group):
    for t in ENTRIES_BY_TYPE_TABLES:
        if t._account_type == group.account_type: return t
  
    


    
    
#~ class EntriesSummaryByBudget(EntriesByBudget,EntriesByType):
    #~ """
    #~ """
    #~ order_by = ('account','partner', 'remark', 'seqno')
    #~ column_names = "summary_description amount1 amount2 amount3 total"
    
    
    
class BudgetSummary(dd.VirtualTable):
    """
    A virtual table showing a list of summary numbers for this budget.
    """
    required_user_groups = ['debts']
    master = Budget
    column_names = "desc amount"
    label = _("Overview")
    
    @classmethod
    def get_data_rows(self,ar):
        budget = ar.master_instance
        if budget is None: 
            return
        yield [u"Monatliche Einkünfte", budget.sum('amount','I',periods=1)]
        yield [u"Monatliche Ausgaben", -budget.sum('amount','E',periods=1)]
        ye = budget.sum('amount','E',periods=12)
        if ye:
            yield [(u"Monatliche Reserve für jährliche Ausgaben (%s / 12)" % ye), -ye/12]
            
        yield [u"Raten der laufenden Kredite", -budget.sum('monthly_rate','L')]
        #~ yield [u"Total Kredite / Schulden", budget.sum('amount','L')]
        #~ u"Restbetrag für Kredite und Zahlungsrückstände"
    
    @dd.displayfield(_("Description"))
    def desc(self,row,ar):
        return row[0]
        
    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount(self,row,ar):
        return row[1]
        

    
#~ class DistByBudget(LiabilitiesByBudget):
class DistByBudget(EntriesByBudget):
    u"""
    Répartition au marc-le-franc.
    A table that distributes the monthly available amount
    proportionally among the debtors.
    
    """
    #~ master = Budget
    #~ model = Entry
    column_names = "summary_description amount dist_perc dist_amount"
    filter = models.Q(dist=True)
    label = _("Debts distribution")
    known_values = dict(account_type=AccountType.liability)
    
    @classmethod
    def get_data_rows(self,ar):
        budget = ar.master_instance
        if budget is None: 
            return
        qs = self.get_request_queryset(ar)
        #~ fldnames = ['amount1','amount2','amount3']
        #~ sa = [models.Sum(n) for n in fldnames]
        total = decimal.Decimal(0)
        
        entries = []
        for e in qs.annotate(models.Sum('amount')):
            #~ assert e.periods is None
            total += e.amount__sum
            entries.append(e)
            
        for e in entries:
            e.dist_perc = 100 * e.amount / total
            #~ if e.dist_perc == 0:
                #~ e.dist_amount = decimal.Decimal(0)
            #~ else:
            e.dist_amount = budget.dist_amount * e.dist_perc / 100
            yield e
            

    @dd.virtualfield(dd.PriceField(_("%")))
    def dist_perc(self,row,ar):
        return row.dist_perc

    @dd.virtualfield(dd.PriceField(_("Amount")))
    def dist_amount(self,row,ar):
        return row.dist_amount

    
    
#~ class ExpensesSummaryByBudget(EntriesSummaryByBudget,EntriesByType):
    #~ _account_type = AccountType.expense
        
#~ class IncomesSummaryByBudget(EntriesSummaryByBudget,EntriesByType):
    #~ _account_type = AccountType.income

#~ class LiabilitiesSummaryByBudget(EntriesSummaryByBudget,EntriesByType):
    #~ _account_type = AccountType.liability

#~ class AssetsSummaryByBudget(EntriesSummaryByBudget,EntriesByType):
    #~ _account_type = AccountType.asset

    
MODULE_NAME = _("Debts mediation")

settings.LINO.add_user_field('debts_level',UserLevel.field(MODULE_NAME))

def site_setup(site):
    site.modules.contacts.Partners.add_detail_tab('debts.BudgetsByPartner')
    site.modules.contacts.AllPersons.add_detail_tab('debts.BudgetsByPartner')
    site.modules.households.Households.add_detail_tab('debts.BudgetsByPartner')

def setup_main_menu(site,ui,user,m):  pass
  
def setup_master_menu(site,ui,user,m): pass

def setup_my_menu(site,ui,user,m): 
    if user.debts_level < UserLevel.user: 
        return
    m  = m.add_menu("debts",MODULE_NAME)
    m.add_action(MyBudgets)
  
def setup_config_menu(site,ui,user,m): 
    if user.debts_level < UserLevel.manager: 
        return
    m  = m.add_menu("debts",MODULE_NAME)
    #~ m.add_action(Accounts)
    m.add_action(AccountGroups)
    #~ m.add_action(DebtTypes)
    m.add_action(Accounts)
  
def setup_explorer_menu(site,ui,user,m):
    if user.debts_level < UserLevel.expert:
        return
    m  = m.add_menu("debts",MODULE_NAME)
    m.add_action(Budgets)
    m.add_action(Entries)
    #~ m.add_action(Debts)
