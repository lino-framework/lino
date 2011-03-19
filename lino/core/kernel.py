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

import logging
logger = logging.getLogger(__name__)

import os
import sys
#~ import imp
import codecs

from django.conf import settings
from django.utils.importlib import import_module
from django.utils.functional import LazyObject
from django.db import models
#from django.shortcuts import render_to_response 
#from django.contrib.auth.models import User


from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sites.models import Site, RequestSite
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.template import RequestContext, Context, loader
from django.utils.http import urlquote, base36_to_int
from django.utils.translation import ugettext as _

from django.conf.urls.defaults import patterns, url, include
#auth = models.get_app('auth')
from django.contrib.auth import models as auth

from django.utils.safestring import mark_safe

import lino
        
from lino.utils import menus
from lino import reports, actions
from lino.utils import perms
from lino.utils import dblogger
#~ from lino.utils import babel
from lino.core import actors
from lino.core.coretools import app_labels, data_elems # , get_unbound_meth
from lino.utils import get_class_attr

from lino.tools import resolve_model, resolve_field, get_app, model_label, get_field
from lino.utils.config import load_config_files, find_config_file
from lino.reports import DetailLayout
from lino.utils import choosers
from lino import fields
from lino.models import get_site_config

def analyze_models():
    """
    This is a part of a Lino site setup.
    The Django Model definitions are done, now Lino analyzes them and does certain actions.
    
    - Load .dtl files and install them into `_lino_detail_layouts`
    - Install a DisableDeleteHandler for each Model into  `_lino_ddh`
    
    """
    
    ## The following causes django.db.models.loading.cache to 
    ## be populated. This must be done before calling actors.discover() 
    ## or resolve_model().

    models_list = models.get_models() # trigger django.db.models.loading.cache._populate()

    #~ if settings.MODEL_DEBUG:
    if False:
        apps = app_labels()
        logger.debug("%d applications: %s.", len(apps),", ".join(apps))
        logger.debug("%d MODELS:",len(models_list))
        i = 0
        for model in models_list:
            i += 1
            logger.debug("  %2d: %s.%s -> %r",i,model._meta.app_label,model._meta.object_name,model)
            logger.debug("      data_elems : %s",' '.join([de.name for de in data_elems(model)]))
        logger.info("Analyzing Models...")
        

    #~ ddhdict = {}
    for model in models.get_models():
        model._lino_ddh = DisableDeleteHandler(model)
        if hasattr(model,'before_save'): 
            raise Exception(
              "%s has a method before_save! see :doc:`/blog/2010/0804`, :doc:`/blog/2011/0226`" % 
              model)
        
        
    for model in models.get_models():
    
        model._lino_detail_layouts = []
        model._lino_ddh = DisableDeleteHandler(model)
            
        def loader(content,cd,filename):
            dtl = DetailLayout(content,filename,cd)
            model._lino_detail_layouts.append(dtl)
            
        load_config_files('%s.%s.*dtl' % (model._meta.app_label,model.__name__),loader)
            
        #~ if get_unbound_meth(model,'summary_row') is None:
        if get_class_attr(model,'summary_row') is None:
        #~ if not hasattr(model,'summary_row'):
            if len(model._lino_detail_layouts):
                def f(obj,ui,rr,**kw):
                    return u'<a href="%s" target="_blank">%s</a>' % (
                      ui.get_detail_url(obj,fmt='detail'),
                      #~ rr.get_request_url(str(obj.pk),fmt='detail'),
                      unicode(obj))
            else:
                def f(obj,ui,rr,**kw):
                    return unicode(obj)
            model.summary_row = f
            #~ print '20101111 installed summary_row for ', model
        
        #~ virts = []
        for k,v in model.__dict__.items():
            if isinstance(v,fields.VirtualField):
                v.lino_kernel_setup(model,k)
                #~ virts.append(v)
        #~ model._lino_virtual_fields = virts
            
        for f, m in model._meta.get_fields_with_model():
            if isinstance(f,models.ForeignKey):
                #~ print 20101104, model,f.rel.to
                #~ if not ddhdict.has_key(f.rel.to):
                    #~ assert issubclass(f.rel.to,models.Model), "%s.%s is %r (not a Model instance)" % (model,f.name,f.rel.to)
                    #~ ddhdict[f.rel.to] = DisableDeleteHandler(model)
                #~ ddhdict[f.rel.to].add_fk(model,f)
                f.rel.to._lino_ddh.add_fk(model,f)
                
    #~ for model,ddh in ddhdict.items():
        #~ logger.debug("install %s.disable_delete_handler(%s)",
          #~ model.__name__,ddh)
        #~ model.disable_delete_handler = ddh
        
