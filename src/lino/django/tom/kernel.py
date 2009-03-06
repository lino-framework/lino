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



#~ from django.utils.functional import update_wrapper
#~ from django.forms.models import modelform_factory
#~ from django.forms.models import modelformset_factory
#~ from django.shortcuts import render_to_response
#~ from django.conf.urls.defaults import patterns, url, include

from lino.django.tom.menus import MenuContainer

class TheKernel(MenuContainer):
    def __init__(self):
        self._registry={}
        MenuContainer.__init__(self)
        
    #~ def register(self,rptclass):
        #~ self._registry[rptclass.__name__] = rptclass
        
    #~ def get_report(self,name):
        #~ return self._registry[name]()
        
    #~ def get_urls(self):
        
        #~ urlpatterns = []
        
        #~ # Admin-site-wide views.
        #~ urlpatterns = patterns('',
            #~ url(r'^$',
                #~ self.index),
            #~ url(r'^(?P<rptname>\w+)/$',
                #~ self.list_view),
            #~ url(r'^(?P<rptname>\w+)/(?P<rownum>.+)/$',
                #~ self.page_view),
        #~ )
        #~ urlpatterns += MenuContainer.get_urls(self,'menu')
        #~ return urlpatterns
        
    
    
    #~ def view(self,request,action=None,**kw):
        #~ if action is None: 
            #~ action=self.menu
        #~ if isinstance(action,Report):
            #~ return self.view_report(request,action,**kw)
        #~ if isinstance(action,Menu):
            #~ return self.view_menu(request,action,**kw)
    


    #~ def index(self,request):
        #~ context = dict(
            #~ menu=self.menu,
        #~ )
        #~ return render_to_response("reports/index.html",context)    
      
    #~ def list_view(self,request,rptname):
        #~ rpt = self.get_report(rptname)
        #~ fsclass = modelformset_factory(rpt.queryset.model,
                                       #~ fields=rpt.columnNames.split())
        #~ if request.method == 'POST':
            #~ fs = fsclass(request.POST,queryset=rpt.queryset)
            #~ if fs.is_valid():
                #~ fs.save()
        #~ else:
            #~ fs = fsclass(queryset=rpt.queryset)
        #~ context = dict(
            #~ report=rpt,
            #~ formset=fs,
        #~ )
        #~ return render_to_response("reports/list.html",context)    
    
    #~ def page_view(self,request,rptname,rownum):
        #~ rpt = self.get_report(rptname)
        #~ obj=rpt.queryset[int(rownum)]
        #~ if request.method == 'POST':
            #~ frm=rpt.modelForm(request.POST,instance=obj)
            #~ if frm.is_valid():
                #~ frm.save()
        #~ else:
            #~ frm=rpt.modelForm(instance=obj)      
        #~ context = dict(
            #~ report=rpt,
            #~ object=obj,
            #~ form=frm,
        #~ )
        #~ return render_to_response("reports/page.html",context)    
        
        

