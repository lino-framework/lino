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

"See lino.test_apps.properties.models.py"

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from lino import reports
from lino import layouts
from lino.utils import perms
from lino.utils.ticket7623 import child_from_parent


class Property(models.Model):
    name = models.CharField(max_length=40)
    label = models.CharField(max_length=200,blank=True)
    only_for = models.ForeignKey(ContentType,blank=True,null=True,related_name='only_for_properties')
    value_type = models.ForeignKey(ContentType,related_name='value_for_properties')
    
    def __unicode__(self):
        #if self.name is None: return u''
        return self.name
        
    def create_values(self,s,**kw):
        for n in s.splitlines():
            n = n.strip()
            if n:
                self.create_value(n,**kw)
                
    def create_value(self,v,owner=None):
        #print "%s.%s = %r" % (owner,self,v)
        cl = self.value_type.model_class()
        #qs = cl.objects.all()
        #qs.create(name=n,prop=self,owner=owner)
        if owner is None:
            i = cl(value=v,prop=self)
        else:
            i = cl(value=v,prop=self,owner=owner)
        i.save()
        return i
                
    def set_value_for(self,owner,v):
        vm = self.value_type.model_class()
        try:
            pv = vm.objects.get(prop__exact=self,owner_id__exact=owner.pk)
        except vm.DoesNotExist,e:
            self.create_value(v,owner)
        else:
            pv.value = v
            pv.save()
        
    def choices_list(self):
        cl = self.value_type.model_class()
        return cl.objects.filter(owner_id__exact=None,prop__exact=self)
        
                
class Properties(reports.Report):
    model = Property
    columnNames = 'name *' #label only_for value_type'
    order_by = "name"
        

#~ class PropChoice(models.Model):
    #~ prop = models.ForeignKey(Property)
    #~ name = models.CharField(max_length=200)
    #~ short = models.CharField(max_length=40,blank=True,null=True)
    
    #~ def __unicode__(self):
        #~ #if self.name is None: return u''
        #~ return self.name

#~ class PropChoices(reports.Report):
    #~ model = PropChoice

class PropValue(models.Model):
    "Note: PropValue instances with owner None = possible choices"
    owner_type = models.ForeignKey(ContentType,blank=True,null=True)
    owner_id = models.PositiveIntegerField(blank=True,null=True)
    owner = generic.GenericForeignKey('owner_type', 'owner_id')
    prop = models.ForeignKey(Property)
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        #child = child_from_parent(self)
        if self.pk is None:
            return ''
        #~ if not self.owner:
            #~ return ''
        if self.prop_id is None:
            return unicode(self.value)
        return u"%s: %s" % (self.prop.name,self.value)
        
    def prop_choices(self,recipient):
        """
        This report answers the question "What Properties are possible for this PropValue?", 
        which basically is "All Properties that apply to this type of owner". 
        This means currently that Property.only_for must be either None or equal to master_instance.owner_type
        """
        return Property.objects.filter(only_for__in=(recipient.owner_type,None))
        
    def value_choices(self,recipient):
        return recipient.prop.propchoice_set.all(owner__exact=None)

class CharPropValue(PropValue):
    value = models.CharField(max_length=200)
    
class IntegerPropValue(PropValue):
    value = models.IntegerField()

class BooleanPropValue(PropValue):
    value = models.BooleanField()


class PropValues(reports.Report):
    model = PropValue
    order_by = "prop__name"
    
class PropValuesByOwner(reports.Report):
    model = PropValue
    #master = ContentType
    fk_name = 'owner'
    columnNames = "prop value"
    #can_delete = True
    order_by = "prop__name"


