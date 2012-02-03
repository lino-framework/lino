## Copyright 2009-2012 Luc Saffre
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

import json
import cgi
import os
import sys
import traceback
import codecs
import yaml
#~ import datetime
#import logging ; logger = logging.getLogger('lino.reports')
#~ import cPickle as pickle
#~ import pprint

from appy import Object

from django.conf import settings
#~ from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django.utils.encoding import force_unicode
from django.utils.importlib import import_module

from django.db import models
from django.db.models.query import QuerySet
from django.db.models.fields.related import ForeignRelatedObjectsDescriptor
from django import forms
from django.conf.urls.defaults import patterns, url, include
from django.forms.models import modelform_factory
from django.forms.models import _get_foreign_key
#~ from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

#~ from dateutil import parser as dateparser

from django.http import HttpResponse
from django.utils.safestring import mark_safe


import lino
#~ from lino import layouts
from lino.core import fields
from lino.core import actions
from lino.utils import perms, menus, call_on_bases
from lino.utils import babel
from lino.tools import obj2str
from lino.utils.config import load_config_files, Configured
#~ from lino.core import datalinks
#~ from lino.core import boolean_texts
from lino.core import actors
#~ from lino.core import action_requests
from lino.ui import base

from lino.ui import requests as ext_requests

from lino.tools import resolve_model, resolve_field, get_app, full_model_name, get_field, UnresolvedModel
#~ from lino.utils.config import LOCAL_CONFIG_DIR
from lino.core.coretools import get_slave, get_model_report, get_data_elem
from lino.utils.tables import AbstractTable, AbstractTableRequest, VirtualTable
#~ from lino.utils.tables import GridEdit #, ComputedColumn


#~ from lino.modlib import field_choices

        

def unused_parse_js_date(s,name):
    #~ v = dateparser.parse(s)
    #~ v = dateparser.parse(s,fuzzy=True)
    return datetime.date(*settings.LINO.parse_date(s))
    #~ print "parse_js_date %s : %r -> %s" % (name,s,v)
    #~ return v
    
    
def wildcard_data_elems(model):
    """
    Yields names that will be used as wildcard column_names of a Table.
    """
    meta = model._meta
    #~ for f in meta.fields: yield f.name
    #~ for f in meta.many_to_many: yield f.name
    #~ for f in meta.virtual_fields: yield f.name
    for f in meta.fields: 
        #~ if f.editable:
        if not isinstance(f,fields.VirtualField):
            if not getattr(f,'_lino_babel_field',False):
                yield f
    for f in meta.many_to_many: yield f
    for f in meta.virtual_fields: 
        if not isinstance(f,fields.VirtualField):
            yield f
    # todo: for slave in self.report.slaves
  
    #~ for de in data_elems(self.model): yield de
      
    

def is_installed(app_label):
    if not '.' in app_label:
        app_label = '.' + app_label
    for s in settings.INSTALLED_APPS:
        if s.endswith(app_label):
            return True

def inject_field(model,name,field,doc=None):
    """
    Adds the given field to the given model.
    See also :doc:`/tickets/49`.
    """
    #~ model = resolve_model(model)
    if doc:
        field.__doc__ = doc
    model.add_to_class(name,field)
    return field



def fields_list(model,field_names):
    #~ return tuple([get_field(model,n) for n in field_names.split()])
    #~ if model.__name__ == 'Company':
        #~ print 20110929, [get_field(model,n) for n in field_names.split()]
    return [get_field(model,n).name for n in field_names.split()]


#~ def summary_row(obj,ui,rr,**kw):
def summary_row(obj,ui,**kw):
    m = getattr(obj,'summary_row',None)
    if m:
        #~ return m(ui,rr,**kw)
        #~ print 20120116, obj.__class__
        return m(ui,**kw)
    return ui.href_to(obj)
    #~ linkkw = {}
    #~ linkkw.update(fmt='detail')
    #~ url = ui.get_detail_url(obj,**linkkw)
    #~ return '<a href="%s">%s</a>' % (url,cgi.escape(force_unicode(obj)))
  

#~ def summary(ui,rr,separator=', ',max_items=5,before='',after='',**kw):
def summary(ui,objects,separator=', ',max_items=5,before='',after='',**kw):
    """
    Returns this table as a unicode string.
    
    :param max_items: don't include more than the specified number of items.
    """
    #~ if format is None:
        #~ def format(rr,obj):
            #~ return unicode(obj)
    s = u''
    n = 0
    #~ for i in rr.data_iterator:
    for i in objects:
        if n:
            s += separator
        else:
            s += before
        n += 1
        #~ s += summary_row(i,ui,rr,**kw)
        s += summary_row(i,ui,**kw)
        #~ s += i.summary_row(ui,rr,**kw)
        if n >= max_items:
            s += separator + '...' + after
            return s
    if n:
        return s + after
    return s

#~ def default_summary_row(obj,rr):
    #~ return u'<a href="%s" target="_blank">%s</a>' % (rr.get_request_url(str(obj.pk),fmt='detail'),unicode(obj))
    #~ return u'<span onClick="foo">%s</span>' % (ui.get_actor_url(self,str(obj.pk)),unicode(obj))
    #~ return u'<a href="#" onclick="Lino.foo">%s</a>' % unicode(obj)
        


