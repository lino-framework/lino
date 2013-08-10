# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
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
#~ from lino.utils import join_words
from north import dbutils
#~ from lino.models import get_site_config

#~ from lino.modlib.contacts.utils import Genders

#~ from lino.modlib.countries.models import CountryCity
#~ from lino.modlib.countries.models import CountryRegionCity

#~ from lino.modlib.contacts.utils import get_salutation
#~ from lino.modlib.contacts.utils import GENDER_CHOICES, get_salutation

#~ from lino.utils import mti


#~ class ConceptTypes(dd.ChoiceList):
    #~ verbose_name = _("Concept Type")
    #~ verbose_name_plural = _("Concept Types")
    
#~ add = ConceptTypes.add_item
#~ add('10', _("Context"),'context')
#~ add('20', _("Jargon"),'context')

class LinkTypes(dd.ChoiceList):
    verbose_name = _("Link Type")
    verbose_name_plural = _("Link Types")

add = LinkTypes.add_item
#~ add('10', _("Context"),'context')
add('10', _("Jargon"),'jargon')
add('20', _("Obsoletes"),'obsoletes')



class Concept(dd.BabelNamed):
    """
    """
    
    class Meta:
        verbose_name = _("Concept")
        verbose_name_plural = _("Concepts")
        
    abbr = dd.BabelCharField(_("Abbreviation"),max_length=30,blank=True)
    wikipedia = dd.BabelCharField(_("Wikipedia"),max_length=200,blank=True)
      
    definition = dd.BabelTextField(_("Definition"),blank=True)
    is_jargon_domain = models.BooleanField(
        _("Jargon domain"),
        help_text=_("Whether this concept designates a domain of specialized vocabulary."))
        
    def summary_row(self,ar=None):
        if self.abbr:
            return ["%s (%s)" % (dbutils.babelattr(self,'name'),dbutils.babelattr(self,'abbr'))]
        return [dbutils.babelattr(self,'name')]
        
        
    
  
class Concepts(dd.Table):
    #~ required = dd.required(user_level='manager')
    model = Concept
    column_names = 'name id abbr'
    detail_layout = """
    name
    abbr
    definition
    wikipedia
    Parents Children
    """


class TopLevelConcepts(Concepts):
    label = _("Top-level concepts")
    filter = models.Q(is_jargon_domain=True)
    
    
    
    
    
    
class Link(dd.Model):
    
    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")
        
    type = LinkTypes.field(blank=True,default=LinkTypes.jargon)
    parent = dd.ForeignKey(Concept,related_name="children")
    child = dd.ForeignKey(Concept,related_name="parents")
    
    @dd.chooser()
    def child_choices(cls):
        return Concept.objects.filter(is_jargon_domain=True) #         
        
class Links(dd.Table):
    model = Link
    
class Parents(Links):
    master_key = 'child'
    label = _("Parents")
  
class Children(Links):
    master_key = 'parent'
    label = _("Children")

    


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
  
        
  
