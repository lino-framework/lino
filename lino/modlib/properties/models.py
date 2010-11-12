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

"""
Documentation: see lino.test_apps.properties.models.py
"""

#~ import logging
#~ logger = logging.getLogger(__name__)

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
#~ import lino
#~ logger.debug(__file__+' : started')
from lino import reports
#~ from lino import layouts
from lino import actions
from lino.utils import perms
from lino.utils.ticket7623 import child_from_parent


class Property(models.Model):
    name = models.CharField(max_length=40,primary_key=True)
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
                self.create_value(n,**kw).save()
                
    def create_value(self,v,owner=None):
        #print "%s.%s = %r" % (owner,self,v)
        vm = self.value_type.model_class()
        #qs = cl.objects.all()
        #qs.create(name=n,prop=self,owner=owner)
        if owner is None:
            i = vm(value=v,prop=self)
        else:
            i = vm(value=v,prop=self,owner=owner)
        return i
                
    def set_value_for(self,owner,v):
        pv = self.get_value_for(owner)
        pv.value = v
        pv.save()
        
    def get_value_for(self,owner):
        vm = self.value_type.model_class()
        if owner is None:
            #~ try:
                #~ return vm.objects.get(prop__exact=self,owner_id__isnull=True)
            #~ except vm.DoesNotExist,e:
                #~ return vm(prop=self)
            return vm(prop=self)
        assert owner.pk is not None, "must save the owner first"
        try:
            return vm.objects.get(prop__exact=self,owner_id__exact=owner.pk)
        except vm.DoesNotExist,e:
            return vm(prop=self,owner=owner)
            
    def set_choice_for(self,owner,i):
        v = self.choices_list()[i]
        return self.set_value_for(owner,v)
        
    def choices_list(self):
        cl = self.value_type.model_class()
        return cl.choices_list(self)
        
    def values_query(self):
        cl = self.value_type.model_class()
        #~ if len(order_by) == 0:
            #~ order_by = ['value']
        return cl.objects.filter(owner_id__isnull=False,prop__exact=self) #.order_by(*order_by)
        
    def form2obj(self,instance,post_data):
        ""
        v = post_data.get(self.name,None)
        if v is None:
            return
        self.set_value_for(instance,v)
        
        
        
    #~ def get_child(self,instance):
        #~ """
        #~ Calling this on an instance of the base class will be forwarded to the "child" instance.
        #~ Since the `value` is known only by the (concrete) "child" instance, we forward 
        #~ this to the child when this is called on an abstract "parent" instance. To get the child,
        #~ we use Django's implicit OneToOneField (the lower-case version of the model name,
        #~ see http://docs.djangoproject.com/en/dev/topics/db/models/#id7).
        #~ If you know a better method to achieve this, please let me know...
        #~ """
        #~ if instance.__class__ is PropValue: 
            #~ pvm = self.value_type.model_class()
            #~ return getattr(instance,pvm.__name__.lower())
        #~ return instance
                
    @classmethod
    def properties_for_model(cls,model):
        #~ print 'properties_for_model', model
        ct = ContentType.objects.get_for_model(model)
        #~ logger.debug('Property.properties_for_model() %s %s',model,ct)
        #~ return cls.objects.filter(only_for__in=(ct,None))
        q = models.Q(only_for__exact=None) | models.Q(only_for=ct)
        return cls.objects.filter(q)
        
    