def base_attrs(cl):
    #~ if cl is Table or len(cl.__bases__) == 0:
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
            kw = {field.name+"__icontains": search_text}
            q = q | models.Q(**kw)
    if search_text.isdigit():
        for field in qs.model._meta.fields:
            if isinstance(field,(models.IntegerField,models.AutoField)):
                kw = {field.name: int(search_text)}
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
                search_field = getattr(field.rel.to,'grid_search_field',None)
                if search_field is None:
                    search_field = 'name'
                kw[field.name + "__%s__contains" % search_field] = flt['value']
            else:
                raise NotImplementedError(repr(flt))
        elif flttype == 'numeric':
            cmp = str(flt['comparison'])
            if cmp == 'eq': cmp = 'exact'
            kw[field.name+"__"+cmp] = flt['value']
        elif flttype == 'boolean':
            kw[field.name+"__equals"] = flt['value']
        elif flttype == 'date':
            v = datetime.date(*settings.LINO.parse_date(flt['value']))
            #~ v = parse_js_date(flt['value'],field.name)
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
    
#~ def de_verbose_name(de):
    #~ if isinstance(de,models.Field):
        #~ return de.verbose_name
    #~ return de.name

    
    
# TODO : move these global variables to LinoSite
master_reports = []
slave_reports = []
generic_slaves = {}
frames = []
custom_tables = []
#~ rptname_choices = []

config_dirs = []

  
def register_frame(frm):
    frames.append(frm)
    
def register_report(rpt):
    #~ logger.debug("20120103 register_report %s", rpt.actor_id)
    #rptclass.app_label = rptclass.__module__.split('.')[-2]
    
    #~ if rpt.typo_check:
        #~ myattrs = set(rpt.__dict__.keys())
        #~ for attr in base_attrs(rpt):
            #~ myattrs.discard(attr)
        #~ if len(myattrs):
            #~ logger.warning("%s defines new attribute(s) %s", rpt, ",".join(myattrs))
            
    if issubclass(rpt,Table) and rpt.model is None:
        #~ logger.debug("20111113 %s is an abstract report", rpt)
        return
        
    #~ for name,v in rpt.__dict__.items():
    #~ for name in rpt.__class__.__dict__.keys():
    #~ for name in dir(rpt):
        #~ v = getattr(rpt,name)
        #~ if isinstance(v,Group):
            #~ v.name = name
            #~ v.add_to_table(rpt)
            #~ rpt.custom_groups = rpt.custom_groups + [v]
        #~ if isinstance(v,ComputedColumn):
            #~ v.name = name
            #~ v.add_to_table(rpt)
            #~ d = dict()
            #~ d.update(rpt.computed_columns)
            #~ d[name] = v
            #~ rpt.computed_columns = d
            
    #~ if rpt.model._meta.abstract:
        
    #~ rptname_choices.append((rpt.actor_id, rpt.get_label()))
    #~ rptname_choices.append(rpt.actor_id)
    
    if issubclass(rpt,Table):
        if rpt.master is None:
            if not rpt.model._meta.abstract:
                #~ logger.debug("20120102 register %s : master report", rpt.actor_id)
                master_reports.append(rpt)
            if not rpt.filter and not rpt.known_values and rpt.use_as_default_report:
                #~ logger.info("register %s : model_report for %s", rpt.actor_id, full_model_name(rpt.model))
                rpt.model._lino_model_report = rpt
        elif rpt.master is ContentType:
            #~ logger.debug("register %s : generic slave for %r", rpt.actor_id, rpt.master_key)
            generic_slaves[rpt.actor_id] = rpt
        else:
            #~ logger.debug("20120102 register %s : slave for %r", rpt.actor_id, rpt.master_key)
            slave_reports.append(rpt)
    elif issubclass(rpt,VirtualTable):
        custom_tables.append(rpt)

    
    
def discover():
    """
    - Each model can receive a number of "slaves". 
      Slaves are tables whose data depends on an instance 
      of another model (their master).
      
    - For each model we want to find out the "model table" ot "default table".
      The "choices table" for a foreignkey field is also currently simply the pointed model's
      model_table.
      `_lino_model_report`

    """
              
    logger.info("Analyzing Tables...")
    #~ logger.debug("20111113 Register Table actors...")
    for rpt in actors.actors_list:
        if issubclass(rpt,Table) and rpt is not Table:
            register_report(rpt)
        elif issubclass(rpt,VirtualTable) and rpt is not VirtualTable:
            register_report(rpt)
        if issubclass(rpt,actors.Frame) and rpt is not actors.Frame:
            register_frame(rpt)
            
    logger.debug("Instantiate model tables...")
    for model in models.get_models():
        """Not getattr but __dict__.get because of the mixins.Listings trick."""
        rpt = model.__dict__.get('_lino_model_report',None)
        #~ rpt = getattr(model,'_lino_model_report',None)
        #~ logger.debug('20111113 %s._lino_model_report = %s',model,rpt)
        if rpt is None:
            rpt = table_factory(model)
            register_report(rpt)
            model._lino_model_report = rpt
            
            
    logger.debug("Analyze %d slave tables...",len(slave_reports))
    for rpt in slave_reports:
        rpt.master = resolve_model(rpt.master)
        slaves = getattr(rpt.master,"_lino_slaves",None)
        if slaves is None:
            slaves = {}
            rpt.master._lino_slaves = slaves
        slaves[rpt.actor_id] = rpt
        #~ logger.debug("20111113 %s: slave for %s",rpt.actor_id, rpt.master.__name__)
    #~ logger.debug("Assigned %d slave reports to their master.",len(slave_reports))
        
    #~ logger.debug("reports.setup() done")



class StaticText:
    def __init__(self,text):
        self.text = text
        
