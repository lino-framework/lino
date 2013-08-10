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

'''
This module defines the core classes 

- :class:`FormLayout`, :class:`ListLayout`,
  :class:`ParamsLayout` and :class:`ActionParamsLayout`
  and their common base class :class:`BaseLayout`
- :class:`Panel`
- The internally used :class:`LayoutHandle` class

See also:

- Topic overview: :doc:`/topics/layouts`
- Tutorial: :doc:`/tutorials/layouts`

'''

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import cgi
import os
import sys
import traceback
import codecs
import yaml
#~ import threading
#~ write_lock = threading.RLock()


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import NOT_PROVIDED
from django.db.models.fields.related import SingleRelatedObjectDescriptor
#~ from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from lino.utils.xmlgen.html import E

from lino.core import constants # as ext_requests

#~ from lino import dd

#~ from lino.core import perms
#~ from lino.utils import curry


class LayoutError(RuntimeError):
    pass
  
LABEL_ALIGN_TOP = 'top'
LABEL_ALIGN_LEFT = 'left'
LABEL_ALIGN_RIGHT = 'right'

def DEBUG_LAYOUTS(lo):
    #~ if lo._table.__name__ == 'Users':
        #~ return True
    return False
    
class Panel(object):
    """
    This is available as `dd.Panel`.
    Used when a panel is more complex than what can be expressed 
    using a simple template string.     
    
    The `options` parameter can be:
    
    - label
    - required
    
    Unlike a :class:`FormPanel` it cannot have any child panels 
    and cannot become a tabbed panel.
    """
    def __init__(self,desc,label=None,**options):
        self.desc = desc
        if label is not None:
            options.update(label=label)
        self.options = options
        
    def replace(self,*args,**kw):
        """
        Calls the standard :meth:`string.replace` 
        method on this Panel's template.
        """
        self.desc = self.desc.replace(*args,**kw)

    #~ def remove_element(self,*args):
        #~ """
        #~ Removes specified element names from this Panel's `main` template.
        #~ """
        #~ for name in args:
            #~ if not name in self.desc:
                #~ raise Exception("Panel has no element '%s'" % name)
            #~ self.desc = self.desc.replace(name,'')
        
