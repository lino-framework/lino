## Copyright 2009 Luc Saffre

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


import imp
from lino.tools.my_import import my_import as import_module
from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django import template 
from django.views.decorators.cache import never_cache 
from django.shortcuts import render_to_response 
from lino.django.utils.menus import Menu

class LinoSite(AdminSite):
    index_template = 'lino/index.html'
    login_template = 'lino/login.html'
  
    def __init__(self,*args,**kw):
        AdminSite.__init__(self,*args,**kw)
        self._menu = Menu("lino","Main Menu")
        self.loading = False
        self.done = False
        self.root_path = '/lino/'

    def autodiscover(self):
        if self.done:
            return
        self.loading = True


        for app in settings.INSTALLED_APPS:
            mod = import_module(app)
            try:
                app_path = mod.__path__
            except AttributeError:
                continue

            try:
                imp.find_module('lino_setup', app_path)
            except ImportError:
                continue
            mod = import_module("%s.lino_setup" % app)
            mod.setup_menu(self._menu)
            
        from lino.django.utils.sysadm import setup_menu
        setup_menu(self._menu)
        
        self.done = True
        self.loading = False
        
       
    def register(self,*args,**kw):
        raise NotImplementedError
       
    def unregister(self,*args,**kw):
        raise NotImplementedError
        
    def context(self):
        return dict(
          main_menu=self._menu,
          title=self._menu.label,
          root_path = self.root_path,
        )
        
    def index(self, request, extra_context=None):
        context = self.context()
        context.update(extra_context or {})
        return render_to_response(self.index_template, context,
            context_instance=template.RequestContext(request)
        )
    index = never_cache(index)
    
    def get_urls(self):
        self.autodiscover()
        urlpatterns = AdminSite.get_urls(self)
        urlpatterns += self._menu.get_urls() # self._menu.name)
        return urlpatterns
         
       
site = LinoSite()