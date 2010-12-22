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

import logging
logger = logging.getLogger(__name__)

import os
import traceback
import codecs
import yaml
#~ import datetime
#import logging ; logger = logging.getLogger('lino.reports')
#~ import cPickle as pickle
import pprint

from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.text import capfirst
from django.utils.encoding import force_unicode 

from django.db import models
from django.db.models.query import QuerySet
from django.db.models.fields.related import ForeignRelatedObjectsDescriptor
from django import forms
from django.conf.urls.defaults import patterns, url, include
from django.forms.models import modelform_factory
from django.forms.models import _get_foreign_key
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

#~ from dateutil import parser as dateparser

from django.http import HttpResponse
from django.utils.safestring import mark_safe


import lino
#~ from lino import layouts
from lino import actions
from lino.utils import perms, menus
#~ from lino.utils import printable
from lino.core import datalinks
from lino.core import boolean_texts
from lino.core import actors
#~ from lino.core import action_requests
from lino.ui import base

from lino.tools import resolve_model, resolve_field, get_app, model_label, get_field
from lino.utils.config import find_config_files, LOCAL_CONFIG_DIR
from lino.core.coretools import get_slave, get_model_report, data_elems, get_data_elem

#~ from lino.modlib import field_choices


def parse_js_date(s,name):
    #~ v = dateparser.parse(s)
    #~ v = dateparser.parse(s,fuzzy=True)
    return lino.PARSE_DATE(s)
    #~ print "parse_js_date %s : %r -> %s" % (name,s,v)
    #~ return v


def fields_list(model,field_names):
    return tuple([get_field(model,n) for n in field_names.split()])


def summary(ui,rr,separator=', ',max_items=5,**kw):
    """
    Returns this report as a unicode string.
    
    :param max_items: don't include more than the specified number of items.
    """
    #~ if format is None:
        #~ def format(rr,obj):
            #~ return unicode(obj)
    s = u''
    n = 0
    for i in rr:
        if n :
            s += separator
        n += 1
        s += i.summary_row(ui,rr,**kw)
        if n >= max_items:
            s += separator + '...'
            return s
    return s

#~ def default_summary_row(obj,rr):
    #~ return u'<a href="%s" target="_blank">%s</a>' % (rr.get_request_url(str(obj.pk),fmt='detail'),unicode(obj))
    #~ return u'<span onClick="foo">%s</span>' % (ui.get_actor_url(self,str(obj.pk)),unicode(obj))
    #~ return u'<a href="#" onclick="Lino.foo">%s</a>' % unicode(obj)
        


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
            v = parse_js_date(flt['value'],field.name)
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

config_dirs = []

def register_report(rpt):
    #rptclass.app_label = rptclass.__module__.split('.')[-2]
    if rpt.typo_check:
        myattrs = set(rpt.__class__.__dict__.keys())
        for attr in base_attrs(rpt.__class__):
            myattrs.discard(attr)
        if len(myattrs):
            logger.warning("%s defines new attribute(s) %s", rpt.__class__, ",".join(myattrs))
    
    if rpt.model is None:
        #~ logger.debug("%s is an abstract report", rpt)
        return
        
    #~ rptname_choices.append((rpt.actor_id, rpt.get_label()))
    rptname_choices.append(rpt.actor_id)
    
    if rpt.master is None:
        master_reports.append(rpt)
        if rpt.use_as_default_report:
            #~ logger.debug("register %s : model_report for %s", rpt.actor_id, model_label(rpt.model))
            rpt.model._lino_model_report = rpt
        else:
            #~ logger.debug("register %s: not used as model_report",rpt.actor_id)
            pass
    elif rpt.master is ContentType:
        #~ logger.debug("register %s : generic slave for %r", rpt.actor_id, rpt.fk_name)
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
              
    logger.info("Analyzing Reports...")
    #~ logger.debug("Register Report actors...")
    for rpt in actors.actors_list:
        if isinstance(rpt,Report) and rpt.__class__ is not Report:
            register_report(rpt)
            
    #~ logger.debug("Instantiate model reports...")
    for model in models.get_models():
        rpt = getattr(model,'_lino_model_report',None)
        if rpt is None:
            rpt = report_factory(model)
            register_report(rpt)
            model._lino_model_report = rpt
            
            
    #~ logger.debug("Analyze %d slave reports...",len(slave_reports))
    for rpt in slave_reports:
        slaves = getattr(rpt.master,"_lino_slaves",None)
        if slaves is None:
            slaves = {}
            rpt.master._lino_slaves = slaves
        slaves[rpt.actor_id] = rpt
        #~ logger.debug("%s: slave for %s",rpt.actor_id, rpt.master.__name__)
    #~ logger.debug("Assigned %d slave reports to their master.",len(slave_reports))
        
    #~ logger.debug("Setup model reports...")
    #~ for model in models.get_models():
        #~ model._lino_model_report.setup()
        
    #~ logger.debug("Instantiate property editors...")
    #~ for model in models.get_models():
        #~ pw = ext_elems.PropertiesWindow(model)
        #~ model._lino_properties_window = pw
            
    #~ logger.debug("reports.setup() done")


