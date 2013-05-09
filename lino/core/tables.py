# -*- coding: UTF-8 -*-
## Copyright 2009-2013 Luc Saffre
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

u"""
>>> DATA = [ 
... ["Belgium", "Eupen", 17000] ,
... ["Belgium", u"Liège", 400000] ,
... ["Belgium", "Raeren", 5000] ,
... ["Estonia", "Tallinn", 400000] ,
... ["Estonia", "Vigala", 1500] ,
... ]


>>> class CitiesAndInhabitants(VirtualTable):
...     column_names = "country city population"
...     @classmethod
...     def get_data_rows(self,ar):
...         return DATA
...
...     @column(label="Country")
...     def country(obj,ar):
...         return obj[0]
...     @column(label="City")
...     def city(obj,ar):
...         return obj[1]
...     @column(label="Population")
...     def city(obj,ar):
...         return obj[2]
...

>>> CitiesAndInhabitants.request().render_to_html()

"""

import logging
logger = logging.getLogger(__name__)

import os
import yaml
import json

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode

from atelier import rstgen

from north import dbutils

from lino.core import actors
from lino.core import actions
from lino.core.dbutils import obj2str
from lino.core.model import Model

from lino.core.fields import FakeField
from lino.core.requests import ActionRequest

from lino.ui import base
from lino.core import constants #  as ext_requests
from lino.utils.config import Configured, load_config_files
from lino.utils.config import find_config_file

from lino.utils.appy_pod import Renderer


class InvalidRequest(Exception):
    pass

from lino.utils.xmlgen.html import RstTable

MAX_ROW_COUNT = 300


class GridConfig(Configured):
  
    def __init__(self,report,data,*args,**kw):
        self.report = report
        self.data = data
        self.label_en = data.get('label')
        self.data.update(label=_(self.label_en))
        super(GridConfig,self).__init__(*args,**kw)
        must_save = self.validate()
        if must_save:
            msg = self.save_config()
            #~ msg = self.save_grid_config()
            logger.debug(msg)
  
    def validate(self):
        """
        Removes unknown columns
        """
        must_save = False
        gc = self.data
        columns = gc['columns']
        col_count = len(columns)
        widths = gc.get('widths',None)
        hiddens = gc.get('hiddens',None)
        if widths is None:
            widths = [None for x in columns]
            gc.update(widths=widths)
        elif col_count != len(widths):
            raise Exception("%d columns, but %d widths" % (col_count,len(widths)))
        if hiddens is None:
            hiddens = [False for x in columns]
            gc.update(hiddens=hiddens)
        elif col_count != len(hiddens):
            raise Exception("%d columns, but %d hiddens" % (col_count,len(hiddens)))
            
        valid_columns = []
        valid_widths = []
        valid_hiddens = []
        for i,colname in enumerate(gc['columns']):
            f = self.report.get_data_elem(colname)
            if f is None:
                logger.debug("Removed unknown column %d (%r). Must save.",i,colname)
                must_save = True
            else:
                valid_columns.append(colname)
                valid_widths.append(widths[i])
                valid_hiddens.append(hiddens[i])
        gc.update(widths=valid_widths)
        gc.update(hiddens=valid_hiddens)
        gc.update(columns=valid_columns)
        return must_save
            
    def unused_write_content(self,f):
        self.data.update(label=self.label_en)
        f.write(yaml.dump(self.data))
        self.data.update(label=_(self.label_en))
        
    def write_content(self,f):
        f.write(yaml.dump(self.data))
        
        


WARNINGS_LOGGED = dict()



