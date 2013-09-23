# -*- coding: UTF-8 -*-
## Copyright 2011-2013 Luc Saffre
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
"""

import os
import cgi
import datetime

from django.db import models
#~ from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


from lino import mixins
from lino import dd

def customize_contacts():
    dd.inject_field('contacts.Partner',
        'national_id_et',
        models.CharField(max_length=200,
        blank=True,verbose_name=_("National ID")
        #~ ,validators=[niss_validator]
        )
      )
    dd.inject_field('contacts.Partner',
        'bank_account1',
        models.CharField(max_length=100,
        blank=True,verbose_name=_("Bank account")
        #~ ,validators=[niss_validator]
        )
      )

customize_contacts()

#~ from lino.modlib.contacts import models as contacts
#~ from lino.modlib.notes import models as notes
contacts = dd.resolve_app('contacts')
households = dd.resolve_app('households')

#~ class Person(contacts.PersonMixin,contacts.Partner,contacts.Born,mixins.Printable):
class Person(contacts.Person,mixins.Born,mixins.Printable,mixins.CreatedModified):
    class Meta(contacts.Person.Meta):
        app_label = 'contacts'

class Household(households.Household,mixins.CreatedModified):
    class Meta(households.Household.Meta):
        app_label = 'households'

class Company(contacts.Company,mixins.CreatedModified):
    class Meta(contacts.Company.Meta):
        app_label = 'contacts'



def site_setup(site):
    """
    This is the place where we can override or 
    define application-specific things.
    This includes especially those detail layouts 
    which depend on the *combination* of installed modules.
    """
    #~ todo: 
    site.modules.contacts.Partners.add_detail_tab("tickets","tickets.TicketsByPartner")
    site.modules.contacts.Companies.add_detail_tab("tickets","tickets.TicketsByPartner")
    site.modules.contacts.Persons.add_detail_tab("tickets","tickets.TicketsByPartner")
    site.modules.contacts.Persons.set_detail_layout(
        name_box = """last_name first_name:15 
        gender title:10 birth_date""",
        info_box = "id:5 language:10 \nage")
    
    site.modules.system.SiteConfigs.set_detail_layout(
        """
        site_company next_partner_id:10
        default_build_method 
        clients_account   sales_account     sales_vat_account
        suppliers_account purchases_account purchases_vat_account
        """)
        
    
    


    
