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

u"""
Debt mediation
--------------

médiation de dettes / Schuldnerberatung

"""

import logging
logger = logging.getLogger(__name__)

import os
import cgi
import datetime

from lxml import etree


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
#~ from lino.utils.babel import add_babel_field, DEFAULT_LANGUAGE, babelattr, babeldict_getitem
from lino.utils import babel 
from lino.utils.choosers import chooser
from lino.utils import mti
from lino.mixins.printable import DirectPrintAction, Printable
#~ from lino.mixins.reminder import ReminderEntry
from lino.tools import obj2str

from lino.modlib.countries.models import CountryCity
from lino.modlib.properties import models as properties
#~ from lino.modlib.cal.models import DurationUnit, update_reminder
from lino.modlib.families import models as families
#~ from lino.modlib.contacts.models import Contact
#~ from lino.tools import resolve_model, UnresolvedModel


class AccountType(ChoiceList):
    u"""
    PCMN belge:
    CLASSE 0 : Droits & engagements hors bilan
    CLASSE 1 : Fonds propres, provisions pour risques & charges et Dettes à plus d'un an
    CLASSE 2 : Frais d'établissement, actifs immobilisés et créances à plus d'un an
    CLASSE 3 : Stock & commandes en cours d'exécution
    CLASSE 4 : Créances et dettes à un an au plus
    CLASSE 5 : Placements de trésorerie et valeurs disponibles
    CLASSE 6 : Charges
    CLASSE 7 : Produits
    
    Provisions pour risques et charges : Gesetzliche Rücklagen
    
    Créances et dettes : Kredite, Anleihen, Schulden

    """

    label = _("Account Type")
    
add = AccountType.add_item
add('I', _("Income"),alias="income") # Gain/Revenue     Einnahmen  Produits
add('E', _("Expense"),alias="expense") # Loss/Cost       Ausgaben   Charges
add('A', _("Asset"),alias="asset")   # Aktiva, Anleihe
add('C', _("Capital"),alias="capital")  # owner's equity
add('L', _("Liability"),alias="liability") # capital acquired from others Guthaben, Schulden, Verbindlichkeit


#~ class Account(babel.BabelNamed):
    #~ """
    #~ Deserves more documentation.
    #~ """
    #~ class Meta:
        #~ verbose_name = _("Budget Account")
        #~ verbose_name_plural = _("Budget Accounts")
        
    #~ type = AccountType.field()
    
#~ class Accounts(dd.Table):
    #~ model = Account