class StaticText:
    def __init__(self,text):
        self.text = text
        
#~ class Picture:
    #~ pass
    
class DataView:
    def __init__(self,tpl):
        self.xtemplate = tpl


class ReportHandle(datalinks.DataLink,base.Handle): 
  
    
    def __init__(self,ui,report):
        #logger.debug('ReportHandle.__init__(%s)',rd)
        assert isinstance(report,Report)
        self.report = report
        self._layouts = None
        #~ actors.ActorHandle.__init__(self,report)
        datalinks.DataLink.__init__(self,ui)
        base.Handle.__init__(self,ui)
        if self.report.model is not None:
            self.list_layout = LayoutHandle(self,ListLayout('main = '+self.report.column_names))
            self.content_type = ContentType.objects.get_for_model(self.report.model).pk
            self.data_elems = report.data_elems
            self.get_data_elem = report.get_data_elem
        
  
    def __str__(self):
        return str(self.report) + 'Handle'
            
    def setup_layouts(self):
        if self._layouts is not None:
            return
        #~ self.default_action = self.report.default_action(self)
        self._layouts = [ self.list_layout ] 
        if self.report.model is not None:
            self._layouts += [ LayoutHandle(self,dtl) for dtl in self.report.model._lino_detail_layouts ]

    def submit_elems(self):
        return []
        
    def get_layout(self,i):
        self.setup_layouts()
        return self._layouts[i]
        
    def get_used_layouts(self):
        self.setup_layouts()
        return self._layouts
        
    def get_detail_layouts(self):
        self.setup_layouts()
        return self._layouts[1:]
        
    def get_list_layout(self):
        self.setup_layouts()
        return self._layouts[0]
        
    #~ def get_absolute_url(self,*args,**kw):
        #~ return self.ui.get_report_url(self,*args,**kw)
        
    #~ def data_elems(self):
        #~ for de in self.report.data_elems(): yield de
    #~ def get_data_elem(self,name):
        #~ return get_data_elem(self.report.model,name)
        
    def get_slaves(self):
        return [ sl.get_handle(self.ui) for sl in self.report._slaves ]
            
    def get_action(self,name):
        return self.report.get_action(name)
    def get_actions(self,*args,**kw):
        return self.report.get_actions(*args,**kw)
        
    def get_details(self):
        return self.report.details
        #~ return self.layouts[1:]
          
        
    #~ def request(self,*args,**kw):
        #~ ar = ReportActionRequest(self.ui,self.report.list_action)
        #~ ar.setup(*args,**kw)
        #~ return ar
        
    def update_detail(self,tab,desc):
        old_dtl = self.report.model._lino_detail_layouts[tab]
        #~ old_dtl._kw.update(desc=desc)
        #~ old_dtl._desc=desc
        dtl = DetailLayout(desc,old_dtl.cd,old_dtl.filename)
        self.report.model._lino_detail_layouts[tab] = dtl
        self._layouts[tab+1] = LayoutHandle(self,dtl)
        self.ui.setup_handle(self)
        #~ self.report.save_config()
        dtl.save_config()

class InvalidRequest(Exception):
    pass