#~ class Picture:
    #~ pass
    
#~ class DataView:
    #~ def __init__(self,tpl):
        #~ self.xtemplate = tpl
        


      

class TableRequest(AbstractTableRequest):
    """
    An Action Request on a given Table.
    """
    
    master_instance = None
    master = None
    instance = None
    extra = None
    layout = None
    
    #~ sort_column = None
    #~ sort_direction = None
    
    
    def parse_req(self,request,**kw):
        #~ logger.info("20120121 %s.parse_req()",self)
        rh = self.ah
        master = kw.get('master',self.report.master)
        if master is ContentType or master is models.Model:
            mt = request.REQUEST.get(ext_requests.URL_PARAM_MASTER_TYPE)
            try:
                master = kw['master'] = ContentType.objects.get(pk=mt).model_class()
            except ContentType.DoesNotExist,e:
                pass
                #~ master is None
                #~ raise ContentType.DoesNotExist("ContentType %r does not exist." % mt)
                
            #~ print kw
        if master is not None and not kw.has_key('master_instance'):
            pk = request.REQUEST.get(ext_requests.URL_PARAM_MASTER_PK,None)
            #~ print '20100406a', self.report,URL_PARAM_MASTER_PK,"=",pk
            #~ if pk in ('', '-99999'):
            if pk == '':
                pk = None
            if pk is None:
                kw['master_instance'] = None
            else:
                try:
                    kw['master_instance'] = master.objects.get(pk=pk)
                except ValueError,e:
                    raise Exception("Invalid primary key %r for %s",pk,master.__name__)
                except master.DoesNotExist,e:
                    # todo: ReportRequest should become a subclass of Dialog and this exception should call dlg.error()
                    raise Exception("There's no %s with primary key %r" % (master.__name__,pk))
            #~ print '20100212', self #, kw['master_instance']
        #~ print '20100406b', self.report,kw
        
        if settings.LINO.use_filterRow:
            exclude = dict()
            for f in rh.store.fields:
                if f.field:
                    filterOption = request.REQUEST.get('filter[%s_filterOption]' % f.field.name)
                    if filterOption == 'empty':
                        kw[f.field.name + "__isnull"] = True
                    elif filterOption == 'notempty':
                        kw[f.field.name + "__isnull"] = False
                    else:
                        filterValue = request.REQUEST.get('filter[%s]' % f.field.name)
                        if filterValue:
                            if not filterOption: filterOption = 'contains'
                            if filterOption == 'contains':
                                kw[f.field.name + "__icontains"] = filterValue
                            elif filterOption == 'doesnotcontain':
                                exclude[f.field.name + "__icontains"] = filterValue
                            else:
                                print "unknown filterOption %r" % filterOption
            if len(exclude):
                kw.update(exclude=exclude)
                
        if settings.LINO.use_gridfilters:
            filter = request.REQUEST.get(ext_requests.URL_PARAM_GRIDFILTER,None)
            if filter is not None:
                filter = json.loads(filter)
                kw['gridfilters'] = [ext_requests.dict2kw(flt) for flt in filter]
                
        quick_search = request.REQUEST.get(ext_requests.URL_PARAM_FILTER,None)
        if quick_search:
            kw.update(quick_search=quick_search)
        #~ else:
            #~ kw.update(limit=self.report.page_length)
            
        sort = request.REQUEST.get(ext_requests.URL_PARAM_SORT,None)
        if sort:
            #~ self.sort_column = sort
            sort_dir = request.REQUEST.get(ext_requests.URL_PARAM_SORTDIR,'ASC')
            if sort_dir == 'DESC':
                sort = '-' + sort
                #~ self.sort_direction = 'DESC'
            kw.update(order_by=[sort])
        
        kw = AbstractTableRequest.parse_req(self,request,**kw)
        #~ raise Exception("20120121 %s.parse_req(%s)" % (self,kw))
        return kw
        
            
    def setup(self,
            master=None,
            master_instance=None,
            master_id=None,
            layout=None,
            filter=None,
            create_rows=None,
            quick_search=None,
            gridfilters=None,
            order_by=None,
            exclude=None,
            extra=None,
            **kw):
            
        #~ logger.info("20120121 %s.setup()",self)
        self.filter = filter
        #~ if isinstance(self.action,GridEdit):
            #~ self.expand_memos = expand_memos or self.report.expand_memos
        self.quick_search = quick_search
        self.gridfilters = gridfilters
        self.order_by = order_by
        self.exclude = exclude or self.report.exclude
        self.extra = extra

        #~ if selected_rows is not None:
            #~ self.selected_rows = selected_rows
        
        if master is None:
            master = self.report.master
            # master might still be None
        self.master = master
        
        #~ if self.report.params:
            #~ raise Exception("%s.params is %r" % (self.report,self.report.params))
        #~ kw.update(self.report.params)
        #~ self.params = kw
        
        if master_id is not None:
            assert master_instance is None
            master_instance = self.master.objects.get(pk=master_id)
            
        self.create_kw = self.report.get_create_kw(master_instance)
        self.master_instance = master_instance
        
        #~ if self.master and master_instance is None:
            #~ raise Exception("20120121 %s : no master" % self)
            
        AbstractTableRequest.setup(self,**kw)
        
        #~ assert isinstance(self._data_iterator,models.query.QuerySet)
        
        
        #~ self.total_count = self._data_iterator.count()
        
        if create_rows is None:
            if self.create_kw is None:
                create_rows = 0
            #~ elif self.user is not None and self.report.can_add.passes(self.user):
            #~ elif self.report.can_add.passes(self.user):
            #~ elif self.report.get_permission(actors.CreatePermission,self.user):
            #~ a = self.report.get_action('SubmitInsert')
            #~ if a and self.report.get_permission(a,self.user):
            elif self.report.get_permission(self.report.submit_action,self.user,None):
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
        
            
        """
        Table.page_length is not a default value for ReportRequest.limit
        For example CSVReportRequest wants all rows.
        """
        self.page_length = self.report.page_length
        
        #~ logger.info("20120121 %s.setup() done",self)
        
    def __str__(self):
        return self.__class__.__name__ + '(' + self.report.actor_id + ",%r,...)" % self.master_instance

    def get_status(self,ui,**kw):
        kw = AbstractTableRequest.get_status(self,ui,**kw)
        #~ if self.report.__class__.__name__ == 'MyPersonsByGroup':
            #~ print 20111223, self.known_values
        bp = kw.setdefault('base_params',{})
        if self.quick_search:
            bp[ext_requests.URL_PARAM_FILTER] = self.quick_search
        if self.master_instance is not None:
            bp[ext_requests.URL_PARAM_MASTER_PK] = self.master_instance.pk
            mt = ContentType.objects.get_for_model(self.master_instance.__class__).pk
            bp[ext_requests.URL_PARAM_MASTER_TYPE] = mt
        return kw
        

