# -*- coding: UTF-8 -*-
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

u"""
>>> DATA = [ 
... ["Belgium", "Eupen", 17000] ,
... ["Belgium", u"Liège", 400000] ,
... ["Belgium", "Raeren", 5000] ,
... ["Estonia", "Tallinn", 400000] ,
... ["Estonia", "Vigala", 1500] ,
... ]


>>> class CitiesAndInhabitants(CustomTable):
...     column_names = "country city population"
...     @classmethod
...         def get_data_rows(self,ar):
...             return DATA
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

import yaml

from django.utils.translation import ugettext_lazy as _

from lino.core import actors
from lino.core import actions
from lino.core.fields import FakeField
from lino.ui import base
from lino.ui import requests as ext_requests
from lino.utils import perms
from lino.utils.config import Configured, load_config_files


class InvalidRequest(Exception):
    pass
    
    
    
class ReportAction(actions.Action):
  
    def __init__(self,report,*args,**kw):
        self.actor = report # actor who offers this action
        self.can_view = report.can_view
        super(ReportAction,self).__init__(*args,**kw)

    def get_button_label(self):
        if self is self.actor.default_action:
            return self.label 
        else:
            return u"%s %s" % (self.label,self.actor.label)
            
    #~ def get_list_title(self,rh):
    def get_action_title(self,rr):
        return rr.get_title()
        
    def __str__(self):
        return str(self.actor) + '.' + self.name
        


class GridEdit(ReportAction,actions.OpenWindowAction):
  
    callable_from = tuple()
    name = 'grid'
    
    def __init__(self,rpt):
        self.label = rpt.button_label or rpt.label
        ReportAction.__init__(self,rpt)


class ShowDetailAction(ReportAction,actions.OpenWindowAction):
    callable_from = (GridEdit,)
    #~ show_in_detail = False
    #~ needs_selection = True
    name = 'detail'
    label = _("Detail")
    
    #~ def get_elem_title(self,elem):
        #~ return _("%s (Detail)")  % unicode(elem)
    

class RowAction(actions.Action):
    callable_from = (GridEdit,ShowDetailAction)
    
    def disabled_for(self,obj,request):
        return False
    #~ needs_selection = False
    #~ needs_validation = False
    #~ def before_run(self,ar):
        #~ if self.needs_selection and len(ar.selected_rows) == 0:
            #~ return _("No selection. Nothing to do.")
            


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
        
        










class ActionRequest(object):
    def __init__(self,ui,action):
        self.ui = ui
        self.action = action
        
    def request2kw(self,ui,**kw):
        return kw
  

class AbstractTableRequest(ActionRequest):
  
    limit = None
    offset = None
    create_rows = None
    
    #~ def __init__(self,ui,report,request,action,*args,**kw):
    def __init__(self,ui,report,request,action,**kw):
        if not (isinstance(report,type) and issubclass(report,AbstractTable)):
            raise Exception("Expected an AbstractTable subclass, got %r" % report)
        #~ reports.ReportActionRequest.__init__(self,rh.ui,rh.report,action)
        ActionRequest.__init__(self,ui,action)
        self.report = report
        self.ah = report.get_handle(ui)
        #~ self.ah = rh
        self.request = request
        if request is not None:
            kw = self.parse_req(request,self.ah,**kw)
        self.setup(**kw)
        #~ self.setup(*args,**kw)
        self.data_iterator = self.get_data_iterator()
        self.sliced_data_iterator = self.data_iterator
        if self.offset is not None:
            self.sliced_data_iterator = self.sliced_data_iterator[self.offset:]
        if self.limit is not None:
            self.sliced_data_iterator = self.sliced_data_iterator[:self.limit]
        
        
    
    def parse_req(self,request,rh,**kw):
        if rh.report.parameters:
            kw.update(param_values=self.ui.parse_params(rh,request))
        #~ kw.update(self.report.known_values)
        #~ for fieldname, default in self.report.known_values.items():
            #~ v = request.REQUEST.get(fieldname,None)
            #~ if v is not None:
                #~ kw[fieldname] = v
        kw.update(user=request.user)
        
        offset = request.REQUEST.get(ext_requests.URL_PARAM_START,None)
        if offset:
            kw.update(offset=int(offset))
        limit = request.REQUEST.get(ext_requests.URL_PARAM_LIMIT,None)
        if limit:
            kw.update(limit=int(limit))
        
        
        #~ kw.update(param_values=request.REQUEST.getlist(ext_requests.URL_PARAM_PARAM_VALUES))
        
        #~ def parse_param(fld,request,kv):
            #~ v = request.REQUEST.get(fld.name,None)
            #~ if v is not None:
                #~ kv[fld.name] = v
            
        #~ kv = kw.get('known_values',{})
        #~ for fld in self.report.params:
            #~ parse_param(fld,request,kv)
        #~ if kv:
            #~ kw.update(known_values=kv)
        
        kw = rh.report.parse_req(request,**kw)
        return kw
        
    def setup(self,
            user=None,
            subst_user=None,
            known_values=None,
            param_values=None,
            offset=None,limit=None,
            **kw):
        if user is not None and not self.report.can_view.passes(user):
            msg = _("User %(user)s cannot view %(report)s.") % dict(user=user,report=self.report)
            raise InvalidRequest(msg)
            
        #~ if user is None:
            #~ raise InvalidRequest("%s : user is None" % self)
            
        #~ 20120111 
        self.user = user
        self.subst_user = subst_user
        #~ self.known_values = known_values or self.report.known_values
        #~ if self.report.known_values:
        for k,v in self.report.known_values.items():
            kw.setdefault(k,v)
        if known_values:
            kw.update(known_values)
        #~ if self.report.__class__.__name__ == 'SoftSkillsByPerson':
            #~ logger.info("20111223 %r %r", kw, self.report.known_values)
        self.known_values = kw
        self.param_values = param_values
        if offset is not None:
            self.offset = offset
            
        if limit is not None:
            self.limit = limit
            
        
        self.report.setup_request(self)
        
        
            
    def get_data_iterator(self):
        raise NotImplementedError
        
    def get_base_filename(self):
        return str(self.report)
        #~ s = self.get_title()
        #~ return s.encode('us-ascii','replace')
        
    #~ def __iter__(self):
        #~ return self._sliced_data_iterator.__iter__()
        
    #~ def __getitem__(self,*args):
        #~ return self._data_iterator.__getitem__(*args)
        
    #~ def __len__(self):
        #~ return self._data_iterator.__len__()
        
    def get_user(self):
        return self.subst_user or self.user
        
    def get_action_title(self):
        return self.action.get_action_title(self)
        
    def get_title(self):
        return self.report.get_title(self)
        
        
    def render_to_dict(self):
        return self.action.render_to_dict(self)
        
    #~ def row2dict(self,row,d):
        #~ # overridden in extjs.ext_requests.ViewReportRequest
        #~ return self.report.row2dict(row,d)

    def get_request_url(self,*args,**kw):
        return self.ui.get_request_url(self,*args,**kw)

    def spawn_request(self,rpt,**kw):
        #~ rh = rpt.get_handle(self.ui)
        kw.update(user=self.user)
        #~ return ViewReportRequest(None,rh,rpt.default_action,**kw)
        return self.__class__(self.ui,rpt,None,rpt.default_action,**kw)
        
    def request2kw(self,ui,**kw):
        if self.subst_user is not None:
            kw[ext_requests.URL_PARAM_SUBST_USER] = self.subst_user.username
            
        if self.known_values:
            #~ kv = dict()
            for k,v in self.known_values.items():
                if self.report.known_values.get(k,None) != v:
                    kw[k] = v
                
            #~ kw[ext_requests.URL_PARAM_KNOWN_VALUES] = self.known_values
        return kw
            
    def confirm(self,step,*messages):
        if self.request.REQUEST.get(ext_requests.URL_PARAM_ACTION_STEP,None) == str(step):
            return
        raise actions.ConfirmationRequired(step,messages)

        
        
class CustomTableRequest(AbstractTableRequest):
  
    def get_data_iterator(self):
        l = []
        for row in self.report.get_data_rows(self):
            group = self.report.group_from_row(row)
            group.process_row(l,row)
        return l
        
    def setup(self,**kw):
        AbstractTableRequest.setup(self,**kw)
        #~ self.total_count = len(self._data_iterator)




class TableHandle(base.Handle): 
    
    def __init__(self,ui,report):
        self.report = report
        self._layouts = None
        base.Handle.__init__(self,ui)
  
    def __str__(self):
        return str(self.report) + 'Handle'
            
    def setup_layouts(self):
        if self._layouts is not None:
            return
        self._layouts = [ self.list_layout ] 
              
    def get_actor_url(self,*args,**kw):
        return self.ui.get_actor_url(self.report,*args,**kw)
        
    def submit_elems(self):
        return []
        
    def get_list_layout(self):
        self.setup_layouts()
        return self._layouts[0]
        
    def get_columns(self):
        layout = self.get_list_layout()
        #~ print 20110315, layout._main.columns
        return layout._main.columns
        
    def get_slaves(self):
        return [ sl.get_handle(self.ui) for sl in self.report._slaves ]
            
    def get_action(self,name):
        return self.report.get_action(name)
    def get_actions(self,*args,**kw):
        return self.report.get_actions(*args,**kw)
        
    def update_detail(self,tab,desc):
        #~ raise Exception("Not yet fully converted to Lino 1.3.0")
        old_dl = self.report.get_detail().layouts[tab]
        dtl = DetailLayout(desc,old_dl.filename,old_dl.cd)
        self.report.get_detail().layouts[tab] = dtl
        #~ dh = dtl.get_handle(self.ui)
        #~ self._layouts[tab+1] = LayoutHandle(self.ui,self.report.model,dtl)
        self.ui.setup_handle(self)
        #~ self.report.save_config()
        dtl.save_config()



class AbstractTable(actors.Actor):
    """
    Base class for :class:`Table` and `CustomTable`.
    
    An AbstractTable is the definition of a tabular data view, 
    usually displayed in a Grid (but it's up to the user 
    interface to decide how to implement this).
    
    The `column_names` attribute defines the "horizontal layout".
    The "vertical layout" is some iterable.
    """
    _handle_class = TableHandle
    
    parameters = None
    """
    User-definable parameter fields for this table.
    Set this to a `dict` of `name = models.XyzField()` pairs.
    """
    
    params_template = None
    """
    If this table has parameters, specify here how they should be 
    laid out in the parameters panel.
    """
    
    params_panel_hidden = True
    """
    If this table has parameters, set this to False if the parameters 
    panel should be hidden when the table is rendered in a grid widget.
    """
    
    #~ field = None
    
    title = None
    
    column_names = '*'
    """
    A string that describes the list of columns of this table.
    """
    
    group_by = None
    """
    A list of field names that define the groups of rows in this table.
    Each group can have her own header and/or total lines.
    """
    
    #~ computed_columns = {}
    #~ """
    #~ Used internally to store :class:`computed columns <ComputedColumn>` defined by this Table.
    #~ """
    
    custom_groups = []
    """
    Used internally to store :class:`groups <Group>` defined by this Table.
    """
    
    column_defaults = {}
    """
    A dictionary of default parameters for :class:`computed columns <ComputedColumn>` on this table.
    """
    
    #~ hide_columns = None
    hidden_columns = frozenset()
    form_class = None
    help_url = None
    #master_instance = None
    
    page_length = 30
    """
    Number of rows to display per page.
    """
    
    cell_edit = True 
    """
    `True` to use ExtJS CellSelectionModel, `False` to use RowSelectionModel.
    """
    
    #~ date_format = lino.DATE_FORMAT_EXTJS
    #~ boolean_texts = boolean_texts
    boolean_texts = boolean_texts = (_('Yes'),_('No'),' ')
    
    can_view = perms.always
    can_change = perms.is_authenticated
    can_config = perms.is_staff
    
    #~ show_prev_next = True
    show_detail_navigator = False
    """
    Whether a Detail view on a row of this table should feature a navigator
    """
    
    
    #~ default_action = GridEdit
    default_layout = 0
    
    typo_check = True
    """
    True means that Lino shoud issue a warning if a subclass 
    defines any attribute that did not exist in the base class.
    Usually such a warning means that there is something wrong.
    """
    
    known_values = {}
    """
    A `dict` of `fieldname` -> `value` pairs that specify "known values".
    Requests will automatically be filtered to show only existing records 
    with those values.
    This is like :attr:`filter`, but 
    new instances created in this Table will automatically have 
    these values set.
    
    """
    
    #~ url = None
    
    #~ use_layouts = True
    
    button_label = None
    
    active_fields = []
    """A list of field names that are "active" (cause a save and 
    refresh of a Detail or Insert form).
    """
    
    show_slave_grid = True
    """
    How to display this table when it is a slave in a detail window. 
    `True` (default) to render as a grid. 
    `False` to render a summary in a HtmlBoxPanel.
    Example: :class:`links.LinksByOwner`
    """
    
    grid_configs = []
    """
    Will be filled during :meth:`lino.core.table.Table.do_setup`. 
    """
    
    disabled_fields = None
    """
    Return a list of field names that should not be editable 
    for the specified `obj` and `request`.
    
    If defined in the Table, this must be a method that accepts 
    two arguments `request` and `obj`::
    
      def disabled_fields(self,obj,request):
          ...
          return []
    
    If not defined in a subclass, the report will look whether 
    it's model has a `disabled_fields` method expecting a single 
    argument `request` and install a wrapper to this model method.
    See also :doc:`/tickets/2`.
    """
    
    disable_editing = None
    """
    Return `True` if the record as a whole should be read-only.
    Same remarks as for :attr:`disabled_fields`.
    """
    
    has_navigator = True
    """
    Whether a Detail Form should have navigation buttons.
    This option is False in :class:`lino.SiteConfigs`.
    """
    
    detail_action = None
    
    def __init__(self,*args,**kw):
        raise NotImplementedError("20120104")
    
    @classmethod
    def spawn(cls,suffix,**kw):
        kw['app_label'] = cls.app_label
        return type(cls.__name__+str(suffix),(cls,),kw)
        
          
    @classmethod
    def parse_req(self,request,**kw):
        return kw
    
    @classmethod
    def do_setup(self):
      
        super(AbstractTable,self).do_setup()
        
        self.grid_configs = []
        
        def loader(content,cd,filename):
            data = yaml.load(content)
            gc = GridConfig(self,data,filename,cd)
            self.grid_configs.append(gc)
            
        load_config_files(loader,'%s.*gc' % self)
            
        self.default_action = GridEdit(self)
        #~ self.setup_detail_layouts()
        self.set_actions([])
        self.setup_actions()
        self.add_action(self.default_action)
        #~ if self.default_action.actor != self:
            #~ raise Exception("20120103 %r.do_setup() : default.action.actor is %r" % (
              #~ self,self.default_action.actor))
                
        if self.button_label is None:
            self.button_label = self.label
            
        
    @classmethod
    def disabled_actions(self,obj,request):
        l = []
        for a in self.get_actions():
            if isinstance(a,RowAction):
                if a.disabled_for(obj,request):
                    l.append(a.name)
        return l
        
    @classmethod
    def setup_actions(self):
        pass
        
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
    def get_param_elem(self,name):
        if self.parameters:
            return self.parameters.get(name,None)
        #~ for pf in self.params:
            #~ if pf.name == name:  return pf
        return None
      
    @classmethod
    def get_data_elem(self,name):
        #~ cc = self.computed_columns.get(name,None)
        #~ if cc is not None:
            #~ return cc
        vf = self.virtual_fields.get(name,None)
        if vf is not None:
            return vf
        return None
              
        
    @classmethod
    def get_title(self,rr):
        """
        Return the title of this Table for the given request `rr`.
        Override this if your Table's title should mention for example filter conditions.
        """
        return self.title or self.label
        
    @classmethod
    def setup_request(self,req):
        pass
        
    @classmethod
    def wildcard_data_elems(self):
        for cc in self.computed_columns.values():
            yield cc
        #~ return []
        
    @classmethod
    def get_detail(self):
        return None
        
        
    @classmethod
    def unused_row2dict(self,row,d):
        """
        Overridden by lino.modlib.properties.PropValuesByOwner.
        See also lino.ui.extjs.ext_requests.ViewReportRequest.
        """
        for n in self.column_names.split():
            d[n] = getattr(row,n)
        return d
        
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
    