class LayoutHandle:
    """
    LayoutHandle analyzes a Layout and stores the 
    resulting LayoutElements provided by the UI.
    
    """
    
    #~ 20120114 def __init__(self,ui,table,layout,hidden_elements=frozenset()):
    def __init__(self,layout):
      
        #~ logger.debug('20111113 %s.__init__(%s,%s)',self.__class__.__name__,rh,layout)
        assert isinstance(layout,BaseLayout)
        #assert isinstance(link,reports.ReportHandle)
        #~ base.Handle.__init__(self,ui)
        self.layout = layout
        #~ self.ui = settings.SITE.ui
        #~ self.rh = rh
        #~ self.datalink = layout.get_datalink(ui)
        #~ self.label = layout.label # or ''
        self._store_fields = []
        self._names = {}
        
        self.define_panel('main',layout.main)
        
        self.main = self._names.get('main')
        if self.main is None:
            raise Exception(
                "Failed to create main element %r for %s." % (
                layout.main,layout))
        
        self.width = self.main.width
        self.height = self.main.height
        
        self.layout.setup_handle(self)
        for k,v in self.layout._labels.items():
            #~ if not hasattr(self,k):
            if not self._names.has_key(k):
                raise Exception("%s has no attribute %r (layout.main is %r)" % (self,k,layout.main))
            #~ getattr(self,k).label = v
            self._names[k].label = v
        
        
                
    def __str__(self):
        #~ return "%s %s" % (self.rh,self.__class__.__name__)
        return "%s for %s" % (self.__class__.__name__,self.layout)
        
        
    def add_store_field(self,field):
        self._store_fields.append(field)
        
    def add_hidden_field(self,field):
        return HiddenField(self,field)
        
    def get_title(self,ar):
        return self.layout.get_title(ar)
        
    def walk(self):
        return self.main.walk()
        
    def ext_lines(self,request):
        return self.main.ext_lines(request)
  
        
    #~ def desc2elem(self,panelclass,desc_name,desc,**kw):
    def desc2elem(self,elemname,desc,**kw):
        #logger.debug("desc2elem(panelclass,%r,%r)",elemname,desc)
        #assert desc != 'Countries_choices2'
        
        if isinstance(desc,Panel):
            #~ assert not self.layout._element_options.has_key(elemname)
            #~ self.layout._element_options[elemname] = desc.options
            #~ d = self._element_options.setdefault(elemname,{})
            #~ d.update(desc.options)
            if len(kw):
                newkw = dict(desc.options)
                newkw.update(kw)
                kw = newkw
            else:
                kw = desc.options
            desc = desc.desc
        
        # flatten continued lines:
        desc = desc.replace('\\\n','')
        
        if '*' in desc:
            explicit_specs = set()
            for spec in desc.split():
                if spec != '*':
                    name,kw = self.splitdesc(spec)
                    explicit_specs.add(name)
            wildcard_fields = self.layout.join_str.join([
                de.name for de in self.layout._datasource.wildcard_data_elems() \
                  if (de.name not in explicit_specs) \
                    and self.use_as_wildcard(de) \
                ])
            desc = desc.replace('*',wildcard_fields)
            #~ if self.layout._datasource.__name__ == 'Vouchers':
                #~ logger.info('20130204 %s desc -> %r',self,desc)
            #~ if 'CourseRequestsByPerson' in str(self):
                #~ logger.info('20111003 %s desc -> %r',self,desc)
        if "\n" in desc:
            # it's a vertical box
            vertical = True
            """To get a hbox, the template string may not contain any newline.
            """
            elems = []
            i = 0
            for x in desc.splitlines():
                x = x.strip()
                if len(x) > 0 and not x.startswith("# "):
                    #~ if x.startswith(':'): # unused feature 
                        #~ a = x.split(':',2)
                        #~ if len(a) != 3:
                            #~ raise LayoutError('Expected attribute `:attr: value` ')
                        #~ attname = a[1]
                        #~ kw[attname] = a[2].strip()
                    #~ else:
                        i += 1
                        e = self.desc2elem(elemname+'_'+str(i),x)
                        if e is not None:
                            #~ e.allow_read = curry(perms.make_permission(self.layout._datasource,**e.required),e)
                            elems.append(e)
            #~ if len(elems) == 1:
                #~ vertical = False
        else:
            # it's a horizontal box
            vertical = False
            elems = []
            for x in desc.split():
                if not x.startswith("#"):
                    """
                    20100214 pcsw.PersonDetail hatte 2 MainPanels, 
                    weil PageLayout kein einzeiliges (horizontales) `main` vertrug
                    """
                    e = self.create_element(x)
                    if e is None:
                        pass
                    elif isinstance(e,list):
                        elems += e
                    else:
                        elems.append(e)
        if len(elems) == 0:
            #~ raise Exception("20120914 %s %s" % (self,elemname))
            return None
        #return self.vbox_class(self,name,*elems,**kw)
        #~ kw = self.ui.panel_attr2kw(**kw)
        #~ return panelclass(self,elemname,True,*elems,**kw)
        if len(elems) == 1 and elemname != 'main': # panelclass != self.main_class:
            #~ if label:
                #~ elems[0].label = label
            elems[0].setup(**kw)
            return elems[0]
        #~ kw.update(self.layout.panel_options.get(elemname,{}))
        e = create_layout_panel(self,elemname,vertical,elems,**kw)
        #~ e.allow_read = curry(perms.make_permission(self.layout._datasource,**e.required),e)
        return e
            
    def define_panel(self,name,desc,**kw):
        if not desc:
            return 
            #~ raise Exception(
                #~ 'Failed to define empty element %s (in %s)' 
                #~ % (name,self.layout))
        #~ if hasattr(self,name):
        if self._names.has_key(name):
            raise Exception(
                'Duplicate element definition %s = %r in %s' 
                % (name,desc,self.layout))
        #~ if name == 'main':
            #~ e = self.desc2elem(self.main_class,name,desc,**kw)
        #~ else:
            #~ e = self.desc2elem(self.ui.Panel,name,desc,**kw)
        e = self.desc2elem(name,desc,**kw)
        if e is None:
            if False:
                raise Exception(
                    'Failed to define element %s = %s\n(in %s)' 
                    % (name,desc,self.layout))
            return
        #~ e.allow_read = curry(perms.make_permission(self.layout._datasource,**e.required),e)
        self._names[name] = e
        #~ setattr(self,name,e)
        return e
        
            
    def create_element(self,desc_name):
        #~ logger.debug("create_element(%r)", desc_name)
        name,pkw = self.splitdesc(desc_name)
        #~ kw.update(pkw)
        #~ e = getattr(self,name,None)
        if self._names.has_key(name):
            raise Exception(
                'Duplicate element definition %s = %r in %s' 
                % (name,desc_name,self.layout))
        #~ e = self._names.get(name,None)
        #~ if e is not None:
            #~ return e
        desc = getattr(self.layout,name,None)
        if desc is not None:
            return self.define_panel(name,desc,**pkw)
        #~ if str(self.layout._datasource) == 'cal.Events':
            #~ if name == 'start':
                #~ print 20121021, repr(name), "not a panel", repr(self.layout)
            #~ return self.define_panel(name,desc)
        e = create_layout_element(self,name,**pkw)
        #~ e = self.ui.create_layout_element(self,name)
        if e is None: return None # e.g. NullField
        # todo: cannot hide babelfields
        if name in self.layout.hidden_elements:
            #~ print "20130124 hide element %r in %s" % (name, self)
            if isinstance(self.layout,FormLayout):
                return None
            e.hidden = True
        #~ setattr(self,name,e)
        self._names[name] = e
        #~ self.setup_element(e)
        #~ if name == 'invoiceable':
            #~ logger.info("20130612 create_element() --> %r", e)
        return e
        
    #~ def splitdesc(self,picture,**kw):
    def splitdesc(self,picture):
        kw = dict()
        if picture.endswith(')'):
            raise Exception("No longer supported since 20120630")
            a = picture.split("(",1)
            if len(a) == 2:
                pkw = eval('dict('+a[1])
                kw.update(pkw)
                picture = a[0]
                #~ return a[0],kw
        a = picture.split(":",1)
        if len(a) == 1:
            return picture,{}
        if len(a) == 2:
            name = a[0]
            a = a[1].split("x",1)
            if len(a) == 1:
                kw.update(width=int(a[0]))
                #~ return name, dict(width=int(a[0]))
                return name, kw
            elif len(a) == 2:
                kw.update(width=int(a[0]),height=int(a[1]))
                #~ return name, dict(width=int(a[0]),height=int(a[1]))
                return name, kw
        raise Exception("Invalid picture descriptor %s" % picture)
        
    def use_as_wildcard(self,de):
        if de.name.endswith('_ptr'): return False
        #~ and (de.name not in self.hidden_elements) \
        #~ and (de.name not in self.rh.report.known_values.keys()) \
        #~ if de.name == self.rh.report.master_key: return False
        if isinstance(self.layout,ListLayout):
            if de.name == self.layout._datasource.master_key: return False
        return True
  
    def get_data_elem(self,name): 
        return self.layout.get_data_elem(name)
        
    def get_choices_url(self,*args,**kw):
        return self.layout.get_choices_url(settings.SITE.ui,*args,**kw)
        



