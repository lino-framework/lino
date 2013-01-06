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

"""modeltools may not be used in models modules (but well during lino_site set up).
"""

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
    """
    return len(sys.argv) > 1 and sys.argv[1] == 'runserver'


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

def resolve_model(model_spec,app_label=None,strict=False,seed_cache=True):
    """
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
            
        #~ model = models.get_model(app_label,model_name,seed_cache=False)
        model = models.get_model(app_label,model_name,seed_cache=seed_cache)
    else:
        model = model_spec
    if not isinstance(model,type) or not issubclass(model,models.Model):
        if strict:
            if isinstance(strict,basestring):
                raise Exception(strict % model_spec)
            raise Exception(
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

def makedirs_if_missing(dirname):
    """
    Make missing directories if they don't exist 
    and if :attr:`lino.Lino.make_missing_dirs` 
    is `True`.
    """
    #~ if not os.path.exists(dirname):
        #~ os.makedirs(dirname)
    if not os.path.isdir(dirname):
        if settings.LINO.make_missing_dirs:
            os.makedirs(dirname)
        else:
            raise Exception("Please create yourself directory %s" % dirname)
        
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
  




def app_labels():
    return [a.__name__.split('.')[-2] for a in loading.get_apps()]
        
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

    
def is_installed_model_spec(model_spec):
    app_label, model_name = model_spec.split(".")
    return settings.LINO.is_installed(app_label)
    
