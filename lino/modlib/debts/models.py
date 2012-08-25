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
from lino.utils.choicelists import HowWell, Gender
#~ from lino.core.perms import UserLevels
from lino.utils.choicelists import ChoiceList
#~ from lino.modlib.properties.utils import KnowledgeField #, StrengthField
#~ from lino.modlib.uploads.models import UploadsByPerson
from lino.core.modeltools import get_field
from lino.core.modeltools import resolve_field
from lino.core.modeltools import range_filter
from lino.utils import babel 
from lino.core import actions
from lino.utils.choosers import chooser
from lino.utils import mti
from lino.mixins.printable import DirectPrintAction, Printable
#~ from lino.mixins.reminder import ReminderEntry
from lino.core.modeltools import obj2str

from lino.modlib.countries.models import CountryCity
from lino.modlib.properties import models as properties
#~ from lino.modlib.households import models as households
from lino.modlib.accounts.utils import AccountTypes
#~ from lino.modlib.contacts.models import Contact
#~ from lino.core.modeltools import resolve_model, UnresolvedModel

accounts = dd.resolve_app('accounts')
households = dd.resolve_app('households')
properties = dd.resolve_app('properties')

from lino.mixins.printable import decfmt

MAX_SUB_BUDGETS = 3


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
        #~ if user.debts_level < UserLevels.user:
            #~ return False
        #~ return super(DebtsUserTable,self).get_permission(action,user,obj)
        




