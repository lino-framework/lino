## Copyright 2009-2011 Luc Saffre
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
A collection of tools for doing child/parent conversions (metamorphoses)
for models that use Django's multi-table inheritance.

See detailed presentation in :mod:`lino.test_apps.1.models`.

"""
import logging
logger = logging.getLogger(__name__)

def convert(obj,target_class,**attrs):
    """
    Converts the database records for the given 
    model instance `obj` into an instance of `target_class`.
    All field values that are also in the target_class, 
    including related objects, will be transferred.
    `attrs` may specify additional values that will override existing data.
    Returns the new instance which is already saved.
    
    Note that this
    will make the variable used by the caller refer to an invalid Model instance 
    object which does not represent any existing record. 
    
    """
    for field in target_class._meta.fields:
        if field.name not in attrs and hasattr(obj, field.name):
            attrs[field.name] = getattr(obj, field.name)
    pk = obj.pk
    related_objects = {}
    for r in target_class._meta.many_to_many:
        if getattr(r,'through',None) is not None:
            raise Exception("ManyToManyField.through not yet supported.")
        if hasattr(obj,r.name):
            m = getattr(obj,r.name)
            related_objects[r.name] = [x for x in m.all()]
    logger.info("convert %s to %s : attrs=%s, related_objects=%s",
      obj.__class__.__name__,target_class.__name__,
      attrs,related_objects)
    obj.delete()
    
    class InvalidModelInstance(object):
        def __str__(self):
            return "<%s object>" % self.__class__.__name__
    obj.__class__ = InvalidModelInstance
    
    #~ for n in ('save','__unicode__','delete','__getattr__'):
        #~ def func(*args,**kw):
            #~ raise Exception("Tried to call method %s on invalid object reference.")
        #~ setattr(obj,n,func)
        #~ obj.__dict__ = {}
    
    obj = target_class(**attrs)
    obj.save()
    for k,v in related_objects.items():
        #~ logger.info('%s = %s', f.name,[x for x in m.all()])
        setattr(obj,k,v)
    obj.save()
    return obj








def unused_child_from_parent(model, *parents,**kw):
    """
    Probably obsolete. use :func:`convert` instead.
    
    Inspired by 
    `Tom Tobin's patch suggestion 
    <http://bazaar.launchpad.net/~theonion/django/makechild/revision/5060>`_
    in 
    :djangoticket:`7623`.
    `icket 7623
    <http://code.djangoproject.com/ticket/7623>`_
    
    Creates a new instance of `model` copying data from the given `parents` 
    (which must be instances of a base class of model), updates 
    it with the given kwargs, saves it to the database, and returns the 
    created object.     
    """
    model_parents = tuple(model._meta.parents.keys())
    if not model_parents:
        raise ValueError("%r is not a child model; it has no parents" % model)
    attrs = {}
    for parent in parents:
        if not isinstance(parent, model_parents):
            raise ValueError("%r is not a parent instance of %r" % (parent, model))
        for field in parent._meta.fields:
            if field.name not in attrs:
                attrs[field.name] = getattr(parent, field.name)

        attrs[model._meta.parents[parent.__class__].name] = parent
    attrs.update(kw)
    return model(**attrs)

#~ def remove_child(obj,fieldname,**attrs):
    #~ for field in target_class._meta.get_fields_with_model():
        #~ if field.name != fieldname and field.name not in attrs and hasattr(obj, field.name):
            #~ attrs[field.name] = getattr(obj, field.name)
            
    #~ pk = obj.pk
    #~ related_objects = []
    #~ for r in target_class._meta.many_to_many:
        #~ related_objects.append(r,getattr(obj,r.name))
    #~ obj.delete()
    #~ obj = 
    #~ for r,q in related_objects:
        #~ setattr(obj,r.name,q)
    

      
from django.db import models
from lino.tools import resolve_model
from lino.fields import VirtualField

class EnableChild(VirtualField):
    """
    Docuemted and tested in :mod:`lino.test_apps.1.models`
    """
    def __init__(self,child_model,**kw):
        self.child_model = child_model
        VirtualField.__init__(self,models.BooleanField(**kw),self.has_child)

    def lino_kernel_setup(self,model,name):
        self.child_model = resolve_model(self.child_model,model._meta.app_label)
        VirtualField.lino_kernel_setup(self,model,name)
    
    def has_child(self,obj,request=None):
        "Returns True if "
        try:
            self.child_model.objects.get(pk=obj.pk)
        except self.child_model.DoesNotExist:
            return False
        return True

    def set_value_in_object(self,obj,v,request=None):
        if self.has_child(obj):
            logger.debug('set_value_in_object : %s has child %s',
                obj.__class__.__name__,self.child_model.__name__)
            # child exists, convert if it may not 
            if not v:
                return convert(obj,self.model)
        else:
            logger.debug('set_value_in_object : %s has no child %s',
                obj.__class__.__name__,self.child_model.__name__)
            if v:
                # child doesn't exist. convert if it should
                return convert(obj,self.child_model)
        # otherwise do nothing
        return obj
                
    #~ def set_is_restaurant(self,v):
        #~ if v:
            #~ try:
                #~ p = Restaurant.objects.get(pk=self.pk)
                #~ self.restaurant = p
            #~ except Restaurant.DoesNotExist:
                #~ p = child_from_parent(Restaurant,self)
                #~ p.save()
                #~ self.restaurant = p
            
        #~ else:
            #~ self.restaurant = None
            
    #~ def unused_get_is_restaurant(self):
        #~ try:
            #~ Restaurant.objects.get(pk=self.pk)
        #~ except Restaurant.DoesNotExist:
            #~ return False
        #~ return True
        
    #~ def unused_set_is_restaurant(self,v):
        #~ try:
            #~ p = Restaurant.objects.get(pk=self.pk)
            #~ if not v:
                #~ p.companydelete()
        #~ except Restaurant.DoesNotExist:
            #~ if v:
                #~ p = Restaurant(pk=self.pk)
                #~ p = child_from_parent(Restaurant,self)
                #~ p.save()

