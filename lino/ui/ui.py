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

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import os
import sys
import cgi
import time
import datetime
#import traceback
import cPickle as pickle
from urllib import urlencode
import codecs
import jinja2

#~ from lxml import etree


#~ import Cheetah
#~ from Cheetah.Template import Template as CheetahTemplate

from django.db import models
from django.conf import settings
from django.http import HttpResponse, Http404
from django.utils import functional
from django.utils.encoding import force_unicode
from django.db.models.fields.related import SingleRelatedObjectDescriptor
#~ from django.utils.functional import Promise

from django.template.loader import get_template
from django.template import RequestContext

from django.utils.translation import ugettext as _
#~ from django.utils import simplejson as json
from django.utils import translation

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf.urls import patterns, url, include


import lino
from lino.core import constants as ext_requests
from . import elems as ext_elems
from . import store as ext_store
#~ from lino.ui.extjs3 import ext_elems
#~ from lino.ui.extjs3 import ext_store
#~ from lino.ui.extjs3 import ext_windows
#~ from lino.ui import requests as ext_requests

from lino import dd
from lino.core import actions 
#~ from lino.core.actions import action2str
from lino.core import dbtables
from lino.core import layouts
from lino.core import tables
#~ from lino.utils.xmlgen import xhtml as xhg
from lino.core import fields
from lino.ui import base
from lino.core import actors
    
from lino.utils import choosers
from lino.utils import babel
from lino.utils.jsgen import py2js, js_code, id2js
from lino.utils.xmlgen import html as xghtml
from lino.utils.config import make_dummy_messages_file

from lino.utils.jscompressor import JSCompressor
if False:
    jscompress = JSCompressor().compress
else:    
    def jscompress(s): return s
      
from lino.mixins import printable



#~ from lino.utils.choicelists import DoYouLike, HowWell
#~ STRENGTH_CHOICES = DoYouLike.get_choices()
#~ KNOWLEDGE_CHOICES = HowWell.get_choices()

#~ NOT_GIVEN = object()


from . import views

from lino.core.signals import pre_ui_build, post_ui_build




def parse_bool(s):
    return s == 'true'
    
def parse_int(s,default=None):
    if s is None: return None
    return int(s)


    