#~ class IterActionRequest(actions.ActionRequest)
    #~ def __init__(self,ui,iter,action):
        #~ self.iter = iter
        #~ actions.ActionRequest.__init__(self,ui,action)
        
        
def has_fk(rr,name):
    if isinstance(rr,TableRequest):
        return rr.report.master_key == name
    return False

        
def model2report(m):
    def f(table,*args):
        return m(*args)
        #~ return getattr(obj,name)(request)
    return classmethod(f)


class RemoteField(object):
    primary_key = False
    def __init__(self,func,name,fld,**kw):
        self.func = func
        self.name = name
        self.field = fld



class Table(AbstractTable):
    """
    An :class:`AbstractTable` that works on a Django 
    Model using a Django QuerySet.
    
    A Table definition adds attributes
    like `model` and `master` and `master_key` 
    who are important because Lino handles relations automagically.
    
    Another class of attributes are
    `filter`, 'exclude' and `sort_order` 
    which it simply forwards to the QuerySet.
    
    """
    #~ hide_details = []
    #~ """
    #~ A list of base classes whose `.dtl` files should not be loaded for this report.
    #~ """
    
    model = None
    """
    The model on which this table iterates.
    """
    
    show_detail_navigator = True
    
    #~ base_queryset = None 
    #~ """Internally used to store one Queryset instance that is reused for each request.
    #~ Didn't yet measure this, but I believe that this is important for performance 
    #~ because Django then will cache database lookups.
    #~ """
    
    #~ default_params = {}
    """See :doc:`/blog/2011/0701`.
    """
    
    use_as_default_report = True
    """
    Set this to False if this Table should not become the model's default table.
    """
    
    order_by = None
    
    expand_memos = False
    """
    (No longer used; see :doc:`/tickets/44`). 
    Whether multi-line text fields in Grid views should be expanded in by default or not.
    """
    
    #~ can_add = perms.is_authenticated
    #~ """
    #~ A permission descriptor that defines who can add (create) rows in this table.
    #~ """
    
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
    """
    If specified, this must be a models.Q objectt
    (and no longer a dict of (fieldname -> value) pairs)
    which will be used as a filter.
    
    Unlike :attr:`known_values`, this can use the full range of 
    Django's `field lookup methods 
    <https://docs.djangoproject.com/en/dev/topics/db/queries/#field-lookups>`_
    
    Note that if the user can create rows in a filtered table, 
    you should make sure that new records satisfy your filter condition 
    by default, otherwise you can get surprising behaviour if the user 
    creates a new row.
    If your filter consists of simple static values on some known field, 
    then you'll prefer to use :attr:`known_values` instead of :attr:`filter.`
    """
    exclude = None
    
    master_key = None
    """
    The name of the ForeignKey field of this report's model that points to it's master.
    Setting this will turn the report into a slave report.
    """
    
    master_field = None
    """
    For internal use. Automatically set to the field descriptor of the :attr:`master_key`.
    """
    
    master = None
    """
    For internal use. Automatically set to the model pointed to by the :attr:`master_key`.
    """
    
    handle_uploaded_files = None
    """
    Handler for uploaded files.
    Same remarks as for :attr:`lino.core.actors.Actor.disabled_fields`.
    """
    
    
    @classmethod
    def request(self,ui=None,request=None,action=None,**kw):
        if action is None:
            action = self.default_action
        return TableRequest(ui,self,request,action,**kw)
        
    @classmethod
    def init_label(self):
        return self.model._meta.verbose_name_plural
        
    @classmethod
    def column_choices(self):
        return [ de.name for de in self.wildcard_data_elems() ]
          
    #~ @classmethod
    #~ def elem_filename_root(cls,elem):
        #~ return elem._meta.app_label + '.' + elem.__class__.__name__ + '-' + str(elem.pk)

    @classmethod
    def get_detail_sets(self):
        """
        Yield a list of (app_label,name) tuples for which the kernel 
        should try to create a Detail Set.
        """
        if self.model is not None:
            def yield_model_detail_sets(m):
                for b in m.__bases__:
                    if issubclass(b,models.Model) and b is not models.Model:
                        for ds in yield_model_detail_sets(b):
                            yield ds
                yield m._meta.app_label + '/' + m.__name__
          
            for ds in yield_model_detail_sets(self.model):
                yield ds
            
        for s in super(Table,self).get_detail_sets():
            yield s
            
    #~ @classmethod
    #~ def find_field(cls,model,name):
        #~ for vf in cls.model._meta.virtual_fields:
            #~ if vf.name == name:
                #~ return vf
        #~ return cls.model._meta.get_field(name)
    
            
    @classmethod
    def wildcard_data_elems(self):
        return wildcard_data_elems(self.model)
          
    @classmethod
    def class_init(self):
        super(Table,self).class_init()
        #~ if self.model is None:
            #~ if self.base_queryset is not None:
                #~ self.model = self.base_queryset.model
            # raise Exception("No model in %s" %  self)
        #~ else:
            #~ self.model = resolve_model(self.model,self.app_label)
            
        if self.model is not None:
            self.model = resolve_model(self.model,self.app_label)
            
        #~ logger.debug("20120103 class_init(%s) : model is %s",self,self.model)
        
        if isinstance(self.model,UnresolvedModel):
            self.model = None
            
        
        if self.model is not None:
          
            if self.label is None:
                #~ self.label = capfirst(self.model._meta.verbose_name_plural)
                self.label = self.init_label()
          
            for name in ('disabled_fields',
                         'handle_uploaded_files', 
                         #~ 'get_permission', 
                         'disable_editing'):
                if getattr(self,name) is None:
                    m = getattr(self.model,name,None)
                    if m is not None:
                        #~ logger.debug('20111113 Install model method %s.%s to %s',self.model.__name__,name,self)
                        setattr(self,name,model2report(m))
                        #~ 'dictproxy' object does not support item assignment:
                        #~ self.__dict__[name] = model2report(m) 
                        
            if self.master_key:
                #~ assert self.model is not None, "%s has .master_key but .model is None" % self
                #~ self.master = resolve_model(self.master,self.app_label)
                try:
                    fk, remote, direct, m2m = self.model._meta.get_field_by_name(self.master_key)
                    assert direct
                    assert not m2m
                    master = fk.rel.to
                except models.FieldDoesNotExist,e:
                    #~ logger.debug("FieldDoesNotExist in %r._meta.get_field_by_name(%r)",self.model,self.master_key)
                    master = None
                    for vf in self.model._meta.virtual_fields:
                        if vf.name == self.master_key:
                            fk = vf
                            master = ContentType
                if master is None:
                    raise Exception("%s : no master for master_key %r in %s" % (
                        self,self.master_key,self.model.__name__))
                self.master = master
                #~ self.fk = fk
                self.master_field = fk
        #~ else:
            #~ assert self.master is None
        
        
        if self.order_by is not None:
            if not isinstance(self.order_by,(list,tuple)):
                raise Exception("%s.order_by is %r (must be a list or tuple)" % (self,self.order_by))
            if False: 
              # good idea, but doesn't yet work for foreign fields, 
              # e.g. order_by = ['content_type__app_label']
              for fieldname in self.order_by:
                  if fieldname.startswith('-'):
                      fieldname = fieldname[1:]
                  try:
                      fk, remote, direct, m2m = self.model._meta.get_field_by_name(fieldname)
                      assert direct
                      assert not m2m
                  except models.FieldDoesNotExist,e:
                      raise Exception("Unknown fieldname %r in %s.order_by" % (fieldname,self))
        
    @classmethod
    def do_setup(self):
            
        super(Table,self).do_setup()
        #~ AbstractTable.do_setup(self)
        if self.model is None:
            return 
            
        if hasattr(self.model,'_lino_slaves'):
            self._slaves = self.model._lino_slaves.values()
        else:
            self._slaves = []
            
        m = getattr(self.model,'setup_report',None)
        if m:
            m(self)
        
    @classmethod
    def disable_delete(self,obj,request):
        """
        Return either `None` if the given `obj` *is allowed* 
        to be deleted by `request`,
        or a string with a message explaining why, if not.
        """
        return self.model._lino_ddh.disable_delete(obj,request)
        
    @classmethod
    def setup_actions(self):
        if self.model is not None:
            #~ if len(self.detail_layouts) > 0:
            #~ if self.model._lino_detail:
            if self._lino_detail:
                self.detail_action = actions.ShowDetailAction(self)
                self.add_action(self.detail_action)
                if self.editable:
                    self.add_action(self.submit_action)
                    self.add_action(actions.InsertRow(self))
                    #~ self.add_action(actions.DuplicateRow(self))
                    self.add_action(actions.SubmitInsert())
              
            if self.editable:
                self.add_action(actions.DeleteSelected())
            
            #~ if hasattr(self.model,'get_image_url'):
                #~ self.add_action(actions.ImageAction())

    @classmethod
    def get_data_elem(self,name):
        cc = super(Table,self).get_data_elem(name)
        #~ cc = AbstractTable.get_data_elem(self,name)
        if cc:
            return cc
        
        parts = name.split('__')
        if len(parts) > 1:
            model = self.model
            for n in parts:
                fld = get_data_elem(model,n)
                if fld is None:
                    raise Exception("Part %s of %s got None" % (n,model))
                if fld.rel:
                    model = fld.rel.to
                else:
                    model = False
            def func(obj):
                #~ logger.info('20120109 %s',name)
                #~ print '20120109', name
                try:
                    for n in parts:
                        obj = getattr(obj,n)
                    #~ logger.info('20120109 %s --> %r', name,obj)
                    return obj
                except Exception,e:
                    return None
            #~ de = get_data_elem(model,name)
            return RemoteField(func,name,fld)
            #~ col = RemoteField(func,name,fld)
            #~ return self._add_column(col)
            
            #~ return self.add_column(fn,name=name,
              #~ verbose_name=fld.verbose_name)
            
        #~ logger.info("20120202 Table.get_data_elem found nothing")
        return get_data_elem(self.model,name)
        #~ de = get_data_elem(self.model,name)
        #~ if de is not None: 
            #~ return de
        #~ return self.get_action(name)
        
        
    #~ @classmethod
    #~ def get_detail(self):
        #~ return self.model._lino_detail
        
    @classmethod
    def get_title(self,rr):
        assert rr is not None
        #~ if rr is not None and self.master is not None:
        if self.master is not None:
            #~ return _("%(details)s by %(model)s %(master)s") % dict(
            return _("%(details)s of %(master)s") % dict(
              #~ model=self.master._meta.verbose_name,
              #~ model=rr.master_instance._meta.verbose_name,
              details=self.model._meta.verbose_name_plural,
              master=rr.master_instance)
        #~ return AbstractTable.get_title(self,rr)
        return super(Table,self).get_title(rr)
        
    @classmethod
    def get_queryset(self):
        """
        Return an iterable over the items processed by this report.
        Override this to use e.g. select_related()
        or to return a list.
        """
        return self.model.objects.all()
      
    @classmethod
    def get_request_queryset(self,rr):
        """
        Build a Queryset for the specified request on this report.
        Upon first call, this will also lazily install Table.queryset 
        which will be reused on every subsequent call.
        """
        #~ See 20120123
        #~ from lino.modlib.jobs.models import Jobs
        #~ if rr.report is Jobs:
            #~ logger.info("20120123 get_request_queryset()")
        #~ qs = self.__dict__.get('base_queryset',None)
        #~ if qs is None:
            #~ qs = self.base_queryset = self.get_queryset()
            #~ if rr.report is Jobs:
                #~ logger.info("20120123 Setting base_queryset")
        qs = self.get_queryset()
        #~ kw = self.get_filter_kw(rr.master_instance,**rr.params)
        kw = self.get_filter_kw(rr.master_instance)
        if kw is None:
            return []
        if len(kw):
            qs = qs.filter(**kw)

        if rr.exclude:
            #~ qs = qs.exclude(**rr.exclude)
            qs = qs.exclude(rr.exclude)
            
        if self.filter:
            #~ qs = qs.filter(**self.filter)
            qs = qs.filter(self.filter)
            
        if rr.filter:
            #~ print rr.filter
            #~ qs = qs.filter(**rr.filter)
            qs = qs.filter(rr.filter)
            
        if rr.known_values:
            #~ logger.info("20120111 known values %r",rr.known_values)
            d = {}
            for k,v in rr.known_values.items():
                if v is None:
                    d[k+"__isnull"] = True
                else:
                    #~ d[k+"__exact"] = v
                    d[k] = v
                qs = qs.filter(**d)
                
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
            #~ logger.info("20120122 order_by %s",order_by)
            qs = qs.order_by(*order_by)
        return qs

    @classmethod
    def create_instance(self,req,**kw):
        instance = self.model(**kw)
        #~ self.on_create(instance,req)
        
        """
        Used e.g. by modlib.notes.Note.on_create().
        on_create gets the request as argument.
        Didn't yet find out how to do that using a standard Django signal.
        """
        m = getattr(instance,'on_create',None)
        if m:
            m(req)
        #~ print 20110128, instance
        return instance
        
    @classmethod
    def slave_as_summary_meth(self,ui,row_separator):
        """
        Creates and returns the method to be used when 
        :attr:`AbstractTable.show_slave_grid` is `False`.
        """
        def meth(master,request):
            rr = TableRequest(ui,self,None,self.default_action,master_instance=master)
            #~ rr = self.request(ui,master_instance=master)
            s = summary(ui,rr.data_iterator,row_separator)
            #~ s = summary(ui,rr,row_separator)
            #~ s = ', '.join([fmt(r) for r in rr])
            #~ print 'reports.py 20101017', s
            return s
        return meth
        
        
    @classmethod
    def get_create_kw(self,master_instance,**kw):
        return self.get_filter_kw(master_instance,**kw)
        
    @classmethod
    def get_filter_kw(self,master_instance,**kw):
        #logger.debug('%s.get_filter_kw(%r) master=%r',self,kw,self.master)
        if self.master is None:
            assert master_instance is None, "Table %s doesn't accept a master" % self.actor_id
        elif self.master is models.Model:
            pass
        elif isinstance(self.master_field,generic.GenericForeignKey):
        #~ elif self.master is ContentType:
            #~ print 20110415
            if master_instance is None:
                pass
                #~ kw[self.fk.ct_field] = None
                #~ kw[self.fk.fk_field] = None
            else:
                ct = ContentType.objects.get_for_model(master_instance.__class__)
                kw[self.master_field.ct_field] = ct
                kw[self.master_field.fk_field] = master_instance.pk
        elif self.master_field is not None:
            if master_instance is None:
                if not self.master_field.null:
                    return # cannot add rows to this report
            elif not isinstance(master_instance,self.master):
                raise Exception("%r is not a %s (master_key is %r)" % (
                  master_instance,self.master.__name__,self.master_field))
            kw[self.master_field.name] = master_instance
            
        #~ else:
            #~ kw['master'] = master_instance
        return kw
        
    #~ def on_create(self,instance,request):
        #~ pass
        
    #~ def get_label(self):
        #~ return self.label
        
    #~ def __str__(self):
        #~ return rc_name(self.__class__)
        
    @classmethod
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





