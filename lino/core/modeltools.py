# -*- coding: UTF-8 -*-
## Copyright 2009-2013 Luc Saffre
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

"""

from __future__ import unicode_literals


import logging
logger = logging.getLogger(__name__)


import os
import sys
import datetime

from django.db import models
from django.conf import settings
from django.db.models import Q
from django.db.models.fields import FieldDoesNotExist
from django.utils.importlib import import_module
from django.db.models import loading

#~ from django_site.modeltools import 


def resolve_app(app_label,strict=False):
    """
    Return the `modules` module of the given `app_label` if it is installed. 
    Otherwise return either the :term:`dummy module` for `app_label` 
    if it exists, or `None`.
    If the optional second argument `strict` is `True`, then 
    
    This function is designed for use in models modules and available 
    through the shortcut ``dd.resolve_app``.
    
    For example, instead of writing::
    
        from lino.modlib.contacts import models as contacts
        
    it is recommended to write::
        
        contacts = dd.resolve_app('contacts')
        
    Because it makes your code usable 
    (1) in applications that don't have the 'contacts' module installed
    and
    (2) in applications who have another implementation of the contacts module.
    
    """
    #~ app_label = app_label
    for app_name in settings.INSTALLED_APPS:
        if app_name == app_label or app_name.endswith('.'+app_label):
            return import_module('.models', app_name)
    #~ return import_module('lino.modlib.%s.dummy' % app_label)
    try:
        return import_module('lino.modlib.%s.dummy' % app_label)
    except ImportError:
        if strict: 
            raise
            #~ raise Exception("strict resolve_app failed for app_label %r" % app_label)
        
    #~ if not emptyOK:
    #~ raise ImportError("No application labeled %r." % app_label)
#~ resolve_app = get_app

#~ def get_models_for(app_label):
    #~ a = models.get_app(app_label)
    
class UnresolvedModel:
    """
    This is the object returned by :func:`resolve_model` 
    if the specified model is not installed.
    
    We don't want resolve_model to raise an Exception because there are 
    cases of :doc:`data migration </topics/datamig>` where it would 
    disturb. 
    Asking for a non-installed model is not a sin, but trying to use it is.
    
    I didn't yet bother very much about finding a way to make the 
    model_spec appear in error messages such as
    ``AttributeError: UnresolvedModel instance has no attribute '_meta'``.
    Current workaround is to uncomment the ``print`` statement 
    below in such situations...
    
    """
    def __init__(self,model_spec,app_label):
        self.model_spec = model_spec
        self.app_label = app_label
        #~ print repr(self)
        
    def __repr__(self):
        return self.__class__.__name__ + '(%s,%s)' % (self.model_spec,self.app_label)
        
    #~ def __getattr__(self,name):
        #~ raise AttributeError("%s has no attribute %r" % (self,name))

#~ def resolve_model(model_spec,app_label=None,strict=False,seed_cache=True):
def resolve_model(model_spec,app_label=None,strict=False):
    """
    Return the class object of the specified model.
    This works also in combination  with :attr:`lino.Lino.override_modlib_models`,
    so you don't need to worry about where the real class definition is.
    
    Attention: this function **does not** trigger a loading of Django's 
    model cache, so you should not use it at module-level unless you 
    know what you do.
    
    For example,    
    ``dd.resolve_model("contacts.Person")`` 
    will return the `Person` model 
    
    if the concrete Person model is not defined 
    This works also if the concrete Person model is not defined 
    in `lino.modlib.contacts.models` because it is in
    :attr:`lino.Lino.override_modlib_models`.
    
    Note: when use this 
    :func:`resolve_model <lino.core.modeltools.resolve_model>`
    See also django.db.models.fields.related.add_lazy_relation()
    """
    #~ models.get_apps() # trigger django.db.models.loading.cache._populate()
    if isinstance(model_spec,basestring):
        if '.' in model_spec:
            app_label, model_name = model_spec.split(".")
        else:
            model_name = model_spec
            
        #~ try:
            #~ app_label, model_name = model_spec.split(".")
        #~ except ValueError:
            #~ # If we can't split, assume a model in current app
            #~ #app_label = rpt.app_label
            #~ model_name = model_spec
            
        model = models.get_model(app_label,model_name,seed_cache=False)
        #~ model = models.get_model(app_label,model_name,seed_cache=seed_cache)
    else:
        model = model_spec
    if not isinstance(model,type) or not issubclass(model,models.Model):
        if strict:
            if False:
                from django.db.models import loading
                print 20130219, settings.INSTALLED_APPS
                print loading.get_models()
                #~ if len(loading.cache.postponed) > 0:
              
            if isinstance(strict,basestring):
                raise Exception(strict % model_spec)
            raise ImportError(
                "resolve_model(%r,app_label=%r) found %r (settings %s)" % (
                model_spec,app_label,model,settings.SETTINGS_MODULE))
        #~ logger.info("20120628 unresolved %r",model)
        return UnresolvedModel(model_spec,app_label)
    return model
    
def old_resolve_model(model_spec,app_label=None,strict=False):
    """
    doesn't work for contacts.Company because the model is defined somewhere else.
    """
    models.get_apps() # trigger django.db.models.loading.cache._populate()
    if isinstance(model_spec,basestring):
        if '.' in model_spec:
            app_label, model_name = model_spec.split(".")
        else:
            model_name = model_spec
        app = resolve_app(app_label)
        model = getattr(app,model_name,None)
    else:
        model = model_spec
    if not isinstance(model,type) or not issubclass(model,models.Model):
        if strict:
            raise Exception(
                "resolve_model(%r,app_label=%r) found %r (settings %s)" % (
                model_spec,app_label,model,settings.SETTINGS_MODULE))
        return UnresolvedModel(model_spec,app_label)
    return model
    
def get_field(model,name):
    '''Returns the field descriptor of the named field in the specified model.
    '''
    for vf in model._meta.virtual_fields:
        if vf.name == name:
            return vf
    fld, remote_model, direct, m2m = model._meta.get_field_by_name(name)
    # see blog/2011/0525
    #~ if remote_model is not None:
        #~ raise Exception("get_field(%r,%r) got a remote model ?!" % (model,name))
    return fld
  
class UnresolvedField(object):
    """
    Returned by :func:`resolve_field` if the specified field doesn't exist.
    This case happens when sphinx autodoc tries to import a module.
    See ticket :doc:`/tickets/4`.
    """
    def __init__(self,name):
        self.name = name
        self.verbose_name = "Unresolved Field " + name

def resolve_field(name,app_label=None):
    """
    Returns the field descriptor specified by the string `name` which 
    should be either `model.field` or `app_label.model.field`.
    """
    l = name.split('.')
    if len(l) == 3:
        app_label = l[0]
        del l[0]
    if len(l) == 2:
        #print "models.get_model(",app_label,l[0],False,")"
        #~ model = models.get_model(app_label,l[0],False)
        model = models.get_model(app_label,l[0])
        if model is None:
            raise FieldDoesNotExist("No model named '%s.%s'" % (app_label,l[0]))
        fld, remote_model, direct, m2m = model._meta.get_field_by_name(l[1])
        #~ try:
            #~ fld, remote_model, direct, m2m = model._meta.get_field_by_name(l[1])
        #~ except FieldDoesNotExist:
            #~ return UnresolvedField(name)
        assert remote_model is None or issubclass(model,remote_model), \
            "resolve_field(%r) : remote model is %r (expected None or base of %r)" % (name,remote_model,model)
        return fld
    raise FieldDoesNotExist(name)
    #~ return UnresolvedField(name)


#~ def requires_apps(self,*app_labels):
    #~ for app_label in app_labels:
        #~ get_app(app_label)
    
    
    



#~ def get_slave(model,name):
    #~ """Return the named table, knowing that it is a 
    #~ slave of the specified `model`. 
    #~ If name has no app_label specified, use the model's app_label.
    #~ """
    #~ if not '.' in name:
        #~ name = model._meta.app_label + '.' + name
    #~ rpt = actors.get_actor(name)
    #~ if rpt is None: 
        #~ return None
    #~ return rpt

def get_model_report(model):
    if not hasattr(model,'_lino_default_table'):
        raise Exception("%r has no _lino_default_table" % model)
    return model._lino_default_table

    


    
        