class BaseLayout(object):
    """
    Base class for all Layouts (:class:`FormLayout`, :class:`ListLayout` 
    and  :class:`ParamsLayout`).
    
    A Layout instance just holds the string templates. 
    It is designed to be subclassed by applications programmers, 
    but in most cases it is more convenient (and recommended) 
    to use the methods 
    :meth:`set_detail_layout <lino.core.actors.Actor.set_detail_layout>`,
    :meth:`set_insert_layout <lino.core.actors.Actor.set_insert_layout>`,
    :meth:`add_detail_panel <lino.core.actors.Actor.add_detail_panel>`
    and
    :meth:`add_detail_tab <lino.core.actors.Actor.add_detail_tab>`
    on the :class:`Actor <lino.core.actors.Actor>`.

    
    """
    _handle_class = LayoutHandle
    #~ __metaclass__ = LayoutMeta
    
    #~ _table = None # deprecated
    _datasource = None
    
    window_size = None
    """
    A tuple `(width,height)` that specifies the size of the window to be used for this layout.
    For example, specifying `window_size=(50,30)` means "50 characters wide and 30 lines high".
    The `height` value can also be the string ``'auto'``.
    """
    
    main = None
    
    #~ panel_options = {}
    #~ """
    #~ A dict of 
    #~ """
    
    #~ 20120923 
    #~ _added_panels = dict()
    #~ _labels = dict()
    #~ _element_options = dict()
    
    #~ def __init__(self,table=None,main=None,hidden_elements=frozenset(),window_size=None):
    def __init__(self,main=None,datasource=None,hidden_elements=None,**kw):
        """
        datasource is either an actor or an action.
        """
        #~ assert table is not None
        #~ self._table = table
        #~ self._datasource = datasource 
        self._labels = self.override_labels()
        self._added_panels = dict()
        #~ self._window_size = window_size
        self.hidden_elements = hidden_elements or frozenset()
        self._element_options = dict()
        if main is not None:
            self.main = main
        #~ elif not hasattr(self,'main'):
        elif self.main is None:
            raise Exception("Cannot instantiate %s without `main`." % self.__class__)
        self.set_datasource(datasource)
        for k,v in kw.items():
            #~ if not hasattr(self,k):
                #~ raise Exception("Got unexpected keyword %s=%r" % (k,v))
            setattr(self,k,v)
            
    def set_datasource(self,ds):
        self._datasource = ds
        if ds is not None:
            self.hidden_elements = self.hidden_elements | ds.hidden_elements
            #~ if str(ds).endswith('Partners'):
                #~ print "20130124 set_datasource ", self,self.hidden_elements
      
            
    
    def override_labels(self):
        return dict()
        
    def get_data_elem(self,name): 
        return self._datasource.get_data_elem(name)
        
    def remove_element(self,*args):
        """
        Removes specified element names from this Panel's `main` template.
        """
        for name in args:
            self.main = self.main.replace(name,'')
        
        
    def setup_handle(self,lh):
        pass
        
    def update(self,**kw):
        """
        Update the template of one or more panels.
        """
        #~ if hasattr(self,'_extjs3_handle'):
            #~ raise Exception("Cannot update form layout after UI has been set up.")
        for k,v in kw.items():
            if DEBUG_LAYOUTS(self):
                msg = """\
In %s, updating attribute %r:
--- before:
%s
--- after:
%s
---""" % (self,k,getattr(self,k,'(undefined)'),v)
                logger.info(msg)
            setattr(self,k,v)
            
    def add_panel(self,name,tpl,label=None,**options):
        """
        Adds a new panel to this layout.
        
        Arguments:
        
        - `name` is the internal name of the panel
        - `tpl` the template string
        - `label` an optional label
        - any further keyword are passed as options to the new panel
        """
        #~ if hasattr(self,'_extjs3_handle'):
            #~ raise Exception("Cannot update for layout after UI has been set up.")
        if '\n' in name:
           raise Exception("name may not contain any newline") 
        if ' ' in name:
           raise Exception("name may not contain any whitespace") 
        #~ if getattr(self,name,None) is not None:
           #~ raise Exception("name %r already defined in %s" % (name,self)) 
        self._add_panel(name,tpl,label,options)
        
    #~ @classmethod    
    def _add_panel(self,name,tpl,label,options):
        if tpl is None:
            return # when does this occur?
        if hasattr(self,name):
            raise Exception("Oops: %s has already a name %r" % (self,name))
        if DEBUG_LAYOUTS(self):
            msg = """\
Adding panel %r to %s ---:
%s
---""" % (name,self,tpl)
            logger.info(msg)
        setattr(self,name,tpl)
        self._added_panels[name] = tpl # 20120914c
        if label is not None:
            self._labels[name] = label
        if options:
            self._element_options[name] = options
            
    #~ @classmethod    
    def add_tabpanel(self,name,tpl=None,label=None,**options):
        """
        Add a tab panel to an existing layout.
        Arguments: see :meth:`BaseLayout.add_panel`.
        The difference with :meth:`BaseLayout.add_panel` 
        is that this potentially turns the existing `main` panel to a tabbed panel.
        
        Arguments:
        
        - `name` is the internal name of the panel
        - `tpl` the template string
        - `label` an optional label
        """
        #~ print "20120526 add_detail_tab", self, name
        #~ if hasattr(self,'_extjs3_handle'):
            #~ raise Exception("Cannot update form layout after UI has been set up.")
        if '\n' in name:
           raise Exception("name may not contain any newline") 
        if ' ' in name:
           raise Exception("name may not contain any whitespace") 
        if '\n' in self.main:
            if hasattr(self,'general'):
                raise NotImplementedError("""\
%s has both a vertical `main` and a panel called `general`.""" % self)
            self.general = self.main
            self.main = "general " + name
            self._labels['general'] = _("General")
            if DEBUG_LAYOUTS(self):
                msg = """\
add_tabpanel() on %s moving content of vertical 'main' panel to 'general'.
New 'main' panel is %r"""
                logger.info(msg,self,self.main)
        else:
            self.main += " " + name
            if DEBUG_LAYOUTS(self):
                msg = """\
add_tabpanel() on %s horizontal 'main' panel %r."""
                logger.info(msg,self,self.main)
        #~ if tpl is not None:
        self._add_panel(name,tpl,label,options)
            #~ self._add_panel(name,tpl)
            #~ setattr(self,name,tpl)
            #~ self._added_panels[name] = tpl # 20120914c
        #~ if label is not None:
            #~ self._labels[name] = label
        #~ self._element_options[name] = options
        #~ if kw:
            #~ print 20120525, self, self.detail_layout._element_options
            
            
    #~ def before_setup_handle(self):
        #~ pass

            
    def get_layout_handle(self,ui):
        """
        Same code as lino.ui.base.Handled.get_handle, 
        except that here it's an instance method.
        """
        #~ assert ui is None or isinstance(ui,UI), \
            #~ "%s.get_handle() : %r is not a BaseUI" % (self,ui)
        #~ if ui is None:
            #~ hname = '_lino_console_handler'
        #~ else:
            #~ hname = ui._handle_attr_name
        hname = constants._handle_attr_name
            
            
        #~ write_lock.acquire()
        #~ try:
        # we do not want any inherited handle
        h = self.__dict__.get(hname,None)
        if h is None:
            #~ self.before_setup_handle()
            #~ print 20130404, self._handle_class
            h = self._handle_class(self)
            setattr(self,hname,h)
            #~ h.setup()
        #~ finally:
            #~ write_lock.release()
        return h
        
    def __str__(self):
        #~ return "%s Detail(%s)" % (self._datasource,[str(x) for x in self.layouts])
        return "%s on %s" % (self.__class__.__name__,self._datasource)
        
    def get_choices_url(self,ui,field,**kw):
        return settings.SITE.build_admin_url("choices",
          self._datasource.app_label,
          self._datasource.__name__,
          field.name,**kw)
        
        
            
