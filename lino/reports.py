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
import traceback
#import logging ; logger = logging.getLogger('lino.reports')
import cPickle as pickle

from django.conf import settings
from django.utils.importlib import import_module
from django.utils.translation import ugettext as _

from django.db import models
from django.db.models.query import QuerySet
from django import forms
from django.conf.urls.defaults import patterns, url, include
from django.forms.models import modelform_factory
from django.forms.models import _get_foreign_key
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from dateutil import parser as dateparser

from django.http import HttpResponse
from django.utils.safestring import mark_safe


import lino
from lino import layouts
from lino import actions
from lino.utils import perms, menus
from lino.utils import mixins
from lino.core import datalinks
from lino.core import actors
#~ from lino.core import action_requests
from lino.ui import base

from lino.modlib.tools import resolve_model, resolve_field, get_app, model_label, get_field
from lino.core.coretools import get_slave, get_model_report, data_elems, get_data_elem

#~ from lino.modlib import field_choices

def base_attrs(cl):
    #~ if cl is Report or len(cl.__bases__) == 0:
        #~ return
    #~ myattrs = set(cl.__dict__.keys())
    for b in cl.__bases__:
        for k in base_attrs(b):
            yield k
        for k in b.__dict__.keys():
            yield k


def add_quick_search_filter(qs,search_text):
    if not isinstance(qs,QuerySet): 
        # TODO: filter also simple lists 
        return qs
    q = models.Q()
    for field in qs.model._meta.fields:
        if isinstance(field,models.CharField):
            kw = {field.name+"__contains": search_text}
            q = q | models.Q(**kw)
    return qs.filter(q)
    
    
def add_gridfilters(qs,gridfilters):
    """
    Converts a `filter` request in the format used by :extux:`Ext.ux.grid.GridFilters` into a 
    `Django field lookup <http://docs.djangoproject.com/en/1.2/ref/models/querysets/#field-lookups>`_
    on a :class:`django.db.models.query.QuerySet`.
    
    :param qs: the queryset to be modified.
    :param gridfilters: a list of dictionaries, each having 3 keys `field`, `type` and `value`.
    
    """
    if not isinstance(qs,QuerySet): 
        raise NotImplementedError('TODO: filter also simple lists')
    q = models.Q()
    for flt in gridfilters:
        field = get_field(qs.model,flt['field'])
        flttype = flt['type']
        kw = {}
        if flttype == 'string':
            if isinstance(field,models.CharField):
                kw[field.name+"__contains"] =  flt['value']
            elif isinstance(field,models.ForeignKey):
                kw[field.name+"__name__contains"] = flt['value']
            else:
                raise NotImplementedError(repr(flt))
        elif flttype == 'numeric':
            cmp = str(flt['comparison'])
            if cmp == 'eq': cmp = 'exact'
            kw[field.name+"__"+cmp] = flt['value']
        elif flttype == 'boolean':
            kw[field.name+"__equals"] = flt['value']
        elif flttype == 'date':
            v = dateparser.parse(flt['value'],fuzzy=True)
            cmp = str(flt['comparison'])
            if cmp == 'eq': cmp = 'exact'
            kw[field.name+"__"+cmp] = v
            #~ print kw
        else:
            raise NotImplementedError(repr(flt))
        q = q & models.Q(**kw)
    return qs.filter(q)
        

def rc_name(rptclass):
    return rptclass.app_label + '.' + rptclass.__name__
    
def de_verbose_name(de):
    if isinstance(de,models.Field):
        return de.verbose_name
    return de.name

    
    
# TODO : move these global variables to LinoSite
master_reports = []
slave_reports = []
generic_slaves = {}
rptname_choices = []

