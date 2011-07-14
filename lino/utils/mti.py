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
A collection of tools for doing multi-table child/parent conversions 

See detailed presentation in :mod:`lino.test_apps.1.models`.

"""
import logging
logger = logging.getLogger(__name__)



from django.db.models.deletion import Collector
from django.db import router

class ChildCollector(Collector):
    """
    A Collector that does not delete the parents.
    """
  
    def collect(self, objs, source=None, nullable=False, collect_related=True,
        source_attr=None,collect_parents=True):

        new_objs = self.add(objs, source, nullable)
        if not new_objs:
            return
        model = new_objs[0].__class__

        if collect_related:
            #~ for m,related in model._meta.get_all_related_objects_with_model(include_hidden=True):
            for related in model._meta.get_all_related_objects(include_hidden=True,local_only=True):
                field = related.field
                if related.model._meta.auto_created:
                    self.add_batch(related.model, field, new_objs)
                else:
                    sub_objs = self.related_objects(related, new_objs)
                    if not sub_objs:
                        continue
                    field.rel.on_delete(self, field, sub_objs, self.using)

            # TODO This entire block is only needed as a special case to
            # support cascade-deletes for GenericRelation. It should be
            # removed/fixed when the ORM gains a proper abstraction for virtual
            # or composite fields, and GFKs are reworked to fit into that.
            for relation in model._meta.many_to_many:
                if not relation.rel.through:
                    sub_objs = relation.bulk_related_objects(new_objs, self.using)
                    self.collect(sub_objs,
                                 source=model,
                                 source_attr=relation.rel.related_name,
                                 nullable=True)
  

def delete_child(obj,child_model,using=None):
    using = using or router.db_for_write(obj.__class__, instance=obj)
    try:
        child = child_model.objects.get(pk=obj.pk)
    except child_model.DoesNotExist:
        raise Exception(u"%s has no child in %s" % (obj,child_model.__name__))
    logger.info(u"Delete child %s from %s",child_model.__name__,obj)
    collector = ChildCollector(using=using)
    collector.collect([child],source=obj.__class__,nullable=True,collect_parents=False)
    collector.delete()
    

def insert_child(obj,child_model,**attrs):
    assert child_model != obj.__class__
    parent_link_field = child_model._meta.parents.get(obj.__class__,None)
    if parent_link_field is None:
        raise Exception("A %s cannot be parent for a %s" % (obj.__class__.__name__,child_model.__name__))
    attrs[parent_link_field.name] = obj
    #~ for pm,pf in child_model._meta.parents.items(): # pm : parent model, pf : parent link field
        #~ attrs[pf.name] = obj
    #~ attrs["%s_ptr" % obj.__class__.__name__.lower()] = obj
    for field in obj._meta.fields:
        attrs[field.name] = getattr(obj, field.name)
    #~ logger.info(u"Promote %s to %s : attrs=%s",
        #~ obj.__class__.__name__,child_model.__name__,attrs)
    logger.info(u"Promote %s to %s",
        obj.__class__.__name__,child_model.__name__)
    new_obj = child_model(**attrs)
    new_obj.save()
    return new_obj

reduce = delete_child
promote = insert_child



def unused_convert_first_attempt(obj,target_class,**attrs):
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
    
    See detailed presentation in :mod:`lino.test_apps.1.models`.

    """
    for field in target_class._meta.fields:
        if field.name not in attrs and hasattr(obj, field.name):
            attrs[field.name] = getattr(obj, field.name)
    pk = obj.pk
    related_objects = {}
    for r in target_class._meta.many_to_many:
        if getattr(r,'through',None) is not None:
            raise Exception("ManyToManyField.through not supported.")
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
    
    obj = target_class(**attrs)
    obj.save()
    for k,v in related_objects.items():
        #~ logger.info('%s = %s', f.name,[x for x in m.all()])
        setattr(obj,k,v)
    obj.save()
    return obj

class InvalidModelInstance(object):
    def __str__(self):
        return "<%s object>" % self.__class__.__name__

def unused_convert_second_attempt(obj,target_class,**attrs):
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
    
    See detailed presentation in :mod:`lino.test_apps.1.models`.

    """
    pk = obj.pk
    related_objects = {}
    assert target_class != obj.__class__
    if issubclass(target_class,obj.__class__):
        # convert parent to child (adding data) : "specialize", "promote"
        attrs["%s_ptr" % obj.__class__.__name__.lower()] = obj
        for field in obj._meta.fields:
            attrs[field.name] = getattr(obj, field.name)
        logger.info("specialize %s to %s : attrs=%s",
          obj.__class__.__name__,target_class.__name__,
          attrs)
    elif issubclass(obj.__class__,target_class):
        # convert child to parent (removing data) : "generalize", "reduce"
        for field in target_class._meta.fields:
            if field.name not in attrs and hasattr(obj, field.name):
                attrs[field.name] = getattr(obj, field.name)
        for r in target_class._meta.many_to_many:
            if getattr(r,'through',None) is not None:
                raise Exception("ManyToManyField.through not supported.")
            if hasattr(obj,r.name):
                m = getattr(obj,r.name)
                related_objects[r.name] = [x for x in m.all()]
        logger.info("generalize %s to %s : attrs=%s, related_objects=%s",
          obj.__class__.__name__,target_class.__name__,
          attrs,related_objects)
        obj.delete()
    else:
        raise NotImplementedError
    
    new_obj = target_class(**attrs)
    new_obj.save()
    if related_objects:
        for k,v in related_objects.items():
            #~ logger.info('%s = %s', f.name,[x for x in m.all()])
            setattr(new_obj,k,v)
        new_obj.save()
    obj.__class__ = InvalidModelInstance
    return new_obj

     
from django.db import models
from lino.tools import resolve_model
from lino.fields import VirtualField

class EnableChild(VirtualField):
    """
    Documented and tested in :mod:`lino.test_apps.1.models`
    """
    
    editable = True
    
    def __init__(self,child_model,**kw):
        self.child_model = child_model
        VirtualField.__init__(self,models.BooleanField(**kw),self.has_child)

    def lino_kernel_setup(self,model,name):
        self.child_model = resolve_model(self.child_model,model._meta.app_label)
        VirtualField.lino_kernel_setup(self,model,name)
    
    def has_child(self,obj,request=None):
        "Returns True if "
        try:
            getattr(obj,self.child_model.__name__.lower())
            #~ self.child_model.objects.get(pk=obj.pk)
        except self.child_model.DoesNotExist:
            return False
        return True

    def set_value_in_object(self,obj,v,request=None):
        if self.has_child(obj,request):
            logger.debug('set_value_in_object : %s has child %s',
                obj.__class__.__name__,self.child_model.__name__)
            # child exists, convert if it may not 
            if not v:
                delete_child(obj,self.child_model)
        else:
            logger.debug('set_value_in_object : %s has no child %s',
                obj.__class__.__name__,self.child_model.__name__)
            if v:
                # child doesn't exist. convert if it should
                insert_child(obj,self.child_model)
        # otherwise do nothing
                