class Properties(reports.Report):
    model = Property
    column_names = 'name *' #label only_for value_type'
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
    """
    Although PropValue is not abstract, you may instantiate only subclasses that define a value field.
    
    PropValue instances with owner None are used to store choices for this property.
    
    """
    owner_type = models.ForeignKey(ContentType,blank=True,null=True)
    owner_id = models.PositiveIntegerField(blank=True,null=True)
    owner = generic.GenericForeignKey('owner_type', 'owner_id')
    prop = models.ForeignKey(Property)
    value_text = models.CharField(max_length=200)
    
    #~ class Meta:
        #~ abstract = True
    
    def save(self,*args,**kw):
        assert self.__class__ is not PropValue
        child = self.get_child()
        self.value_text = unicode(child.value)
        models.Model.save(self,*args,**kw)
        
    def __unicode__(self):
        if self.prop_id is None:
            return ''
        self = self.get_child()
        return unicode(self.value)
        #~ label = self.prop.label or self.prop.name
        #~ if self.owner_id is None:
            #~ return u"One choice for '%s' is %s" % (label,self.value)
        #~ return u"%s for '%s' is %s" % (label,self.owner,self.value)
        
    def get_child(self):
        if self.__class__ is PropValue: 
            pvm = self.prop.value_type.model_class()
            return getattr(self,pvm.__name__.lower())
        return self
        
    def prop_name(self):
        if self.prop_id is None:
            return ''
        return self.prop.name
    prop_name.result_type = models.CharField(max_length=20)
    
    #~ def value(self):
        #~ self = self.prop.get_child(self)
        #~ return self.value
    #~ value.result_type = None # means variable result_type
                
        
    def by_owner(self):
        #~ if self.prop_id is None:
            #~ return ''
        self = self.get_child()
        return u"%s: %s" % (self.prop.name,self.value)
        
    def by_property(self):
        self = self.get_child()
        return u"%s: %s" % (self.owner,self.value)
        
    #~ def value_text(self):
        #~ self = self.prop.get_child(self)
        #~ return unicode(self.value)
        
    @classmethod
    def choices_list(cls,prop):
        #~ return [pv.value for pv in cls.objects.filter(owner_id__isnull=True,prop__exact=prop)]
        return [pv.value for pv in cls.value_choices(prop)]
        
    @classmethod
    def prop_choices(cls,owner):
        """
        This answers the question "What Properties are possible for this PropValue?", 
        which basically is "All Properties that apply to this type of owner". 
        This means currently that Property.only_for must be either None or equal to master_instance.owner_type
        """
        mt = ContentType.objects.get_for_model(owner.__class__)
        return Property.objects.filter(only_for__in=(mt,None))
        
    @classmethod
    def value_choices(cls,prop):
        "List of PropValue instances choices for comboboxes"
        return cls.objects.filter(owner_id__isnull=True,prop__exact=prop)
        #~ return prop.propvalue_set.filter(owner_id__isnull=True)

    @classmethod
    def create_property(cls,**kw):
        kw.update(value_type=ContentType.objects.get_for_model(cls))
        only_for = kw.get('only_for',None)
        if only_for is not None:
            if not isinstance(only_for,ContentType):
                only_for = resolve_model(only_for)
                kw.update(only_for=ContentType.objects.get_for_model(only_for))
        return Property(**kw)
        
class CHAR(PropValue):
    value = models.CharField(max_length=200)
    
class TEXT(PropValue):
    value = models.TextField()
    
class INT(PropValue):
    value = models.IntegerField(null=True)

class BOOL(PropValue):
    value = models.NullBooleanField()
    
    @classmethod
    def choices_list(self,prop):
        return [ True, False ]


class PropValues(reports.Report):
    model = PropValue
    order_by = "prop__name"
    

class PropertiesAction(actions.ToggleWindowAction):
    "Used on reports whose model have properties"
    #~ name = 'props'
    name = 'properties'
    label = _('Properties')
    #~ propvalues_report = None
    
    #~ def __init__(self,report):
        #~ rpt = actor
        #~ if rpt.model is not None:
            #~ from lino.modlib.properties import models as properties
            #~ if rpt.model is not properties.PropValue:
                #~ self.propvalues_report = properties.PropValuesByOwner() # .get_handle(ah.ui)
        #~ actions.ToggleWindowAction.__init__(self,rpt)
        
    #~ def prop_values(self,ui):
        #~ if self.propvalues_report is not None:
          
        #~ from lino.modlib.properties import models as properties
        #~ if self.actor.model is not properties.PropValue:
            #~ rh = properties.PropValuesByOwner().get_handle(ui)
            #~ return rh.request(master=self.actor.model)
    

class PropsEdit(actions.OpenWindowAction):
    "Default action for PropValuesByOwner"
    name = 'pgrid'
    
            

class PropValuesByOwner(reports.Report):
    default_action_class = PropsEdit
    label = _('Properties')
    model = PropValue
    use_layouts = False
    can_add = perms.never
    fk_name = 'owner'
    order_by = "prop__name"
    
    def get_title(self,rr):
        if rr.master_instance is None:
            return _('Properties for %s') % rr.master._meta.verbose_name_plural
        return _('Properties for %s') % rr.master_instance
        
    def get_queryset(self,ar):
        "returns one PropValue instance for each possible Property"
        return [ p.get_value_for(ar.master_instance) 
            for p in Property.properties_for_model(ar.master).order_by('name')]

    def row2dict(self,row,d):
        d['name'] = row.prop.name
        #~ d['label'] = row.prop.label
        #~ d['type'] = row.prop.value_type.__class__.__name__
        d['value'] = row.value
        #~ d['choices'] = [unicode(pv) for pv in row.value_choices(row.prop)]
        return d
        
        
        

def set_value_for(owner,**kw):
    for k,v in kw.items():
        try:
            p = Property.objects.get(pk=k)
        except Property.DoesNotExist:
            #~ print Property.objects.all()
            raise Exception("There's no property named %r" % k)
        p.set_value_for(owner,v)
        
#~ logger.debug(__file__+' : done')