class FieldLayout(BaseLayout):
    pass
    
    #~ def before_setup_handle(self):
        #~ logger.info("20130804 before_setup_handle %s",self)
        #~ ds = settings.SITE.modules.resolve(str(self._datasource))
        #~ if self._datasource is not ds:
            #~ logger.info("20130804 override _datasource of %r by %r",self._datasource,ds)
            #~ self._datasource = ds
        
    
class FormLayout(FieldLayout):
    """
    A Layout description for the main panel of a DetailWindow or InsertWindow.
    """
    join_str = "\n"
    
class ListLayout(FieldLayout):
    """
    A Layout description for the columns of a GridPanel.
    """
    join_str = " "
    
    def set_datasource(self,ds):
        if ds is None:
            raise Exception("20130327 No datasource for %r" % self)
        super(ListLayout,self).set_datasource(ds)

class ParamsLayout(BaseLayout):
    """
    A Layout description for a :attr:`lino.core.actors.Actor.parameters` panel.
    """
    join_str = " "
    url_param_name = constants.URL_PARAM_PARAM_VALUES
    params_store = None

    def get_data_elem(self,name):
        return self._datasource.get_param_elem(name)
        
    def setup_handle(self,lh):
        #~ if self.params_store is None:
        #~ from lino.ui.extjs3 import ext_store
        from lino.ui import store
        self.params_store = store.ParameterStore(lh,self.url_param_name)

