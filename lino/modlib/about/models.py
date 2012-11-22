## Copyright 2012 Luc Saffre
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

import cgi
import inspect
import types
import datetime

from django.utils.translation import ugettext as _
from django.db import models
from django.conf import settings


from lino.utils import AttrDict
from lino.utils.xmlgen import html as xghtml

from lino.utils import codetime, codefiles
from lino.utils import babel
from lino import mixins
from lino import dd


import os


        
class Models(dd.VirtualTable):
    label = _("Models")
    #~ column_defaults = dict(width=8)
    #~ column_names = "app name verbose_name docstring rows"
    column_names = "app name docstring rows detail_action"
    detail_layout = """
    app name docstring rows
    about.FieldsByModel
    """
    
    slave_grid_format = 'html'    
  
    @classmethod
    def get_data_rows(self,ar):
        profile = ar.get_user().profile
        for model in models.get_models():
            if model._lino_default_table.get_view_permission(profile):
                #~ print model
                yield model
                
    @dd.displayfield(_("app_label"))
    def app(self,obj,ar):
        return obj._meta.app_label
        
    @dd.displayfield(_("name"))
    def name(self,obj,ar):
        return obj.__name__
        
    #~ @dd.displayfield(_("Detail Action"))
    @dd.displayfield()
    def detail_action(self,obj,ar):
        #~ return str(obj._lino_default_table.detail_action)
        if obj._lino_default_table.detail_action is None:
            return ''
        return obj._lino_default_table.detail_action.full_name()
        
    #~ @dd.displayfield(_("verbose name"))
    #~ def vebose_name(self,obj,ar):
        #~ return unicode(obj._meta.vebose_name)
        
    @dd.displayfield(_("docstring"))
    def docstring(self,obj,ar):
        return obj.__doc__
        #~ return restify(unicode(obj.__doc__))
        
    @dd.requestfield(_("Rows"))
    def rows(self,obj,ar):
        #~ if obj._lino_default_table.get_view_permission(ar.get_user()):
        return obj._lino_default_table.request(ar.ui,
          user=ar.get_user(),renderer=ar.renderer)


class FieldsByModel(dd.VirtualTable):
    label = _("Fields")
    #~ master_key = "model"
    master = Models
    column_names = "name verbose_name help_text_column"
    
    @classmethod
    def get_data_rows(self,ar):
        model = ar.master_instance
        if model:
            for (fld,remote) in model._meta.get_fields_with_model():
                yield fld
                
    @dd.displayfield(_("name"))
    def name(self,fld,ar):
        return fld.name
        
    @dd.displayfield(_("verbose name"))
    def verbose_name(self,fld,ar):
        return unicode(fld.vebose_name)
        
    @dd.displayfield(_("help text"))
    def help_text_column(self,obj,ar):
        #~ return obj.__doc__
        return restify(unicode(obj.help_text))



class Inspected(object):
    def __init__(self,parent,prefix,name,value):
        self.parent = parent
        self.prefix = prefix
        self.name = name
        self.value = value