class TableRequest(ActionRequest):
    """
    An :class:`action request <lino.core.actions.ActionRequest>` 
    on a :class:`Table`.
    """
    
    master_instance = None
    master = None
    
    #~ instance = None
    extra = None
    title = None
    #~ layout = None
    
    limit = None
    offset = None
    #~ create_rows = None
    
    #~ no_data_text = None
    no_data_text = _("No data to display") # Keine Daten anzuzeigen
    
    _data_iterator = None
    _sliced_data_iterator = None
    
    #~ def __init__(self,master_instance=None,*args,**kw):
        #~ if master_instance is not None:
            #~ kw.update(master_instance=master_instance)
        #~ ActionRequest.__init__(self,*args,**kw)
        
    #~ def __init__(self,ui,actor,request=None,action=None,**kw):
        #~ ActionRequest.__init__(self,ui,actor,request,action,**kw)
        
    def execute(self):
        #~ if self.actor.parameters:
            #~ logger.info("20121203 TableRequest.execute() %s",self.param_values)
        self._data_iterator = self.get_data_iterator()
        self._sliced_data_iterator = self._data_iterator
        if self.offset is not None:
            self._sliced_data_iterator = self._sliced_data_iterator[self.offset:]
        if self.limit is not None:
            self._sliced_data_iterator = self._sliced_data_iterator[:self.limit]
            
    def must_execute(self):
        return self._data_iterator is None
        
    def get_data_iterator_property(self):
        if self._data_iterator is None:
            self.execute()
        return self._data_iterator
        
    def get_sliced_data_iterator_property(self):
        if self._sliced_data_iterator is None:
            self.execute()
        return self._sliced_data_iterator 
        
    data_iterator = property(get_data_iterator_property)
    sliced_data_iterator = property(get_sliced_data_iterator_property)
    

    @classmethod
    def get_row_by_pk(self,pk):
        return self.data_iterator[int(pk) - 1]
        
    def get_data_iterator(self):
        if self.actor.get_data_rows is not None:
            l = []
            try:
                rows = self.actor.get_data_rows(self)
                for row in rows:
                    if len(l) > 300:
                        raise Exception("20120521 More than 300 items in %s" % 
                            unicode(rows))
                    group = self.actor.group_from_row(row)
                    group.process_row(l,row)
            except Warning,e:
                self.no_data_text = unicode(e)
                return []
            except Exception,e:
                self.no_data_text = unicode(e)
                w = WARNINGS_LOGGED.get(str(e))
                if w is None:
                    WARNINGS_LOGGED[str(e)] = True
                    logger.exception(e)
                return []
            return l
        #~ logger.info("20120914 tables.get_data_iterator %s",self)
        #~ logger.info("20120914 tables.get_data_iterator %s",self.actor)
        return self.actor.get_request_queryset(self)
        
    def get_total_count(self):
        """
        Calling `len()` on a QuerySet will execute the whole SELECT.
        See `/blog/2012/0124`
        """
        di = self.data_iterator
        if isinstance(di,QuerySet):
            return di.count()
        return len(di)
        

    def __iter__(self):
        return self.data_iterator.__iter__()
        
    
        
    def parse_req(self,request,rqdata,**kw):
        #~ logger.info("20120723 %s.parse_req()",self.actor)
        #~ rh = self.ah
        master = kw.get('master',self.actor.master)
        if master is not None:
            """
            If `master` is `ContentType` or some abstract model, then 
            """
            #~ if master is ContentType or master is models.Model:
            if master is ContentType or master._meta.abstract:
                mt = rqdata.get(constants.URL_PARAM_MASTER_TYPE)
                try:
                    master = kw['master'] = ContentType.objects.get(pk=mt).model_class()
                except ContentType.DoesNotExist,e:
                    pass
                    #~ master is None
                    #~ raise ContentType.DoesNotExist("ContentType %r does not exist." % mt)
                    
                #~ print kw
            if not kw.has_key('master_instance'):
                pk = rqdata.get(constants.URL_PARAM_MASTER_PK,None)
                #~ print '20100406a', self.actor,URL_PARAM_MASTER_PK,"=",pk
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
        #~ print '20100406b', self.actor,kw
        
        if settings.SITE.use_filterRow:
            exclude = dict()
            for f in self.ah.store.fields:
                if f.field:
                    filterOption = rqdata.get('filter[%s_filterOption]' % f.field.name)
                    if filterOption == 'empty':
                        kw[f.field.name + "__isnull"] = True
                    elif filterOption == 'notempty':
                        kw[f.field.name + "__isnull"] = False
                    else:
                        filterValue = rqdata.get('filter[%s]' % f.field.name)
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
                
        if settings.SITE.use_gridfilters:
            filter = rqdata.get(constants.URL_PARAM_GRIDFILTER,None)
            if filter is not None:
                filter = json.loads(filter)
                kw['gridfilters'] = [constants.dict2kw(flt) for flt in filter]
                
        kw = ActionRequest.parse_req(self,request,rqdata,**kw)
        #~ raise Exception("20120121 %s.parse_req(%s)" % (self,kw))
        
        #~ kw.update(self.report.known_values)
        #~ for fieldname, default in self.report.known_values.items():
            #~ v = request.REQUEST.get(fieldname,None)
            #~ if v is not None:
                #~ kw[fieldname] = v
                
        quick_search = rqdata.get(constants.URL_PARAM_FILTER,None)
        if quick_search:
            kw.update(quick_search=quick_search)
            
        sort = rqdata.get(constants.URL_PARAM_SORT,None)
        if sort:
            #~ self.sort_column = sort
            sort_dir = rqdata.get(constants.URL_PARAM_SORTDIR,'ASC')
            if sort_dir == 'DESC':
                sort = '-' + sort
                #~ self.sort_direction = 'DESC'
            kw.update(order_by=[sort])
        
                
        offset = rqdata.get(constants.URL_PARAM_START,None)
        if offset:
            kw.update(offset=int(offset))
        limit = rqdata.get(constants.URL_PARAM_LIMIT,None)
        if limit:
            kw.update(limit=int(limit))
        
        return self.actor.parse_req(request,rqdata,**kw)
        
            
    def setup(self,
            quick_search=None,
            order_by=None,
            offset=None,limit=None,
            master=None,
            title=None,
            master_instance=None,
            master_id=None,
            #~ layout=None,
            filter=None,
            #~ create_rows=None,
            gridfilters=None,
            exclude=None,
            extra=None,
            **kw):
            
        if self.actor.__name__ == 'PrintExpensesByBudget':
            assert master_instance is not None
            
        self.quick_search = quick_search
        self.order_by = order_by
        
            
        #~ logger.info("20120519 %s.setup()",self)
        self.filter = filter
        self.gridfilters = gridfilters
        self.exclude = exclude or self.actor.exclude
        self.extra = extra

        if master is None:
            master = self.actor.master
            # master might still be None
        self.master = master
        
        if title is not None:
            self.title = title
            
        if master_id is not None:
            assert master_instance is None
            master_instance = self.master.objects.get(pk=master_id)
            
        #~ if master is not None:
            #~ if not isinstance(master_instance,master):
                #~ raise Exception("%r is not a %r" % (master_instance,master))
            
        self.master_instance = master_instance
        
        #~ AbstractTableRequest.setup(self,**kw)
        
        """
        Table.page_length is not a default value for ReportRequest.limit
        For example CSVReportRequest wants all rows.
        """
        self.page_length = self.actor.page_length
        
        #~ logger.info("20120121 %s.setup() done",self)
        
        #~ if self.actor.__name__ == 'PrintExpensesByBudget':
            #~ print '20130327 1 tables.py', kw.get('master_instance')
            
        ActionRequest.setup(self,**kw)
        
        #~ if self.actor.__name__ == 'PrintExpensesByBudget':
            #~ print '20130327 2 tables.py', self, self.master_instance
        
        """
        20120519 : outbox.MyOutbox had no phantom record when called from menu.
        When called by permalink it had. Because get_create_kw was called before 
        Actor.setup_request() which sets the master_instance.
        """
        self.actor.setup_request(self)
        
        self.create_kw = self.actor.get_create_kw(self.master_instance)
        
        if offset is not None:
            self.offset = offset
            
        if limit is not None:
            self.limit = limit
            
    
    def table2xhtml(self):
        return self.ui.table2xhtml(self)
        
    def get_field_info(ar,column_names=None):
        """
        Return a tuple (fields, headers, widths) which expresses which columns, headers 
        and widths the user wants for this TableRequest. If `self` has web request info, 
        checks for GET parameters cn, cw and ch (coming from the grid widget). Otherwise 
        Also apply the tables's :meth:`override_column_headers 
        <lino.core.actors.Actor.override_column_headers>` method.
        """
        if ar.request is None:
            columns = None
        else:
            columns = [str(x) for x in ar.request.REQUEST.getlist(constants.URL_PARAM_COLUMNS)]
        
        if columns:
            #~ widths = [int(x) for x in ar.request.REQUEST.getlist(constants.URL_PARAM_WIDTHS)]
            all_widths = ar.request.REQUEST.getlist(constants.URL_PARAM_WIDTHS)
            hiddens = [(x == 'true') for x in ar.request.REQUEST.getlist(constants.URL_PARAM_HIDDENS)]
            fields = []
            widths = []
            headers = []
            #~ ah = ar.actor.get_handle(self.extjs_ui)
            #~ ah = ar.actor.get_handle(settings.SITE.ui)
            ah = ar.actor.get_handle()
            for i,cn in enumerate(columns):
                col = None
                for e in ah.list_layout.main.columns:
                    if e.name == cn:
                        col = e
                        break
                if col is None:
                    #~ names = [e.name for e in ar.ah.list_layout._main.walk()]
                    #~ raise Exception("No column named %r in %s" % (cn,ah.list_layout.main.columns))
                    raise Exception("No column named %r in %s" % (cn,ar.ah.list_layout.main.columns))
                if not hiddens[i]:
                    fields.append(col)
                    #~ fields.append(col.field._lino_atomizer)
                    headers.append(unicode(col.label or col.name))
                    widths.append(int(all_widths[i]))
        else:
            if column_names:
                from lino.core import layouts
                #~ assert ar.actor is not None
                ll = layouts.ListLayout(column_names,datasource=ar.actor)
                #~ lh = ll.get_layout_handle(self.extjs_ui)
                lh = ll.get_layout_handle(settings.SITE.ui)
                columns = lh.main.columns
            else:
                #~ ah = ar.actor.get_handle(self.extjs_ui)
                ah = ar.actor.get_request_handle(ar)
                columns = ah.list_layout.main.columns
                #~ columns = ar.ah.list_layout.main.columns
            #~ fields = ar.ah.store.list_fields
            headers = [unicode(col.label or col.name) for col in columns]
            widths = ["%d" % (col.width or col.preferred_width) for col in columns]
            #~ 20130415 widths = ["%d%%" % (col.width or col.preferred_width) for col in columns]
            #~ fields = [col.field._lino_atomizer for col in columns]
            fields = columns

        oh = ar.actor.override_column_headers(ar)
        if oh:
            for i,e in enumerate(columns):
                header = oh.get(e.name,None)
                if header is not None:
                    headers[i] = header
            #~ print 20120507, oh, headers
            
        return fields, headers, widths
        
        
    def appy_render(ar,target_file):
        
        if ar.get_total_count() > MAX_ROW_COUNT:
            raise Exception(_("List contains more than %d rows") % MAX_ROW_COUNT)
    
        tpl_leaf = "Table.odt" 
        tplgroup = None
        tplfile = find_config_file(tpl_leaf,tplgroup)
        if not tplfile:
            raise Exception("No file %s / %s" % (tplgroup,tpl_leaf))
            
        ar.renderer = ar.ui.ext_renderer # 20120624
        
        context = dict(
            ar=ar,
            title=unicode(ar.get_title()),
            dtos=dbutils.dtos,
            dtosl=dbutils.dtosl,
            dtomy=dbutils.dtomy,
            babelattr=dbutils.babelattr,
            babelitem=dbutils.babelitem,
            tr=dbutils.babelitem,
            settings=settings,
            _ = _,
            #~ knowledge_text=fields.knowledge_text,
            )
        if os.path.exists(target_file):
            os.remove(target_file)
        logger.info(u"appy.pod render %s -> %s (params=%s",
            tplfile,target_file,settings.SITE.appy_params)
        renderer = Renderer(ar,tplfile, context, target_file,**settings.SITE.appy_params)
        renderer.run()
        
        
    def get_title(self):
        if self.title is not None:  
            return self.title
        return self.actor.get_title(self)
        
        
        
    def get_status(self,ui,**kw):
        kw = ActionRequest.get_status(self,ui,**kw)
        bp = kw['base_params']
        if self.quick_search:
            bp[constants.URL_PARAM_FILTER] = self.quick_search
            
        if self.known_values:
            for k,v in self.known_values.items():
                if self.actor.known_values.get(k,None) != v:
                    bp[k] = v
        if self.master_instance is not None:
            if self.master is not None:
                bp[constants.URL_PARAM_MASTER_PK] = self.master_instance.pk
                if ContentType._meta.installed:
                    mt = ContentType.objects.get_for_model(self.master_instance.__class__).pk
                    bp[constants.URL_PARAM_MASTER_TYPE] = mt
            else:
                bp[constants.URL_PARAM_MASTER_PK] = self.master_instance
        return kw
        
        
    def __repr__(self):
        #~ kw = dict(actor=str(self.actor))
        kw = dict()
        if self.master_instance is not None:
            #~ kw.update(master_instance=self.master_instance.pk)
            kw.update(master_instance=obj2str(self.master_instance))
        if self.filter is not None:
            kw.update(filter=repr(self.filter))
        if self.known_values:
            kw.update(known_values=self.known_values)
        u = self.get_user()
        if u is not None:
            kw.update(user=u.username)
        #~ return self.__class__.__name__ + '(%s)' % kw
        #~ return self.__class__.__name__ + ' '+str(self.bound_action)+'(%s)' % kw
        return "<%s %s(%s)>" %  (self.__class__.__name__,self.bound_action.full_name(),kw)







        


