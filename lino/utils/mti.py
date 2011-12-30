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
A collection of tools for working with
Multi-table inheritance (:doc:`/topics/mti`).

Tested and documented in :mod:`lino.test_apps.1.models`.

"""
import logging
logger = logging.getLogger(__name__)


from django.db import models
from django.db import router
from django.db.models.deletion import Collector

from lino.tools import resolve_model
from lino.core.fields import VirtualField


class MultiTableBase(models.Model):
    """
    Mixin for Models that use MTI.
    Subclassed by :class:`lino.modlib.journals.models.Journaled`.
    """
    class Meta:
        abstract = True
    
    def get_child_model(self):
        return self.__class__
        
    def get_child_instance(self):
        model = self.get_child_model()
        if model is self.__class__:
            return self
        related_name = model.__name__.lower()
        return getattr(self,related_name)
        
    def insert_child(self,*args,**attrs):
        return insert_child(self,*args,**attrs)


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
  
from django.core.exceptions import ValidationError

def get_child(obj,child_model):
    try:
        return child_model.objects.get(pk=obj.pk)
    except child_model.DoesNotExist:
        raise Exception("%s has no child in %s" % (obj,child_model.__name__))
  
def delete_child(obj,child_model,using=None,request=None):
    """
    Delete the `child_model` instance related to `obj` without 
    deleting `obj`.
    """
    #~ logger.info(u"delete_child %s from %s",child_model.__name__,obj)
    using = using or router.db_for_write(obj.__class__, instance=obj)
    child = get_child(obj,child_model)
    if request is not None:
        msg = child_model._lino_ddh.disable_delete(child,request)
        if msg:
            raise ValidationError(msg)
    logger.debug(u"Delete child %s from %s",child_model.__name__,obj)
    collector = ChildCollector(using=using)
    collector.collect([child],source=obj.__class__,nullable=True,collect_parents=False)
    collector.delete()
    

def insert_child(obj,child_model,**attrs):
    """
    Create and save an instance of `child_model` from existing `obj`.
    """
    #~ assert child_model != obj.__class__
    #~ if child_model == obj.__class__:
        #~ raise ValidationError(
            #~ "A %s cannot be parent for itself" % 
            #~ obj.__class__.__name__)
    parent_link_field = child_model._meta.parents.get(obj.__class__,None)
    if parent_link_field is None:
        raise ValidationError("A %s cannot be parent for a %s" % (
            obj.__class__.__name__,child_model.__name__))
    attrs[parent_link_field.name] = obj
    #~ for pm,pf in child_model._meta.parents.items(): # pm : parent model, pf : parent link field
        #~ attrs[pf.name] = obj
    #~ attrs["%s_ptr" % obj.__class__.__name__.lower()] = obj
    for field in obj._meta.fields:
        attrs[field.name] = getattr(obj, field.name)
    #~ logger.info(u"Promote %s to %s : attrs=%s",
        #~ obj.__class__.__name__,child_model.__name__,attrs)
    #~ logger.debug(u"Promote %s to %s",
        #~ obj.__class__.__name__,child_model.__name__)
    new_obj = child_model(**attrs)
    new_obj.save()
    return new_obj

#~ def insert_child_and_save(obj,child_model,**attrs):
    #~ """
    #~ Insert (create) and save a `child_model` instance of existing `obj`.
    #~ """
    #~ obj = insert_child(obj,child_model,**attrs)
    #~ obj.save()
    #~ return obj
    

     
class EnableChild(VirtualField):
    """
    Documented and tested in :mod:`lino.test_apps.1.models`
    """
    
    editable = True
    
    def __init__(self,child_model,**kw):
        kw.update(default=False)
        self.child_model = child_model
        VirtualField.__init__(self,models.BooleanField(**kw),self.has_child)
        
    def is_enabled(self,lh):
        """
        When a DetailLayout is inherited by an MTI 
        child, EnableChild fields must be disabled.
        """
        return lh.table.model != self.child_model and issubclass(self.child_model,lh.table.model)

    def lino_kernel_setup(self,model,name):
        self.child_model = resolve_model(self.child_model,model._meta.app_label)
        VirtualField.lino_kernel_setup(self,model,name)
    
    def has_child(self,obj,request=None):
        """
        Returns True if `obj` has an MTI child in `self.child_model`.
        The optional 2nd argument `request` (passed from
        `VirtualField.value_from_object`) is ignored.
        """
        try:
            getattr(obj,self.child_model.__name__.lower())
            #~ self.child_model.objects.get(pk=obj.pk)
        except self.child_model.DoesNotExist:
            return False
        return True

    def set_value_in_object(self,request,obj,v):
        if self.has_child(obj):
            #~ logger.debug('set_value_in_object : %s has child %s',
                #~ obj.__class__.__name__,self.child_model.__name__)
            # child exists, delete it if it may not 
            if not v:
                delete_child(obj,self.child_model,request=request)
        else:
            #~ logger.debug('set_value_in_object : %s has no child %s',
                #~ obj.__class__.__name__,self.child_model.__name__)
            if v:
                # child doesn't exist. insert if it should
                insert_child(obj,self.child_model)
                





def create_child(parent_model,pk_,child_model,**kw):
    """
    Similar to :func:`insert_child`, but very tricky. 
    Used by :mod:`lino.utils.dpy`
    See :mod:`lino.test_apps.1.models`.
    """
    parent_link_field = child_model._meta.parents.get(parent_model,None)
    if parent_link_field is None:
        raise ValidationError("A %s cannot be parent for a %s" % (
            parent_model.__name__,child_model.__name__))
    if True:
        ignored = {}
        for f in parent_model._meta.fields:
            if f.name in kw:
                ignored[f.name] = kw.pop(f.name)
        kw[parent_link_field.name+"_id"] = pk_ 
        if ignored:
            logging.warning(
              "create_child() %s %s from %s : ignored non-local fields %s",
              child_model.__name__,
              pk_,
              parent_model.__name__, 
              ignored)
        child_obj = child_model(**kw)
    else:
        attrs = {}
        attrs[parent_link_field.name+"_id"] = pk_
        #~ for lf in child_model._meta.local_fields:
        # backwards compat 20111211 : dpy fixtures created by Version 1.2.8 still 
        # specify also field values of parent_model. Ignore these silently
        # otherwise Django would also try to create a parent_model record.
        for f,m in child_model._meta.get_fields_with_model():
            if m is None or not issubclass(m,child_model):
            #~ if m is None or m is child_model or not issubclass(m,parent_model):
                if f.name in kw:
                    attrs[f.name] = kw.pop(f.name)
        if kw:
            logging.warning(
              "create_child() %s %s from %s : ignored non-local fields %s",
              child_model.__name__,
              pk_,
              parent_model.__name__, 
              kw)
        
        child_obj = child_model(**attrs)
    def full_clean(*args,**kw):
        pass
        
    def save(*args,**kw):
        kw.update(raw=True,force_insert=True)
        child_obj.save_base(**kw)
        
    child_obj.save = save
    child_obj.full_clean = full_clean
    return child_obj
        