class Inspector(dd.VirtualTable):
    """
    Shows a simplistic "inspector" which once helped me for debugging.
    Needs more work to become seriously useful...
    
    """
    label = _("Inspector")
    required = dict(user_level='admin')
    column_names = "i_name i_type i_value"
    parameters = dict(
      inspected=models.CharField(_("Inspected object"),max_length=100,blank=True),
      show_callables=models.BooleanField(_("show callables"),default=False)
      )
    params_layout = 'inspected show_callables'
    #~ editable = False
    #~ slave_grid_format = 'html'    
  
    @classmethod
    def get_inspected(self,name):
        #~ ctx = dict(settings=settings,lino=lino)
        if not name:
            return settings
        try:
            o = eval('settings.'+name)
        except Exception,e:
            o = e
        return o
        
        #~ o = settings
        #~ try:
            #~ for ch in name.split('.'):
                #~ o = getattr(o,ch)
        #~ except Exception,e:
            #~ o = e
        #~ return o
        
    @classmethod
    def get_data_rows(self,ar):
        #~ logger.info("20120210 %s, %s",ar.quick_search,ar.param_values.inspected)
        
        if ar.param_values.show_callables:
            def flt(v): return True
        else:
            def flt(v): 
                if isinstance(v,(
                    types.FunctionType,
                    types.GeneratorType,
                    types.UnboundMethodType,
                    types.UnboundMethodType,
                    types.BuiltinMethodType,
                    types.BuiltinFunctionType,
                    )): 
                    return False
                return True
          
        
        o = self.get_inspected(ar.param_values.inspected)
        if isinstance(o,(list,tuple)):
            for i,v in enumerate(o):
                k = "[" + str(i) + "]"
                yield Inspected(o,'',k,v)
        elif isinstance(o,AttrDict):
            for k,v in o.items():
                yield Inspected(o,'.',k,v)
        elif isinstance(o,dict):
            for k,v in o.items():
                k = "[" + repr(k) + "]"
                yield Inspected(o,'',k,v)
        else:
            for k in dir(o):
                if not k.startswith('__'):
                    if not ar.quick_search or (ar.quick_search.lower() in k.lower()):
                        v = getattr(o,k)
                        if flt(v):
                        #~ if not inspect.isbuiltin(v) and not inspect.ismethod(v):
                            #~ if ar.param_values.show_callables or not inspect.isfunction(v):
                            #~ if isinstance(v,types.FunctionType ar.param_values.show_callables or not callable(v):
                            yield Inspected(o,'.',k,v)
        #~ for k,v in o.__dict__.items():
            #~ yield Inspected(o,k,v)
            
                
    @dd.displayfield(_("Name"))
    def i_name(self,obj,ar):
        pv = dict()
        if ar.param_values.inspected:
            pv.update(inspected=ar.param_values.inspected+obj.prefix+obj.name)
        else:
            pv.update(inspected=obj.name)
        #~ newreq = ar.spawn(ar.ui,user=ar.user,renderer=ar.renderer,param_values=pv)
        newreq = ar.spawn(param_values=pv)
        return ar.href_to_request(newreq,obj.name)
        #~ return obj.name
        
    @dd.displayfield(_("Value"))
    def i_value(self,obj,ar):
        return cgi.escape(unicode(obj.value))
        
    @dd.displayfield(_("Type"))
    def i_type(self,obj,ar):
        return cgi.escape(str(type(obj.value)))
        

#~ class AboutDetail(dd.FormLayout):
    #~ """
    #~ The Detail Layout for :class:`About`
    #~ """
    #~ window_size = (60,30)
    #~ main = """
    #~ versions:40x5 startup_time:30
    #~ about.Models:70x10
    #~ """


class About(mixins.EmptyTable):
    """
    A modal window displaying information about this server.
    """
    required = dict(auth=False)
    label = _("About") 
    #~ hide_window_title = True
    hide_top_toolbar = True
    #~ window_size = (700,400)
    #~ detail_layout = AboutDetail(window_size = (700,400))
    #~ detail_layout = AboutDetail()
    detail_layout = dd.FormLayout("""
    about_html
    """,window_size = (60,20))
    
    #~ versions = dd.Constant(lino.welcome_html())
    
    #~ do_build = BuildSiteCache()
    
    #~ @classmethod
    #~ def setup_actions(self):
        #~ super(About,self).setup_actions()
        #~ self.add_action(BuildSiteCache())
   
    #~ @dd.constant(_("Versions"))
    #~ @dd.constant()
    #~ def versions(cls,ui):
        #~ return settings.LINO.welcome_html(ui)
        
    @dd.constant()
    def about_html(cls,ui):
      
    #~ @dd.displayfield()
    #~ def about_html(cls,obj,ar):
        #~ ui = ar.ui
        #~ return settings.LINO.welcome_html(ui)
        body = []
        
        p = []
        for name,version,url in settings.LINO.using(ui):
            if len(p):
                #~ body.append(xghtml.E.br())
                p.append(', ')
            p.append(xghtml.E.a(name,href=url,target='_blank'))
            p.append(' ')
            p.append(version)
        body.append(xghtml.E.p(*p))
        
        #~ print "20121112 startup_time", settings.LINO.startup_time.date()
        def dtfmt(dt):
            if isinstance(dt,float):
                dt = datetime.datetime.fromtimestamp(dt)
                #~ raise ValueError("Expected float, go %r" % dt)
            return unicode(_("%(date)s at %(time)s")) % dict(
              date=babel.dtosl(dt.date()),
              time=dt.time())
            
        items = []
        E = xghtml.E
        times = []
        times.append((_("Server uptime"),settings.LINO.startup_time))
        for src in ("lino","lino_welfare"):
            label = _("Source timestamp (%s)") % src
            value = codetime('%s.*' % src)
            times.append((label,value))
        for label,value in times:
            if value is not None:
                items.append(E.li(unicode(label),' : ',E.b(dtfmt(value))))
        body.append(E.ul(*items))
        
        return xghtml.E.div(*body,class_='htmlText')
        
        
    #~ @dd.displayfield(_("Versions"))
    #~ def versions(self,obj,ar):
        #~ return lino.welcome_html(ar.ui)
        
    #~ @dd.constantfield(_("Versions"))
    #~ def versions(cls,self,req):
        #~ return lino.welcome_html()
        
    #~ @dd.virtualfield(models.DateTimeField(_("Server up since")))
    #~ def startup_time(cls,self,req):
        #~ return settings.LINO.startup_time
    