class ExtUI(base.UI):
    """
    The central instance of Lino's ExtJS3 User Interface.
    """
    _handle_attr_name = '_extjs3_handle'
    #~ _response = None
    name = 'extjs3'
    verbose_name = "ExtJS with Windows"
    #~ Panel = ext_elems.Panel
    
    
    #~ USE_WINDOWS = False  # If you change this, then change also Lino.USE_WINDOWS in lino.js

    #~ def __init__(self,*args,**kw):
    def __init__(self):
        #~ logger.info("20130221 lino.ui.ExtUI.__init__()")
        pre_ui_build.send(self)
        
        from lino.utils import codetime
        self.mtime = codetime()
        
        #~ raise Exception("20120614")
        #~ self.pdf_renderer = PdfRenderer(self) # 20120624
        from .extjs import ExtRenderer
        self.ext_renderer = ExtRenderer(self)
        from .render import PlainRenderer, TextRenderer
        self.plain_renderer = PlainRenderer(self)
        self.text_renderer = TextRenderer(self)
        self.reserved_names = [getattr(ext_requests,n) for n in ext_requests.URL_PARAMS]
          
        names = set()
        for n in self.reserved_names:
            if n in names:
                raise Exception("Duplicate reserved name %r" % n)
            names.add(n)
        base.UI.__init__(self) 
        
        #~ trigger creation of params_layout.params_store
        for res in actors.actors_list:
            for ba in res.get_actions():
                if ba.action.parameters:
                    ba.action.params_layout.get_layout_handle(self)
        
        post_ui_build.send(self)
        
    def get_patterns(self):
        """
        """
        self.ext_renderer.build_site_cache()
        return super(ExtUI,self).get_patterns()
        
        
    def create_layout_panel(self,lh,name,vertical,elems,**kw):
        """
        This also must translate ui-agnostic parameters 
        like `label_align` to their ExtJS equivalent `labelAlign`.
        """
        pkw = dict()
        pkw.update(labelAlign=kw.pop('label_align','top'))
        pkw.update(hideCheckBoxLabels=kw.pop('hideCheckBoxLabels',True))
        pkw.update(label=kw.pop('label',None))
        pkw.update(width=kw.pop('width',None))
        pkw.update(height=kw.pop('height',None))
        #~ required = {}
        #~ main panel 
        # 20121116
        #~ if False and name == 'main' and isinstance(lh.layout,layouts.ListLayout):
        #~ if name != 'main' and isinstance(lh.layout,layouts.ListLayout):
        #~ required.update(lh.layout._datasource.required)
        #~ todo: requirements sind eine negativ-liste. aber auth=True muss in eine positiv-liste
        v = kw.pop('required',dd.NOT_PROVIDED)
        if v is not dd.NOT_PROVIDED:
            pkw.update(required=v)
        if kw:
            raise Exception("Unknown panel attributes %r for %s" % (kw,lh))
        if name == 'main':
            if isinstance(lh.layout,layouts.ListLayout):
                #~ return ext_elems.GridMainPanel(lh,name,vertical,*elems,**pkw)
                #~ return ext_elems.GridMainPanel(lh,name,lh.layout._datasource,*elems,**pkw)
                e = ext_elems.GridElement(lh,name,lh.layout._datasource,*elems,**pkw)
            elif isinstance(lh.layout,layouts.ActionParamsLayout) : 
                e = ext_elems.ActionParamsPanel(lh,name,vertical,*elems,**pkw)
            elif isinstance(lh.layout,layouts.ParamsLayout) : 
                e = ext_elems.ParamsPanel(lh,name,vertical,*elems,**pkw)
                #~ fkw = dict(layout='fit', autoHeight= True, frame= True, items=pp)
                #~ if lh.layout._datasource.params_panel_hidden:
                    #~ fkw.update(hidden=True)
                #~ return ext_elems.FormPanel(**fkw)
            elif isinstance(lh.layout,layouts.FormLayout): 
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

    def create_layout_element(self,lh,name,**kw):
        """
        Create a layout element from the named data element.
        """
        #~ if True: 
        if settings.SITE.catch_layout_exceptions: 
            try:
                de = lh.get_data_elem(name)
            except Exception, e:
                logger.exception(e)
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
            #~ return self.create_field_element(lh,de.related.field,**kw)
            
        if isinstance(de,fields.RemoteField):
            return self.create_field_element(lh,de,**kw)
        if isinstance(de,models.Field):
            if isinstance(de,(babel.BabelCharField,babel.BabelTextField)):
                if len(babel.BABEL_LANGS) > 0:
                    elems = [ self.create_field_element(lh,de,**kw) ]
                    for lang in babel.BABEL_LANGS:
                        bf = lh.get_data_elem(name+'_'+lang)
                        elems.append(self.create_field_element(lh,bf,**kw))
                    return elems
            return self.create_field_element(lh,de,**kw)
            
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
            if isinstance(lh.layout,layouts.FormLayout):
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
                        kw.update(ls_bbar_actions=[self.ext_renderer.a2btn(a)])
                    #~ else:
                        #~ print 20120619, de, 'has no insert_action'
                    field = fields.HtmlBox(verbose_name=de.label,**o)
                    field.help_text = de.help_text
                    field.name = de.__name__
                    field._return_type_for_method = de.slave_as_summary_meth(self,'<br>')
                    lh.add_store_field(field)
                    e = ext_elems.HtmlBoxElement(lh,field,**kw)
                    return e
                    
                elif de.slave_grid_format == 'html':
                    #~ a = de.get_action('insert')
                    if de.editable:
                        a = de.insert_action
                        if a is not None:
                            kw.update(ls_insert_handler=js_code("Lino.%s" % a.full_name()))
                            kw.update(ls_bbar_actions=[self.ext_renderer.a2btn(a)])
                    field = fields.HtmlBox(verbose_name=de.label)
                    field.name = de.__name__
                    field.help_text = de.help_text
                    field._return_type_for_method = de.slave_as_html_meth(self)
                    lh.add_store_field(field)
                    #~ kw.update(required=de.required) # e.g. lino.Home.UsersWithClients not visible for everybody
                    e = ext_elems.HtmlBoxElement(lh,field,**kw)
                    e.add_requirements(**de.required)
                    return e
            else:
                #~ field = fields.TextField(verbose_name=de.label)
                field = fields.HtmlBox(verbose_name=de.label)
                field.name = de.__name__
                field._return_type_for_method = de.slave_as_summary_meth(self,', ')
                lh.add_store_field(field)
                e = ext_elems.HtmlBoxElement(lh,field,**kw)
                return e
                
        if isinstance(de,fields.VirtualField):
            return self.create_vurt_element(lh,name,de,**kw)
            
        if callable(de):
            rt = getattr(de,'return_type',None)
            if rt is not None:
                return self.create_meth_element(lh,name,de,rt,**kw)
                
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
            msg += " Cannot handle %r" % de
        raise KeyError(msg)
        

    def create_vurt_element(self,lh,name,vf,**kw):
        #~ assert vf.get.func_code.co_argcount == 2, (name, vf.get.func_code.co_varnames)
        e = self.create_field_element(lh,vf,**kw)
        if not vf.is_enabled(lh):
            e.editable = False
        return e
        
    def create_meth_element(self,lh,name,meth,rt,**kw):
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
        e = self.create_field_element(lh,rt,**kw)
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
          
        
    def create_field_element(self,lh,field,**kw):
        #~ e = lh.main_class.field2elem(lh,field,**kw)
        e = ext_elems.field2elem(lh,field,**kw)
        assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,name)
        lh.add_store_field(e.field)
        return e
        #return FieldElement(self,field,**kw)
        

    #~ def save_window_config(self,a,wc):
        #~ self.window_configs[str(a)] = wc
        #~ #a.window_wrapper.config.update(wc=wc)
        #~ a.window_wrapper.update_config(wc)
        #~ f = open(self.window_configs_file,'wb')
        #~ pickle.dump(self.window_configs,f)
        #~ f.close()
        #~ logger.debug("save_window_config(%r) -> %s",wc,a)
        #~ self.build_site_cache()
        #~ lh = actors.get_actor(name).get_handle(self)
        #~ if lh is not None:
            #~ lh.window_wrapper.try_apply_window_config(wc)
        #~ self._response = None

    #~ def load_window_config(self,action,**kw):
        #~ wc = self.window_configs.get(str(action),None)
        #~ if wc is not None:
            #~ logger.debug("load_window_config(%r) -> %s",str(action),wc)
            #~ for n in ('x','y','width','height'):
                #~ if wc.get(n,0) is None:
                    #~ del wc[n]
                    #~ #raise Exception('invalid window configuration %r' % wc)
            #~ kw.update(**wc)
        #~ return kw

  
            
    #~ def quicklink(self,request,app_label,actor,**kw):
        #~ rpt = self.requested_report(request,app_label,actor)
        #~ return self.action_href(rpt.default_action,**kw)

    def setup_handle(self,h,ar):
        """
        ar is usually None, except for actors with dynamic handle
        """
        if h.actor.is_abstract():
            return
            
        #~ logger.info('20121010 ExtUI.setup_handle() %s',h.actor)
            
        if isinstance(h,tables.TableHandle):
            #~ if issubclass(h.actor,dbtables.Table):
            ll = layouts.ListLayout(
                h.actor.get_column_names(ar),
                h.actor,
                hidden_elements=h.actor.hidden_columns | h.actor.hidden_elements)
            #~ h.list_layout = layouts.ListLayoutHandle(h,ll,hidden_elements=h.actor.hidden_columns)
            h.list_layout = ll.get_layout_handle(self)
        else:
            h.list_layout = None
                
        if h.actor.parameters:
            h.params_layout_handle = h.actor.make_params_layout_handle(self)
            #~ logger.info("20120121 %s params_layout_handle is %s",h,h.params_layout_handle)
        
        h.store = ext_store.Store(h)
        
        #~ if h.store.param_fields:
            #~ logger.info("20120121 %s param_fields is %s",h,h.store.param_fields)
        
        #~ 20120614 if h.list_layout:
            #~ h.on_render = self.build_on_render(h.list_layout.main)
            
        #~ elif isinstance(h,dbtables.FrameHandle):
            #~ if issubclass(h.report,dbtables.EmptyTable):
                #~ h.store = ext_store.Store(h)
          
    def table2xhtml(self,ar,max_row_count=300):
        #~ doc = xghtml.Document(force_unicode(ar.get_title()))
        #~ t = doc.add_table()
        t = xghtml.Table()
        self.ar2html(ar,t,ar.data_iterator)
        # return xghtml.E.tostring(t.as_element())
        return t.as_element()
        
    def ar2html(self,ar,tble,data_iterator):
        """
        Render the given ActionRequest ar to html
        """
        tble.attrib.update(cellspacing="3px",bgcolor="#ffffff", width="100%")
        
        fields = ar.ah.store.list_fields
        grid = ar.ah.list_layout.main
        columns = grid.columns
        headers = [force_unicode(col.label or col.name) for col in columns]
        cellwidths = None
        
        if ar.request is not None:
            widths = [x for x in ar.request.REQUEST.getlist(ext_requests.URL_PARAM_WIDTHS)]
            col_names = [str(x) for x in ar.request.REQUEST.getlist(ext_requests.URL_PARAM_COLUMNS)]
            hiddens = [(x == 'true') for x in ar.request.REQUEST.getlist(ext_requests.URL_PARAM_HIDDENS)]
        
            if col_names:
                fields = []
                headers = []
                cellwidths = []
                columns = []
                for i,cn in enumerate(col_names):
                    col = None
                    for e in grid.columns:
                        if e.name == cn:
                            col = e
                            break
                    #~ col = ar.ah.list_layout._main.find_by_name(cn)
                    #~ col = ar.ah.list_layout._main.columns[ci]
                    if col is None:
                        #~ names = [e.name for e in ar.ah.list_layout._main.walk()]
                        raise Exception("No column named %r in %s" % (cn,grid.columns))
                    if not hiddens[i]:
                        columns.append(col)
                        fields.append(col.field._lino_atomizer)
                        headers.append(force_unicode(col.label or col.name))
                        cellwidths.append(widths[i])
          
        
        #~ for k,v in ar.actor.override_column_headers(ar):
            
        oh = ar.actor.override_column_headers(ar)
        if oh:
            for i,e in enumerate(columns):
                header = oh.get(e.name,None)
                if header is not None:
                    headers[i] = unicode(header)
            #~ print 20120507, oh, headers
          
        if ar.renderer.is_interactive:
            #~ print 20120901, ar.order_by
            for i,e in enumerate(columns):
                if e.sortable and ar.order_by != [e.name]:
                    kw = {ext_requests.URL_PARAM_SORT:e.name}
                    url = ar.renderer.get_request_url(ar,**kw)
                    if url is not None:
                        headers[i] = xghtml.E.a(headers[i],href=url)
        
        #~ cellattrs = dict(align="center",valign="middle",bgcolor="#eeeeee")
        cellattrs = dict(align="left",valign="top",bgcolor="#eeeeee")
        #~ cellattrs = dict()
        
        #~ headers = [x for x in ar.ah.store.headers2html(ar,fields,headers,**cellattrs)]        
        headers = [x for x in grid.headers2html(ar,columns,headers,**cellattrs)]        
        sums  = [fld.zero for fld in columns]
        #~ hr = tble.add_header_row(*headers,**cellattrs)
        if cellwidths:
            for i,td in enumerate(headers): 
                td.attrib.update(width=cellwidths[i])
        tble.head.append(xghtml.E.tr(*headers))
        #~ print 20120623, ar.actor
        recno = 0
        for row in data_iterator:
            recno += 1
            #~ cells = [x for x in ar.ah.store.row2html(ar,columns,row,sums,**cellattrs)]
            cells = [x for x in grid.row2html(ar,columns,row,sums,**cellattrs)]
            #~ print 20120623, cells
            #~ tble.add_body_row(*cells)
            tble.body.append(xghtml.E.tr(*cells))
            
        if recno == 0:
            tble.clear()
            tble.body.append(ar.no_data_text)
            
        
        if not ar.actor.hide_sums:
            has_sum = False
            for i in sums:
                if i:
                    has_sum = True
                    break
            if has_sum:
                cells = grid.sums2html(ar,columns,sums,**cellattrs)
                tble.body.append(xghtml.E.tr(*cells))
                #~ tble.add_body_row(*ar.ah.store.sums2html(ar,fields,sums,**cellattrs))
            
            
    def action_response(self,rv):
        """
        Builds a JSON response from given dict, 
        checking first whether there are only allowed keys 
        (defined in :attr:`ACTION_RESPONSES`)
        """
        rv = self.check_action_response(rv)
        return views.json_response(rv)
    

    def row_action_button(self,*args,**kw):
        """
        See :meth:`ExtRenderer.row_action_button`
        """
        return self.ext_renderer.row_action_button(*args,**kw)