class TableHandle(base.Handle): 
  
    _layouts = None
    
    def __init__(self,actor):
        self.actor = actor
        base.Handle.__init__(self)
  
    def __str__(self):
        #~ return str(self.ui.__class__)+str(self.actor) + 'Handle'
        return str(self.actor) + 'Handle'
            
    def setup_layouts(self):
        if self._layouts is not None:
            return
        self._layouts = [ self.list_layout ] 
              
    def get_actor_url(self,*args,**kw):
        return self.ui.get_actor_url(self.actor,*args,**kw)
        
    def submit_elems(self):
        return []
        
    def get_list_layout(self):
        self.setup_layouts()
        return self._layouts[0]
        
    def get_columns(self):
        lh = self.get_list_layout()
        #~ print 20110315, layout._main.columns
        return lh.main.columns
        
    def get_slaves(self):
        return [ sl.get_handle(self.ui) for sl in self.actor._slaves ]
            
        

class Group(object):
  
    def __init__(self):
        self.sums = []
        
    def process_row(self,collector,row):
        collector.append(row)

    #~ def add_to_table(self,table):
        #~ self.table = table
        #~ for col in table.computed_columns.values():




class AbstractTable(actors.Actor):
    """
    Base class for :class:`Table` and `VirtualTable`.
    
    An AbstractTable is the definition of a tabular data view, 
    usually displayed in a Grid (but it's up to the user 
    interface to decide how to implement this).
    
    The `column_names` attribute defines the "horizontal layout".
    The "vertical layout" is some iterable.
    """
    _handle_class = TableHandle
    
    column_names = '*'
    """
    A string that describes the list of columns of this table.
    """
    
    group_by = None
    """
    A list of field names that define the groups of rows in this table.
    Each group can have her own header and/or total lines.
    """
    
    custom_groups = []
    """
    Used internally to store :class:`groups <Group>` defined by this Table.
    """
    
    preview_limit = None
    """
    The LIMIT to use when this is being used in "preview mode", 
    e.g. as a slave table in a detail window.
    If this is None, preview requests for this table will request all rows.
    Since preview tables usually have no paging toolbar, that's what we want.
    But if there are many rows, this can lead to waste of performance.
    
    Not tested. This was one idea while trying to solve the 20130107 problem 
    "AvailableCoaches slave table shows only 5 records".    
    """
    
    get_data_rows = None
    """
    Custom tables must define a class method of this name which 
    will be called with a TableRequest object and which is expected
    to return or yield the list of "rows"::
    
        @classmethod
        def get_data_rows(self,ar):
            ...
            yield somerow
            
    Model tables may also define such a method in case they need local filtering.
    
    """
    
    
    auto_fit_column_widths = False
    """
    Set this to True if you want to have 
    the column widths adjusted to always fill the available width.
    This implies that there will be no horizontal scrollbar.
    """
    
    #~ hide_columns = None
    #~ hidden_columns = frozenset()
    
    hidden_columns = frozenset()
    """
    If given, this is specifies the data elements
    that should be hidden by default when rendering 
    this actor in a grid.
    
    When specified as class attribute of a 
    :class:`lino.core.model.Model` 
    or a :class:`dd.Table <lino.core.dbtables.Table>`, 
    this can be a single string containing 
    a space-separated list of field names. 
    Lino will automatically resolve this using 
    :func:`dd.fields_list <lino.core.fields.fields_list>` 
    during server startup.
    
    Otherwise it must be specified as a set of strings, 
    each one the name of a data element.
    """
    
    #~ hidden_elements = None
    
    form_class = None
    help_url = None
    #master_instance = None
    
    page_length = 20
    """
    Number of rows to display per page.
    """
    
    cell_edit = True 
    """
    `True` to use ExtJS CellSelectionModel, `False` to use RowSelectionModel.
    """
    
    show_detail_navigator = False
    """
    Whether a Detail view on a row of this table should have a navigator.
    """
    
    default_group = Group()
    
    
    #~ default_action = GridEdit
    default_layout = 0
    
    typo_check = True
    """
    True means that Lino shoud issue a warning if a subclass 
    defines any attribute that did not exist in the base class.
    Usually such a warning means that there is something wrong.
    """
    
    
    slave_grid_format = 'grid'
    """
    How to display this table when it is a slave in a detail window. 
    `grid` (default) to render as a grid. 
    `summary` to render a summary in a HtmlBoxPanel.
    `html` to render plain html a HtmlBoxPanel.
    Example: :class:`links.LinksByController`
    """
    
    grid_configs = []
    """
    Will be filled during :meth:`lino.core.table.Table.do_setup`. 
    """
    
    order_by = None
    
    filter = None
    """
    If specified, this must be a `models.Q` object
    (not a dict of (fieldname -> value) pairs)
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
    
    
    extra = None
    """
    Examples::
    
      extra = dict(select=dict(lower_name='lower(name)'))
      # (or if you prefer:) 
      # extra = {'select':{'lower_name':'lower(name)'},'order_by'=['lower_name']}
    
    List of SQL functions and which RDBMS supports them:
    http://en.wikibooks.org/wiki/SQL_Dialects_Reference/Functions_and_expressions/String_functions
    
    """
    
    
    def __init__(self,*args,**kw):
        raise NotImplementedError("20120104")
    
    @classmethod
    def spawn(cls,suffix,**kw):
        kw['app_label'] = cls.app_label
        return type(cls.__name__+str(suffix),(cls,),kw)
        
          
    @classmethod
    def parse_req(self,request,rqdata,**kw):
        return kw
    
        
    #~ grid = actions.GridEdit()
    
    @classmethod
    def get_default_action(cls):
        #~ return actions.BoundAction(cls,cls.grid)
        #~ return 'grid'
        return actions.GridEdit()
        
    @classmethod
    def class_init(self):
        """
        Sets table-specific default values for certain attributes.
        """
        #~ if self.default_action is None:
            #~ self.default_action = actions.GridEdit()
    
        if self.get_data_rows is not None:
            self.show_detail_navigator = False
            
        """
        :class:`lino_welfare.modellib.debts.models.DistByBudget` 
        defines its own `get_data_rows` but inherits from 
        :class:`lino_welfare.modellib.debts.models.EntriesByBudget` 
        which has no `get_data_rows`.
        """
        if self.__dict__.get('editable') is None:
            self.editable = (self.get_data_rows is None)
            #~ logger.info("20130204 %s editable = %s",self.__name__,self.editable)
        #~ if self.editable is None:
            #~ if self.get_data_rows is not None:
                #~ self.editable = False
            #~ self.editable = (self.get_data_rows is None)
        super(AbstractTable,self).class_init()
      
      
        
      
    @classmethod
    def do_setup(self):
      
        self.setup_columns()
        
        super(AbstractTable,self).do_setup()
        
        self.grid_configs = []
        
        def loader(content,cd,filename):
            data = yaml.load(content)
            gc = GridConfig(self,data,filename,cd)
            self.grid_configs.append(gc)
            
        load_config_files(loader,'%s.*gc' % self)
        
        #~ self.default_action = self.add_action(actions.GridEdit())
        #~ self.setup_detail_layouts()
        #~ self.set_actions([])
        #~ self.add_action(self.default_action)
        #~ self.setup_actions()
        #~ if self.default_action.actor != self:
            #~ raise Exception("20120103 %r.do_setup() : default.action.actor is %r" % (
              #~ self,self.default_action.actor))
                
        #~ if self.button_label is None:
            #~ self.button_label = self.label
            
        
    @classmethod
    def setup_columns(self):
        pass
        
    @classmethod
    def get_column_names(self,ar):
        """
        Dynamic tables must subclass this method
        """
        return self.column_names
        
    #~ @classmethod
    #~ def add_column(self,*args,**kw):
        #~ """
        #~ Use this from an overridden `before_ui_handle` method to 
        #~ dynamically define computed columns to this table.
        #~ """
        #~ return self._add_column(ComputedColumn(*args,**kw))
        
    #~ @classmethod
    #~ def _add_column(self,col):
        #~ col.add_to_table(self)
        #~ # make sure we don't add it to an inherited `computed_columns`:
        #~ self.computed_columns = dict(self.computed_columns)
        #~ self.computed_columns[col.name] = col
        #~ return col
      
    @classmethod
    def group_from_row(self,row):
        return self.default_group
    
    @classmethod
    def wildcard_data_elems(self):
        for cc in self.virtual_fields.values():
            yield cc
        #~ return []
        
    #~ @classmethod
    #~ def get_detail(self):
        #~ return None

    #~ removed 20130424 because that doesn't work for PendingCourseRequests
    #~ i.e. both get_data_rows and editable
    #~ @classmethod
    #~ def get_row_permission(self,obj,ar,state,ba):
        #~ if self.get_data_rows:
            #~ return ba.action.readonly
        #~ return True
        
        
    @classmethod
    def save_grid_config(self,index,data):
        if len(self.grid_configs) == 0:
            gc = GridConfig(self,data,'%s.gc' % self)
            self.grid_configs.append(gc)
        else:
            gc = self.grid_configs[index]
        gc.data = data
        gc.validate()
        #~ self.grid_configs[index] = gc
        return gc.save_config()
        #~ filename = self.get_grid_config_file(gc)
        #~ f = open(filename,'w')
        #~ f.write("# Generated file. Delete it to restore default configuration.\n")
        #~ d = dict(grid_configs=self.grid_configs)
        #~ f.write(yaml.dump(d))
        #~ f.close()
        #~ return "Grid Config has been saved to %s" % filename
    
    @classmethod
    def get_create_kw(self,master_instance,**kw):
        return self.get_filter_kw(master_instance,**kw)
        
    @classmethod
    def get_filter_kw(self,master_instance,**kw):
        """
        Return a dict with the "master keywords" for this table 
        and a given `master_instance`.
        """
        if self.master is None:
            pass
            # master_instance may be e.g. a lino.core.actions.EmptyTableRow
            # UsersWithClients as "slave" of the "table" Home
            
            #~ if master_instance is not None:
                #~ raise Exception("Unexpected master %r for table %s" % (master_instance,self.actor_id))
            #~ assert master_instance is None, "Table %s doesn't accept a master" % self.actor_id
        elif self.master is models.Model:
            pass
        elif isinstance(self.master_field,generic.GenericForeignKey):
        #~ elif self.master is ContentType:
            #~ print 20110415
            if master_instance is None:
                """
                20120222 : here was only `pass`, and the two other lines
                were uncommented. don't remember why I commented them out.
                But it caused all tasks to appear in UploadsByController of 
                an insert window for uploads.
                """
                #~ pass
                kw[self.master_field.ct_field] = None
                kw[self.master_field.fk_field] = None
            else:
                ct = ContentType.objects.get_for_model(master_instance.__class__)
                kw[self.master_field.ct_field] = ct
                kw[self.master_field.fk_field] = master_instance.pk
        elif self.master_field is not None:
            if master_instance is None:
                if not self.master_field.null:
                    #~ logger.info('20120519 %s.get_filter_kw()--> None',self)
                    return # cannot add rows to this table
            else:
                master_instance = master_instance.get_typed_instance(self.master)
                if not isinstance(master_instance,self.master):
                    raise Exception("%r is not a %s (%s.master_key = '%s')" % (
                      master_instance.__class__,self.master,self,self.master_key))
            kw[self.master_field.name] = master_instance
            
        #~ logger.info('20120519 %s.get_filter_kw(%r) --> %r',self,master_instance,kw)
        return kw
        
    #~ @classmethod
    #~ def request(cls,ui=None,request=None,action=None,**kw):
        #~ self = cls
        #~ if action is None:
            #~ action = self.default_action
        #~ return TableRequest(ui,self,request,action,**kw)
        
    @classmethod
    def request(self,master_instance=None,**kw):
        kw.update(actor=self)
        if master_instance is not None:
            kw.update(master_instance=master_instance)
        ar = TableRequest(**kw)
        #~ if self.__name__ == 'RetrieveTIGroupsResult':
            #~ print 20130425, __file__, ar
        
        #~ if self.__name__ == 'PrintExpensesByBudget':
            #~ assert ar.master_instance is not None
            #~ print '20130327 tables.py', self, ar.master_instance
        return ar
        

    @classmethod
    def run_action_from_console(self,pk=None,an=None):
        """
        Not yet stable. Used by print_tx25.py.
        To be combined with the `show` management command.
        """
        from north import dbutils
        dbutils.set_language(None)
        settings.SITE.startup()
        #~ settings.SITE.ui
        if pk is not None:
            elem = self.get_row_by_pk(pk)
            #~ elem = self.model.objects.get(pk=pk)
            if an is None:
                an = self.default_elem_action_name
        elif an is None:
            an = self.default_list_action_name
        ba = self.get_action_by_name(an)
        #~ print ba
        ar = self.request(action=ba)
        #~ ar = TableRequest(None,self,None,ba)
        kw = ba.action.run_from_ui(elem,ar)
        #~ kw = self.check_action_response(kw)
        msg = kw.get('message')
        if msg: 
            print msg
        url = kw.get('open_url') or kw.get('open_davlink_url')
        if url:
            os.startfile(url)
        
    @classmethod
    def to_rst(cls,ar,column_names=None,**kwargs):
        fields, headers, widths = ar.get_field_info(column_names)
        #~ # in case column_names contains remote fields
        #~ settings.SITE.startup() 
        #~ settings.SITE.resolve_virtual_fields()

        
        grid = ar.ah.list_layout.main
                    
        sums  = [fld.zero for fld in fields]
        rows = []  
        recno = 0
        #~ for row in ar:
        for row in ar.sliced_data_iterator:
            recno += 1
            rows.append([x for x in grid.row2text(ar,fields,row,sums)])
            #~ rows.append([x for x in grid.row2html(ar,fields,row,sums)])
                
        has_sum = False
        for i in sums:
            if i:
                #~ print '20120914 zero?', repr(i)
                has_sum = True
                break
        if has_sum:
            rows.append([x for x in grid.sums2html(ar,fields,sums)])
              
        t = RstTable(headers,**kwargs)
        return t.to_rst(rows)
        
        #~ return HtmlTable(headers,rows)
      
        

class VirtualTable(AbstractTable):
    """
    An :class:`AbstractTable` that works on an 
    volatile (non persistent) list of rows.
    By nature it cannot have database fields, only virtual fields.
    """
    

