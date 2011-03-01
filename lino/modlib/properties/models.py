# -*- coding: UTF-8 -*-
## Copyright 2008-2011 Luc Saffre
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

Todo:

Property.type should not be a ForeignKey to PropType, 
but a simple reference to a PropertyType instance.
There should be a list of PropertyType objects, 
some of them not stored (like YesNo and 
and only 

"""

import os
import cgi
import datetime

from django.db import models
#~ from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode 

#~ import lino
#~ logger.debug(__file__+' : started')

from lino import reports
#~ from lino import layouts
from lino.utils import perms
from lino.utils import babel
#~ from lino.utils.babel import babelattr
#~ from lino.utils import printable
from lino import mixins
from lino import actions
#~ from lino import fields
from lino.modlib.contacts import models as contacts
from lino.modlib.notes import models as notes
from lino.modlib.links import models as links
from lino.modlib.uploads import models as uploads
#~ from lino.modlib.uploads.models import UploadsByPerson
from lino.models import get_site_config
from lino.tools import get_field
from lino.tools import resolve_field
from lino.utils.choosers import chooser
from lino.mixins.printable import DirectPrintAction
from lino.mixins.reminder import ReminderEntry

from lino.utils.choicelists import get_choicelist, choicelist_choices
    

class PropType(models.Model):
    """
    The type of the values that a property accepts.
    Each PropType may (or may not) imply a list of choices.
    
    Examples: of property types:
    - Knowledge (Choices: "merely", "acceptable", "good", "very good",...)
    - YesNo (no choices)
    
    """
    class Meta:
        verbose_name = _("Property Type")
        verbose_name_plural = _("Property Types")
        
    name = babel.BabelCharField(max_length=200,verbose_name=_("Designation"))
    
    choicelist = models.CharField(
        max_length=50, blank=True,
        verbose_name=_("Choices List"),
        choices=choicelist_choices())
    
    default_value = models.CharField(_("default value"),
        max_length=settings.LINO_SITE.propvalue_max_length,
        blank=True)
    """
    The default value to set when creating a :class:`PropertyOccurence`.
    This is currently used only in some fixture...
    """
        
    limit_to_choices = models.BooleanField(_("Limit to choices"))
    """
    not yet supported
    """
    
    multiple_choices = models.BooleanField(_("Multiple choices"))
    """
    not yet supported
    """
    
    @chooser()
    def default_value_choices(cls):
        return self.choices_for(None)
        
    def __unicode__(self):
        return babel.babelattr(self,'name')
        
    def choices_for(self,property):
        if self.choicelist:
            return get_choicelist(self.choicelist).get_choices()
        return [(pc.value, pc.text) for pc in 
            PropChoice.objects.filter(type=self).order_by('value')]
            
#~ add_babel_field(PropType,'name')

class PropChoice(models.Model):
    """
    A Choice for this PropType.
    `value` is the value to be stored in :attr:`PropValue.value`.
    `text` is the text to be displayed in combo boxes.
    """
    class Meta:
        verbose_name = _("Property Choice")
        verbose_name_plural = _("Property Choices")
        
    type = models.ForeignKey(PropType,verbose_name=_("Property Type"))
    value = models.CharField(max_length=settings.LINO_SITE.propvalue_max_length,verbose_name=_("Value"))
    text = babel.BabelCharField(max_length=200,verbose_name=_("Designation"))
    
    def __unicode__(self):
        return babel.babelattr(self,'text')
#~ add_babel_field(PropChoice,'text')

class PropGroup(models.Model):
    """
    A Property Group defines a list of Properties that fit together under a common name.
    Examples of Property Groups: Skills, Soft Skills, Obstacles
    There will be one menu entry per Group.
    """
    class Meta:
        verbose_name = _("Property Group")
        verbose_name_plural = _("Property Groups")
        
    name = babel.BabelCharField(max_length=200,verbose_name=_("Designation"))
    
    def __unicode__(self):
        return babel.babelattr(self,'name')

#~ add_babel_field(PropGroup,'name')


class Property(models.Model):
    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")
        
    name = babel.BabelCharField(max_length=200,verbose_name=_("Designation"))
    group = models.ForeignKey(PropGroup,verbose_name=_("Property Group"))
    type = models.ForeignKey(PropType,verbose_name=_("Property Type"))
    
    def __unicode__(self):
        return babel.babelattr(self,'name')
#~ add_babel_field(Property,'name')


class PropertyOccurence(models.Model):
    """
    A Property Occurence is when a Property occurs, possibly having a certain value.
    
    Abstract base class for 
    | :class:`lino.modlib.dsbe.models.PersonProperty`,
    | :class:`lino.modlib.dsbe.models.WantedProperty`, 
    | :class:`lino.modlib.dsbe.models.AvoidedProperty`,
    | ...
    
    """
    
    class Meta:
        abstract = True
        
    group = models.ForeignKey(PropGroup,verbose_name=_("Property group"))
    property = models.ForeignKey(Property,verbose_name=_("Property")) # ,blank=True,null=True)
    # property must be nullable?
    value = models.CharField(_("Value"),max_length=settings.LINO_SITE.propvalue_max_length,blank=True)
    
    def get_text(self):
        c = PropChoice.objects.get(type=self.property.type,value=self.value)
        return babel.babelattr(c,'name')
    
    @chooser()
    def value_choices(cls,property):
        if property is None:
            return []
        return property.type.choices_for(property)
            
    @chooser()
    def property_choices(cls,group):
        #~ print group
        if group is None:
            return []
        return Property.objects.filter(group=group).order_by('name')
        
    def get_value_display(self,value):
        if not value or self.property_id is None:
            return ''
        if self.property.type.choicelist:
            cl = get_choicelist(self.property.type.choicelist)
            return cl.get_text_for_value(value)
        l = []
        for v in value.split(','):
            try:
                v = PropChoice.objects.get(value=v,type=self.property.type).text
            except PropChoice.DoesNotExist:
                pass
            l.append(v)
        return ','.join(l)
        
        
    def full_clean(self):
        if self.property_id is not None:
            self.group = self.property.group
        super(PropertyOccurence,self).full_clean()
        #~ if self.group != self.property.group:
            #~ raise ValidationError()
    #~ def save(self,*args,**kw):
        #~ self.group = self.property.group
        #~ r = super(PropertyOccurence,self).save(*args,**kw)
        #~ return r
        
    def __unicode__(self):
        if self.property_id is None:
            return u"Undefined %s" % self.group
        return u'%s.%s=%s ' % (self.group,self.property,self.value)
    


class PropGroups(reports.Report):
    model = PropGroup

class PropTypes(reports.Report):
    model = PropType

class PropChoices(reports.Report):
    model = PropChoice
    
class Properties(reports.Report):
    model = Property
    order_by = ['name']
    #~ column_names = "id name"
    
class PropsByGroup(Properties):
    fk_name = 'group'

class PropsByType(Properties):
    fk_name = 'type'

class ChoicesByType(PropChoices):
    fk_name = 'type'
    

#~ class PropsByGroup(reports.Report):
    #~ model = Property
    #~ fk_name = 'group'
    #~ column_names = "* group" 
    #~ """
    #~ group must be in the store, but should not be visible. 
    #~ needed to set context of property combobox.
    #~ """
    #~ hide_columns = ['group'] # doen's work yet
    

from lino.models import SiteConfig
SiteConfig.add_to_class('propgroup_skills',
    models.ForeignKey(PropGroup,
        blank=True,null=True,
        verbose_name=_("Skills Property Group"),
        related_name='skills_sites',
        ))
SiteConfig.add_to_class('propgroup_softskills',
    models.ForeignKey(PropGroup,
        blank=True,null=True,
        verbose_name=_("Soft Skills Property Group"),
        related_name='softskills_sites',
        ))
SiteConfig.add_to_class('propgroup_obstacles',
    models.ForeignKey(PropGroup,
        blank=True,null=True,
        verbose_name=_("Obstacles Property Group"),
        related_name='obstacles_sites',
        ))

