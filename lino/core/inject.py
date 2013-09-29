## Copyright 2011-2013 Luc Saffre
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

from django.conf import settings
from django.db.models.signals import class_prepared
from django.db.models.fields import FieldDoesNotExist
from django.dispatch import receiver

from lino.core import fields
from lino.core.signals import pre_analyze

PENDING_INJECTS = dict()
PREPARED_MODELS = dict()

def fix_field_cache(model):
    """
    Remove duplicate entries in `_field_cache` to fix Django issue #10808
    """
    cache = []
    field_names = set()
    for f,m in model._meta._field_cache:
        if f.attname not in field_names:
            field_names.add(f.attname)
            cache.append( (f,m) )
    model._meta._field_cache = tuple(cache)
    model._meta._field_name_cache = [x for x, _ in cache]
    #~ if model.__name__ in ('Company','Partner'):
        #~ logger.info("20130106 fixed field_cache %s (%s)",model,' '.join(field_names))


@receiver(class_prepared)
def on_class_prepared(sender,**kw):
    """
    This is Lino's general `class_prepared` handler.
    It does two things:
    
    - Run pending calls to :func:`inject_field` and :func:`update_field`.
    
    - Apply a workaround for Django's ticket 10808.
      In a Diamond inheritance pattern, `_meta._field_cache` contains certain fields twice.    
      So we remove these duplicate fields from `_meta._field_cache`.
      (A better solution would be of course to not collect them.)
    """
    #~ if sender.__name__ in ('Company','Partner'):
        #~ print("20130212 on_class_prepared",sender)
    model = sender
    #~ return
    #~ if model is None:
        #~ return 
    k = model._meta.app_label + '.' + model.__name__
    PREPARED_MODELS[k] = model
    #~ logger.info("20120627 on_class_prepared %r = %r",k,model)
    todos = PENDING_INJECTS.pop(k,None)
    if todos is not None:
        for f in todos:
            f(model)
        #~ for k,v in injects.items():
            #~ model.add_to_class(k,v)

    """
    django.db.models.options
    """
    if hasattr(model._meta,'_field_cache'):
        fix_field_cache(model)
    #~ else:
        #~ logger.info("20120905 Could not fix Django issue #10808 for %s",model)




@receiver(pre_analyze)
def check_pending_injects(sender,models_list=None,**kw): # def check_pending_injects(signal,sender,models_list=None,**kw): 
    # called from kernel.analyze_models()
    site = sender
    #~ logger.info("20130212 check_pending_injects()...")
    if PENDING_INJECTS:
        msg = ''
        for spec,funcs in PENDING_INJECTS.items():
            msg += spec + ': ' 
            #~ msg += '\n'.join([str(dir(func)) for func in funcs])
            #~ msg += '\n'.join([str(func.func_code.co_consts) for func in funcs])
            msg += str(funcs)
        raise Exception("Oops, there are pending injects: %s" % msg)
        #~ logger.warning("pending injects: %s", msg)

    """
    20130106
    now we loop a last time over each model and fill it's _meta._field_cache
    otherwise if some application module used inject_field() on a model which 
    has subclasses, then the new field would not be seen by subclasses
    """
    #~ for model in models.get_models():
    for model in models_list:
        model._meta._fill_fields_cache()
        fix_field_cache(model)

#~ from lino.core.dbutils import is_installed_model_spec

def do_when_prepared(todo,*model_specs):
    """
    Execute the specified function `todo` on all specified models, 
    but only when they are prepared. 
    If a specified model hasn't yet been prepared, 
    adds the call to a queue and execute it later.
    """
    for model_spec in model_specs:
        if model_spec is None:
            continue # e.g. inject_field during autodoc when user_model is None
            
        if isinstance(model_spec,basestring):
            if not settings.SITE.is_installed_model_spec(model_spec):
                continue
            k = model_spec
            model = PREPARED_MODELS.get(k,None)
            if model is None: 
                injects = PENDING_INJECTS.setdefault(k,[])
                injects.append(todo)
                #~ d[name] = field
                #~ if model_spec == "system.SiteConfig":
                    #~ logger.info("20130228 Defer %s for %s", todo, model_spec)
                continue
        else:
            model = model_spec
            #~ k = model_spec._meta.app_label + '.' + model_spec.__name__
        #~ if model._meta.abstract:
            #~ raise Exception("Trying do_when_prepared on abstract model %s" % model)
        todo(model)


def when_prepared(*model_specs):
    """
    Decorator to declare a function which will automatically run when 
    the specified models has been prepared.
    If the model has already been prepared, the function is executed 
    immediately.
    """
    def decorator(fn):
        return do_when_prepared(fn,*model_specs)
    return decorator
  
    

def inject_action(model_spec,**actions):
    """
    Add the specified action(s) to the specified model.
    """
    def todo(model):
        model.define_action(**actions)
    return do_when_prepared(todo,model_spec)    
    
def inject_field(model_spec,name,field,doc=None):
    """
    Add the given field to the given model.
    See also :doc:`/tickets/49`.
    
    Since `inject_field` is usually called at the global level 
    of `models modules`, it cannot know whether the given `model_spec` 
    has already been imported (and its class prepared) or not. 
    That's why it uses Django's `class_prepared` signal to maintain 
    its own list of models.
    """
    if doc:
        field.__doc__ = doc
    def todo(model):
        model.add_to_class(name,field)
        model._meta._fill_fields_cache()
        fix_field_cache(model)

    return do_when_prepared(todo,model_spec)    
    
    

def update_field(model_spec,name,**kw):
    """
    Update some attribute of the specified existing field.
    For example 
    :class:`PersonMixin <lino.modlib.contacts.models.PersonMixin>` 
    defines a field `first_name` which may not be blank.
    If you inherit from 
    :class:`PersonMixin <lino.modlib.contacts.models.PersonMixin>`
    but want `first_name` to be optional::
    
      class MyPerson(contacts.PersonMixin):
        ...
      dd.update_field(MyPerson,'first_name',blank=True)
      
    Or you want to change the label of a field defined in an inherited mixin,
    as done in  :mod:`lino.modlib.outbox.models`::
    
      dd.update_field(Mail,'user',verbose_name=_("Sender"))
    
    """
    def todo(model):
        try:
            fld = model._meta.get_field(name)
            #~ fld = model._meta.get_field_by_name(name)[0]
        except FieldDoesNotExist:
            logger.warning("Cannot update unresolved field %s.%s", model,name)
            return
        if fld.model != model:
            raise Exception('20120715 update_field(%s.%s) : %s' % (model,fld,fld.model))
            #~ logger.warning('20120715 update_field(%s.%s) : %s',model,fld,fld.model)
        for k,v in kw.items():
            setattr(fld,k,v)
        #~ if model.__name__ == "SiteConfig":
            #~ logger.info("20130228 updated field %s in %s",name,model)
    return do_when_prepared(todo,model_spec)    
        

def inject_quick_add_buttons(model,name,target):
    """
    Injects a virtual display field `name` into the specified `model`.
    This field will show up to three buttons
    `[New]` `[Show last]` `[Show all]`. 
    `target` is the table that will run these actions.
    It must be a slave of `model`.
    """
    def fn(self,ar):
        return ar.renderer.quick_add_buttons(
          ar.spawn(target,master_instance=self))
    inject_field(model,name,
        fields.VirtualField(fields.DisplayField(
            target.model._meta.verbose_name_plural),fn))
