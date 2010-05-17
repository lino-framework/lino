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

"""
Note that the following won't work because `contacs.Person` is abstract:

  >>> get_app('contacts')
  >>> p = contacts.Person(name="Foo")

The real contacts.Person is defined in your application (lino-dsbe and lino-igen). 
To get it, use resolve_model:

  >>> resolve_model('contacts.Person')
  >>> p = Person(name="Foo")
    

"""
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
      


def resolve_model(model_spec,app_label=None,who=None):
    # Same logic as in django.db.models.fields.related.add_lazy_relation()
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
            "resolve_model(%r,app_label=%r,who=%r) found %r" % (
            model_spec,app_label,who,model))
    return model
    
    


def resolve_field(name,app_label):
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
    
    