class Budget(mixins.AutoUser,mixins.CachedPrintable,mixins.Duplicable):
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
    print_todos = models.BooleanField(
        verbose_name=_("Print to-do list"),
        help_text=u"""\
Einträge im Feld "To-do" werden nur ausgedruckt, 
wenn die Option "To-dos drucken" des Budgets angekreuzt ist. 
Diese Option wird aber momentan noch ignoriert 
(d.h. To-do-Liste wird gar nicht ausgedruckt), 
weil wir noch überlegen müssen, *wie* sie ausgedruckt werden sollen. 
Vielleicht mit Fußnoten?
""")
    intro = dd.RichTextField(_("Introduction"),format="html",blank=True)
    conclusion = dd.RichTextField(_("Conclusion"),format="html",blank=True)
    dist_amount = dd.PriceField(_("Disposable amount"),default=120,help_text=_("""\
The monthly amount available for distribution among debtors."""))
    
    #~ def duplicated_fields(self):
        #~ return dd.fields_list('partner print_todo intro conclusion dist_amount')
        
    #~ duplicated_fields = """partner print_todos intro 
    #~ conclusion dist_amount actor_set entry_set"""
                
    def __unicode__(self):
        if self.pk is None:
            return unicode(_("New"))+' '+unicode(self._meta.verbose_name)
        return force_unicode(
            _("Budget %(pk)d for %(partner)s") 
                % dict(pk=self.pk,partner=self.partner))
        
    def get_actors(self):
        attname = "_cached_actors"
        if hasattr(self,attname):
            return getattr(self,attname)
        l = list(self.actor_set.all())
        if len(l) > 0:
            main_header = _("Common")
        else:
            main_header = _("Betrag")
        l.insert(0,MainActor(self,main_header))
        setattr(self,attname,l)
        return l
        
    def get_actor_index(self,actor):
        for i,a in enumerate(self.get_actors()):
            if actor == a:
                return i 
        raise Exception("No actor '%s' in %s" % (actor,self))
        
    def get_actor(self,n):
        l = self.get_actors()
        if len(l) > n:
            return l[n]
        else:
            return None
        

    @property
    def actor1(self):
        return self.get_actor(0)
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
            kw.update(account_type__in=[AccountTypes.items_dict[t] for t in types])
        #~ for t in types:
        #~ types = [AccountTypes.items_dict[t] for t in types]
        #~ types = [t for t in types]
        for g in AccountGroup.objects.filter(**kw).order_by('seqno'):
            if Entry.objects.filter(budget=self,account__group=g).count():
                yield g
        
    def entries_by_group(self,ar,group,**kw):
        """
        Return a TableRequest showing the Entries for the given `group`, 
        using the table layout depending on AccountType.
        Shows all Entries of the specified `AccountGroup`.
        """
        t = entries_table_for_group(group)
        sar = ar.spawn(t,master_instance=self,
            title=unicode(group),
            filter=models.Q(account__group=group),**kw)
        #~ print 20120606, sar
        return sar
        
    #~ def msum(self,fldname,types=None,**kw): 
        #~ # kw.update(account__yearly=False)
        #~ kw.update(periods=1)
        #~ return self.sum(fldname,types,**kw)
        
    #~ def ysum(self,fldname,types=None,**kw): 
        #~ # kw.update(account__yearly=True)
        #~ kw.update(periods=12)
        #~ return self.sum(fldname,types,**kw)
        
    def sum(self,fldname,types=None,*args,**kw): 
        """
        Compute and return the sum of `fldname` (either ``amount`` or `monthly_rate`
        """
        fldnames = [fldname]
        if types is not None:
            kw.update(account_type__in=[AccountTypes.items_dict[t] for t in types])
        #~ d = Entry.objects.filter(budget=self,**kw).aggregate(models.Sum(*fldnames))
        sa = [models.Sum(n) for n in fldnames]
        rv = decimal.Decimal(0)
        #~ for e in Entry.objects.filter(budget=self,**kw).annotate(*sa):
        kw.update(budget=self)
        for e in Entry.objects.filter(*args,**kw).annotate(models.Sum(fldname)):
            amount = decimal.Decimal(0)
            for n in fldnames:
                amount += getattr(e,n+'__sum',0)
            #~ if e.periods is not None:
            if e.periods != 1:
                amount = amount / decimal.Decimal(e.periods)
            rv += amount
        return rv
      
    #~ @dd.displayfield(_("Summary"))
    #~ def summary(self,rr):
        #~ return 'Not <b>yet</b> written.'
      
    #~ def full_clean(self,*args,**kw):
        #~ super(Budget,self).full_clean(*args,**kw)
        
    #~ def save(self,*args,**kw):
        #~ super(Budget,self).save(*args,**kw)
        
    #~ def _changed(self,ar):
    def after_ui_save(self,ar,**kw):
        """
        Called from `extjs3.ext_ui.ExtUI.form2obj_and_save`
        after successful save()
        """
        self.fill_defaults(ar)
        return kw
        
    def fill_defaults(self,ar):
        #~ if self.closed:
        if not self.partner or self.build_time:
            return
        if self.entry_set.all().count() > 0:
            return
        self.save()
        flt = models.Q(required_for_household=True)
        flt = flt | models.Q(required_for_person=True)
        required = accounts.Account.objects.filter(flt)\
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
                e.periods = e.account.periods
                e.full_clean()
                e.save()
                #~ print e
        if self.actor_set.all().count() == 0:
            household = self.partner.get_mti_child('household')
            if household:
                mr = False
                mrs = False
                for m in household.member_set.all():
                    #~ if m.role and m.role.header:
                        #~ header = m.role.header
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
            
    def BudgetSummary(self,ar):
        return ar.spawn(BudgetSummary,master_instance=self)
        
    def DistByBudget(self,ar):
        return ar.spawn(DistByBudget,master_instance=self)
        
    #~ @dd.action(_("Duplicate"))
    #~ def duplicate_row(self,ar):
        #~ dup = mixins.duplicate_row(self)
        #~ kw = dict()
        #~ kw.update(refresh=True)
        #~ kw.update(message="Duplicated %s to %s." % (self,dup))
        #~ return ar.ui.success_response(**kw)
        
    @dd.virtualfield(dd.HtmlBox(_("Preview")))
    def preview(self,ar):
        html = ''
        def render(sar):
            html = '<h2>%s</h2>' % cgi.escape(unicode(sar.get_title()))
            html += ar.ui.table2xhtml(sar)
            return html
        for grp in self.account_groups():
            html += render(self.entries_by_group(ar,grp))
        html += render(self.BudgetSummary(ar))
        html += render(self.DistByBudget(ar))
        return html
        
      