#~ class ComputedColumn(FakeField):
    #~ """
    #~ A Column whose value is not retrieved from the database but 
    #~ "computed" by a custom function.
    #~ """
    #~ def __init__(self,func,verbose_name=None,name=None,width=None):
        #~ self.func = func
        #~ self.name = name
        #~ self.verbose_name = verbose_name or name
        #~ self.width = width
        
    #~ def add_to_table(self,table):
        #~ self.table = table
        #~ if self.width is None:
            #~ self.width = table.column_defaults.get('width',None)
        
        
#~ def computed(*args,**kw):
    #~ """
    #~ Decorator used to define computed columns as part 
    #~ of the Table's definition.
    #~ """
    #~ def decorator(fn):
        #~ def wrapped(*args):
            #~ return fn(*args)
        #~ return ComputedColumn(wrapped,*args,**kw)
    #~ return decorator
    


class Group(object):
  
    def __init__(self):
        self.sums = []
        
    def process_row(self,collector,row):
        collector.append(row)

    #~ def add_to_table(self,table):
        #~ self.table = table
        #~ for col in table.computed_columns.values():




#~ def redirect(obj,name,*other):
    #~ """
    #~ """
    #~ logger.info('redirect()')
    #~ o = getattr(obj,name)
    #~ if other:
        #~ return redirect(o,*other)
    #~ return o
        

class CustomTable(AbstractTable):
    """
    An :class:`AbstractTable` that works on an arbitrary 
    list of "rows", using only computed columns.
    """
    
    default_group = Group()
    
    @classmethod
    def group_from_row(self,row):
        return self.default_group
        
    @classmethod
    def get_data_rows(self,ar):
        raise NotImplementedError
    
    @classmethod
    def request(cls,ui=None,request=None,action=None,**kw):
        self = cls
        if action is None:
            action = self.default_action
        return CustomTableRequest(ui,self,request,action,**kw)
        #~ return self.default_action.request(ui,**kw)





