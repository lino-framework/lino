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

from lino.utils import actors
from lino import reports, forms

class UI:
    """
    """
    
    def get_urls():
        pass
        
    def setup_site(self,lino_site):
        pass
    
    def field2elem(self,lui,field,**kw):
        pass
        
    def _get_report_handle(self,app_label,rptname):
        rpt = actors.get_actor(app_label,rptname)
        #rpt = get_report(app_label,rptname)
        return self.get_report_handle(rpt)
        
    def get_report_handle(self,rpt):
        return self.get_actor_handle(rpt,reports.ReportHandle)
    def get_form_handle(self,frm):
        return self.get_actor_handle(frm,forms.FormHandle)
        
    def get_actor_handle(self,actor,cls):
        #lino.log.debug('get_report_handle(%s)',rpt)
        actor.setup()
        h = actor._handles.get(self,None)
        if h is None:
            h = cls(self,actor)
            actor._handles[self] = h
            h.setup()
        return h
        
        
        
    def old_get_form_handle(self,frm):
        frm.setup()
        h = frm._handles.get(self,None)
        if h is None:
            h = forms.FormHandle(self,frm)
            frm._handles[self] = h
            h.setup()
        return h
        
    def old_get_dialog_handle(self,layout):
        assert isinstance(layout,layouts.DialogLayout)
        h = layout._handles.get(self,None)
        if h is None:
            lnk = layouts.DialogLink(self,layout)
            h = layouts.LayoutHandle(lnk,layout,1)
            layout._handles[self] = h
            #h.setup()
        return h
        