class BudgetDetail(dd.FormLayout):
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
    main = "general entries1 entries2 summary_tab preview"
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
    
    
    summary_tab = """
    BudgetSummary:30x5 summary1
    DistByBudget
    """
    summary1 = """
    conclusion:30x5 
    dist_amount build_time
    print_todos 
    """
    
    #~ ExpensesSummaryByBudget IncomesSummaryByBudget 
    #~ LiabilitiesSummaryByBudget AssetsSummaryByBudget
    
    def setup_handle(self,h):
        h.general.label = _("General")
        h.entries1.label = _("Expenses & Income")
        h.entries2.label = _("Liabilities & Assets")
        h.summary_tab.label = pgettext_lazy(u"debts",u"Summary")
        #~ h.tmp_tab.label = _("Preview")
        
    
  
class Budgets(dd.Table):
    """
    Base class for lists of :class:`Budgets <Budget>`.
    Serves as base for :class:`MyBudgets` and :class:`BudgetsByPartner`,
    but is directly used by :menuselection:`Explorer --> Debts -->Budgets`.
    """
    model = Budget
    required = dict(user_groups = ['debts'])
    #~ required_user_groups = ['debts']
    detail_layout = BudgetDetail()
    insert_layout = dd.FormLayout("""
    partner 
    date user 
    """,
    window_size=(50,'auto'))
    
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
    def __init__(self,budget,header):
        self.budget = budget
        self.partner = budget.partner
        self.header = header
        self.remark = ''
        
    
class SequencedBudgetComponent(mixins.Sequenced):

    class Meta:
        abstract = True
        
    budget = models.ForeignKey(Budget)
        
    def get_siblings(self):
        "Overrides :meth:`lino.mixins.Sequenced.get_siblings`"
        return self.__class__.objects.filter(budget=self.budget).order_by('seqno')
        
    def get_row_permission(self,user,state,action):
        if not self.budget.get_row_permission(user,state,action):
            return False
        return super(SequencedBudgetComponent,self).get_row_permission(user,state,action)
  
#~ class Actor(ActorBase,mixins.Sequenced):
class Actor(ActorBase,SequencedBudgetComponent):
    """
    """
    class Meta:
        verbose_name = _("Budget Actor")
        verbose_name_plural = _("Budget Actors")
        
    allow_cascaded_delete = True
        
    #~ budget = models.ForeignKey(Budget,related_name="actors")
    #~ budget = models.ForeignKey(Budget)
    partner = models.ForeignKey('contacts.Partner',blank=True)
    #~ sub_budget = models.ForeignKey(Budget,
        #~ verbose_name=_("Linked Budget"),
        #~ related_name="used_by")
    header = models.CharField(_("Header"),max_length=20,blank=True)
    remark = dd.RichTextField(_("Remark"),format="html",blank=True)
    #~ remark = models.CharField(_("Remark"),max_length=200,blank=True)
    #~ closed = models.BooleanField(verbose_name=_("Closed"))
    
      
    #~ def get_siblings(self):
        #~ "Overrides :meth:`lino.mixins.Sequenced.get_siblings`"
        #~ return self.__class__.objects.filter(budget=self.budget).order_by('seqno')
        
    #~ @property
    #~ def partner(self):
        #~ return self.partner
        
        
    def save(self,*args,**kw):
        if not self.header:
            self.header = _("Actor") + " " + str(self.seqno)
        super(Actor,self).save(*args,**kw)
        
    
class Actors(dd.Table):
    required = dict(user_groups = ['debts'])
    #~ required_user_groups = ['debts']
    model = Actor
    column_names = "budget seqno partner header remark *"

class ActorsByBudget(Actors):
    master_key = 'budget'
    column_names = "seqno partner header remark *"
    


