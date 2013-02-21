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

from __future__ import unicode_literals


import logging
logger = logging.getLogger(__name__)

import os
import sys
#~ import imp
import codecs
import atexit
#~ import collections
from UserDict import IterableUserDict

from django.db.models import loading
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.functional import LazyObject
from django.db import models
#from django.shortcuts import render_to_response 
#from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sites.models import Site, RequestSite
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.template import RequestContext, Context, loader
from django.utils.http import urlquote, base36_to_int
from django.utils.translation import ugettext as _

from django.utils.safestring import mark_safe

import lino
        
from lino import dd
#~ from lino.core import signals
from lino.core import actions
from lino.core import fields
from lino.core import layouts
from lino.core import actors
from lino.core import dbtables
from lino.core.modeltools import app_labels # , data_elems # , get_unbound_meth
from lino.utils import get_class_attr, class_dict_items

from lino.core.modeltools import resolve_model, resolve_field, get_field, full_model_name, obj2str
    
from lino.utils.config import load_config_files, find_config_file
from lino.utils import choosers
#~ from lino.utils import codetime
from lino.utils import curry
#~ from lino.models import get_site_config
from lino.utils import babel
from lino.utils import AttrDict
#~ from lino.core import perms

#~ BLANK_STATE = ''


DONE = False

#~ self.GFK_LIST = []


def analyze_models(self):
    """
    This is a part of a Lino site setup.
    The Django Model definitions are done, now Lino analyzes them and does certain actions.
    
    - Verify that there are no more pending injects
    - Install a DisableDeleteHandler for each Model into `_lino_ddh`
    - Install :class:`lino.dd.Model` attributes and methods into Models that
      don't inherit from it.
    
    """
    #~ print 20130219, __file__, "setup_choicelists 1"
    
    global DONE
    if DONE: 
        #~ print "20130219 DONE"
        return
    DONE = True
    
    #~ logger.info("Analyzing models...")
    
    #~ self = settings.LINO
    #~ logger.info(self.welcome_text())
    
    """
    Set the site's default language
    """
    babel.set_language(None)
            
    #~ logger.info(lino.welcome_text())
    #~ raise Exception("20111229")
    
    models_list = models.get_models(include_auto_created=True) 
    # this also triggers django.db.models.loading.cache._populate()
    
    if self.user_model:
        self.user_model = resolve_model(self.user_model,
            strict="Unresolved model '%s' in user_model.")
    #~ if self.person_model:
        #~ self.person_model = resolve_model(self.person_model,strict="Unresolved model '%s' in person_model.")
        
    #~ print 20130219, __file__, "setup_choicelists 2"
    
    if self.project_model:
        self.project_model = resolve_model(self.project_model,
            strict="Unresolved model '%s' in project_model.")
        
    #~ print 20130219, __file__, "setup_choicelists 3"
    
    for m in self.override_modlib_models:
        resolve_model(m,
            strict="Unresolved model '%s' in override_modlib_models.")
    
    for model in models_list:
        #~ print 20130216, model
        #~ fix_field_cache(model)
      
        model._lino_ddh = DisableDeleteHandler(model)
        
        for k in dd.Model.LINO_MODEL_ATTRIBS:
            if not hasattr(model,k):
                #~ setattr(model,k,getattr(dd.Model,k))
                setattr(model,k,dd.Model.__dict__[k])
                #~ model.__dict__[k] = getattr(dd.Model,k)
                #~ logger.info("20121127 Install default %s for %s",k,model)
              
        if isinstance(model.hidden_columns,basestring):
            model.hidden_columns = frozenset(dd.fields_list(model,model.hidden_columns))

        if model._meta.abstract:
            raise Exception("Tiens?")
            
        self.modules.define(model._meta.app_label,model.__name__,model)
                
        for f in model._meta.virtual_fields:
            if isinstance(f,generic.GenericForeignKey):
                settings.LINO.GFK_LIST.append(f)
                
    dd.pre_analyze.send(self,models_list=models_list)
    self.setup_choicelists()
    self.setup_workflows()
    
    for model in models_list:
        
        for f, m in model._meta.get_fields_with_model():
            #~ if isinstance(f,models.CharField) and f.null:
            if f.__class__ is models.CharField and f.null:
                msg = "Nullable CharField %s in %s" % (f.name,model)
                raise Exception(msg)
                #~ if f.__class__ is models.CharField:
                    #~ raise Exception(msg)
                #~ else:
                    #~ logger.info(msg)
            elif isinstance(f,models.ForeignKey):
                if isinstance(f.rel.to,basestring):
                    raise Exception("%s %s relates to %r" % (model,f.name,f.rel.to))
                if f.verbose_name == f.name.replace('_', ' '):
                    """
                    If verbose name was not set by user code, 
                    Django sets it to ``field.name.replace('_', ' ')``.
                    We replace this default value by
                    ``f.rel.to._meta.verbose_name``.
                    """
                    f.verbose_name = f.rel.to._meta.verbose_name
                    
                """
                If JobProvider is an MTI child of Company,
                then mti.delete_child(JobProvider) must not fail on a 
                JobProvider being refered only by objects that can refer 
                to a Company as well.
                """
                if hasattr(f.rel.to,'_lino_ddh'):
                    #~ f.rel.to._lino_ddh.add_fk(model,f) # 20120728
                    f.rel.to._lino_ddh.add_fk(m or model,f)
                        
    #~ for model in models.get_models():

            #~ for k,v in class_dict_items(model):
                #~ if isinstance(v,dd.VirtualField):
                    #~ v.lino_resolve_type()
                    
                    
    
    for a in models.get_apps():
        #~ for app_label,a in loading.cache.app_store.items():
        app_label = a.__name__.split('.')[-2]
        #~ logger.info("Installing %s = %s" ,app_label,a)
        
        for k,v in a.__dict__.items():
            if isinstance(v,type) and issubclass(v,layouts.BaseLayout):
                #~ print "%s.%s = %r" % (app_label,k,v)
                self.modules.define(app_label,k,v)
            #~ if isinstance(v,type)  and issubclass(v,dd.Module):
                #~ logger.info("20120128 Found module %s",v)
            if k.startswith('setup_'):
                self.modules.define(app_label,k,v)
                    
    for model in models_list:
      
        """
        Virtual fields declared on the model must have 
        been attached before calling Model.site_setup(), 
        e.g. because pcsw.Person.site_setup() 
        declares `is_client` as imported field.
        """
      
        model.on_analyze(self)
            
        for k,v in class_dict_items(model):
            if isinstance(v,dd.VirtualField):
                v.attach_to_model(model,k)
                    
                    
    actors.discover()
    
    dbtables.discover()
    
    choosers.discover()
                    
    #~ from lino.core import ui
    #~ ui.site_setup(self)
        
    #~ logger.info("20130121 GFK_LIST is %s",['%s.%s'%(full_model_name(f.model),f.name) for f in settings.LINO.GFK_LIST])
    dd.post_analyze.send(self,models_list=models_list)
    
    if len(sys.argv) == 0:
        process_name = 'WSGI'
    else:
        process_name = ' '.join(sys.argv)
    logger.info("Started %s on %r. Languages: %s. %d models, %s actors.", 
    #~ logger.info("Lino Site %r started. Languages: %s. %d models, %s actors.", 
        process_name,self.title, ', '.join(babel.AVAILABLE_LANGUAGES),
        len(models_list),
        len(actors.actors_list))
    #~ logger.info(settings.INSTALLED_APPS)
    
    def goodbye():
        logger.info("Stopped %s",process_name)
    atexit.register(goodbye)
    
    return models_list

