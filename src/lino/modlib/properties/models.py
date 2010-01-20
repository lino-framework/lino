## Copyright 2009-2010 Luc Saffre
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


from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from lino import reports
from lino import layouts
from lino.utils import perms


class Property(models.Model):
    short = models.CharField(max_length=40)
    name = models.CharField(max_length=200)
    only_for = models.ForeignKey(ContentType,blank=True,null=True)
    
    def __unicode__(self):
        #if self.name is None: return u''
        return self.name
        
class Properties(reports.Report):
    model = Property
    columnNames = 'short name only_for'
    order_by = "short"
        

class PropChoice(models.Model):
    prop = models.ForeignKey(Property)
    name = models.CharField(max_length=200)
    short = models.CharField(max_length=40)
    
    def __unicode__(self):
        #if self.name is None: return u''
        return self.name

class PropChoices(reports.Report):
    model = PropChoice

class PropValue(models.Model):
    owner_type = models.ForeignKey(ContentType)
    owner_id = models.PositiveIntegerField()
    owner = generic.GenericForeignKey('owner_type', 'owner_id')
    prop = models.ForeignKey(Property)
    value = models.CharField(max_length=200)
    
    def __unicode__(self):
        if self.pk is None:
            return ''
        #~ if not self.owner:
            #~ return ''
        #~ if self.prop is None:
            #~ return ''
        return "%s: %s" % (self.prop.short,self.value)
        
    def prop_choices_filter(self,recipient):
        """
        recipient is a PropValue instance which doesn't know her .prop attribute.
        This report answers the question "What Properties are possible for this PropValue?", 
        which basically is "All Properties that apply to this type of owner". 
        This means currently that Property.only_for must be either None or equal to master_instance.owner_type
        """
        return dict(only_for__in=(recipient.owner_type,None))
  

class PropValues(reports.Report):
    model = PropValue
    order_by = "prop__short"
    
class PropValuesByOwner(reports.Report):
    model = PropValue
    #master = ContentType
    fk_name = 'owner'
    columnNames = "prop value"
    #can_delete = True
    order_by = "prop__short"