class ReportActionRequest:
    limit = None
    offset = None
    master_instance = None
    master = None
    instance = None
    create_rows = None
    extra = None
    layout = None
    #~ selected_rows = []
    
    def __init__(self,ui,report,action):
    #~ def __init__(self,rh,action):
        #~ assert isinstance(rh,ReportHandle)
        assert ui.create_meth_element is not None
        #~ if ui is not None: assert ui.create_meth_element is not None
        self.report = report
        self.ah = report.get_handle(ui)
        self.ui = ui
        # Subclasses (e.g. BaseViewReportRequest) may set `master` before calling ReportRequest.__init__()
        if self.master is None:
            self.master = report.master
        #~ actions.ActionRequest.__init__(self,rpt,action,ui)
        #~ actions.ActionRequest.__init__(self,ui,action)
        #~ self.rh = self.ah
        self.action = action
      
    def __str__(self):
        return self.__class__.__name__ + '(' + self.report.actor_id + ",%r,...)" % self.master_instance

    def setup(self,
            master=None,
            master_instance=None,
            #~ master_id=None,
            offset=None,limit=None,
            layout=None,user=None,
            create_rows=None,
            quick_search=None,
            gridfilters=None,
            order_by=None,
            extra=None,
            #~ selected_rows=None,
            **kw):
        if user is not None and not self.report.can_view.passes(user):
            msg = _("User %(user)s cannot view %(report)s.") % dict(user=user,report=self.report)
            raise InvalidRequest(msg)
        self.user = user
        self.quick_search = quick_search
        self.gridfilters = gridfilters
        self.order_by = order_by
        self.extra = extra
        #~ if selected_rows is not None:
            #~ self.selected_rows = selected_rows
        
        if master is None:
            master = self.report.master
            # master might still be None
        self.master = master
        
        kw.update(self.report.params)
        self.params = kw
        
        #~ if master_id is not None:
            #~ assert master_instance is None
            #~ master_instance = self.master.get(pk=master_pk)
            
        self.master_kw = self.report.get_master_kw(master_instance)
        self.master_instance = master_instance
        if self.create_rows is None:
            if create_rows is None:
                if self.master_kw is None:
                    create_rows = 0
                elif self.user is not None and self.report.can_add.passes(self.user):
                    create_rows = 1
                else:
                    create_rows = 0
            self.create_rows = create_rows
        if self.ui is not None:
            if layout is None:
                layout = self.ah._layouts[self.report.default_layout]
            else:
                layout = self.ah._layouts[layout]
            self.layout = layout
        self.report.setup_request(self)
        self.queryset = self.get_queryset()
        #~ self.setup_queryset()
        #~ logger.debug(unicode(self))
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
        return self.report.get_request_queryset(self)
        #~ return self.report.get_queryset(master_instance=self.master_instance,**kw)
        
    def __iter__(self):
        return self.queryset.__iter__()
        
    def __len__(self):
        return self.queryset.__len__()
        
    def create_instance(self,**kw):
        if self.master_kw:
            kw.update(self.master_kw)
        #logger.debug('%s.create_instance(%r)',self,kw)
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
        
    #~ def as_text(self,*args,**kw):
        #~ from lino.ui import console
        #~ rh = self.get_report_handle(rpt)
        #~ rr = renderers_text.TextReportRequest(rh,*args,**kw)
        #~ return rr.render()
        #~ return console.ui.report_as_text(self)

    def get_request_url(self,*args,**kw):
        return self.ui.get_request_url(self,*args,**kw)


#~ class IterActionRequest(actions.ActionRequest)
    #~ def __init__(self,ui,iter,action):
        #~ self.iter = iter
        #~ actions.ActionRequest.__init__(self,ui,action)
        
def model2report(m):
    def f(self,request,obj):
        return m(obj,request)
        #~ return getattr(obj,name)(request)
    return f


