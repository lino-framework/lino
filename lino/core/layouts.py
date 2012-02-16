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

#~ from lino.tools import resolve_model, resolve_field, get_app, full_model_name, get_field, UnresolvedModel
from lino.tools import resolve_model, UnresolvedModel
#~ from lino.utils.config import LOCAL_CONFIG_DIR
from lino.core.coretools import get_slave, get_model_report, get_data_elem
from lino.utils.tables import AbstractTable, AbstractTableRequest, VirtualTable
#~ from lino.utils.tables import GridEdit #, ComputedColumn

class LayoutError(RuntimeError):
    pass
  
LABEL_ALIGN_TOP = 'top'
LABEL_ALIGN_LEFT = 'left'
LABEL_ALIGN_RIGHT = 'right'


class LayoutHandle:
    """
    LayoutHandle analyzes a Layout and builds a tree of LayoutElements.
    
    """
    
    #~ 20120114 def __init__(self,ui,table,layout,hidden_elements=frozenset()):
    def __init__(self,ui,layout):
      
        #~ logger.debug('20111113 %s.__init__(%s,%s)',self.__class__.__name__,rh,layout)
        assert isinstance(layout,BaseLayout)
        #assert isinstance(link,reports.ReportHandle)
        #~ base.Handle.__init__(self,ui)
        #~ actors.ActorHandle.__init__(self,layout)
        self.layout = layout
        self.ui = ui
        #~ self.rh = rh
        #~ self.datalink = layout.get_datalink(ui)
        #~ self.label = layout.label # or ''
        self._store_fields = []
        #~ self._elems_by_field = {}
        #~ self._submit_fields = []
        #~ self.slave_grids = []
        #~ self._buttons = []
        #~ self.main_class = ui.main_panel_class(layout)
        
        self.define_elem('main',layout.main)
        
        if self.main is None:
            raise Exception("Failed to create main element %r for %s." % (layout.main,layout))
        
        self.width = self.main.width
        self.height = self.main.height
        
        self.layout.setup_handle(self)
        
        
                
    def __str__(self):
        #~ return "%s %s" % (self.rh,self.__class__.__name__)
        return "%s for %s" % (self.__class__.__name__,self.layout)
        
        
    def add_store_field(self,field):
        self._store_fields.append(field)
        
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
            f.write(u"\n".join(self.main.debug_lines()))
            f.write('''</table></body></html>''')
            f.close()
        
    def get_title(self,ar):
        return self.layout.get_title(ar)
        
    def walk(self):
        return self.main.walk()
        
    def ext_lines(self,request):
        return self.main.ext_lines(request)
  
        
    def define_elem(self,name,desc,**kw):
        if not desc:
            raise Exception(
                'Failed to define empty element %s (in %s)' 
                % (name,self.layout))
            #~ return
        if hasattr(self,name):
            raise Exception(
                'Duplicate element definition %s = %r in %s' 
                % (name,desc,self.layout))
        #~ if name == 'main':
            #~ e = self.desc2elem(self.main_class,name,desc,**kw)
        #~ else:
            #~ e = self.desc2elem(self.ui.Panel,name,desc,**kw)
        e = self.desc2elem(name,desc,**kw)
        if e is None:
            raise Exception(
                'Failed to define element %s = %s\n(in %s)' 
                % (name,desc,self.layout))
                #~ return
        setattr(self,name,e)
        return e
        
    #~ define_panel = define_elem
            
    #~ def desc2elem(self,panelclass,desc_name,desc,**kw):
    def desc2elem(self,elemname,desc,**kw):
        #logger.debug("desc2elem(panelclass,%r,%r)",elemname,desc)
        #assert desc != 'Countries_choices2'
        
        # flatten continued lines:
        desc = desc.replace('\\\n','')
        
        if '*' in desc:
            explicit_specs = set()
            for spec in desc.split():
                if spec != '*':
                    name,kw = self.splitdesc(spec)
                    explicit_specs.add(name)
            wildcard_fields = self.layout.join_str.join([
                de.name for de in self.layout._table.wildcard_data_elems() \
                  if (de.name not in explicit_specs) \
                    and self.use_as_wildcard(de) \
                ])
            desc = desc.replace('*',wildcard_fields)
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
                  
                    if x.startswith(':'):
                        a = x.split(':',2)
                        if len(a) != 3:
                            raise LayoutError('Expected attribute `:attr: value` ')
                        attname = a[1]
                        kw[attname] = a[2].strip()
                    else:
                        i += 1
                        e = self.desc2elem(elemname+'_'+str(i),x)
                        if e is not None:
                            elems.append(e)
            if len(elems) == 1:
                vertical = False
        else:
            # it's a horizontal box
            vertical = False
            elems = []
            for x in desc.split():
                if not x.startswith("#"):
                    """
                    20100214 dsbe.PersonDetail hatte 2 MainPanels, 
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
            return None
        #return self.vbox_class(self,name,*elems,**kw)
        #~ kw = self.ui.panel_attr2kw(**kw)
        #~ return panelclass(self,elemname,True,*elems,**kw)
        if False:
            label = kw.get('label',None)
            if label:
                self.layout.add_dummy_message(label)
                kw.update(label = _(label))
        if len(elems) == 1 and elemname != 'main': # panelclass != self.main_class:
            #~ if label:
                #~ elems[0].label = label
            return elems[0]
        return self.ui.create_layout_panel(self,elemname,vertical,elems,**kw)
            
    def create_element(self,desc_name,**kw):
        #~ logger.debug("create_element(%r)", desc_name)
        name,pkw = self.splitdesc(desc_name)
        kw.update(pkw)
        e = getattr(self,name,None)
        if e is not None:
            return e
        desc = getattr(self.layout,name,None)
        if desc is not None:
            return self.define_elem(name,desc,**kw)
        e = self.ui.create_layout_element(self,name,**kw)
        # todo: cannot hide babelfields
        if name in self.layout.hidden_elements:
            e.hidden = True
        #~ self.setup_element(e)
        return e
        
    def splitdesc(self,picture,**kw):
        if picture.endswith(')'):
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
            if de.name == self.layout._table.master_key: return False
        return True
        
        return True
  
    def get_data_elem(self,name): 
        return self.layout.get_data_elem(name)
        

class unused_ListLayoutHandle(LayoutHandle):
  
    def __init__(self,rh,*args,**kw):
        self.rh = rh
        #~ 20120114 LayoutHandle.__init__(self,rh.ui,rh.report,*args,**kw)
        LayoutHandle.__init__(self,rh.ui,*args,**kw)
        
    def use_as_wildcard(self,de):
        if de.name.endswith('_ptr'): return False
        #~ and (de.name not in self.hidden_elements) \
        #~ and (de.name not in self.rh.report.known_values.keys()) \




#~ LAYOUTS = []

#~ class LayoutMeta(type):
  
    #~ def __new__(meta, classname, bases, classDict):
        #~ cls = type.__new__(meta, classname, bases, classDict)
        #~ LAYOUTS.append(cls)
        #~ return cls


#~ class BaseLayout(Configured):
class BaseLayout(object):
  
    _handle_class = LayoutHandle
    #~ __metaclass__ = LayoutMeta
    
    _table = None
    
    def __init__(self,table,main=None,hidden_elements=frozenset()):
        self._table = table
        self.hidden_elements = hidden_elements 
        if main:
            self.main = main
        if not hasattr(self,'main'):
            raise Exception("Cannot instantiate %s with empty main" % self.__class__)
    
    def get_data_elem(self,name): 
        return self._table.get_data_elem(name)
        
    def setup_handle(self,lh):
        pass
        
    def get_handle(self,ui):
        """
        Same code as lino.ui.base.Handled.get_handle, 
        except that here it's an instance method.
        """
        #~ assert ui is None or isinstance(ui,UI), \
            #~ "%s.get_handle() : %r is not a BaseUI" % (self,ui)
        if ui is None:
            hname = '_lino_console_handler'
        else:
            hname = ui._handle_attr_name
        h = self.__dict__.get(hname,None)
        if h is None:
            h = self._handle_class(ui,self)
            setattr(self,hname,h)
            #~ h.setup()
        return h
        
    def __str__(self):
        #~ return "%s Detail(%s)" % (self.actor,[str(x) for x in self.layouts])
        return "%s on %s" % (self.__class__.__name__,self._table)

        
            
class DetailLayout(BaseLayout):
    #~ show_labels = True
    join_str = "\n"
    #~ only_for_report = None
    #~ tabbed = False
    #~ def __init__(self,*args,**kw):
        #~ BaseLayout.__init(self,*args,**kw)
        #~ if self.main
        
    def __init__(self,*args,**kw):
        super(DetailLayout,self).__init__(None,*args,**kw)
        

class ListLayout(BaseLayout):
    #~ _handle_class = ListLayoutHandle
    #~ show_labels = False
    join_str = " "
    
    

class ParamsLayout(BaseLayout):
    #~ label_align = LABEL_ALIGN_TOP
    #~ show_labels = True
    join_str = " "

    def get_data_elem(self,name): 
        return self._table.get_param_elem(name)

#~ def setup_layouts():
    #~ for cl in LAYOUTS:
        #~ if layout.actor is None:
            #~ continue
        #~ if isinstance(layout.actor,basestring):
            #~ layout.actor = settings.LINO.modules.resolve(layout.actor)
        #~ if issubclass(layout.actor,models.Model):
            #~ layout.actor = layout.actor._lino_model_report
        #~ if layout.actor is None:
            #~ continue

        #~ if issubclass(DetailLayout):
            #~ layout.actor._lino_detail = LayoutHandle(ui)





if False:


  class unused_DetailHandle(base.Handle):
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
          
      def find_by_name(self,name):
          for lh in self.lh_list:
              e = lh.main.find_by_name(name)
              if e is not None:
                  return e
        
        

  class unused_Detail(object):
      """
      The UI-agnostic representation of a Detail window.
      Equivalent to a collection of .dtl files.
      """
      _handle_class = DetailHandle    
      
      #~ def __init__(self,model,layouts):
      def __init__(self,actor,layouts):
          #~ self.model = model
          #~ self.table = model._lino_model_report,
          self.actor = actor
          #~ self.table = model._lino_model_report,
          self.layouts = layouts
          self._handles = {}


      def get_handle(self,ui):
          "similar to Handled.get_handle, but now its an instance method"
          #~ assert ui is None or isinstance(ui,UI), \
              #~ "%s.get_handle() : %r is not a BaseUI" % (self,ui)
          if ui is None:
              hname = '_lino_console_handler'
          else:
              hname = ui._handle_attr_name
          h = self.__dict__.get(hname,None)
          if h is None:
              h = self._handle_class(ui,self)
              setattr(self,hname,h)
              h.setup()
          return h

      #~ def get_handle(self,k):
          #~ h = self._handles.get(k,None)
          #~ if h is None:
              #~ h = DetailHandle(k,self)
              #~ self._handles[k] = h
              #~ h.setup()
          #~ return h
          
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

