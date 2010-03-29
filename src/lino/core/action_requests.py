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

import traceback
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.db import models

import lino
from lino import actions
from lino import reports

class ActionResponse:
    redirect = None
    alert_msg = None
    confirm_msg = None
    notify_msg = None
    refresh_menu = False
    refresh_caller = False
    close_caller = False
    show_window = None
    success = True # for Ext.form.Action.Submit
    errors = None # for Ext.form.Action.Submit
    
    def __init__(self,**kw):
        for k,v in kw.items():
            assert hasattr(self,k)
            setattr(self,k,v)
              
    
    def as_dict(self):
        return dict(
          success=self.success,
          redirect=self.redirect,
          alert_msg=self.alert_msg,
          notify_msg=self.notify_msg,
          confirm_msg=self.confirm_msg,
          refresh_menu=self.refresh_menu,
          refresh_caller=self.refresh_caller,
          close_caller=self.close_caller,
          show_window=self.show_window,
        )

class ActionRequest:
    """
    An ActionRequest will be created for every request.
    
    """
    selected_rows = []
    
    def __init__(self,ah,action):
        #~ self.is_over = False
        self.ui = ah.ui
        self.ah = ah # actor handle
        #~ self.params = params
        self.action = action # ah.actor.get_action(action_name)
        if not isinstance(action,actions.Action):
            raise Exception("%s : %r is not an Action." % (self,action))
        self.response = None
        
    def __str__(self):
        return 'ActionRequest `%s.%s`' % (self.ah,self.action)
        
    def run(self):
        msg = self.action.before_run(self)
        if msg:
            return ActionResponse(notify_msg=msg,success=False)
        lino.log.debug('ActionRequest._start() %s.%s',self.ah,self.action.name)
        #~ lino.log.debug('ActionRequest._start() %s.%s(%r)',self.ah,self.action.name,self.params)
        self.response = ActionResponse()
        
        try:
            self.action.run_action(self)
        except Exception,e:
            traceback.print_exc(e)
        return self.response
        
    """
    API used during `Action.run_action()`.
    """
        
    def get_user(self):
        raise NotImplementedError()
        
        
    ## message methods to be used in yield statements
        
    def close_caller(self):
        self.response.close_caller = True
        return self
        
    def refresh_caller(self):
        self.response.refresh_caller = True
        return self
        
    def refresh_menu(self):
        self.response.refresh_menu = True
        return self
        
    def show_window(self,js):
        #~ assert js.strip().startswith('function')
        #~ self.response.show_window = py2js(js)
        self.response.show_window = js
        return self
        
    def show_modal_window(self,js):
        self.response.show_modal_window = js
        return self
        
    def redirect(self,url):
        self.response.redirect = url
        return self
        
    def confirm(self,msg,**kw):
        self.response.confirm_msg = msg
        return self
        
    def alert(self,msg,**kw):
        self.response.alert_msg = msg
        return self

    def exception(self,e):
        self.response.alert_msg = unicode(e)
        traceback.print_exc(e)
        return self

    def notify(self,msg):
        self.response.notify_msg = msg
        return self

    def cancel(self,msg=None):
        if msg is not None:
              self.notify(msg)
        return self.close_caller().over()
        
    def ok(self,msg=None):
        if msg is not None:
              self.notify(msg)
        return self.close_caller().over()



class ReportActionRequest(ActionRequest): # was ReportRequest
    limit = None
    offset = None
    master_instance = None
    master = None
    instance = None
    extra = None
    layout = None
    
    def __init__(self,rh,action):
        assert isinstance(rh,reports.ReportHandle)
        self.report = rh.report
        self.rh = rh
        self.ui = rh.ui
        # Subclasses (e.g. BaseViewReportRequest) may set `master` before calling ReportRequest.__init__()
        if self.master is None:
            self.master = rh.report.master
            
        ActionRequest.__init__(self,rh,action)
      
    def __str__(self):
        return self.__class__.__name__ + '(' + self.report.actor_id + ",%r,...)" % self.master_instance

    def setup(self,
            master=None,
            master_instance=None,
            offset=None,limit=None,
            layout=None,user=None,
            extra=None,quick_search=None,
            order_by=None,
            selected_rows=None,
            **kw):
        self.user = user
        self.quick_search = quick_search
        self.order_by = order_by
        if selected_rows is not None:
            self.selected_rows = selected_rows
        
        if master is None:
            master = self.report.master
            # master might still be None
        self.master = master
        
        kw.update(self.report.params)
        self.params = kw
        self.master_kw = self.report.get_master_kw(master_instance)
        self.master_instance = master_instance
        if self.extra is None:
            if extra is None:
                if self.master_kw is None:
                    extra = 0
                elif self.report.can_add.passes(self):
                    extra = 1
                else:
                    extra = 0
            self.extra = extra
        if self.report.use_layouts:
            if layout is None:
                layout = self.rh.layouts[self.report.default_layout]
            else:
                layout = self.rh.layouts[layout]
                #~ assert isinstance(layout,layouts.LayoutHandle), \
                    #~ "Value %r is not a LayoutHandle" % layout
            self.layout = layout
        self.report.setup_request(self)
        self.setup_queryset()
        #~ lino.log.debug(unicode(self))
        # get_queryset() may return a list
        if isinstance(self.queryset,models.query.QuerySet):
            self.total_count = self.queryset.count()
        else:
            self.total_count = len(self.queryset)
        
        if offset is not None:
            self.queryset = self.queryset[offset:]
            self.offset = offset
            
        #~ if limit is None:
            #~ limit = self.report.page_length
            
        """
        Report.page_length is not a default value for ReportRequest.limit
        For example CSVReportRequest wants all rows.
        """
        if limit is not None:
            self.queryset = self.queryset[:limit]
            self.limit = limit
            
        self.page_length = self.report.page_length

    def get_title(self):
        return self.report.get_title(self)
        
    def __iter__(self):
        return self.queryset.__iter__()
        
    def __len__(self):
        return self.queryset.__len__()
        
    def create_instance(self,**kw):
        kw.update(self.master_kw)
        #lino.log.debug('%s.create_instance(%r)',self,kw)
        return self.report.create_instance(self,**kw)
        
    def get_user(self):
        raise NotImplementedError
        
    def setup_queryset(self):
        # overridden by ChoicesReportRequest
        self.queryset = self.rh.get_queryset(self)
        #~ return self.report.get_queryset(master_instance=self.master_instance,**kw)
        
    def render_to_dict(self):
        rows = [ self.row2dict(row,{}) for row in self.queryset ]
        #~ rows = []
        #~ for row in self.queryset:
            #~ d = self.row2dict(row,{})
            #~ rows.append(d)
        total_count = self.total_count
        #lino.log.debug('%s.render_to_dict() total_count=%d extra=%d',self,total_count,self.extra)
        # add extra blank row(s):
        for i in range(0,self.extra):
            row = self.create_instance()
            #~ d = self.row2dict(row,{})
            #~ rows.append(d)
            rows.append(self.row2dict(row,{}))
            total_count += 1
        return dict(count=total_count,rows=rows,title=self.report.get_title(self))
        
    def row2dict(self,row,d):
        # overridden in extjs.ViewReport
        return self.report.row2dict(row,d)
        