class Report(actors.Actor): #,base.Handled):
    """
    Reports are a central concept in Lino and deserve more than one sentence of documentation.
    """
    default_action_class = actions.GridEdit
    _handle_class = ReportHandle
    #~ _handle_selector = base.UI
    params = {}
    field = None
    
    base_queryset = None 
    "See :meth:`Report.get_queryset`"
    
    model = None
    use_as_default_report = True
    order_by = None
    
    extra = None
    """
    Examples::
    
      extra = dict(select=dict(lower_name='lower(name)'))
      # (or if you prefer:) 
      # extra = {'select':{'lower_name':'lower(name)'},'order_by'=['lower_name']}
      
    
    List of SQL functions and which RDBMS supports them:
    http://en.wikibooks.org/wiki/SQL_Dialects_Reference/Functions_and_expressions/String_functions
    
    """
    
    filter = None
    exclude = None
    title = None
    column_names = '*'
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
    #~ display_field = '__unicode__'
    #date_format = 'Y-m-d'
    #date_format = '%d.%m.%y'
    
    #~ detail_layouts = None
    
    #~ page_layout = None # (layouts.PageLayout ,)
    #~ row_layout_class = None
    
    cell_edit = True # use ExtJS CellSelectionModel (False to use ExtJS RowSelectionModel)
    
    date_format = lino.DATE_FORMAT_EXTJS
    boolean_texts = boolean_texts
    
    can_view = perms.always
    can_add = perms.is_authenticated
    can_change = perms.is_authenticated
    #~ can_delete = perms.is_authenticated
    can_config = perms.is_staff
    
    show_prev_next = True
    
    #~ default_action = GridEdit
    default_layout = 0
    
    typo_check = True
    url = None
    
    #~ use_layouts = True
    
    button_label = None
    
    #~ detail_layouts = []
    
    show_slave_grid = True
    """
    How to display this report when it is a slave in a Detail. 
    Usually a slave report is rendered as a grid. 
    If `show_slave_grid` is ``False``, show only a summary.
    Example: :class:`links.LinksByOwner`
    """
    
    grid_configs = {}
    """
    Will be filled during :meth:`lino.reports.Report.do_setup`. 
    """
    
    disabled_fields = None
    """
    Return a list of field names that should not be editable 
    for the specified `obj` and `request`.
    
    If defined in the Report, this must be a method that accepts two arguments `request` and `obj`::
    
      def disabled_fields(self,request,obj):
          ...
          return []
    
    If not defined in a subclass, the report will look whether it's model has a `disabled_fields` 
    method expecting a single argument `request` and install a wrapper to this model method.
    See also :doc:`/tickets/closed/2`.
    """
    
    disable_delete = None
    """
    Return either `None` if this `obj` *is allowed* to be deleted by `request`,
    or a string with a message explaining why, if not.
    
    Same remarks as for :attr:`disabled_fields`.
    """
    
    handle_uploaded_files = None
    """
    Same remarks as for :attr:`disabled_fields`.
    """
    
    has_navigator = True
    """
    Whether a Detail Form should have navigation buttons.
    This option is False in :class:`lino.SiteConfigs`.
    """
    
    def __init__(self):
        if self.model is None:
            if self.base_queryset is not None:
                self.model = self.base_queryset.model
            # raise Exception(self.__class__)
        else:
            self.model = resolve_model(self.model,self.app_label,self)
            
        if self.model is not None:
            self.app_label = self.model._meta.app_label
            if self.label is None:
                self.label = capfirst(self.model._meta.verbose_name_plural)
            
        #~ logger.debug("Report.__init__() %s", self)
        actors.Actor.__init__(self)
        #~ base.Handled.__init__(self)
        
        if self.model is not None:
          
            for name in ('disabled_fields','disable_delete','handle_uploaded_files'):
                if getattr(self,name) is None:
                    m = getattr(self.model,name,None)
                    if m is not None:
                        logger.debug('Install model method %s.%s to %s',self.model.__name__,name,self)
                        setattr(self.__class__,name,model2report(m))
                        
            #~ if self.disable_delete is None:
                #~ m = getattr(self.model,'disable_delete',None)
                #~ if m:
                    #~ def disable_delete(self,request,obj):
                        #~ return obj.disable_delete(request)
                    #~ self.__class__.disable_delete = disable_delete
                    #~ print 20101104, self, 'install disable_delete from',self.model.__name__
                
        
        if self.fk_name:
            if self.model is not None:
                #~ assert self.model is not None, "%s has .fk_name but .model is None" % self
                #~ self.master = resolve_model(self.master,self.app_label)
                try:
                    fk, remote, direct, m2m = self.model._meta.get_field_by_name(self.fk_name)
                    assert direct
                    assert not m2m
                    master = fk.rel.to
                except models.FieldDoesNotExist,e:
                    #~ logger.debug("FieldDoesNotExist in %r._meta.get_field_by_name(%r)",self.model,self.fk_name)
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
            #~ logger.warning("DEPRECATED: replace %s.master by fk_name" % self.actor_id)
            #~ #assert isinstance(self.master,object), "%s.master is a %r" % (self.name,self.master)
            #~ assert issubclass(self.master,models.Model), "%s.master is a %r" % (self.actor_id,self.master)
            #~ self.fk = _get_foreign_key(self.master,self.model) #,self.fk_name)
        
        self.default_action = self.default_action_class(self)
        #~ self.list_action = ListAction(self)
        
        if self.order_by is not None:
            if not isinstance(self.order_by,(list,tuple)):
                raise Exception("%s.order_by is %r (must be a list or tuple)" % (self,self.order_by))
            if False: 
              # good idea, but doesn't yet work for foreign fields, 
              # e.g. order_by = ['content_type__app_label']
              for fieldname in self.order_by:
                  try:
                      fk, remote, direct, m2m = self.model._meta.get_field_by_name(fieldname)
                      assert direct
                      assert not m2m
                  except models.FieldDoesNotExist,e:
                      raise Exception("Unknown fieldname %r in %s.order_by" % (fieldname,self))
        
        
    @classmethod
    def spawn(cls,suffix,**kw):
        kw['app_label'] = cls.app_label
        return type(cls.__name__+str(suffix),(cls,),kw)
        
    def column_choices(self):
        return [ de.name for de in self.data_elems() ]
          
    def validate_gc(self,d):
        if not d.has_key('grid_configs'):
            raise Exception("grid_configs is missing")
        for name,gc in d['grid_configs'].items():
            if len(gc['columns']) != len(gc['widths']):
                raise Exception("len(gc['columns']) != len(gc['widths'])")
            for colname in gc['columns']:
                f = self.get_data_elem(colname)
                if f is None:
                    raise Exception("unknown data element %r" % colname)
      
    def do_setup(self):
      
        filename = self.get_grid_config_file()
        if os.path.exists(filename):
            logger.info("Loading %s...",filename)
            d = yaml.load(codecs.open(filename,encoding='utf-8').read())
            if d is not None:
                self.validate_gc(d)
                self.grid_configs = d['grid_configs']
            #~ execfile(filename,dict(self=self))
            #~ self.grid_configs = pickle.load(open(filename,"rU"))
        else:
            self.grid_configs = {}
            
        #~ alist = [ ac(self) for ac in self.actions ]
        alist = []
          
        if self.model is not None:
          
                
            #~ if issubclass(self.model,printable.Printable):
                #~ alist.append(printable.PrintAction(self))
                #~ alist.append(printable.ClearCacheAction(self))
                    
            if hasattr(self.model,'_lino_slaves'):
                self._slaves = self.model._lino_slaves.values()
            else:
                self._slaves = []
                
            if len(self.model._lino_detail_layouts) > 0:
                alist.append(actions.ShowDetailAction(self))
                alist.append(actions.SubmitDetail(self))
                alist.append(actions.InsertRow(self))
                alist.append(actions.SubmitInsert(self))
                    
            alist.append(actions.DeleteSelected(self))
            
                
            #~ self.list_layout = layouts.list_layout_factory(self)
            #~ self.detail_layouts = layouts.get_detail_layouts_for_report(self)
            #~ self.detail_layouts = 
              
            if hasattr(self.model,'get_image_url'):
                alist.append(actions.ImageAction(self))
        alist.append(self.default_action)
        self.set_actions(alist)
                
        if self.button_label is None:
            self.button_label = self.label
            
        if self.model is not None:
            m = getattr(self.model,'setup_report',None)
            if m:
                m(self)
        

    def get_grid_config_file(self):
        #~ filename = str(self) + ".py"
        filename = str(self) + ".rpt"
        return os.path.join(settings.DATA_DIR,filename)
        
    def save_config(self):
        filename = self.get_grid_config_file()
        f = open(filename,'w')
        f.write("# Generated file. Delete it to restore factory settings.\n")
        d = dict(grid_configs=self.grid_configs)
        f.write(yaml.dump(d))
        #~ f.write('self.grid_configs = %s\n' % pprint.pformat(self.grid_configs))
        f.close()
        return "Grid Config has been saved to %s" % filename
        
            
        
    def data_elems(self):
        for de in data_elems(self.model): yield de
          
    def get_data_elem(self,name):
        return get_data_elem(self.model,name)
        
    def get_details(self):
        return self.details
            
    def get_title(self,rr):
        """
        Return the title of this Report for the given request `rr`.
        Override this if your Report's title should mention for example filter conditions.
        """
        assert rr is not None
        #~ if rr is not None and self.master is not None:
        if self.master is not None:
            return _("%(details)s by %(model)s %(master)s") % dict(
              model=self.master._meta.verbose_name,
              #~ model=rr.master_instance._meta.verbose_name,
              details=self.model._meta.verbose_name_plural,
              master=rr.master_instance)
        return self.title or self.label
        
    def get_queryset(self):
        """
        Return an iterable over the items processed by this report.
        Override this to use e.g. select_related()
        or to return a list.
        """
        return self.model.objects.all()
      
    def get_request_queryset(self,rr):
        """
        Build a Queryset for the specified request on this report.
        Upon first call, this will also lazily install Report.queryset 
        which will be reused on every subsequent call.
        """
        if self.base_queryset is None:
            self.base_queryset = self.get_queryset()
        qs = self.base_queryset
        #~ if self.queryset is not None:
            #~ qs = self.queryset
        #~ else:
            #~ qs = self.model.objects.all()
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
        extra = rr.extra or self.extra
        if extra is not None:
            qs = qs.extra(**extra)
        order_by = rr.order_by or self.order_by
        if order_by:
            qs = qs.order_by(*order_by)
        return qs

    def slave_as_summary_meth(self,ui,row_separator):
        """
        Creates and returns the method to be used when :attr:`Report.show_slave_grid` is `False`.
        """
        def meth(master):
            rr = self.request(ui,master_instance=master)
            s = summary(ui,rr,row_separator)
            #~ s = ', '.join([fmt(r) for r in rr])
            #~ print 'reports.py 20101017', s
            return s
        return meth
        
        
    def setup_request(self,req):
        pass
        
    def get_master_kw(self,master_instance,**kw):
        #logger.debug('%s.get_master_kw(%r) master=%r',self,kw,self.master)
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
        Used e.g. by modlib.notes.Note.on_create().
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


    #~ @classmethod
    #~ def reset_details(cls):
        #~ return
        #~ cls.detail_layouts = []
      
    #~ @classmethod
    #~ def add_detail(cls,*args,**kw):
        #~ return
        #~ dtl = DetailLayout(*args,**kw)
        #~ cls.detail_layouts = list(cls.detail_layouts) # disconnect from base class
        #~ for i,layout in enumerate(cls.detail_layouts):
            #~ if layout.label == dtl.label:
                #~ cls.detail_layouts[i] = dtl
                #~ return
        #~ cls.detail_layouts.append(dtl)
        
    @classmethod
    def request(cls,ui=None,**kw):
        self = cls()
        ar = ReportActionRequest(ui,self,self.default_action)
        #~ ar = ReportActionRequest(ui,self.list_action)
        ar.setup(**kw)
        return ar
        #~ return self.get_handle(ui).request(**kw)

    def row2dict(self,row,d):
        """
        Overridden by lino.modlib.properties.PropValuesByOwner.
        See also lino.ui.extjs.ext_requests.ViewReportRequest.
        """
        for n in self.column_names.split():
            d[n] = getattr(row,n)
        return d
        
        
