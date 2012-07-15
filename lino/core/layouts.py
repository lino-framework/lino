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

'''

See :doc:`/topics/layouts`

'''

import logging
logger = logging.getLogger(__name__)

import cgi
import os
import sys
import traceback
import codecs
import yaml


from django.utils.translation import ugettext_lazy as _

#~ from lino.core import perms
#~ from lino.utils import curry


class LayoutError(RuntimeError):
    pass
  
LABEL_ALIGN_TOP = 'top'
LABEL_ALIGN_LEFT = 'left'
LABEL_ALIGN_RIGHT = 'right'


class LayoutHandle:
    """
    LayoutHandle analyzes a Layout and stores the 
    resulting LayoutElements provided by the UI.
    
    """
    
    #~ 20120114 def __init__(self,ui,table,layout,hidden_elements=frozenset()):
    def __init__(self,ui,layout):
      
        #~ logger.debug('20111113 %s.__init__(%s,%s)',self.__class__.__name__,rh,layout)
        assert isinstance(layout,BaseLayout)
        #assert isinstance(link,reports.ReportHandle)
        #~ base.Handle.__init__(self,ui)
        self.layout = layout
        self.ui = ui
        #~ self.rh = rh
        #~ self.datalink = layout.get_datalink(ui)
        #~ self.label = layout.label # or ''
        self._store_fields = []
        
        self.define_panel('main',layout.main)
        
        if self.main is None:
            raise Exception(
                "Failed to create main element %r for %s." % (
                layout.main,layout))
        
        self.width = self.main.width
        self.height = self.main.height
        
        self.layout.setup_handle(self)
        for k,v in self.layout._labels.items():
            getattr(self,k).label = v
        
        
                
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
  
        
    def define_panel(self,name,desc,**kw):
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
        #~ e.allow_read = curry(perms.make_permission(self.layout._table,**e.required),e)
        setattr(self,name,e)
        return e
        
            
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
                            #~ e.allow_read = curry(perms.make_permission(self.layout._table,**e.required),e)
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
                        #~ e.allow_read = curry(perms.make_permission(self.layout._table,**e.required),e)
                        elems.append(e)
        if len(elems) == 0:
            return None
        #return self.vbox_class(self,name,*elems,**kw)
        #~ kw = self.ui.panel_attr2kw(**kw)
        #~ return panelclass(self,elemname,True,*elems,**kw)
        if len(elems) == 1 and elemname != 'main': # panelclass != self.main_class:
            #~ if label:
                #~ elems[0].label = label
            return elems[0]
        #~ kw.update(self.layout.panel_options.get(elemname,{}))
        e = self.ui.create_layout_panel(self,elemname,vertical,elems,**kw)
        #~ e.allow_read = curry(perms.make_permission(self.layout._table,**e.required),e)
        return e
            
    def create_element(self,desc_name):
        #~ logger.debug("create_element(%r)", desc_name)
        name,pkw = self.splitdesc(desc_name)
        #~ kw.update(pkw)
        e = getattr(self,name,None)
        if e is not None:
            return e
        desc = getattr(self.layout,name,None)
        if desc is not None:
            return self.define_panel(name,desc,**pkw)
            #~ return self.define_panel(name,desc)
        e = self.ui.create_layout_element(self,name,**pkw)
        #~ e = self.ui.create_layout_element(self,name)
        if e is None: return None # e.g. NullField
        # todo: cannot hide babelfields
        if name in self.layout.hidden_elements:
            e.hidden = True
        setattr(self,name,e)
        #~ self.setup_element(e)
        return e
        
    #~ def splitdesc(self,picture,**kw):
    def splitdesc(self,picture):
        kw = dict()
        if picture.endswith(')'):
            raise Exception("No longer supported sincve 20120630")
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
    
    _table = None
    
    window_size = None
    """
    A tuple `(width,height)` that specifies the size of the window to be used for this layout.
    For example, specifying `window_size=(50,30)` means "50 characters wide and 30 lines high".
    The `height` value can also be the string ``'auto'``.
    """
    
    #~ panel_options = {}
    #~ """
    #~ A dict of 
    #~ """
    
    #~ def __init__(self,table=None,main=None,hidden_elements=frozenset(),window_size=None):
    def __init__(self,main=None,table=None,hidden_elements=frozenset(),**kw):
        self._table = table
        self._labels = dict()
        #~ self._window_size = window_size
        self.hidden_elements = hidden_elements 
        self._element_options = dict()
        if main is not None:
            self.main = main
        elif not hasattr(self,'main'):
            raise Exception("Cannot instantiate %s without `main`." % self.__class__)
        for k,v in kw.items():
            #~ if not hasattr(self,k):
                #~ raise Exception("Got unexpected keyword %s=%r" % (k,v))
            setattr(self,k,v)
    
    def get_data_elem(self,name): 
        return self._table.get_data_elem(name)
        
    def setup_handle(self,lh):
        pass
        
    def update(self,**kw):
        """
        Update the template of one or more panels.
        """
        if hasattr(self,'_extjs3_handle'):
            raise Exception("Cannot update form layout after UI has been set up.")
        for k,v in kw.items():
            #~ if not hasattr(self,k):
                #~ raise Exception("%s has no attribute %r" % (self,k))
            msg = """\
In %s, updating attribute %r:
--- before:
%s
--- after:
%s
---""" % (self,k,getattr(self,k,'(undefined)'),v)
            logger.debug(msg)
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
        if hasattr(self,'_extjs3_handle'):
            raise Exception("Cannot update for layout after UI has been set up.")
        if '\n' in name:
           raise Exception("name may not contain any newline") 
        if ' ' in name:
           raise Exception("name may not contain any whitespace") 
        if getattr(self,name,None) is not None:
           raise Exception("name %r already defined in %s" % (name,self)) 
        msg = """\
Adding panel %r to %s ---:
%s
---""" % (name,self,tpl)
        logger.debug(msg)
        setattr(self,name,tpl)
        if label is not None:
            self._labels[name] = label
        if options:
            self._element_options[name] = options
        
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
        if hasattr(self,'_extjs3_handle'):
            raise Exception("Cannot update form layout after UI has been set up.")
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
            msg = """\
add_tabpanel() on %s moving content of vertical 'main' panel to 'general'.
New 'main' panel is %r"""
            logger.debug(msg,self,self.main)
        else:
            self.main += " " + name
            msg = """\
add_tabpanel() on %s horizontal 'main' panel %r."""
            logger.debug(msg,self,self.main)
        if tpl is not None:
            if hasattr(self,name):
                raise Exception("Oops: %s has already a name %r" % (self,name))
            setattr(self,name,tpl)
        if label is not None:
            self._labels[name] = label
        self._element_options[name] = options
        #~ if kw:
            #~ print 20120525, self, self.detail_layout._element_options
            
            
            
    def get_layout_handle(self,ui):
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

        
            
class FormLayout(BaseLayout):
    """
    A Layout description for the main panel of a DetailWindow or InsertWindow.
    """
    join_str = "\n"
    
        
class ListLayout(BaseLayout):
    """
    A Layout description for the columns of a GridPanel.
    """
    join_str = " "

class ParamsLayout(BaseLayout):
    """
    A Layout description for a parameter panel.
    """
    join_str = " "

    def get_data_elem(self,name): 
        return self._table.get_param_elem(name)