def register_report(rpt):
    #rptclass.app_label = rptclass.__module__.split('.')[-2]
    if rpt.typo_check:
        myattrs = set(rpt.__class__.__dict__.keys())
        for attr in base_attrs(rpt.__class__):
            myattrs.discard(attr)
        if len(myattrs):
            lino.log.warning("%s defines new attribute(s) %s", rpt.__class__, ",".join(myattrs))
    
    if rpt.model is None:
        #~ lino.log.debug("%s is an abstract report", rpt)
        return
        
    #~ rptname_choices.append((rpt.actor_id, rpt.get_label()))
    rptname_choices.append(rpt.actor_id)
    
    if rpt.master is None:
        master_reports.append(rpt)
        if rpt.use_as_default_report:
            #~ lino.log.debug("register %s : model_report for %s", rpt.actor_id, model_label(rpt.model))
            rpt.model._lino_model_report = rpt
        else:
            #~ lino.log.debug("register %s: not used as model_report",rpt.actor_id)
            pass
    elif rpt.master is ContentType:
        #~ lino.log.debug("register %s : generic slave for %r", rpt.actor_id, rpt.fk_name)
        generic_slaves[rpt.actor_id] = rpt
    else:
        slave_reports.append(rpt)

    
    
def discover():
    """
    - Each model can receive a number of "slaves". 
      Slaves are reports whose data depends on an instance of another model (their master).
      
    - For each model we want to find out the "model report" ot "default report".
      The "choices report" for a foreignkey field is also currently simply the pointed model's
      model_report.
      `_lino_model_report`

    """
    
    lino.log.info("Analyzing Reports...")
    #~ lino.log.debug("Register Report actors...")
    for rpt in actors.actors_list:
        if isinstance(rpt,Report) and rpt.__class__ is not Report:
            register_report(rpt)
            
    #~ lino.log.debug("Instantiate model reports...")
    for model in models.get_models():
        rpt = getattr(model,'_lino_model_report',None)
        if rpt is None:
            rpt = report_factory(model)
            register_report(rpt)
            model._lino_model_report = rpt
            
    #~ lino.log.debug("Analyze %d slave reports...",len(slave_reports))
    for rpt in slave_reports:
        slaves = getattr(rpt.master,"_lino_slaves",None)
        if slaves is None:
            slaves = {}
            rpt.master._lino_slaves = slaves
        slaves[rpt.actor_id] = rpt
        #~ lino.log.debug("%s: slave for %s",rpt.actor_id, rpt.master.__name__)
    #~ lino.log.debug("Assigned %d slave reports to their master.",len(slave_reports))
        
    #~ lino.log.debug("Setup model reports...")
    #~ for model in models.get_models():
        #~ model._lino_model_report.setup()
        
    #~ lino.log.debug("Instantiate property editors...")
    #~ for model in models.get_models():
        #~ pw = ext_elems.PropertiesWindow(model)
        #~ model._lino_properties_window = pw
            
    #~ lino.log.debug("reports.setup() done")




class ReportHandle(datalinks.DataLink,base.Handle): 
  
    #~ properties = None
    
    #~ detail_link = None
    
    
    def __init__(self,ui,report):
        #lino.log.debug('ReportHandle.__init__(%s)',rd)
        assert isinstance(report,Report)
        self.report = report
        self._layouts = None
        #~ actors.ActorHandle.__init__(self,report)
        datalinks.DataLink.__init__(self,ui)
        base.Handle.__init__(self,ui)
        if self.report.use_layouts:
            self.list_layout = self.report.list_layout.get_handle(self.ui)
        if self.report.model is not None:
            self.content_type = ContentType.objects.get_for_model(self.report.model).pk
        self.data_elems = report.data_elems
        self.get_data_elem = report.get_data_elem
        
  
    def __str__(self):
        return str(self.report) + 'Handle'
            
    def setup_layouts(self):
        if self._layouts is not None:
            return
        #~ self.default_action = self.report.default_action(self)
        if self.report.use_layouts:
            self._layouts = [ self.list_layout ] + [ dtl.layout.get_handle(self.ui) for dtl in self.report.details ]
            #~ if len(self.details) > 0:
                #~ self.detail_link = DetailDataLink(self,self.details[0])
                
                
        else:
            self._layouts = []

    def submit_elems(self):
        return []
        
    def get_layout(self,i):
        self.setup_layouts()
        return self._layouts[i]
        
    def get_used_layouts(self):
        self.setup_layouts()
        return self._layouts
        
    def get_absolute_url(self,*args,**kw):
        return self.ui.get_report_url(self,*args,**kw)
        
    #~ def data_elems(self):
        #~ for de in self.report.data_elems(): yield de
    #~ def get_data_elem(self,name):
        #~ return get_data_elem(self.report.model,name)
        
    def get_action(self,name):
        return self.report.get_action(name)
    def get_actions(self,*args,**kw):
        return self.report.get_actions(*args,**kw)
        
    def get_details(self):
        return self.report.details
        #~ return self.layouts[1:]
          
    def get_slaves(self):
        return [ sl.get_handle(self.ui) for sl in self.report._slaves ]
            
    def get_title(self,rr):
        return self.report.get_title(rr)
        
    #~ def request(self,**kw):
        #~ return self.ui.get_report_ar(self,**kw)
        
    def request(self,*args,**kw):
        ar = ReportActionRequest(self,self.report.list_action)
        ar.setup(*args,**kw)
        return ar