class ActionParamsLayout(ParamsLayout):
    """
    A Layout description for an :attr:`lino.core.actions.Action.parameters` panel.
    """
    join_str = "\n"
    window_size = (50,'auto')
    url_param_name = constants.URL_PARAM_FIELD_VALUES
    
    def get_choices_url(self,ui,field,**kw):
        return settings.SITE.build_admin_url("apchoices",
          self._datasource.defining_actor.app_label,
          self._datasource.defining_actor.__name__,
          self._datasource.action_name,
          field.name,**kw)
    

    def unused_get_choices_url(self,ui,field,**kw):
        """
        """
        a = self._datasource
        return settings.SITE.build_admin_url("apchoices",
          field.rel.to._meta.app_label,
          field.rel.to.__name__,
          #~ 'oops', # todo: instantiate ActionParamsLayout per BoundAction (not per Action)?
          #~ ba.actor.app_label,
          #~ ba.actor.__name__,
          a.action_name,
          field.name,**kw)



def create_layout_panel(lh,name,vertical,elems,**kw):
    """
    This also must translate ui-agnostic parameters 
    like `label_align` to their ExtJS equivalent `labelAlign`.
    """
    from lino.ui import elems as ext_elems
    pkw = dict()
    pkw.update(labelAlign=kw.pop('label_align','top'))
    pkw.update(hideCheckBoxLabels=kw.pop('hideCheckBoxLabels',True))
    pkw.update(label=kw.pop('label',None))
    pkw.update(width=kw.pop('width',None))
    pkw.update(height=kw.pop('height',None))
    #~ required = {}
    #~ main panel 
    # 20121116
    #~ if False and name == 'main' and isinstance(lh.layout,ListLayout):
    #~ if name != 'main' and isinstance(lh.layout,ListLayout):
    #~ required.update(lh.layout._datasource.required)
    #~ todo: requirements sind eine negativ-liste. aber auth=True muss in eine positiv-liste
    v = kw.pop('required',NOT_PROVIDED)
    if v is not NOT_PROVIDED:
        pkw.update(required=v)
    if kw:
        raise Exception("Unknown panel attributes %r for %s" % (kw,lh))
    if name == 'main':
        if isinstance(lh.layout,ListLayout):
            #~ return ext_elems.GridMainPanel(lh,name,vertical,*elems,**pkw)
            #~ return ext_elems.GridMainPanel(lh,name,lh.layout._datasource,*elems,**pkw)
            e = ext_elems.GridElement(lh,name,lh.layout._datasource,*elems,**pkw)
        elif isinstance(lh.layout,ActionParamsLayout) : 
            e = ext_elems.ActionParamsPanel(lh,name,vertical,*elems,**pkw)
        elif isinstance(lh.layout,ParamsLayout) : 
            e = ext_elems.ParamsPanel(lh,name,vertical,*elems,**pkw)
            #~ fkw = dict(layout='fit', autoHeight= True, frame= True, items=pp)
            #~ if lh.layout._datasource.params_panel_hidden:
                #~ fkw.update(hidden=True)
            #~ return ext_elems.FormPanel(**fkw)
        elif isinstance(lh.layout,FormLayout): 
            if len(elems) == 1 or vertical:
                e = ext_elems.DetailMainPanel(lh,name,vertical,*elems,**pkw)
            else:
                e = ext_elems.TabPanel(lh,name,*elems,**pkw)
        else:
            raise Exception("No element class for layout %r" % lh.layout)
        #~ actions.loosen_requirements(e,**lh.layout._datasource.required)
        #~ e.debug_permissions = True
        return e
    return ext_elems.Panel(lh,name,vertical,*elems,**pkw)