def table_factory(model):
    """
    Automatically define a Table class for the specified model.
    This is used during kernel setup to cerate default tables for 
    models who have no table found.
    """
    #~ logger.info('table_factory(%s)',model.__name__)
    bases = (Table,)
    for b in model.__bases__:
        rpt = getattr(b,'_lino_model_report',None)
        if rpt is not None:
            if issubclass(model,rpt.model):
            #~ if issubclass(rpt.model,model):
                bases = (rpt,)
                #~ bases = (rpt.__class__,)
    #~ logger.info('table_factory(%s) : bases is %s',model.__name__,bases)
    app_label = model._meta.app_label
    name = model.__name__ + "Table"
    cls = type(name,bases,dict(model=model,app_label=app_label))
    cls.class_init()
    #~ cls.setup()
    
    """
    20120104 We even add the factored class to the module because 
    actor lookup needs it. Otherwise we'd get a 
    `'module' object has no attribute 'DataControlListingTable'` error.
    
    We cannot simply do ``setattr(settings.LINO.modules.get(app_label),name,cls)``
    because this code is executed when `settings.LINO.modules` doesn't yet exist.
    """
    
    m = import_module(model.__module__)
    if getattr(m,name,None) is not None:
        raise Exception(
          "Name of factored class %s clashes with existing name in %s" 
          %(cls,m))
    setattr(m,name,cls)
    return actors.register_actor(cls)


