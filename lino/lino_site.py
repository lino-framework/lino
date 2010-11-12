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
Importing this module will instantiate the :class:`LinoSite`. 
This will automatically happen when your Django server gets its first web request 
because the :xfile:`urls.py` of a Lino website contains::

    from lino import lino_site
    urlpatterns = patterns('',
        (r'', include(lino_site.get_urls())),
    )
    
The LinoSite first makes sure that the django.db.models.loading.cache is populated. 
Then it analyzes the models and finds the corresponding Reports and Layouts.

"""

import logging
logger = logging.getLogger(__name__)

import os
import sys
#~ import imp

from django.conf import settings
from django.utils.importlib import import_module

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
        
from lino import reports, actions
from lino.utils import perms
from lino.utils import menus
from lino.core import actors
from lino.core.coretools import app_labels, data_elems, get_unbound_meth

from lino.tools import resolve_model, resolve_field, get_app, model_label, get_field, find_config_files
from lino.reports import DetailLayout

## The following not only logs diagnostic information, it also has an 
## important side effect: it causes django.db.models.loading.cache to 
## be populated. This must be done before calling actors.discover().

apps = app_labels()
logger.debug("%d applications: %s.", len(apps),", ".join(apps))
models_list = models.get_models() # populates django.db.models.loading.cache 

if settings.MODEL_DEBUG:
    logger.debug("%d MODELS:",len(models_list))
    i = 0
    for model in models_list:
        i += 1
        logger.debug("  %2d: %s.%s -> %r",i,model._meta.app_label,model._meta.object_name,model)
        logger.debug("      data_elems : %s",' '.join([de.name for de in data_elems(model)]))

from lino.utils import choosers


def discover():
    
    logger.info("Analyzing Models...")
    ddhdict = {}
    for model in models.get_models():
    
        model._lino_detail_layouts = []
        """
        Naming conventions for :xfile:`*.dtl` files are:
        
        - the first detail is called appname.Model.dtl
        - If there are more Details, then they are called 
          appname.Model.2.dtl, appname.Model.3.dtl etc.
        
        The `sort()` below must remove the filename extension (".dtl") 
        because otherwise the frist Detail would come last.
        """
        dtl_files = find_config_files('%s.%s.*dtl' % (model._meta.app_label,model.__name__)).items()
        def fcmp(a,b):
            return cmp(a[0][:-4],b[0][:-4])
        dtl_files.sort(fcmp)
        for filename,cd in dtl_files:
            fn = os.path.join(cd.name,filename)
            logger.info("Loading %s...",fn)
            s = open(fn).read()
            dtl = DetailLayout(s,cd,filename)
            model._lino_detail_layouts.append(dtl)
            
        if get_unbound_meth(model,'summary_row') is None:
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
        
            
            
        for f, m in model._meta.get_fields_with_model():
            if isinstance(f,models.ForeignKey):
                #~ print 20101104, model,f.rel.to
                if not ddhdict.has_key(f.rel.to):
                    ddhdict[f.rel.to] = DisableDeleteHandler(model)
                ddhdict[f.rel.to].add_fk(model,f)
                
    for model,ddh in ddhdict.items():
        if not hasattr(model,'disable_delete'):
            logger.debug("install %s.disable_delete(%s)",
              model.__name__,ddh)
            model.disable_delete = ddh.handler()

class DisableDeleteHandler():
    def __init__(self,model):
        self.model = model
        self.fklist = []
        
    def add_fk(self,model,fk):
        self.fklist.append((model,fk))
        
    def __str__(self):
        return ','.join([m.__name__+'.'+fk.name for m,fk in self.fklist])
        
    def handler(self):
        def disable_delete(obj,request):
            #~ print 20101104, "called %s.disable_delete(%s)" % (obj,self)
            
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
        
        return disable_delete


class LinoSite:
    help_url = "http://code.google.com/p/lino"
    index_html = "This is the main page."
    title = "Unnamed LinoSite"
    domain = "www.example.com"
    
    def __init__(self):
        
        #self.django_settings = settings
        self.init_site_config = lambda sc: sc
        self._menu = menus.Menu("","Main Menu")
        self._setting_up = False
        self._setup_done = False
        self.root_path = '/lino/'
        self._response = None
        
    def setup(self):
        if self._setup_done:
            return
        if self._setting_up:
            #~ logger.warning("LinoSite.setup() called recursively.")
            #~ return 
            raise Exception("LinoSite.setup() called recursively.")
        self._setting_up = True
        
        
        
        discover()
        
        actors.discover()
        
        reports.discover()
        
        choosers.discover()

        for a in actors.actors_list:
            #~ if isinstance(a,layouts.DetailLayout):
                a.setup()
        #~ for a in actors.actors_list:
            #~ if not isinstance(a,layouts.DetailLayout):
                #~ a.setup()

        if settings.MODEL_DEBUG:
            logger.debug("ACTORS:")
            for k in sorted(actors.actors_dict.keys()):
                a = actors.actors_dict[k]
                #~ logger.debug("%s -> %r",k,a.__class__)
                logger.debug("%s -> %r",k,a.debug_summary())
                  
          
        if hasattr(settings,'LINO_SETTINGS'):
            logger.info("Reading %s ...", settings.LINO_SETTINGS)
            execfile(settings.LINO_SETTINGS,dict(lino=self))
        else:
            logger.warning("settings.LINO_SETTINGS entry is missing")
            
        logger.info(lino.welcome_text())
        #~ logger.info("This is Lino version %s." % lino.__version__)
        #~ using = ', '.join(["%s %s" % (n,v) for n,v,u in lino.using()])
        #~ logger.info("Using %s" % using)
        #~ logger.info("Lino Site %r is ready.", self.title)
          
        uis = []
        for ui in settings.USER_INTERFACES:
            logger.info("Starting user interface %s",ui)
            ui_module = import_module(ui)
            #~ self.ui = ui_module.ui
            #~ self.ui.setup_site(self)
            #~ ui_module.ui.setup_site(self)
            uis.append(ui_module.get_ui(self))
        self.uis = uis
        
        self._setup_done = True
        self._setting_up = False
        
        
    def add_menu(self,*args,**kw):
        return self._menu.add_menu(*args,**kw)
       

    def context(self,request,**kw):
        d = dict(
          main_menu = menus.MenuRenderer(self._menu,request),
          root_path = self.root_path,
          lino = self,
          settings = settings,
          debug = True,
          #skin = self.skin,
          request = request
        )
        d.update(kw)
        return d
        
    def select_ui_view(self,request):
        html = '<html><body>'
        html += 'Please select a user interface: <ul>'
        for ui in self.uis:
            html += '<li><a href="%s">%s</a></li>' % (ui.name,ui.verbose_name)
        html += '</ul></body></html>'
        return HttpResponse(html)
        
        
    def get_urls(self):
        self.setup()
        #~ self.setup_ui()
        if len(self.uis) == 1:
            return self.uis[0].get_urls()
        urlpatterns = patterns('',
            ('^$', self.select_ui_view))
        for ui in self.uis:
            urlpatterns += patterns('',
                (ui.name, include(ui.get_urls())),
            )
        return urlpatterns
        #~ return self.ui.get_urls()
        
    def add_program_menu(self):
        return
        m = self.add_menu("app","~Application",)
        #~ m.add_item(url="/accounts/login/",label="Login",can_view=perms.is_anonymous)
        #~ m.add_item(url="/accounts/logout/",label="Logout",can_view=perms.is_authenticated)
        #m.add_item(system.Login(),can_view=perms.is_anonymous)
        #m.add_item(system.Logout(),can_view=perms.is_authenticated)
        
    def get_site_menu(self,user):
        self.setup()
        return self._menu.menu_request(user)
        
      
    def initdb(self,fixtures=[]):
      
        #~ self.setup()
        
        from django.core.management import call_command
        from timtools.console import syscon
        from lino import reports
        
        sites = reports.get_app('sites')
        
        options = dict(interactive=False)
        logger.info("lino_site.initdb(%r)", fixtures)
        if not syscon.confirm("Gonna reset database(s) %s.\nAre you sure?" 
            % settings.DATABASES):
            return
        logger.info("reset")
        if False: # settings.DATABASE_ENGINE == 'sqlite3':
            if settings.DATABASE_NAME != ':memory:':
                if os.path.exists(settings.DATABASE_NAME):
                    os.remove(settings.DATABASE_NAME)
        else:
            call_command('reset',*app_labels(),**options)
        #call_command('reset','songs','auth',interactive=False)
        logger.info("syncdb")
        call_command('syncdb',**options)
        #call_command('flush',interactive=False)
        #~ auth.User.objects.create_superuser('root','luc.saffre@gmx.net','1234')
        #~ auth.User.objects.create_user('user','luc.saffre@gmx.net','1234')
        
        # 20100804 don't remember why this was used:
        #~ sites.Site(id=2,domain=self.domain,name=self.title).save()
        
        logger.info("loaddata %s",' '.join(fixtures))
        call_command('loaddata',*fixtures)
        #~ for fix in fixtures:
            #~ logger.info("loaddata %s",fix)
            #~ call_command('loaddata',fix)
        #self.setup()
        
            

  
  

lino_site = LinoSite()
#~ logger.debug("lino.lino_site has been instantiated")
#'get_urls','fill','context'

initdb = lino_site.initdb
context = lino_site.context
get_urls = lino_site.get_urls
get_site_menu = lino_site.get_site_menu
setup = lino_site.setup