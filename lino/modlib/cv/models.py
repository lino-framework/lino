# -*- coding: UTF-8 -*-
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

import logging
logger = logging.getLogger(__name__)

import os
import cgi
import datetime

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

#~ import lino
#~ logger.debug(__file__+' : started')
#~ from django.utils import translation


#~ from lino import reports
from lino import dd
#~ from lino import layouts
from lino.utils import perms
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
from lino.utils.babel import DEFAULT_LANGUAGE, babelattr, babeldict_getitem
from lino.utils.babel import language_choices
#~ from lino.utils.babel import add_babel_field, DEFAULT_LANGUAGE, babelattr, babeldict_getitem
from lino.utils import babel 
from lino.utils.choosers import chooser
from lino.utils import mti
from lino.mixins.printable import DirectPrintAction, Printable
#~ from lino.mixins.reminder import ReminderEntry
from lino.tools import obj2str

from lino.modlib.countries.models import CountryCity
from lino.modlib.properties import models as properties
#~ from lino.modlib.cal.models import DurationUnit, update_auto_task
from lino.modlib.cal.models import DurationUnit, update_reminder
#~ from lino.modlib.contacts.models import Contact
from lino.tools import resolve_model, UnresolvedModel

#~ # not used here, but these modules are required in INSTALLED_APPS, 
#~ # and other code may import them using 
#~ # ``from lino.apps.pcsw.models import Property``

#~ from lino.modlib.properties.models import Property
#~ # from lino.modlib.notes.models import NoteType
#~ from lino.modlib.countries.models import Country, City

#~ if settings.LINO.user_model:
    #~ User = resolve_model(settings.LINO.user_model,strict=True)



class CefLevel(ChoiceList):
    """
    Levels of the Common European Framework (CEF).
    
    | http://www.coe.int/t/dg4/linguistic/CADRE_EN.asp
    | http://www.coe.int/t/dg4/linguistic/Source/ManualRevision-proofread-FINAL_en.pdf
    | http://www.telc.net/en/what-telc-offers/cef-levels/a2/
    
    """
    label = _("CEF level")
    
    @classmethod
    def display_text(cls,bc):
        def fn(bc):
            return u"%s (%s)" % (bc.value,unicode(bc))
        return lazy(fn,unicode)(bc)
        #~ return u"%s (%s)" % (bc.value,unicode(bc))
    
add = CefLevel.add_item
add('A1', _("basic language skills"))
add('A2', _("basic language skills"))
add('A2+', _("basic language skills"))
add('B1', _("independent use of language"))
add('B2', _("independent use of language"))
add('B2+', _("independent use of language"))
add('C1', _("proficient use of language"))
add('C2', _("proficient use of language"))
add('C2+', _("proficient use of language"))





#
# LanguageKnowledge
#

class LanguageKnowledge(models.Model):
    """Specifies how well a certain Person knows a certain Language.
    Deserves more documentation."""
    class Meta:
        verbose_name = _("language knowledge")
        verbose_name_plural = _("language knowledges")
        
    allow_cascaded_delete = True
    
    #~ person = models.ForeignKey("contacts.Person")
    person = models.ForeignKey(settings.LINO.person_model)
    language = models.ForeignKey("countries.Language",verbose_name=_("Language"))
    #~ language = models.ForeignKey("countries.Language")
    #~ language = fields.LanguageField()
    spoken = HowWell.field(verbose_name=_("spoken"))
    written = HowWell.field(verbose_name=_("written"))
    native = models.BooleanField(verbose_name=_("native language"))
    cef_level = CefLevel.field(blank=True) # ,null=True)
    
    def __unicode__(self):
        if self.language_id is None:
            return ''
        if self.cef_level:
            return u"%s (%s)" % (self.language,self.cef_level)
        if self.spoken > '1' and self.written > '1':
            return _(u"%s (s/w)") % self.language
        elif self.spoken > '1':
            return _(u"%s (s)") % self.language
        elif self.written > '1':
            return _(u"%s (w)") % self.language
        else:
            return unicode(self.language)
      
    