def column_choices(rptname):
    rpt = actors.get_actor(rptname)
    return rpt.column_choices()


class LayoutError(RuntimeError):
    pass
  
LABEL_ALIGN_TOP = 'top'
LABEL_ALIGN_LEFT = 'left'
LABEL_ALIGN_RIGHT = 'right'


        
class BaseLayout(Configured):
    label = None
    has_frame = False # True
    label_align = LABEL_ALIGN_TOP
    hideCheckBoxLabels = True
    #label_align = LABEL_ALIGN_LEFT
    default_button = None
    collapsible_elements  = {}
    write_debug_info = False
    
    #~ 20120114 def __init__(self,desc,*args,**kw):
    def __init__(self,table,desc,*args,**kw):
        #~ self.label = label
        self.table = table
        self._desc = desc
        #~ super(BaseLayout,self).__init__(*args,**kw)
        Configured.__init__(self,*args,**kw)
            
        attrname = None
        for ln in desc.splitlines():
            if ln and not ln.lstrip().startswith('## '):
                if ln[0].isspace():
                    if attrname is None:
                        raise LayoutError('Unexpected indentation.')
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
                        raise Exception(
                            'Duplicate element definition %r in %r' 
                            % (attrname,desc))
                    setattr(self,attrname,a[1].strip())
        if self.label:
            #~ settings.LINO.add_dummy_message(self.label)
            self.add_dummy_message(self.label)
            self.label = _(self.label)
            
    #~ def __str__(self):
            
    def __str__(self):
        if self.filename:
            return "%s(%s %s)" % (self.__class__.__name__,self.cd.name,self.filename)
        return self.__class__.__name__ + "(" + self._desc + ")"
        #~ return "Dynamic " + super(Configured,self).__str__()
        
    def write_content(self,f):
        f.write(self._desc)
        
    def get_data_elem(self,name): 
        return self.table.get_data_elem(name)
            
