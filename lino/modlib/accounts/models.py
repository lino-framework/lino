## Copyright 2008-2012 Luc Saffre
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
Accounts. The base module required for accounting.

"""

import logging
logger = logging.getLogger(__name__)

from django.db import models
import datetime
from decimal import Decimal

from lino import dd
from lino import mixins
from lino.utils import babel
from lino.utils.choicelists import ChoiceList
#contacts = reports.get_app('contacts')
#~ from lino.modlib.journals import models as journals
#~ journals = reports.get_app('journals')
#from lino.modlib.contacts import models as contacts
#from lino.modlib.journals import models as journals
from django.utils.translation import ugettext_lazy as _
from lino.modlib.accounts.utils import AccountTypes




class Chart(babel.BabelNamed):
  
    class Meta:
        verbose_name = _("Account Chart")
        verbose_name_plural = _("Account Charts")
        
class Charts(dd.Table):
    model = Chart
    detail_layout = """
    id name
    GroupsByChart
    """
    
#~ class Group(babel.BabelNamed,mixins.Sequenced):
class Group(babel.BabelNamed):
  
    class Meta:
        verbose_name = _("Account Group")
        verbose_name_plural = _("Account Groups")
        unique_together = ['chart','ref']
        
    chart = models.ForeignKey(Chart)
    ref = models.CharField(max_length=10)
    account_type = AccountTypes.field()
    help_text = dd.RichTextField(_("Introduction"),format="html",blank=True)
    
class Groups(dd.Table):
    model = Group
    order_by = ['chart','ref']
    column_names = 'chart ref name account_type *'
    #~ required = dict(user_groups=['debts'],user_level='manager')
    #~ required_user_groups = ['debts']
    #~ required_user_level = UserLevels.manager
    detail_layout = """
    ref name
    account_type id 
    help_text
    AccountsByGroup
    """
    
class GroupsByChart(Groups):
    master_key = 'chart'
    order_by = ['ref']
    column_names = 'ref name account_type *'

class Account(babel.BabelNamed,mixins.Sequenced):
    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
    group = models.ForeignKey(Group)
    #~ chart = models.ForeignKey(Chart)
    type = AccountTypes.field()
    help_text = dd.RichTextField(_("Introduction"),format="html",blank=True)
    
    def full_clean(self,*args,**kw):
        if not self.name:
            self.name = self.group.name
        if not self.type:
            self.type = self.group.account_type
        #~ if not self.chart:
            #~ self.chart = self.group.chart
        super(Account,self).full_clean(*args,**kw)
        
    
class Accounts(dd.Table):
    model = Account
    #~ required=dict(user_groups=['debts'],user_level='manager')
    
#~ class AccountsByChart(Accounts):
    #~ master_key = 'chart'

class AccountsByGroup(Accounts):
    master_key = 'group'

    

def customize_products():
    dd.inject_field('products.Product',
        'sales_account',
        models.ForeignKey('accounts.Account',
            verbose_name=_("Sales account"),
            blank=True,null=True,
            related_name="products_sales",
            help_text=_("The account to move when this product is used in a sales invoice.")
        ))
    dd.inject_field('products.Product',
        'purchases_account',
        models.ForeignKey('accounts.Account',
            verbose_name=_("Purchases account"),
            blank=True,null=True,
            related_name="products_purchases",
            help_text=_("The account to move when this product is used in a purchases invoice.")
        ))



MODULE_LABEL = _("Accounts")

#~ settings.LINO.add_user_field('debts_level',UserLevel.field(MODULE_LABEL))
#~ settings.LINO.add_user_group('debts',MODULE_LABEL)

def site_setup(site):
    pass

def setup_main_menu(site,ui,user,m):  pass
 
def setup_master_menu(site,ui,user,m): pass

def setup_my_menu(site,ui,user,m): 
    pass
  
def setup_config_menu(site,ui,user,m): 
    #~ if user.profile.debts_level < UserLevels.manager: 
        #~ return
    m  = m.add_menu("accounts",MODULE_LABEL)
    m.add_action(Charts)
  
def setup_explorer_menu(site,ui,user,m):
    m  = m.add_menu("accounts",MODULE_LABEL)
    m.add_action(Groups)
    m.add_action(Accounts)

#~ dd.add_user_group('debts',MODULE_LABEL)

customize_products()