from Cheetah.Template import Template as CheetahTemplate


class DisableDeleteHandler():
    def __init__(self,model):
        self.model = model
        self.fklist = []
        
    def add_fk(self,model,fk):
        self.fklist.append((model,fk))
        
    def __str__(self):
        return ','.join([m.__name__+'.'+fk.name for m,fk in self.fklist])
        
    def disable_delete(self,obj,request):
        #~ print 20101104, "called %s.disable_delete(%s)" % (obj,self)
        h = getattr(self.model,'disable_delete',None)
        if h is not None:
            msg = h(obj,request)
            if msg is not None:
                return msg
        for m,fk in self.fklist:
            kw = {}
            kw[fk.name] = obj
            n = m.objects.filter(**kw).count()
            if n:
                msg = _("Cannot delete %(self)s because %(count)d %(refs)s refer to it.") % dict(
                  self=obj,count=n,
                  refs=m._meta.verbose_name_plural or m._meta.verbose_name+'s')
                #~ print msg
                return msg
        return None
        

def setup_site(self):
  
    logger.info(lino.welcome_text())

    if self._setup_done:
        return
    if self._setting_up:
        #~ logger.warning("LinoSite.setup() called recursively.")
        #~ return 
        raise Exception("LinoSite.setup() called recursively.")
    self._setting_up = True
    
    self.configure(get_site_config())
  
    analyze_models()
    
    actors.discover()
    
    reports.discover()
    
    choosers.discover()
    
    #~ babel.discover() # would have to be called before model setup

    for a in actors.actors_list:
        #~ if isinstance(a,layouts.DetailLayout):
            a.setup()
    #~ for a in actors.actors_list:
        #~ if not isinstance(a,layouts.DetailLayout):
            #~ a.setup()

    #~ if settings.MODEL_DEBUG:
    if True:
        logger.debug("ACTORS:")
        for k in sorted(actors.actors_dict.keys()):
            a = actors.actors_dict[k]
            #~ logger.debug("%s -> %r",k,a.__class__)
            logger.debug("%s -> %r",k,a.debug_summary())
              
      
    self.main_menu = menus.Toolbar('main')
    #~ self.main_menu = menus.Menu("","Main Menu")
    
    self.setup_main_menu()
    
    #~ uis = []
    #~ for ui in settings.USER_INTERFACES:
        #~ logger.info("Starting user interface %s",ui)
        #~ ui_module = import_module(ui)
        #~ uis.append(ui_module.get_ui(self))
    #~ self.uis = uis
    
    #~ from lino.models import get_site_config
    #~ self.config = get_site_config()
    
    if settings.DEBUG:
        generate_dummy_messages(self)
        
    self._setup_done = True
    self._setting_up = False
    
    dblogger.info("Lino Site %r started.", self.title)
    dblogger.info(lino.welcome_text())
        

def generate_dummy_messages(self):
    fn = os.path.join(self.source_dir,'dummy_messages.py')
    #~ fn = os.path.join(os.path.dirname(__file__),'dummy_messages.py')
    f = file(fn,'w')
    f.write("# this file is generated by Lino\n")
    f.write("from django.utils.translation import ugettext\n")
    for m in self.dummy_messages:
        f.write("ugettext(%r)\n" % m)
    f.close()
    logger.info("Wrote %d dummy messages to %s ...", len(self.dummy_messages),fn)
  
        