class ListLayout(BaseLayout):
    #~ label = _("List")
    show_labels = False
    join_str = " "
    
    #~ def setup_element(self,e):
        #~ if isinstance(e,TextFieldElement):
            #~ e.hidden = True


class DetailLayout(BaseLayout):
    #~ label = _("Detail")
    show_labels = True
    join_str = "\n"
    only_for_report = None

class ParamsLayout(BaseLayout):
    #~ label = _("List")
    #~ label_align = LABEL_ALIGN_TOP
    show_labels = True
    join_str = " "

    def get_data_elem(self,name): 
        return self.table.get_param_elem(name)

class LayoutHandle:
    """
    LayoutHandle analyzes a Layout and builds a tree of LayoutElements.
    
    """
    start_focus = None
    
    #~ 20120114 def __init__(self,ui,table,layout,hidden_elements=frozenset()):
    def __init__(self,ui,layout,hidden_elements=frozenset()):
      
        #~ logger.debug('20111113 %s.__init__(%s,%s)',self.__class__.__name__,rh,layout)
        assert isinstance(layout,BaseLayout)
        #assert isinstance(link,reports.ReportHandle)
        #~ base.Handle.__init__(self,ui)
        #~ actors.ActorHandle.__init__(self,layout)
        self.layout = layout
        self.ui = ui
        #~ self.rh = rh
        #~ self.datalink = layout.get_datalink(ui)
        self.label = layout.label # or ''
        self._store_fields = []
        #~ self._elems_by_field = {}
        #~ self._submit_fields = []
        #~ self.slave_grids = []
        #~ self._buttons = []
        self.hidden_elements = hidden_elements # layout.get_hidden_elements(self)
        self.main_class = ui.main_panel_class(layout)
        
        #~ if layout.main is not None:
        if layout.main:
        #~ if hasattr(layout,"main"):
            self._main = self.create_element(self.main_class,'main')
            if self._main is None:
                raise Exception("%s.%s could not create main element" 
                    % (table,self.layout))
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
                
        
    def __str__(self):
        #~ return "%s %s" % (self.rh,self.__class__.__name__)
        return "%s for %s" % (self.__class__.__name__,self.layout)
        
        
    def add_store_field(self,field):
        self._store_fields.append(field)
            
    def has_field(self,f):
        return self._main.has_field(f)
        
    def add_hidden_field(self,field):
        return HiddenField(self,field)
        
    def write_debug_info(self):
        if self.layout.filename and self.layout.write_debug_info:
            filename = "%s.debug.html" % self.layout.filename
            filename = os.path.join(self.layout.cd.name,filename)
            logger.info("Writing %s..." % filename)
            f = codecs.open(filename,"w",encoding='utf-8')
            f.write('''<html><body><table border="1">''')
            f.write('''<h1>%s</h1>''' % self)
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
                de.name for de in self.layout.table.wildcard_data_elems() \
                  if (de.name not in explicit_specs) \
                    and self.use_as_wildcard(de) \
                ])
            desc = desc.replace('*',wildcard_fields)
            #~ if 'CourseRequestsByPerson' in str(self):
                #~ logger.info('20111003 %s desc -> %r',self,desc)
        if "\n" in desc:
            # it's a vertical box
            elems = []
            i = 0
            for x in desc.splitlines():
                x = x.strip()
                if len(x) > 0 and not x.startswith("# "):
                    i += 1
                    e = self.desc2elem(self.ui.Panel,desc_name+'_'+str(i),x,**kw)
                    if e is not None:
                        elems.append(e)
            if len(elems) == 0:
                return None
            if len(elems) == 1 and panelclass != self.main_class:
                return elems[0]
            #return self.vbox_class(self,name,*elems,**kw)
            return panelclass(self,desc_name,True,*elems,**kw)
        else:
            # it's a horizontal box
            elems = []
            for x in desc.split():
                if not x.startswith("#"):
                    """
                    20100214 dsbe.PersonDetail hatte 2 MainPanels, 
                    weil PageLayout kein einzeiliges (horizontales) `main` vertrug
                    """
                    e = self.create_element(self.ui.Panel,x)
                    if e is None:
                        pass
                    elif isinstance(e,list):
                        elems += e
                    else:
                        elems.append(e)
            if len(elems) == 0:
                return None
            if len(elems) == 1 and panelclass != self.main_class:
                return elems[0]
            #return self.hbox_class(self,name,*elems,**kw)
            return panelclass(self,desc_name,False,*elems,**kw)
            
    def create_element(self,panelclass,desc_name):
        #~ logger.debug("create_element(panelclass,%r)", desc_name)
        name,kw = self.splitdesc(desc_name)
        e = self.ui.create_layout_element(self,panelclass,name,**kw)
        # todo: cannot hide babelfields
        if name in self.hidden_elements:
            e.hidden = True
        #~ self.setup_element(e)
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
        
    def use_as_wildcard(self,de):
        if de.name.endswith('_ptr'): return False
        #~ and (de.name not in self.hidden_elements) \
        #~ and (de.name not in self.rh.report.known_values.keys()) \
        #~ if de.name == self.rh.report.master_key: return False
        return True
  
    def get_data_elem(self,name): 
        return self.layout.get_data_elem(name)
        

