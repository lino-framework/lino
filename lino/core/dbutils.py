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
A collection of database utilities, i.e. Django-related

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


from djangosite.dbutils import obj2str, full_model_name, app_labels
from djangosite.dbutils import sorted_models_list
from djangosite.dbutils import is_devserver
from north.dbutils import resolve_model, UnresolvedModel


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
    try:
        return import_module('lino.modlib.%s.dummy' % app_label)
    except ImportError:
        if strict: 
            raise
            #~ raise Exception("strict resolve_app failed for app_label %r" % app_label)

#~ def get_models_for(app_label):
    #~ a = models.get_app(app_label)
    

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

    


    
        