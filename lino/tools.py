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
The Lino process creates a list config_dirs of all configuration directories on server startup
by looping through :setting:`INSTALLED_APPS` that have a :xfile:`config` 
subdir.

"""

import os
from fnmatch import fnmatch

from django.conf import settings
from django.db import models
from django.utils.importlib import import_module


config_dirs = []
LOCAL_CONFIG_DIR = None

class ConfigDir:
    """
    A configuration directory is a directories that may contain configuration files.
    
    """
    def __init__(self,name,can_write):
        self.name = name
        self.can_write = can_write
    def __str__(self):
        return "ConfigDir %s" % self.name
      

for app_name in settings.INSTALLED_APPS:
    app = import_module(app_name)
    fn = getattr(app,'__file__',None)
    if fn is not None:
        dirname = os.path.join(os.path.dirname(fn),'config')
        if os.path.isdir(dirname):
            config_dirs.append(ConfigDir(dirname,False))
    LOCAL_CONFIG_DIR = ConfigDir(os.path.join(settings.PROJECT_DIR,'config'),True)
    config_dirs.append(LOCAL_CONFIG_DIR)

def find_config_files(pattern):
    """Returns a dict of filename -> config_dir entries for 
    each config file on this site that matches the pattern.
    Loops through `config_dirs` and collects matching files. 
    When more than one file of the same name exists in different 
    applications it gets overridden by later apps.
    """
    
    files = {}
    for cd in config_dirs:
        #~ print 'find_config_files() discover', dirname, pattern
        for fn in os.listdir(cd.name):
            if fnmatch(fn,pattern):
                #~ if not files.has_key(fn):
                files[fn] = cd
        #~ else:
            #~ print 'find_config_files() not a directory:', dirname
    return files


def default_language():
    """
    Returns the default language of this website,
    as defined by :setting:`LANGUAGE_CODE` in your :xfile:`settings.py`.
    """
    #~ from django.conf import settings
    return settings.LANGUAGE_CODE[:2]
    

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
    
    
    
def obj2str(i):
    names = [fld.name for (fld,model) in i._meta.get_fields_with_model()]
    s = ','.join(["%s=%r" % (n, getattr(i,n)) for n in names])
    #~ print i, i._meta.get_all_field_names()
    #~ s = ','.join(["%s=%r" % (n, getattr(i,n)) for n in i._meta.get_all_field_names()])
    return "%s(%s)" % (i.__class__.__name__,s)

   