def report_factory(model):
    logger.debug('report_factory(%s) -> app_label=%r',model.__name__,model._meta.app_label)
    cls = type(model.__name__+"Report",(Report,),dict(model=model,app_label=model._meta.app_label))
    return actors.register_actor(cls())


def column_choices(rptname):
    rpt = actors.get_actor(rptname)
    return rpt.column_choices()

def unused_rptname_choices():
    for rpt in actors.actors_list:
      if isinstance(rpt,Report) and rpt.__class__ is not Report:
          yield [rpt.actor_id, rpt.get_label]
          

class LayoutError(RuntimeError):
    pass
  
LABEL_ALIGN_TOP = 'top'
LABEL_ALIGN_LEFT = 'left'
LABEL_ALIGN_RIGHT = 'right'

class BaseLayout:
    label = None
    has_frame = False # True
    label_align = LABEL_ALIGN_TOP
    #label_align = LABEL_ALIGN_LEFT
    default_button = None
    collapsible_elements  = {}
    filename = None
    cd = None # ConfigDir
    write_debug_info = False
    
    def __init__(self,desc,cd=None,filename=None):
        if filename is not None:
            assert not os.sep in filename
        #~ self.label = label
        self._desc = desc
        self.filename = filename
        self.cd = cd
        #~ self._kw = kw
        #~ for k,v in kw.items():
            #~ if not hasattr(self,k):
                #~ raise Exception("Unexpected keyword argument %s=%r" % (k,v))
            #~ setattr(self,k,v)
            
        attrname = None
        for ln in desc.splitlines():
            if ln and not ln.lstrip().startswith('## '):
                if ln[0].isspace():
                    if attrname is None:
                        raise LayoutError('attrname is None')
                    v = getattr(self,attrname) + '\n' + ln.strip()
                    setattr(self,attrname,v) 
                elif ln.startswith(':'):
                    a = ln.split(':',2)
                    if len(a) != 3:
                        raise LayoutError('Expected attribute `:attr:value` ')
                    attname = a[1]
                    if not hasattr(self,attname):
                        raise LayoutError('Invalid layout field %r' % attname)
                    setattr(self,attname,a[2].strip())
                else:
                    a = ln.split('=',1)
                    if len(a) != 2:
                        raise LayoutError('"=" expected in %r' % ln)
                    attrname = a[0].strip()
                    if hasattr(self,attrname):
                        raise Exception('Duplicate element definition')
                    setattr(self,attrname,a[1].strip())
          
    def get_hidden_elements(self,lh):
        return set()
        
    def save_config(self):
        if self.filename:
            if not self.cd.can_write:
                print self.cd, "is not writable", self.filename
                self.cd = LOCAL_CONFIG_DIR
            fn = os.path.join(self.cd.name,self.filename)
            logger.info("Layout.save_config() -> %s",fn)
            f = open(fn,'w')
            f.write(self._desc)
            f.close()
            
    def __str__(self):
        if self.filename:
            return u"%s (from %s)" % (self.filename,self.cd.name)
        return "%s(%r)" % (self.__class__.__name__,self._desc)
        