class Budget(mixins.AutoUser,mixins.CachedPrintable):
    """
    Deserves more documentation.
    """
    class Meta:
        verbose_name = _("Budget")
        verbose_name_plural = _("Budgets")
        
    #~ allow_cascaded_delete = True
    
    date = models.DateField(_("Date"),blank=True,default=datetime.date.today)
    partner = models.ForeignKey('contacts.Partner')
    closed = models.BooleanField(verbose_name=_("Closed"))
    intro = dd.RichTextField(_("Introduction"),format="html",blank=True)
    
    def save(self,*args,**kw):
        super(Budget,self).save(*args,**kw)
        required = Item.objects.filter(optional=False).order_by('seqno').values_list('id',flat=True)
        missing = set(required)
        seqno = 1
        for e in Entry.objects.filter(budget=self).order_by('seqno'):
            #~ if e.item.pk in required:
            missing.remove(e.item.pk)
            seqno = max(seqno,e.seqno)
        #~ print 20120411, required, missing
        for pk in required:
            if pk in missing:
                seqno += 1
                e = Entry(item_id=pk,budget=self,seqno=seqno)
                e.full_clean()
                e.save()
                #~ print e
        if self.actor_set.all().count() == 0:
            try:
                fam = self.partner.family
            except families.Family.DoesNotExist:
                pass
            else:
                for p in [fam.father,fam.mother]:
                    if p is not None:
                        a = Actor(
                            person=p,
                            budget=self,
                            header=unicode(p.get_salutation(nominative=True))
                            )
                        a.full_clean()
                        a.save()
                    
                #~ for m in self.partner.family.membersbyfamily.all():
                    #~ a = Actor(person=m.person,budget=self)
                
    #~ def __unicode__(self):
        #~ return "%s #unicode(join_words(_("Family"),self.name))
                
    @property
    def actor1(self):
        qs = self.actor_set.all()
        if qs.count() > 0:
            return qs[0]
            
    @property
    def actor2(self):
        qs = self.actor_set.all()
        if qs.count() > 1:
            return qs[1]
            
    def item_groups(self):
        return ItemGroup.objects.all()
        
    def unused_entries_by_group(self,ar):
        xml = ''
        ar.renderer = ar.ui.pdf_renderer
        for group in ItemGroup.objects.all():
            sub_ar = ar.spawn(EntriesByBudget,
                master_instance=self,
                item__group=group)
            #~ xml += ui.table2xhtml(sub_ar)
            xml += "<h2>%s</h2>" % group
            xml += etree.tostring(sub_ar.table2xhtml())
            #~ xml += sub_ar.table2xhtml()
            #~ xml += "<text:p>%s</text:p>" % etree.tostring(sub_ar.table2xhtml())
        sub_ar = ar.spawn(DebtsByBudget,
            master_instance=self)
        #~ xml += u"<h2>%s</h2>" % force_unicode(sub_ar.get_title())
        xml += "<h2>Schulden</h2>"
        xml += etree.tostring(sub_ar.table2xhtml())
        xml = "<div>%s</div>" % xml
        return xml
        #~ return self.entries_set.
            
        
      
class BudgetDetail(dd.DetailLayout):
    main = "general ExpensesByBudget IncomesByBudget DebtsByBudget"
    general = """
    date partner id user closed
    intro 
    ActorsByBudget
    """
    def setup_handle(self,h):
        h.general.label = _("General")
    
class Budgets(dd.Table):
    model = Budget
    detail_layout = BudgetDetail()
    #~ master_key = 'person'
    #~ label = _("Language knowledge")
    #~ button_label = _("Languages")
    #~ column_names = "language native spoken written cef_level"

class MyBudgets(Budgets,mixins.ByUser):
    pass
    

class ItemGroup(mixins.Sequenced,babel.BabelNamed):
    class Meta:
        verbose_name = _("Budget Item Group")
        verbose_name_plural = _("Budget Item Groups")
        
    account_type = AccountType.field()
    help_text = dd.RichTextField(_("Introduction"),format="html",blank=True)
    
class ItemGroups(dd.Table):
    model = ItemGroup
    
class Item(mixins.Sequenced,babel.BabelNamed):
    class Meta:
        verbose_name = _("Budget Item")
        verbose_name_plural = _("Budget Items")
    group = models.ForeignKey(ItemGroup)
    account_type = AccountType.field()
    #~ account = models.ForeignKey(Account)
    optional = models.BooleanField(_("Optional"),default=False)
    yearly = models.BooleanField(_("Yearly"),default=False)
    help_text = dd.RichTextField(_("Introduction"),format="html",blank=True)
    
    #~ @chooser()
    #~ def account_choices(cls,account_type):
        #~ Account.objects.filter(type=account_type)
    
    def save(self,*args,**kw):
        if not self.account_type:
            self.account_type = self.group.account_type
        super(Item,self).save(*args,**kw)
        
    
class Items(dd.Table):
    model = Item
    
    


class SequencedBudgetComponent(mixins.Sequenced):
    class Meta:
        abstract = True
        
    budget = models.ForeignKey(Budget)
    
    def set_seqno(self):
        """
        """
        qs = self.__class__.objects.filter(budget=self.budget).order_by('seqno')
        n = qs.count()
        if n == 0:
            self.seqno = 1
        else:
            last = qs[n-1]
            self.seqno = last.seqno + 1
        
  