def create_layout_element(lh,name,**kw):
    """
    Create a layout element from the named data element.
    """
    from north.dbutils import BabelCharField, BabelTextField
    from lino.ui import elems as ext_elems
    from lino.core import fields
    from lino.core import tables
    from lino.utils.jsgen import js_code
    #~ if True: 
    if settings.SITE.catch_layout_exceptions: 
        try:
            de = lh.get_data_elem(name)
        except Exception, e:
            #~ logger.exception(e) # removed 20130422 caused disturbing output when running tests
            de = None
            name += " (" + str(e) + ")"
    else:
        de = lh.get_data_elem(name)
        
    #~ if isinstance(de,fields.FieldSet):
        #~ # return lh.desc2elem(ext_elems.FieldSetPanel,name,de.desc)
        #~ return lh.desc2elem(name,de.desc,**kw)
        
    #~ if isinstance(de,fields.NullField):
        #~ return None
        
    if isinstance(de,fields.DummyField):
        return None
    if isinstance(de,fields.Constant):
        return ext_elems.ConstantElement(lh,de,**kw)
        
        
    if isinstance(de,SingleRelatedObjectDescriptor):
        return ext_elems.SingleRelatedObjectElement(lh,de.related,**kw)
        #~ return create_field_element(lh,de.related.field,**kw)
        
    if isinstance(de,fields.RemoteField):
        return create_field_element(lh,de,**kw)
    if isinstance(de,models.Field):
        if isinstance(de,(BabelCharField,BabelTextField)):
            if len(settings.SITE.BABEL_LANGS) > 0:
                elems = [ create_field_element(lh,de,**kw) ]
                for lang in settings.SITE.BABEL_LANGS:
                    #~ bf = lh.get_data_elem(name+'_'+lang)
                    bf = lh.get_data_elem(name+lang.suffix)
                    elems.append(create_field_element(lh,bf,**kw))
                return elems
        return create_field_element(lh,de,**kw)
        
    #~ if isinstance(de,fields.LinkedForeignKey):
        #~ de.primary_key = False # for ext_store.Store()
        #~ lh.add_store_field(de)
        #~ return ext_elems.LinkedForeignKeyElement(lh,de,**kw)
        
    if isinstance(de,generic.GenericForeignKey):
        # create a horizontal panel with 2 comboboxes
        #~ print 20111123, name,de.ct_field + ' ' + de.fk_field
        #~ return lh.desc2elem(panelclass,name,de.ct_field + ' ' + de.fk_field,**kw)
        #~ return ext_elems.GenericForeignKeyField(lh,name,de,**kw)
        de.primary_key = False # for ext_store.Store()
        lh.add_store_field(de)
        return ext_elems.GenericForeignKeyElement(lh,de,**kw)
        
        
    #~ if isinstance(de,type) and issubclass(de,dd.Table):
    if isinstance(de,type) and issubclass(de,tables.AbstractTable):
        kw.update(master_panel=js_code("this"))
        if isinstance(lh.layout,FormLayout):
            """a Table in a DetailWindow"""
            kw.update(tools=[
              js_code("Lino.show_in_own_window_button(Lino.%s)" % de.default_action.full_name())
              #~ js_code("Lino.report_window_button(Lino.%s)" % de.default_action)
              #~ js_code("Lino.report_window_button(ww,Lino.%s)" % de.default_action)
            ])
            #~ if settings.SITE.use_quicktips and de.help_text:
                #~ kw.update(listeners=dict(render=js_code(
                  #~ "Lino.quicktip_renderer(%s,%s)" % (py2js('Slave'),py2js(de.help_text)))
                #~ ))
           
            if de.slave_grid_format == 'grid':
                #~ if not de.parameters:
                kw.update(hide_top_toolbar=True)
                if de.preview_limit is not None:
                    kw.update(preview_limit=de.preview_limit)
                e = ext_elems.GridElement(lh,name,de,**kw)
                return e
            elif de.slave_grid_format == 'summary':
                # a Table in a DetailWindow, displayed as a summary in a HtmlBox 
                o = dict(drop_zone="FooBar")
                #~ a = de.get_action('insert')
                a = de.insert_action
                if a is not None:
                    kw.update(ls_insert_handler=js_code("Lino.%s" % a.full_name()))
                    kw.update(ls_bbar_actions=[settings.SITE.ui.ext_renderer.a2btn(a)])
                #~ else:
                    #~ print 20120619, de, 'has no insert_action'
                field = fields.HtmlBox(verbose_name=de.label,**o)
                field.help_text = de.help_text
                field.name = de.__name__
                #~ field._return_type_for_method = de.slave_as_summary_meth(self,'<br>')
                field._return_type_for_method = de.slave_as_summary_meth(E.br)
                lh.add_store_field(field)
                e = ext_elems.HtmlBoxElement(lh,field,**kw)
                return e
                
            elif de.slave_grid_format == 'html':
                #~ a = de.get_action('insert')
                if de.editable:
                    a = de.insert_action
                    if a is not None:
                        kw.update(ls_insert_handler=js_code("Lino.%s" % a.full_name()))
                        kw.update(ls_bbar_actions=[settings.SITE.ui.ext_renderer.a2btn(a)])
                field = fields.HtmlBox(verbose_name=de.label)
                field.name = de.__name__
                field.help_text = de.help_text
                #~ field._return_type_for_method = de.slave_as_html_meth(self)
                field._return_type_for_method = de.slave_as_html_meth()
                lh.add_store_field(field)
                #~ kw.update(required=de.required) # e.g. lino.Home.UsersWithClients not visible for everybody
                e = ext_elems.HtmlBoxElement(lh,field,**kw)
                e.add_requirements(**de.required)
                return e
        else:
            #~ field = fields.TextField(verbose_name=de.label)
            field = fields.HtmlBox(verbose_name=de.label)
            field.name = de.__name__
            #~ field._return_type_for_method = de.slave_as_summary_meth(self,', ')
            field._return_type_for_method = de.slave_as_summary_meth(', ')
            lh.add_store_field(field)
            e = ext_elems.HtmlBoxElement(lh,field,**kw)
            return e
            
    if isinstance(de,fields.VirtualField):
        return create_vurt_element(lh,name,de,**kw)
        
    if callable(de):
        rt = getattr(de,'return_type',None)
        if rt is not None:
            return create_meth_element(lh,name,de,rt,**kw)
            
    if not name in ('__str__','__unicode__','name','label'):
        value = getattr(lh,name,None)
        if value is not None:
            return value
            
    if hasattr(lh,'rh'):
        msg = "Unknown element %r referred in layout <%s of %s>." % (
            name,lh.layout,lh.rh.actor)
        l = [de.name for de in lh.rh.actor.wildcard_data_elems()]
        model = getattr(lh.rh.actor,'model',None) # VirtualTables don't have a model
        if getattr(model,'_lino_slaves',None):
            l += [str(rpt) for rpt in model._lino_slaves.values()]
        msg += " Possible names are %s." % ', '.join(l)
    else:
        #~ logger.info("20121023 create_layout_element %r",lh.layout._datasource)
        #~ l = [de.name for de in lh.layout._datasource.wildcard_data_elems()]
        #~ print(20130202, [f.name for f in lh.layout._datasource.model._meta.fields])
        #~ print(20130202, lh.layout._datasource.model._meta.get_all_field_names())
        msg = "Unknown element %r referred in layout <%s>." % (
            name,lh.layout)
        if de is not None:
            msg += " Cannot handle %r" % de
    raise KeyError(msg)
    

