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


import os
import sys
#~ import imp

from django.conf import settings
if hasattr(settings,'LINO_SETTINGS'):
    lino.log.debug('settings.LINO_SETTINGS is %r',settings.LINO_SETTINGS)
        

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


from django.db.models import loading
#~ def db_apps():
    #~ return [a.__name__.split('.')[-2] for a in loading.get_apps()]

import lino
from lino import reports, forms, layouts, actions
from lino import diag
from lino.utils import perms
from lino.utils import menus
from lino.core import actors


class LinoSite:
    help_url = "http://code.google.com/p/lino"
    index_html = "This is the main page."
    title = "Unnamed LinoSite"
    domain = "www.example.com"
    
    def __init__(self):
        
        #self.django_settings = settings
        
        self._menu = menus.Menu("","Main Menu")
        self._setting_up = False
        self._setup_done = False
        self.root_path = '/lino/'
        self._response = None
        
    def setup(self):
        if self._setup_done:
            return
        if self._setting_up:
            lino.log.warning("LinoSite.setup() called recursively.")
            return 
            #raise Exception("LinoSite.setup() called recursively.")
        self._setting_up = True
        

        actors.discover()
        
        #~ layouts.setup()
        
        reports.discover()

        for a in actors.actors_dict.values():
            if isinstance(a,layouts.DetailLayout):
                a.setup()
        for a in actors.actors_dict.values():
            if not isinstance(a,layouts.DetailLayout):
                a.setup()

            
        lino.log.debug("ACTORS:")
        for k in sorted(actors.actors_dict.keys()):
            a = actors.actors_dict[k]
            lino.log.debug("%s -> %r",k,a.__class__)
          
        if hasattr(settings,'LINO_SETTINGS'):
            lino.log.info("Reading %s...", settings.LINO_SETTINGS)
            execfile(settings.LINO_SETTINGS,dict(lino=self))
        else:
            lino.log.warning("settings.LINO_SETTINGS entry is missing")
            
        USER_INTERFACE = 'lino.ui.extjs'
        lino.log.info("Starting user interface %s",USER_INTERFACE)
        from django.utils.importlib import import_module
        ui_module = import_module(USER_INTERFACE)
        self.ui = ui_module.ui
        self.ui.setup_site(self)
        
        lino.log.info("LinoSite %r is ready.", self.title)
          
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
        
        
    def get_urls(self):
        self.setup()
        return self.ui.get_urls()
        
    def add_program_menu(self):
        return
        m = self.add_menu("app","~Application",)
        #~ m.add_item(url="/accounts/login/",label="Login",can_view=perms.is_anonymous)
        #~ m.add_item(url="/accounts/logout/",label="Logout",can_view=perms.is_authenticated)
        #m.add_item(system.Login(),can_view=perms.is_anonymous)
        #m.add_item(system.Logout(),can_view=perms.is_authenticated)
        
    def get_menu(self,request):
        self.setup()
        return self._menu.menu_request(request)
        
      
    def fill(self,fixtures=[]):
      
        # self.setup()
        
        from django.core.management import call_command
        from timtools.console import syscon
        #from lino import reports
        
        sites = reports.get_app('sites')
        
        options = dict(interactive=False)
        lino.log.info("lino_site.fill(%r)", fixtures)
        if not syscon.confirm("Gonna reset database %s. Are you sure?" 
            % settings.DATABASE_NAME):
            return
        lino.log.info("reset")
        if False: # settings.DATABASE_ENGINE == 'sqlite3':
            if settings.DATABASE_NAME != ':memory:':
                if os.path.exists(settings.DATABASE_NAME):
                    os.remove(settings.DATABASE_NAME)
        else:
            call_command('reset',*diag.app_labels(),**options)
        #call_command('reset','songs','auth',interactive=False)
        lino.log.info("syncdb")
        call_command('syncdb',**options)
        #call_command('flush',interactive=False)
        auth.User.objects.create_superuser('root','luc.saffre@gmx.net','1234')
        auth.User.objects.create_user('user','luc.saffre@gmx.net','1234')
        sites.Site(id=2,domain=self.domain,name=self.title).save()
        
        for fix in fixtures:
            lino.log.info("loaddata %s",fix)
            call_command('loaddata',fix)
        #self.setup()
        
            

  
  

lino_site = LinoSite()
lino.log.debug("lino.lino_site has been instantiated")
#'get_urls','fill','context'

fill = lino_site.fill
context = lino_site.context
get_urls = lino_site.get_urls
get_menu = lino_site.get_menu
setup = lino_site.setup