class ReportActionRequest(actions.ActionRequest): # was ReportRequest
    limit = None
    offset = None
    master_instance = None
    master = None
    instance = None
    extra = None
    layout = None
    
    def __init__(self,rh,action):
    #~ def __init__(self,rpt,action,ui):
        assert isinstance(rh,ReportHandle)
        self.report = rh.report
        self.ui = rh.ui
        # Subclasses (e.g. BaseViewReportRequest) may set `master` before calling ReportRequest.__init__()
        if self.master is None:
            self.master = rh.report.master
        #~ actions.ActionRequest.__init__(self,rpt,action,ui)
        actions.ActionRequest.__init__(self,rh,action)
        #~ self.rh = self.ah
      
    def __str__(self):
        return self.__class__.__name__ + '(' + self.report.actor_id + ",%r,...)" % self.master_instance

    def setup(self,
            master=None,
            master_instance=None,
            offset=None,limit=None,
            layout=None,user=None,
            extra=None,quick_search=None,
            gridfilters=None,
            order_by=None,
            selected_rows=None,
            **kw):
        self.user = user
        self.quick_search = quick_search
        self.gridfilters = gridfilters
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
                elif self.report.can_add.passes(self.user):
                    extra = 1
                else:
                    extra = 0
            self.extra = extra
        if self.report.use_layouts:
            if layout is None:
                layout = self.ah._layouts[self.report.default_layout]
            else:
                layout = self.ah._layouts[layout]
            self.layout = layout
        self.report.setup_request(self)
        self.queryset = self.get_queryset()
        #~ self.setup_queryset()
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
        
    def get_queryset(self):
        # overridden by ChoicesReportRequest
        return self.report.get_queryset(self)
        #~ return self.report.get_queryset(master_instance=self.master_instance,**kw)
        
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
        
    def get_title(self):
        return self.report.get_title(self)
        
    def render_to_dict(self):
        return self.action.render_to_dict(self)
        
    def row2dict(self,row,d):
        # overridden in extjs.ext_requests.ViewReportRequest
        return self.report.row2dict(row,d)
        
    #~ def run_action(self,ar):
        #~ ar.show_action_window(self) 
        


        
        