def create_vurt_element(lh,name,vf,**kw):
    #~ assert vf.get.func_code.co_argcount == 2, (name, vf.get.func_code.co_varnames)
    e = create_field_element(lh,vf,**kw)
    if not vf.is_enabled(lh):
        e.editable = False
    return e
    
def create_meth_element(lh,name,meth,rt,**kw):
    #~ if hasattr(rt,'_return_type_for_method'):
        #~ raise Exception(
          #~ "%s.%s : %r has already an attribute '_return_type_for_method'" % (
            #~ lh,name,rt))
    rt.name = name
    rt._return_type_for_method = meth
    if meth.func_code.co_argcount < 2:
        raise Exception("Method %s has %d arguments (must have at least 2)" % (meth,meth.func_code.co_argcount))
        #~ , (name, meth.func_code.co_varnames)
    #~ kw.update(editable=False)
    e = create_field_element(lh,rt,**kw)
    #~ if lh.rh.actor.actor_id == 'contacts.Persons':
        #~ print 'ext_ui.py create_meth_element',name,'-->',e
    #~ if name == 'preview':
        #~ print 20110714, 'ext_ui.create_meth_element', meth, repr(e)
    return e
    #~ e = lh.main_class.field2elem(lh,return_type,**kw)
    #~ assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,name)
    #~ lh._store_fields.append(e.field)
    #~ return e
        
    #~ if rt is None:
        #~ rt = models.TextField()
        
    #~ e = ext_elems.MethodElement(lh,name,meth,rt,**kw)
    #~ assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,name)
    #~ lh._store_fields.append(e.field)
    #~ return e
      
    
def create_field_element(lh,field,**kw):
    #~ e = lh.main_class.field2elem(lh,field,**kw)
    from lino.ui import elems as ext_elems
    e = ext_elems.field2elem(lh,field,**kw)
    assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,kw)
    lh.add_store_field(e.field)
    return e
    #return FieldElement(field,**kw)
    
