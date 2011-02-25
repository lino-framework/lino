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


from django.conf import settings
from django.db import models
from django.utils.importlib import import_module


def get_app(app_label):
    """
    This is called in models modules instead of "from x.y import models as y"
    It is probably quicker than `loading.get_app()`.
    It doesn't work during loading.appcache._populate().
    Didn't test how they compare in multi-threading cases.
    
    """
    for app_name in settings.INSTALLED_APPS:
        if app_name.endswith('.'+app_label):
            return import_module('.models', app_name)
    #~ if not emptyOK:
    raise ImportError("No application labeled %r." % app_label)
      


def resolve_model(model_spec,app_label=None):
    # Same logic as in django.db.models.fields.related.add_lazy_relation()
    #~ from lino import site # needed to trigger site setup
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
        raise Exception(
            "resolve_model(%r,app_label=%r) found %r" % (
            model_spec,app_label,model))
    return model
    
def get_field(model,name):
    fld, remote_model, direct, m2m = model._meta.get_field_by_name(name)
    assert remote_model is None
    return fld
  

def resolve_field(name,app_label=None):
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
    
    
    
def model_label(model):
    return model._meta.app_label + '.' + model._meta.object_name
    
    
    
def obj2str(i,force_detailed=False):
    #~ if not force_detailed and i.pk is not None:
    assert isinstance(i,models.Model)
    if i.pk is None:
        force_detailed = True
    if not force_detailed:
        if i.pk is None:
            return u'(Unsaved %s instance)' % (i.__class__.__name__)
        try:
            return u"%s #%s (%s)" % (i.__class__.__name__,i.pk,i)
        except TypeError,e:
            print i.__class__.__name__,i.pk
            return unicode(e)
    names = [fld.name for (fld,model) in i._meta.get_fields_with_model()]
    s = ','.join(["%s=%r" % (n, getattr(i,n)) for n in names])
    #~ print i, i._meta.get_all_field_names()
    #~ s = ','.join(["%s=%r" % (n, getattr(i,n)) for n in i._meta.get_all_field_names()])
    return u"%s(%s)" % (i.__class__.__name__,s)


    
   