class ListLayoutHandle(LayoutHandle):
  
    def __init__(self,rh,*args,**kw):
        self.rh = rh
        #~ 20120114 LayoutHandle.__init__(self,rh.ui,rh.report,*args,**kw)
        LayoutHandle.__init__(self,rh.ui,*args,**kw)
        
    def use_as_wildcard(self,de):
        if de.name.endswith('_ptr'): return False
        #~ and (de.name not in self.hidden_elements) \
        #~ and (de.name not in self.rh.report.known_values.keys()) \
        if issubclass(self.rh.report,Table):
            if de.name == self.rh.report.master_key: return False
        return True




class DetailHandle(base.Handle):
    """
    """
    def __init__(self,ui,detail):
        self.detail = detail
        #~ self.content_type = ContentType.objects.get_for_model(detail.model).pk
        self.lh_list = [ 
            #~ 20120114 LayoutHandle(ui,detail.model._lino_model_report,dl) for dl in self.detail.layouts
            LayoutHandle(ui,dl) for dl in self.detail.layouts 
            ]
        base.Handle.__init__(self,ui)
      
      

class Detail(object):
    """
    The UI-agnostic representation of a Detail window.
    Equivalent to a collection of .dtl files.
    """
    
    #~ def __init__(self,model,layouts):
    def __init__(self,actor,layouts):
        #~ self.model = model
        #~ self.table = model._lino_model_report,
        self.actor = actor
        #~ self.table = model._lino_model_report,
        self.layouts = layouts
        self._handles = {}
        

    def get_handle(self,k):
        h = self._handles.get(k,None)
        if h is None:
            h = DetailHandle(k,self)
            self._handles[k] = h
            h.setup()
        return h
        
    def __str__(self):
        #~ return "%s Detail(%s)" % (self.actor,[str(x) for x in self.layouts])
        return "%s Detail(%s)" % (self.actor,len(self.layouts))
        

all_details = []

def register_detail(a,layouts):
    for dtl in all_details:
        if dtl.layouts == layouts:
            return dtl
    dtl = Detail(a,layouts)
    all_details.append(dtl)
    return dtl

