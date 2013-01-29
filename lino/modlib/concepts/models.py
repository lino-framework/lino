# -*- coding: UTF-8 -*-
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
This module defines the tables 
- :class:`Partner` (and their specializations :class:`Person` and :class:`Company`)
- :class:`Role` and :class:`RoleType`

"""

from __future__ import unicode_literals


import logging
logger = logging.getLogger(__name__)


import datetime
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
#~ from django.utils.translation import ugettext

from django import forms
from django.utils import translation


import lino
#~ from lino import layouts

from lino import dd
#~ from lino import fields

from lino import mixins
from lino.utils import join_words
from lino.utils.choosers import chooser
from lino.utils import babel 
#~ from lino.models import get_site_config

#~ from lino.modlib.contacts.utils import Genders

#~ from lino.modlib.countries.models import CountryCity
from lino.modlib.countries.models import CountryRegionCity

#~ from lino.modlib.contacts.utils import get_salutation
#~ from lino.modlib.contacts.utils import GENDER_CHOICES, get_salutation


from lino.utils import mti


class Concept(babel.BabelNamed):
    """
    """
    
    class Meta:
        verbose_name = _("Concept")
        verbose_name_plural = _("Concepts")
        
    abbr = babel.BabelCharField(_("Abbreviation"),max_length=30,blank=True)
    wikipedia = babel.BabelCharField(_("Wikipedia"),max_length=200,blank=True)
      
    definition = babel.BabelTextField(_("Definition"),blank=True)
    
        
class Concepts(dd.Table):
    #~ required = dd.required(user_level='manager')
    model = Concept
    column_names = 'name id abbr'
    detail_layout = """
    name
    abbr
    definition
    wikipedia
    """




MODULE_LABEL = _("Concepts")


def setup_main_menu(site,ui,profile,m):
    m = m.add_menu("concepts",MODULE_LABEL)
    m.add_action(Concepts)

def setup_master_menu(site,ui,profile,m): 
    pass
    
def setup_config_menu(site,ui,profile,m): 
    pass
  
def setup_explorer_menu(site,ui,profile,m):
    pass
  
        
  