def is_start_of_docstring(line):
    for delim in '"""',"'''":
        if line.startswith(delim) or line.startswith('u'+delim) or line.startswith('r'+delim) or line.startswith('ru'+delim):
            return delim
            
class SourceFile(object):
    def __init__(self,modulename,filename):
        self.modulename = modulename
        self.filename = filename
        self.analyze()
        
    def analyze(self):
        self.count_code, self.count_total, self.count_blank, self.count_doc = 0, 0, 0, 0
        self.count_comment = 0
        #~ count_code, count_total, count_blank, count_doc = 0, 0, 0, 0
        skip_until = None
        for line in open(self.filename).readlines():
            self.count_total += 1
            line = line.strip()
            if not line:
                self.count_blank += 1
            else:
                if line.startswith('#'):
                    self.count_comment += 1
                    continue
                if skip_until is None:
                    skip_until = is_start_of_docstring(line)
                    if skip_until is not None:
                        self.count_doc += 1
                        #~ skip_until = '"""'
                        continue
                    #~ if line.startswith('"""') or line.startswith('u"""'):
                        #~ count_doc += 1
                        #~ skip_until = '"""'
                        #~ continue
                    #~ if line.startswith("'''") or line.startswith("u'''"):
                        #~ count_doc += 1
                        #~ skip_until = "'''"
                        #~ continue
                    self.count_code += 1
                else:
                    self.count_doc += 1
                    #~ if line.startswith(skip_until):
                    if skip_until in line:
                        skip_until = None

        #~ self.count_code, count_total, count_blank, count_doc
        
        
class SourceFiles(dd.VirtualTable):
    label = _("Source files")
    column_names = 'module_name code_lines doc_lines'
    
    @classmethod
    def get_data_rows(self,ar):
        for name,filename in codefiles('lino*'):
            yield SourceFile(name,filename)
            
    @dd.virtualfield(models.IntegerField(_("Code")))
    def code_lines(self,obj,ar):
        return obj.count_code
            
    @dd.virtualfield(models.IntegerField(_("doc")))
    def doc_lines(self,obj,ar):
        return obj.count_doc
            
    @dd.virtualfield(models.CharField(_("module name")))
    def module_name(self,obj,ar):
        return obj.modulename
            
        

#~ def _test():
    #~ import doctest
    #~ doctest.testmod()

#~ if __name__ == "__main__":
    #~ _test()


def setup_site_menu(site,ui,profile,m): 
    m.add_action(site.modules.about.About)
    if settings.LINO.use_experimental_features:
        m.add_action(site.modules.about.Models)
        m.add_action(site.modules.about.Inspector)
        m.add_action(site.modules.about.SourceFiles)