class ListLayout(BaseLayout):
    #~ label = _("List")
    show_labels = False
    join_str = " "
    

class DetailLayout(BaseLayout):
    #~ label = _("Detail")
    show_labels = True
    join_str = "\n"
    only_for_report = None



class LayoutHandle:
    """
    LayoutHandle analyzes a Layout and builds a tree of LayoutElements.
    
    """
    start_focus = None
    
    def __init__(self,rh,layout):
      
        # logger.debug('LayoutHandle.__init__(%s,%s,%d)',link,layout,index)
        assert isinstance(layout,BaseLayout)
        #assert isinstance(link,reports.ReportHandle)
        #~ base.Handle.__init__(self,ui)
        #~ actors.ActorHandle.__init__(self,layout)
        self.layout = layout
        self.rh = rh
        #~ self.datalink = layout.get_datalink(ui)
        #~ self.name = layout._actor_name
        self.label = layout.label # or ''
        self._store_fields = []
        #~ self._elems_by_field = {}
        #~ self._submit_fields = []
        #~ self.slave_grids = []
        self._buttons = []
        self.hide_elements = layout.get_hidden_elements(self)
        self.main_class = rh.ui.main_panel_class(layout)
        
        if layout.main is not None:
        #~ if hasattr(layout,"main"):
            self._main = self.create_element(self.main_class,'main')
        else:
            raise Exception("%s has no main" % self.layout)
            
        #~ if isinstance(self.layout,ListLayout):
            #~ assert len(self._main.elements) > 0, "%s : Grid has no columns" % self
            #~ self.columns = self._main.elements
            
        #~ self.width = self.layout.width or self._main.width
        #~ self.height = self.layout.height or self._main.height
        self.width = self._main.width
        self.height = self._main.height
        if True:
            self.write_debug_info()
        
        #~ self.default_button = None
        #~ if layout.default_button is not None:
            #~ for e in self._buttons:
                #~ if e.name == layout.default_button:
                    #~ self.default_button = e
                    #~ break
                
    #~ def needs_store(self,rh):
        #~ self._needed_stores.add(rh)
        
    #~ def __str__(self):
        #~ return str(self.layout) + "Handle"
        
    def __str__(self):
        return "%s%s" % (self.rh.report,self.__class__.__name__)
        
    #~ def elems_by_field(self,name):
        #~ return self._elems_by_field.get(name,[])
        
    def add_store_field(self,field):
        self._store_fields.append(field)
            
    def has_field(self,f):
        return self._main.has_field(f)
        
    def unused__repr__(self):
        s = self.name # self.__class__.__name__ 
        if hasattr(self,'_main'):
            s += "(%s)" % self._main
        return s
        
    def setup_element(self,e):
        if e.name in self.hide_elements:
            self.hidden = True
            
    #~ def get_absolute_url(self,**kw):
        #~ return self.datalink.get_absolute_url(layout=self.index,**kw)
        
        
    def add_hidden_field(self,field):
        return HiddenField(self,field)
        
    def write_debug_info(self):
        if self.layout.filename and self.layout.write_debug_info:
            filename = "%s.debug.html" % self.layout.filename
            logger.info("Writing %s..." % filename)
            f = codecs.open(filename,"w",encoding='utf-8')
            f.write('''<html><body><table border="1">''')
            f.write(u"\n".join(self._main.debug_lines()))
            f.write('''</table></body></html>''')
            f.close()
        
    def get_title(self,ar):
        return self.layout.get_title(ar)
        
    def walk(self):
        return self._main.walk()
        
    def ext_lines(self,request):
        return self._main.ext_lines(request)
  
  
    def desc2elem(self,panelclass,desc_name,desc,**kw):
        #logger.debug("desc2elem(panelclass,%r,%r)",desc_name,desc)
        #assert desc != 'Countries_choices2'
        if '*' in desc:
            explicit_specs = set()
            for spec in desc.split():
                if spec != '*':
                    name,kw = self.splitdesc(spec)
                    explicit_specs.add(name)
            wildcard_fields = self.layout.join_str.join([
                de.name for de in self.rh.report.data_elems() \
                  if (de.name not in explicit_specs) \
                    and (de.name not in self.hide_elements) \
                    and (de.name != self.rh.report.fk_name) \
                ])
            desc = desc.replace('*',wildcard_fields)
            #logger.debug('desc -> %r',desc)
        if "\n" in desc:
            elems = []
            i = 0
            for x in desc.splitlines():
                x = x.strip()
                if len(x) > 0 and not x.startswith("# "):
                    i += 1
                    e = self.desc2elem(self.rh.ui.Panel,desc_name+'_'+str(i),x,**kw)
                    if e is not None:
                        elems.append(e)
            if len(elems) == 0:
                return None
            if len(elems) == 1 and panelclass != self.main_class:
                return elems[0]
            #return self.vbox_class(self,name,*elems,**kw)
            return panelclass(self,desc_name,True,*elems,**kw)
        else:
            elems = []
            for x in desc.split():
                if not x.startswith("#"):
                    """
                    20100214 dsbe.PersonDetail hatte 2 MainPanels, 
                    weil PageLayout kein einzeiliges (horizontales) `main` vertrug
                    """
                    #~ e = self.create_element(panelclass,x) 
                    e = self.create_element(self.rh.ui.Panel,x)
                    if e:
                        elems.append(e)
            if len(elems) == 0:
                return None
            if len(elems) == 1 and panelclass != self.main_class:
                return elems[0]
            #return self.hbox_class(self,name,*elems,**kw)
            return panelclass(self,desc_name,False,*elems,**kw)
            
    def create_element(self,panelclass,desc_name):
        #logger.debug("create_element(panelclass,%r)", desc_name)
        name,kw = self.splitdesc(desc_name)
        e = self.rh.ui.create_layout_element(self,panelclass,name,**kw)
        #~ for child in e.walk():
            #~ self._submit_fields += child.submit_fields()
        return e
        
    def splitdesc(self,picture):
        a = picture.split(":",1)
        if len(a) == 1:
            return picture,{}
        if len(a) == 2:
            name = a[0]
            a = a[1].split("x",1)
            if len(a) == 1:
                return name, dict(width=int(a[0]))
            elif len(a) == 2:
                return name, dict(width=int(a[0]),height=int(a[1]))
        raise Exception("Invalid picture descriptor %s" % picture)
        
