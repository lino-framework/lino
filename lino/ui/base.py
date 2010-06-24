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

import lino
from urllib import urlencode

class Handle:
  
    def __init__(self,ui):
        self.ui = ui
        
    def setup(self):
        if self.ui is not None:
            self.ui.setup_handle(self)
        
        
class Handled(object):
  
    "Inherited by Report, Layout, and maybe others"
    
    _handle_class = None
    #~ _handle_selector = None
    
    def __init__(self):
        self._handles = {}
        
    def get_handle(self,k):
        #~ assert k is None or isinstance(k,self._handle_selector), "%s.get_handle() : %r is not a %s" % (self,k,self._handle_selector)
        assert k is None or isinstance(k,UI), "%s.get_handle() : %r is not a BaseUI" % (self,k)
        h = self._handles.get(k,None)
        if h is None:
            h = self._handle_class(k,self)
            self._handles[k] = h
            h.setup()
        return h
        
        
class UI:
    """
    """
    name = None
    verbose_name = None
    
    def build_url(self,*args,**kw):
        url = "/" + "/".join(args)
        if self.name:
            url = "/" + self.name + url
        if len(kw):
            url += "?" + urlencode(kw)
        return url
        
    def a2btn(self,a):
        return dict(
          opens_a_slave=a.opens_a_slave,
          #~ handler=js_code("Lino.%s" % a),
          name=a.name,
          label=unicode(a.label),
          url=self.build_url("api",a.actor.app_label,a.actor._actor_name,fmt=a.name)
        )
        
    def get_urls():
        pass
        
    def field2elem(self,lui,field,**kw):
        pass
        
    def setup_site(self,site):
        self.site = site
        from lino import reports
        # instantiate all ReportHandles already at server startup.
        # TODO: in fact this is currently called only when a first request comes in,
        #       because Django does not yet provide a `server_startup` signal.
        lino.log.debug('%s.setup_site()' % self)
        for rpt in reports.master_reports + reports.slave_reports:
            rpt.get_handle(self)
        
    def setup_handle(self,h):
        pass
        
    def get_report_ar(self,rh,**kw):
        raise NotImplementedError()
        