class Entry(SequencedBudgetComponent):
    """
    """
    class Meta:
        verbose_name = _("Budget Entry")
        verbose_name_plural = _("Budget Entries")
        #~ unique_together = ['budget','account','name']
        #~ unique_together = ['actor','account']
        
    allow_cascaded_delete = True
    
    #~ group = models.ForeignKey(AccountGroup)
    account_type = AccountTypes.field()
    account = models.ForeignKey(accounts.Account)
    partner = models.ForeignKey('contacts.Partner',blank=True,null=True)
    #~ name = models.CharField(_("Remark"),max_length=200,blank=True)
    amount = dd.PriceField(_("Amount"),default=0)
    actor = models.ForeignKey(Actor,
        blank=True,null=True,
        help_text="""\
Hier optional einen Akteur angeben, wenn der Eintrag 
sich nicht auf den Gesamthaushalt bezieht.""")
    #~ amount = dd.PriceField(_("Amount"),default=0)
    circa = models.BooleanField(verbose_name=_("Circa"))
    distribute = models.BooleanField(
        verbose_name=_("Distribute"),
        help_text=u"""\
Ob diese Schuld in die Schuldenverteilung aufgeommen wird oder nicht."""
    )
    todo = models.CharField(verbose_name=_("To Do"),max_length=200,blank=True)
    remark = models.CharField(_("Remark"),
        max_length=200,blank=True,
        help_text=u"""\
Bemerkungen sind intern und werden nie ausgedruckt.""")
    description = models.CharField(_("Description"),
        max_length=200,blank=True,
        help_text=u"""\
Beschreibung wird automatisch mit der Kontobezeichung 
ausgefüllt. Kann man aber manuell ändern. 
Wenn man das Konto ändert, gehen manuelle Änderungen in diesem Feld verloren.
Beim Ausdruck steht in Kolonne "Beschreibung"
lediglich der Inhalt dieses Feld sowie 
(falls angegeben bei Schulden) der Partner.""")
    periods = PeriodsField(_("Periods"),
        help_text=u"""\
Gibt an, für wieviele Monate dieser Betrag sich versteht. 
Also bei monatlichen Ausgaben steht hier 1, 
bei jährlichen Ausgaben 12.""")
    monthly_rate = dd.PriceField(_("Monthly rate"),default=0,
        help_text=u"""
Eventueller Betrag monatlicher Rückzahlungen, über deren Zahlung nicht verhandelt wird. 
Wenn hier ein Betrag steht, darf "Verteilen" nicht angekreuzt sein.
    """)
    
    #~ duplicated_fields = """
    #~ account_type account partner actor distribute 
    #~ circa todo remark description periods monthly_rate
    #~ """.split()

    @chooser()
    def account_choices(cls,account_type):
        return accounts.Account.objects.filter(type=account_type)
        
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

    def full_clean(self,*args,**kw):
        if self.periods <= 0:
            raise ValidationError(_("Periods must be > 0"))
        if self.distribute and self.monthly_rate:
            raise ValidationError(
              #~ _("Cannot set both 'Distribute' and 'Monthly rate'"))
              _("Cannot set 'Distribute' when 'Monthly rate' is %r") % self.monthly_rate)
        super(Entry,self).full_clean(*args,**kw)
      
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
        
    def on_duplicate(self,ar,master):
        """
        This is called when an entry has been duplicated.
        It is needed when we are doing a "related" duplication 
        (initiated by the duplication of a Budget).
        In that case, `master` is not None but the new Budget that has been created.
        We now need to adapt the `actor` of this Entry by making it 
        an actor of the new Budget.
        
        TODO: this method relies on the fact that related Actors 
        get duplicated *before* related Entries. 
        The order of `fklist` in `_lino_ddh` 
        """
        if master is not None and self.actor and self.actor.budget != master: 
            self.actor = master.actor_set.get(seqno=self.actor.seqno)
        super(Entry,self).on_duplicate(ar,master)
            
class Entries(dd.Table):
    model = Entry
    required = dict(user_groups = ['debts'],user_level='manager')
    #~ required_user_groups = ['debts']
    #~ required_user_level = UserLevels.manager


class EntriesByType(Entries):
    _account_type = None
    #~ required_user_level = None
    required=dict(user_groups = ['debts'])
  
    @classmethod
    def class_init(self):
        super(EntriesByType,self).class_init()
        if self._account_type is not None:
            self.label = self._account_type.text
            #~ print 20120411, unicode(self.label)
            self.known_values = dict(account_type=self._account_type)
            
class EntriesByBudget(Entries):
    master_key = 'budget'
    column_names = "account description amount actor:10 periods:10 remark todo seqno"
    required=dict(user_groups = ['debts'])
    #~ required_user_level = None
    order_by = ['seqno']

        
class ExpensesByBudget(EntriesByBudget,EntriesByType):
    _account_type = AccountTypes.expense
        