class LanguageKnowledgesByPerson(dd.Table):
    model = LanguageKnowledge
    master_key = 'person'
    #~ label = _("Language knowledge")
    #~ button_label = _("Languages")
    column_names = "language native spoken written cef_level"

# 
# PROPERTIES
# 


class PersonProperty(properties.PropertyOccurence):
    """A given property defined for a given person. 
    See :mod:`lino.modlib.properties`."""
    
    allow_cascaded_delete = True
    
    class Meta:
        app_label = 'properties'
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")
        
    #~ person = models.ForeignKey("contacts.Person")
    person = models.ForeignKey(settings.LINO.person_model)
    remark = models.CharField(max_length=200,
        blank=True,# null=True,
        verbose_name=_("Remark"))


class PersonProperties(dd.Table):
    model = PersonProperty
    hidden_columns = frozenset(['group'])
    
class PropsByPerson(PersonProperties):
    master_key = 'person'
    column_names = "property value remark *"
    
    
class PersonPropsByProp(PersonProperties):
    model = PersonProperty
    #~ app_label = 'properties'
    master_key = 'property'
    column_names = "person value remark *"
    
#~ class PersonPropsByType(dd.Table):
    #~ model = PersonProperty
    #~ master_key = 'type'
    #~ column_names = "person property value remark *"
    #~ hidden_columns = frozenset(['group'])
    
from django.utils.functional import lazy
    
class ConfiguredPropsByPerson(PropsByPerson):
    """
    Base class for 
    :class`SkillsByPerson`, 
    :class`SoftSkillsByPerson` and
    :class`ObstaclesByPerson`.
    """
    propgroup_config_name = None
    typo_check = False # to avoid warning "ConfiguredPropsByPerson 
                       # defines new attribute(s) propgroup_config_name"
    @classmethod
    def setup_actions(self):
        if self.propgroup_config_name:
            pg = getattr(settings.LINO.site_config,self.propgroup_config_name)
            self.known_values = dict(group=pg)
            if pg is None:
                self.label = _("(Site setting %s is empty)" % self.propgroup_config_name)
            else:
                #~ def f():
                    #~ return babelattr(pg,'name')
                #~ self.label = lazy(f,unicode)()
                self.label = lazy(babelattr,unicode)(pg,'name')
                #~ self.label = babelattr(pg,'name')
        super(PropsByPerson,self).setup_actions()
        
class SkillsByPerson(ConfiguredPropsByPerson):
    propgroup_config_name = 'propgroup_skills'
        
class SoftSkillsByPerson(ConfiguredPropsByPerson):
    propgroup_config_name = 'propgroup_softskills'
        
class ObstaclesByPerson(ConfiguredPropsByPerson):
    propgroup_config_name = 'propgroup_obstacles'
    
    




"""
Here we add some specific fields to the 
standard model SiteConfig.
http://osdir.com/ml/django-users/2009-11/msg00696.html
"""

from lino.models import SiteConfig
    
dd.inject_field(SiteConfig,
    'propgroup_skills',
    models.ForeignKey('properties.PropGroup',
        blank=True,null=True,
        verbose_name=_("Skills Property Group"),
        related_name='skills_sites'),
    """The property group to be used as master 
    for the SkillsByPerson report.""")
dd.inject_field(SiteConfig,
    'propgroup_softskills',
    models.ForeignKey('properties.PropGroup',
        blank=True,null=True,
        verbose_name=_("Soft Skills Property Group"),
        related_name='softskills_sites',
        ),
    """The property group to be used as master 
    for the SoftSkillsByPerson report."""
    )
dd.inject_field(SiteConfig,
    'propgroup_obstacles',
    models.ForeignKey('properties.PropGroup',
        blank=True,null=True,
        verbose_name=_("Obstacles Property Group"),
        related_name='obstacles_sites',
        ),
    """The property group to be used as master 
    for the ObstaclesByPerson report."""
    )



