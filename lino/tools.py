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


from django.conf import settings
from django.db import models
from django.utils.importlib import import_module


def get_app(app_label):
    """
    This is called in models modules instead of "from x.y import models as y"
    It is probably quicker than `django.db.loading.get_app()`.
    May not be called during loading.appcache._populate().
    Didn't test how they compare in multi-threading cases.
    
    """
    for app_name in settings.INSTALLED_APPS:
        if app_name.endswith('.'+app_label):
            return import_module('.models', app_name)
    #~ if not emptyOK:
    raise ImportError("No application labeled %r." % app_label)
resolve_app = get_app      

def get_models_for(app_label):
    a = models.get_app(app_label)
    
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

def resolve_model(model_spec,app_label=None):
    """
    Similar logic as in django.db.models.fields.related.add_lazy_relation()
    """
    models.get_apps() # trigger django.db.models.loading.cache._populate()
    if isinstance(model_spec,basestring):
        try:
            app_label, model_name = model_spec.split(".")
        except ValueError:
            # If we can't split, assume a model in current app
            #app_label = rpt.app_label
            model_name = model_spec
        model = models.get_model(app_label,model_name,False)
    else:
        model = model_spec
    if not isinstance(model,type) or not issubclass(model,models.Model):
        return UnresolvedModel(model_spec,app_label)
        #~ raise Exception(
            #~ "resolve_model(%r,app_label=%r) found %r" % (
            #~ model_spec,app_label,model))
    return model
    
def get_field(model,name):
    '''Returns the field descriptor of the named field in the specified model.
    '''
    fld, remote_model, direct, m2m = model._meta.get_field_by_name(name)
    # see blog/2011/0525
    #~ if remote_model is not None:
        #~ raise Exception("get_field(%r,%r) got a remote model ?!" % (model,name))
    return fld
  

def resolve_field(name,app_label=None):
    """Returns the field descriptor specified by the string `name` which 
    should be either `model.field` or `app.model.field`.
    """
    l = name.split('.')
    if len(l) == 3:
        app_label = l[0]
        del l[0]
    if len(l) == 2:
        #print "models.get_model(",app_label,l[0],False,")"
        model = models.get_model(app_label,l[0],False)
        fld, remote_model, direct, m2m = model._meta.get_field_by_name(l[1])
        assert remote_model is None
        return fld


def requires_apps(self,*app_labels):
    for app_label in app_labels:
        get_app(app_label)
    
    
    
def full_model_name(model):
    """Returns the "full name" of the specified model, e.g. "contacts.Person" etc.
    """
    return model._meta.app_label + '.' + model._meta.object_name
    
    
    
def obj2str(i,force_detailed=False):
    """
    Returns a usable unicode string representation of a model instance, 
    even in some edge cases.
    """
    #~ if not force_detailed and i.pk is not None:
    if not isinstance(i,models.Model): return repr(i)
    if i.pk is None:
        force_detailed = True
    if not force_detailed:
        if i.pk is None:
            return '(Unsaved %s instance)' % (i.__class__.__name__)
        try:
            return u"%s #%s (%s)" % (i.__class__.__name__,repr(i.pk),repr(unicode(i)))
        except Exception,e:
        #~ except TypeError,e:
            return u"Unprintable %s(pk=%s,error=%s" % (
              i.__class__.__name__,repr(i.pk),e)
            #~ return unicode(e)
    #~ names = [fld.name for (fld,model) in i._meta.get_fields_with_model()]
    #~ s = ','.join(["%s=%r" % (n, getattr(i,n)) for n in names])
    pairs = []
    for (fld,model) in i._meta.get_fields_with_model():
        v = getattr(i,fld.name)
        if v:
            pairs.append("%s=%s" % (fld.name,obj2str(v)))
    s = ','.join(pairs)
    #~ s = ','.join(["%s=%s" % (n, obj2str(getattr(i,n))) for n in names])
    #~ print i, i._meta.get_all_field_names()
    #~ s = ','.join(["%s=%r" % (n, getattr(i,n)) for n in i._meta.get_all_field_names()])
    return "%s(%s)" % (i.__class__.__name__,s)


def sorted_models_list():
    models_list = models.get_models() # trigger django.db.models.loading.cache._populate()
    def fn(a,b):
        return cmp(full_model_name(a),full_model_name(b))
    models_list.sort(fn)
    return models_list
    

    
   