class IncomesByBudget(EntriesByBudget,EntriesByType):
    _account_type = AccountTypes.income
    
class LiabilitiesByBudget(EntriesByBudget,EntriesByType):
    _account_type = AccountTypes.liability
    column_names = "account partner remark amount actor:10 distribute monthly_rate todo seqno"
    
class AssetsByBudget(EntriesByBudget,EntriesByType):
    _account_type = AccountTypes.asset
    column_names = "account remark amount actor todo seqno"


#~ class PrintEntriesByBudget(EntriesByBudget,EntriesByType):
class PrintEntriesByBudget(dd.VirtualTable):
    """
    Base class for the printable tables of entries by budget
    (:class:`PrintExpensesByBudget`,
    :class:`PrintIncomesByBudget`,
    :class:`PrintLiabilitiesByBudget` and
    :class:`PrintAssetsByBudget`).
    
    This is historically the first table that uses Lino's 
    per-request dynamic columns feature.
    """
    slave_grid_format = 'html'
    _account_type = None
    
    @classmethod
    def class_init(self):
        super(PrintEntriesByBudget,self).class_init()
        if self._account_type is not None:
            self.label = self._account_type.text
            
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
        if 'dynamic_amounts' in self.column_names:
            #~ todo
            amounts = ''
            if ar.master_instance is not None:
                actors = ar.master_instance.get_actors()
                if len(actors) == 1:
                    amounts = 'amount0'
                else:
                    for i,a in enumerate(actors):
                        amounts += 'amount'+str(i) + ' '
                    amounts += 'total '
            return self.column_names.replace('dynamic_amounts',amounts)
        return self.column_names
        
    @classmethod
    def override_column_headers(self,ar):
        d = dict()
        #~ d.update(amount0='')
        if ar.master_instance is not None:
            #~ if len(ar.master_instance.get_actors()) > 1:
            for i,a in enumerate(ar.master_instance.get_actors()):
                d['amount'+str(i)] = a.header
        return d
        
    
    class Row:
        has_data = False
        def __init__(self,e):
            self.description = e.description
            self.partner = e.partner
            self.account = e.account
            #~ self.todos = [''] * len(e.budget.get_actors())
            self.todo = ''
            self.amounts = [decimal.Decimal(0)] * len(e.budget.get_actors())
            self.total = decimal.Decimal(0)
            self.collect(e)
            
        def matches(self,e):
            if e.partner != self.partner: return False
            if e.account != self.account: return False
            if e.description != self.description: return False
            return True
              
        def collect(self,e):
            if e.actor is None:
                i = 0
            else:
                i = e.budget.get_actor_index(e.actor)
            amount = e.amount / e.periods
            if amount != 0:
                self.has_data = True
            self.amounts[i] += amount
            self.total += amount
            if self.todo:
                self.todo += ', '
            self.todo += e.todo
            return True
            
    @classmethod
    def get_data_rows(self,ar):
        """
        """
        budget = ar.master_instance
        if budget is None: 
            return
        #~ qs = self.get_request_queryset(ar)
        qs = budget.entry_set.filter(account__type=self._account_type).order_by('seqno')
        if ar.filter:
            qs = qs.filter(ar.filter)
        row = None
        for e in qs:
            if row is None:
                row = self.Row(e)
            elif row.matches(e):
                row.collect(e)
            else:
                if row.has_data: yield row
                row = self.Row(e)
        if row is not None:
            if row.has_data: yield row
                
            
        
    @dd.virtualfield(dd.PriceField(_("Total")))
    def total(self,obj,ar):
        return obj.total
        
    @dd.displayfield(_("Description"))
    def description(self,obj,ar):
        return obj.description
        
    #~ @dd.displayfield(_("Partner"))
    @dd.virtualfield(models.ForeignKey(contacts.Partner))
    def partner(self,obj,ar):
        return obj.partner
        
    # TODO: generate them dynamically:
    
    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount0(self,obj,ar):
        return obj.amounts[0]
        
    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount1(self,obj,ar):
        return obj.amounts[1]
        
    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount2(self,obj,ar):
        return obj.amounts[2]
        
    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount3(self,obj,ar):
        return obj.amounts[3]
        
    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount4(self,obj,ar):
        return obj.amounts[4]
  
  
  