class Report(actors.Actor,base.Handled): # actions.Action): # 
    default_action_class = actions.GridEdit
    _handle_class = ReportHandle
    #~ _handle_selector = base.UI
    params = {}
    field = None
    queryset = None 
    model = None
    use_as_default_report = True
    order_by = None
    filter = None
    exclude = None
    title = None
    column_names = None
    hide_columns = None
    #~ hide_fields = None
    #label = None
    #~ param_form = ReportParameterForm
    #default_filter = ''
    #name = None
    form_class = None
    master = None
    #~ slaves = None
    fk_name = None
    help_url = None
    #master_instance = None
    page_length = 10
    display_field = '__unicode__'
    #date_format = 'Y-m-d'
    #date_format = '%d.%m.%y'
    
    #~ page_layout = None # (layouts.PageLayout ,)
    #~ row_layout_class = None
    
    date_format = 'd.m.Y'
    boolean_texts = (_('Yes'),_('No'),' ')
    
    can_view = perms.always
    can_add = perms.is_authenticated
    can_change = perms.is_authenticated
    can_delete = perms.is_authenticated
    can_config = perms.is_staff
    
    show_prev_next = True
    
    #~ default_action = GridEdit
    default_layout = 0
    
    typo_check = True
    url = None
    
    use_layouts = True
    
    button_label = None
    
    details = []
    
    grid_configs = {}
    """
    Will be filled during :meth:`lino.reports.Report.do_setup`. 
    """
    
    disabled_fields = None # see docs
    """
    If `disabled_fields` is not None, it must be a method that accepts two arguments `request` and `obj` 
    and returns a list of field names that should not be editable. 
    See usage example in :class::`dsbe.models.Persons` and :doc:`/blog/2010/0804`.
    
    """
    
    
    def __init__(self):
        if self.model is None:
            if self.queryset is not None:
                self.model = self.queryset.model
            # raise Exception(self.__class__)
        else:
            self.model = resolve_model(self.model,self.app_label,self)
        if self.model is not None:
            self.app_label = self.model._meta.app_label
            self.actions = self.actions + [ actions.DeleteSelected ] #, InsertRow ]
            m = getattr(self.model,'setup_report',None)
            if m:
                m(self)
        
        actors.Actor.__init__(self)
        base.Handled.__init__(self)
        
        #~ lino.log.debug("Report.__init__() %s", self)
        
        if self.fk_name:
            #~ self.master = resolve_model(self.master,self.app_label)
            try:
                fk, remote, direct, m2m = self.model._meta.get_field_by_name(self.fk_name)
                assert direct
                assert not m2m
                master = fk.rel.to
            except models.FieldDoesNotExist,e:
                #~ lino.log.debug("FieldDoesNotExist in %r._meta.get_field_by_name(%r)",self.model,self.fk_name)
                master = None
                for vf in self.model._meta.virtual_fields:
                    if vf.name == self.fk_name:
                        fk = vf
                        master = ContentType
            if master is None:
                raise Exception("%s : no master for fk_name %r in %s" % (
                    self,self.fk_name,self.model.__name__))
            self.master = master
            self.fk = fk
        else:
            assert self.master is None
        #~ elif self.master:
            #~ lino.log.warning("DEPRECATED: replace %s.master by fk_name" % self.actor_id)
            #~ #assert isinstance(self.master,object), "%s.master is a %r" % (self.name,self.master)
            #~ assert issubclass(self.master,models.Model), "%s.master is a %r" % (self.actor_id,self.master)
            #~ self.fk = _get_foreign_key(self.master,self.model) #,self.fk_name)
        
        self.default_action = self.default_action_class(self)
        #~ self.list_action = ListAction(self)
        
        
        #self.setup()
        
        #register_report(self)
        
        
    @classmethod
    def spawn(cls,suffix,**kw):
        kw['app_label'] = cls.app_label
        return type(cls.__name__+str(suffix),(cls,),kw)
        
    def column_choices(self):
        return [ de.name for de in self.data_elems() ]
        #~ l = []
        #~ for de in self.data_elems():
            #~ if isinstance(de,models.Field):
                #~ l.append((de.name, unicode(de.verbose_name)))
            #~ else:
                #~ l.append((de.name, unicode(de)))  
        #~ return l
      
    def do_setup(self):
      
        alist = [ ac(self) for ac in self.actions ]
          
        if self.model is not None:
            self.list_layout = layouts.list_layout_factory(self)
            self.detail_layouts = getattr(self.model,'_lino_layouts',[])
              
            if hasattr(self.model,'get_image_url'):
                alist.append(actions.ImageAction(self))
                
            if issubclass(self.model,mixins.Printable):
                alist.append(mixins.PrintAction(self))
                #~ print 20100517, mixins.pm_list
                #~ for pm in mixins.pm_list:
                    #~ if pm.button_label:
                        #~ actions.append(mixins.PrintAction(self,pm))
                    
            if hasattr(self.model,'_lino_slaves'):
                self._slaves = self.model._lino_slaves.values()
            else:
                self._slaves = []
                
            if len(self.detail_layouts) > 0:
                alist.append(actions.ShowDetailAction(self))
                alist.append(actions.SubmitDetail(self))
                alist.append(actions.InsertRow(self))
                alist.append(actions.SubmitInsert(self))
                    
            #~ for slave in self._slaves:
                #~ actions.append(SlaveGridAction(self,slave))
                
            if False: # lino.modlib.properties and lino.modlib.links are currently not necessary
                from lino.modlib.properties import models as properties
                if properties.Property.properties_for_model(self.model).count() > 0:
                    a = properties.PropertiesAction(self)
                    alist.append(a)
                    
                from lino.modlib.links import models as links
                alist.append(SlaveGridAction(self,links.LinksByOwner()))
            
        alist.append(self.default_action)
        #~ actions.append(self.data_action)
        self.set_actions(alist)
                
        if self.button_label is None:
            self.button_label = self.label
            
        #~ from lino.modlib.system import models as system
        #~ self.grid_configs = [gc.name for gc in system.GridConfig.objects.filter(rptname=self.actor_id)]
        filename = self.get_grid_config_file()
        if os.path.exists(filename):
            lino.log.info("Loading %s...",filename)
            execfile(filename,dict(self=self))
            #~ self.grid_configs = pickle.load(open(filename,"rU"))
        else:
            self.grid_configs = {}
        

    def get_grid_config_file(self):
        filename = str(self) + ".py"
        return os.path.join(settings.DATA_DIR,filename)
        
    #~ def debug_summary(self):
        #~ if self.model is not None:
            #~ return '%s detail_layouts=%s' % (self.__class__,[l.__class__ for l in self.detail_layouts])
        #~ return self.__class__
        
    # implements actions.Action
    def unused_get_url(self,ui,**kw):
        kw['run'] = True
        rh = self.get_handle(ui)
        return rh.get_absolute_url(**kw)
        #return ui.get_report_url(rh,**kw)
        
        
    #~ def get_action(self,name):
        #~ for a in self.actions:
            #~ if a.name == name:
                #~ return a
        #~ return actors.Actor.get_action(self,name)
              
    def add_actions(self,*args):
        """Used in Model.setup_report() to specify actions for each report on
        this model."""
        self.actions += args
        #~ for a in more_actions:
            #~ self._actions.append(a)
        
    #~ def unused_ext_components(self):
        #~ if len(self.store.layouts) == 2:
            #~ for s in self.store.layouts:
                #~ yield s._main
        #~ else:
            #~ yield self.store.layouts[0]._main
            #~ comps = [l._main for l in self.store.layouts[1:]]
            #~ yield extjs.TabPanel(None,"EastPanel",*comps)
            
        #~ yield self.layouts[0]._main
        #~ if len(self.layouts) == 2:
            #~ yield self.layouts[1]._main
        #~ else:
            #~ comps = [l._main for l in self.layouts[1:]]
            #~ yield layouts.TabPanel(None,"EastPanel",*comps)

    def data_elems(self):
        for de in data_elems(self.model): yield de
          
    def get_data_elem(self,name):
        return get_data_elem(self.model,name)
        
    def get_details(self):
        return self.details
            
    def get_title(self,rr):
        #~ if self.title is None:
            #~ return self.label
        title = self.title or self.label
        if rr is not None and self.master is not None:
            title += ": " + unicode(rr.master_instance)
        return title
        
    def get_queryset(self,rr):
        if self.queryset is not None:
            qs = self.queryset
        else:
            qs = self.model.objects.all()
        kw = self.get_master_kw(rr.master_instance,**rr.params)
        if kw is None:
            return []
        if len(kw):
            qs = qs.filter(**kw)

        if self.filter:
            qs = qs.filter(**self.filter)
        if self.exclude:
            qs = qs.exclude(**self.exclude)
              
        if rr.quick_search is not None:
            #~ qs = add_quick_search_filter(qs,self.model,rr.quick_search)
            qs = add_quick_search_filter(qs,rr.quick_search)
        if rr.gridfilters is not None:
            qs = add_gridfilters(qs,rr.gridfilters)
        order_by = rr.order_by or self.order_by
        if order_by:
            qs = qs.order_by(*order_by.split())
        return qs
        

    def as_string(self,qs,max_items=10,format=unicode,separator=', '):
        """
        Returns this report as a unicode string.
        
        :param max_items: don't include more than
        """
        s = u''
        n = 0
        for i in qs:
            if n :
                s += separator
            n += 1
            s += format(i)
            if n >= max_items:
                s += separator + '...'
                return s
        return s
        
    def setup_request(self,req):
        pass
        
    def get_master_kw(self,master_instance,**kw):
        #lino.log.debug('%s.get_master_kw(%r) master=%r',self,kw,self.master)
        if self.master is None:
            assert master_instance is None, "Report %s doesn't accept a master" % self.actor_id
        elif self.master is ContentType:
            if master_instance is None:
                kw[self.fk.ct_field] = None,
                kw[self.fk.fk_field] = None
            else:
                ct = ContentType.objects.get_for_model(master_instance.__class__)
                kw[self.fk.ct_field] = ct
                kw[self.fk.fk_field] = master_instance.pk
        else:
            if master_instance is None:
                if not self.fk.null:
                    return # cannot add rows to this report
                kw[self.fk.name] = master_instance
                
                #kw["%s__exact" % self.fk.name] = None
            elif not isinstance(master_instance,self.master):
                raise Exception("%r is not a %s" % (master_instance,self.master.__name__))
            else:
                kw[self.fk.name] = master_instance
        return kw
        
    #~ def on_create(self,instance,request):
        #~ pass
        
    def create_instance(self,req,**kw):
        instance = self.model(**kw)
        #~ self.on_create(instance,req)
        
        """
        Used e.b. by modlib.notes.Note.on_create().
        on_create gets the request as argument.
        Didn't yet find out how to do that using a standard Django signal 
        """
        m = getattr(instance,'on_create',None)
        if m:
            m(req)
        return instance
        
    def getLabel(self):
        return self.label
        
    #~ def __str__(self):
        #~ return rc_name(self.__class__)
        
    def ajax_update(self,request):
        print request.POST
        return HttpResponse("1", mimetype='text/x-json')


    def as_text(self, *args,**kw):
        from lino.ui import console
        return console.ui.report_as_text(self)
        
    @classmethod
    def unused_register_page_layout(cls,layout):
        if cls.page_layout is not None:
            lino.warning('Detail layout %s in %s overridden by %s',
              cls.page_layout,cls,layout)
        cls.page_layout = layout
        #~ cls.page_layout = tuple(cls.page_layouts) + layouts
        
    #~ def render_to_dict(self,**kw):
        #~ rh = self.get_handle(None) # ReportHandle(None,self)
        #~ rr = self.request(None,**kw)
        #~ return rr.render_to_dict()
        
    def request(self,ui=None,**kw):
        return self.get_handle(ui).request(**kw)

    def row2dict(self,row,d):
        """
        Overridden by lino.modlib.properties.PropValuesByOwner.
        See also lino.ui.extjs.ext_requests.ViewReportRequest.
        """
        for n in self.column_names.split():
            d[n] = getattr(row,n)
        return d
        
        
def report_factory(model):
    lino.log.debug('report_factory(%s) -> app_label=%r',model.__name__,model._meta.app_label)
    cls = type(model.__name__+"Report",(Report,),dict(model=model,app_label=model._meta.app_label))
    return actors.register_actor(cls())

#~ def choice_report_factory(model,field):
    #~ clsname = model.__name__+"_"+field.name+'_'+"Choices"
    #~ fldname = model._meta.app_label+'.'+model.__class__.__name__+'.'+field.name
    #~ return type(clsname,(Report,),dict(field=fldname,app_label=model._meta.app_label,column_names='__unicode__'))



def column_choices(rptname):
    rpt = actors.get_actor(rptname)
    return rpt.column_choices()

def unused_rptname_choices():
    for rpt in actors.actors_list:
      if isinstance(rpt,Report) and rpt.__class__ is not Report:
          yield [rpt.actor_id, rpt.get_label]
          