class Actor(SequencedBudgetComponent):
    class Meta:
        verbose_name = _("Budget Actor")
        verbose_name_plural = _("Budget Actors")
        
    person = models.ForeignKey(settings.LINO.person_model,blank=True,null=True)
    header = models.CharField(_("Header"),max_length=20,blank=True)
    remark = models.CharField(_("Remark"),max_length=200,blank=True)
    #~ closed = models.BooleanField(verbose_name=_("Closed"))
    
    
class Actors(dd.Table):
    model = Actor

class ActorsByBudget(Actors):
    master_key = 'budget'
    
    

class Entry(SequencedBudgetComponent):
    class Meta:
        verbose_name = _("Budget Entry")
        verbose_name_plural = _("Budget Entries")
        unique_together = ['budget','item']
    
    #~ group = models.ForeignKey(ItemGroup)
    account_type = AccountType.field()
    item = models.ForeignKey(Item)
    name = models.CharField(_("Description"),max_length=200,blank=True)
    amount1 = dd.PriceField(_("Amount") + " 1",blank=True,null=True)
    amount2 = dd.PriceField(_("Amount") + " 2",blank=True,null=True)
    amount3 = dd.PriceField(_("Amount") + " 3",blank=True,null=True)
    circa = models.BooleanField(verbose_name=_("Circa"))
    todo = models.BooleanField(verbose_name=_("To Do"))
    remark = models.CharField(_("Remark"),max_length=200,blank=True)

    @chooser()
    def item_choices(cls,account_type):
        return Item.objects.filter(account_type=account_type)
        
    def save(self,*args,**kw):
        if not self.name:
            self.name = self.item.name
        self.account_type = self.item.account_type
        super(Entry,self).save(*args,**kw)
        
class Entries(dd.Table):
    model = Entry

#~ class EntriesByType(Entries):
    #~ master_key = 'account_type'
    
#~ class EntriesByGroup(Entries):
    #~ master_key = 'budget'
    
class EntriesByBudget(Entries):
    master_key = 'budget'
    column_names = "name amount1 amount2 amount3"
    
class EntriesByBudgetAndType(EntriesByBudget):
  
    column_names = "item name amount1 amount2 amount3 circa todo remark"
    _account_type = None
    
    @classmethod
    def class_init(self):
        super(EntriesByBudgetAndType,self).class_init()
        if self._account_type is not None:
            self.label = self._account_type.text
            #~ print 20120411, unicode(self.label)
            self.known_values = dict(account_type=self._account_type)
    
class ExpensesByBudget(EntriesByBudgetAndType):
    _account_type = AccountType.expense
        
class IncomesByBudget(EntriesByBudgetAndType):
    _account_type = AccountType.income
    


class Debt(SequencedBudgetComponent):
    class Meta:
        verbose_name = _("Debt")
        verbose_name_plural = _("Debts")
        
    partner = models.ForeignKey('contacts.Partner',blank=True,null=True)
    amount = dd.PriceField(_("Remaining"),blank=True,null=True)
    remark = models.CharField(_("Remark"),max_length=200,blank=True)

class Debts(dd.Table):
    model = Debt
    
class DebtsByBudget(Debts):
    master_key = 'budget'
    column_names = 'partner amount remark'
    

if settings.LINO.user_model:
  
    USER_MODEL = dd.resolve_model(settings.LINO.user_model)

    dd.inject_field(USER_MODEL,
        'is_debts',
        models.BooleanField(
            verbose_name=_("is Debts user")
        ),"""Whether this user is responsible for Debts Mediation.
        """)


def site_setup(site):  pass

def setup_main_menu(site,ui,user,m):  pass
  
def setup_master_menu(site,ui,user,m): pass

def setup_my_menu(site,ui,user,m): 
    m  = m.add_menu("debts",_("Debts"))
    m.add_action(MyBudgets)
  
def setup_config_menu(site,ui,user,m): 
    m  = m.add_menu("debts",_("Debts"))
    #~ m.add_action(Accounts)
    m.add_action(ItemGroups)
    m.add_action(Items)
  
def setup_explorer_menu(site,ui,user,m):
    m  = m.add_menu("debts",_("Debts"))
    m.add_action(Budgets)
    m.add_action(Entries)