class PrintExpensesByBudget(PrintEntriesByBudget):
    """
    Print version of :class:`ExpensesByBudget` table.
    """
    _account_type = AccountTypes.expense
    column_names = "description dynamic_amounts"
        
class PrintIncomesByBudget(PrintEntriesByBudget):
    """
    Print version of :class:`IncomesByBudget` table.
    """
    _account_type = AccountTypes.income
    column_names = "description dynamic_amounts"
    
class PrintLiabilitiesByBudget(PrintEntriesByBudget):
    """
    Print version of :class:`LiabilitiesByBudget` table.
    """
    _account_type = AccountTypes.liability
    #~ column_names = "partner description total monthly_rate todo"
    column_names = "partner:20 description:20 dynamic_amounts"
    
class PrintAssetsByBudget(PrintEntriesByBudget):
    """
    Print version of :class:`AssetsByBudget` table.
    """
    _account_type = AccountTypes.asset
    column_names = "description dynamic_amounts"

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
    required=dict(user_groups = ['debts'])
    #~ required_user_groups = ['debts']
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
            yield [
              (u"Monatliche Reserve für jährliche Ausgaben (%s / 12)" 
                % decfmt(ye*12,places=2)), 
              -ye]
            
        #~ ye = budget.sum('amount','E',models.Q(periods__ne=1) & models.Q(periods__ne=12))
        #~ if ye:
            #~ yield [
              #~ u"Monatliche Reserve für sonstige periodische Ausgaben", 
              #~ -ye]
            
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
    column_names = "partner description amount dist_perc dist_amount"
    filter = models.Q(distribute=True)
    label = _("Debts distribution")
    known_values = dict(account_type=AccountTypes.liability)
    
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

    @dd.virtualfield(dd.PriceField(_("Monthly payback suggested")))
    def dist_amount(self,row,ar):
        return row.dist_amount

    @classmethod
    def override_column_headers(self,ar):
        d = dict()
        d.update(partner=_("Creditor"))
        d.update(amount=_("Debt"))
        return d
    
    
    
MODULE_LABEL = _("Debts mediation")

#~ settings.LINO.add_user_field('debts_level',UserLevel.field(MODULE_LABEL))
#~ settings.LINO.add_user_group('debts',MODULE_LABEL)

def site_setup(site):
    site.modules.contacts.Partners.add_detail_tab('debts.BudgetsByPartner')
    site.modules.contacts.AllPersons.add_detail_tab('debts.BudgetsByPartner')
    site.modules.households.Households.add_detail_tab('debts.BudgetsByPartner')
    #~ site.modules.accounts.Accounts.set_required(
        #~ user_groups=['debts'],user_level='manager')


def setup_main_menu(site,ui,user,m):  pass
  
def setup_master_menu(site,ui,user,m): pass

def setup_my_menu(site,ui,user,m): 
    #~ if user.profile.debts_level < UserLevels.user: 
        #~ return
    m  = m.add_menu("debts",MODULE_LABEL)
    m.add_action(MyBudgets)
  
def setup_config_menu(site,ui,user,m): 
    pass
    #~ if user.profile.debts_level < UserLevels.manager: 
        #~ return
    #~ m  = m.add_menu("debts",MODULE_LABEL)
    #~ m.add_action(Accounts)
    #~ m.add_action(accounts.Groups)
    #~ m.add_action(DebtTypes)
    #~ m.add_action(Accounts)
  
def setup_explorer_menu(site,ui,user,m):
    #~ if user.profile.debts_level < UserLevels.manager:
        #~ return
    m  = m.add_menu("debts",MODULE_LABEL)
    m.add_action(Budgets)
    m.add_action(Entries)
    #~ m.add_action(Debts)

dd.add_user_group('debts',MODULE_LABEL)


def customize_accounts():
    dd.inject_field(accounts.Account,
        'required_for_household',
        models.BooleanField(
        _("Required for Households"),default=False)
      )
    dd.inject_field(accounts.Account,
        'required_for_person',
        models.BooleanField(
        _("Required for Persons"),default=False)
      )
    dd.inject_field(accounts.Account,
        'periods',
        PeriodsField(_("Periods"))
      )

customize_accounts()

