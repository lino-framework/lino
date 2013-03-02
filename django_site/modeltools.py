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

from django.core.validators import validate_email, ValidationError, URLValidator
validate_url = URLValidator()
def is_valid_url(s):
    try:
        validate_url(s)
        return True
    except ValidationError:
        return False
        
def is_valid_email(s):
    try:
        validate_email(s)
        return True
    except ValidationError:
        return False
        
        
    
def is_devserver():
    """
    Returns True if we are running a development server.
    
    Thanks to Aryeh Leib Taurog in 
    `How can I tell whether my Django application is running on development server or not?
    <http://stackoverflow.com/questions/1291755>`_
    
    Added the `len(sys.argv) > 1` test because in a 
    wsgi application the process is called without arguments.
    
    Not only for `runserver` but also for `testserver`.
    """
    return len(sys.argv) > 1 and sys.argv[1] in ('runserver','testserver')



def full_model_name(model,sep='.'):
    """Returns the "full name" of the given model, e.g. "contacts.Person" etc.
    """
    return model._meta.app_label + sep + model._meta.object_name
    
    
    
def obj2unicode(i):
    """Returns a user-friendly unicode representation of a model instance."""
    return u'%s "%s"' % (i._meta.verbose_name,unicode(i))
    
def obj2str(i,force_detailed=False):
    """
    Returns a human-readable ascii string representation of a model instance, 
    even in some edge cases.
    """
    if not isinstance(i,models.Model): 
        if isinstance(i,long): return str(i) # AutoField is long on mysql, int on sqlite
        if isinstance(i,datetime.date): return i.isoformat()
        if isinstance(i,unicode): return repr(i)[1:]
        return repr(i)
    if i.pk is None:
        force_detailed = True
    if not force_detailed:
        if i.pk is None:
            return '(Unsaved %s instance)' % (i.__class__.__name__)
        try:
            return u"%s #%s (%s)" % (i.__class__.__name__,str(i.pk),repr(unicode(i)))
        except Exception,e:
        #~ except TypeError,e:
            return "Unprintable %s(pk=%r,error=%r" % (
              i.__class__.__name__,i.pk,e)
            #~ return unicode(e)
    #~ names = [fld.name for (fld,model) in i._meta.get_fields_with_model()]
    #~ s = ','.join(["%s=%r" % (n, getattr(i,n)) for n in names])
    pairs = []
    for (fld,model) in i._meta.get_fields_with_model():
        #~ if fld.name == 'language':
            #~ print 20120905, model, fld
        if isinstance(fld,models.ForeignKey):
            v = getattr(i,fld.attname) 
            #~ v = getattr(i,fld.name+"_id") 
            #~ if getattr(i,fld.name+"_id") is not None:
                #~ v = getattr(i,fld.name)
        else:
            v = getattr(i,fld.name)
        if v:
            pairs.append("%s=%s" % (fld.name,obj2str(v)))
    s = ','.join(pairs)
    #~ s = ','.join(["%s=%s" % (n, obj2str(getattr(i,n))) for n in names])
    #~ print i, i._meta.get_all_field_names()
    #~ s = ','.join(["%s=%r" % (n, getattr(i,n)) for n in i._meta.get_all_field_names()])
    return "%s(%s)" % (i.__class__.__name__,s)
    #~ return "%s(%s)" % (i.__class__,s)


def sorted_models_list():
    models_list = models.get_models() # trigger django.db.models.loading.cache._populate()
    def fn(a,b):
        return cmp(full_model_name(a),full_model_name(b))
    models_list.sort(fn)
    return models_list

def models_by_base(base):
    """
    Yields a list of installed models that are 
    subclass of the given base class.
    """
    for m in models.get_models():
        if issubclass(m,base):
            yield m
    
#~ models_by_abc = models_by_base

def app_labels():
    return [a.__name__.split('.')[-2] for a in loading.get_apps()]
        

def range_filter(v,f1,f2):
    """
    Returns a Q object (to be added as a filter on a queryset)
    to inlude only instances where v is contained within the range between f1 and f2.
    `v` being a value and f1 and f2 being the names of fields of same data type as v.
    """
    #~ filter = Q(**{f2+'__isnull':False}) | Q(**{f1+'__isnull':False})
    q1 = Q(**{f1+'__isnull':True}) | Q(**{f1+'__lte':v})
    q2 = Q(**{f2+'__isnull':True}) | Q(**{f2+'__gte':v})
    return Q(q1,q2)
  