class DisableDeleteHandler():
    """
    Used to find out whether a known object can be deleted or not.
    Lino's default behaviour is to forbit deletion if there is any other 
    object in the database that refers to this. To implement this, 
    Lino installs a DisableDeleteHandler instance on each model 
    during :func:`analyze_models`. In an attribute `_lino_ddh`.
    """
    def __init__(self,model):
        self.model = model
        self.fklist = []
        
    def add_fk(self,model,fk):
        self.fklist.append((model,fk))
        
    def __str__(self):
        return ','.join([m.__name__+'.'+fk.name for m,fk in self.fklist])
        
    def disable_delete_on_object(self,obj):
        #~ print 20101104, "called %s.disable_delete(%s)" % (obj,self)
        #~ h = getattr(self.model,'disable_delete',None)
        #~ if h is not None:
            #~ msg = h(obj,ar)
        #~     if msg is not None:
            #~     return msg
        for m,fk in self.fklist:
            #~ kw = {}
            #~ kw[fk.name] = obj
            #~ if not getattr(m,'allow_cascaded_delete',False):
            if not fk.name in m.allow_cascaded_delete:
                n = m.objects.filter(**{fk.name : obj}).count()
                if n:
                    msg = _("Cannot delete %(self)s because %(count)d %(refs)s refer to it.") % dict(
                      self=obj,count=n,
                      refs=m._meta.verbose_name_plural or m._meta.verbose_name+'s')
                    #~ print msg
                    return msg
        return None
        


def startup_site(self):
    """
    This is the code that runs when you call :meth:`lino.Lino.startup`.
    """
    
    logger.info(self.welcome_text())
    
    analyze_models(self)
    
    self.on_each_app('site_setup')
    
    """
    Actor.after_site_setup() is called after the app's site_setup().
    Example: pcsw.site_setup() adds a detail to properties.Properties, 
    the base class for properties.PropsByGroup. 
    The latter would not 
    install a detail_action during her after_site_setup() 
    and also would never get it later.
    """
    for a in actors.actors_list:
        a.after_site_setup(self)
        
    self.on_site_startup()
        
    """
    resolve_virtual_fields() comes even after after_site_setup() 
    because after_site_setup()
    may add more virtual fields in custom setup_columns methods.
    """
            
    fields.resolve_virtual_fields()
    


def unused_generate_dummy_messages(self):
    fn = os.path.join(self.source_dir,'dummy_messages.py')
    self.dummy_messages
    raise Exception("use write_message_file() instead!")
    

