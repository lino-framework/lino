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

#~ from lxml import etree


#~ import Cheetah
from Cheetah.Template import Template as CheetahTemplate

from django.db import models
from django.db import IntegrityError
from django.conf import settings
from django.http import HttpResponse, Http404
from django.utils import functional
from django.utils.encoding import force_unicode
#~ from django.utils.functional import Promise

from django.template.loader import get_template
from django.template import RequestContext

from django.utils.translation import ugettext as _
from django.utils import simplejson as json
from django.utils import translation

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf.urls.defaults import patterns, url, include


import lino
from lino.ui.extjs3 import ext_elems
from lino.ui.extjs3 import ext_store
#~ from lino.ui.extjs3 import ext_windows
from lino.ui import requests as ext_requests

#~ from lino.ui import store as ext_store
from lino import dd
from lino.core import actions 
#~ from lino.core.actions import action2str
from lino.core import table
from lino.core import layouts
from lino.utils import tables
#~ from lino.utils.xmlgen import xhtml as xhg
from lino.core import fields
from lino.ui import base
from lino.core import actors
from lino.core.modeltools import makedirs_if_missing
from lino.core.modeltools import full_model_name
from lino.core.modeltools import is_devserver
    
from lino.utils import ucsv
from lino.utils import choosers
from lino.utils import babel
from lino.utils import choicelists
from lino.core import menus
from lino.utils import jsgen
from lino.utils.config import find_config_file
from lino.utils.jsgen import py2js, js_code, id2js
from lino.utils.xmlgen import html as xghtml
from lino.utils.config import make_dummy_messages_file

from lino.utils.jscompressor import JSCompressor
if False:
    jscompress = JSCompressor().compress
else:    
    def jscompress(s): return s
      
from lino.mixins import printable

from lino.core.modeltools import app_labels

from lino.utils.babel import LANGUAGE_CHOICES

from lino.utils.choicelists import DoYouLike, HowWell
STRENGTH_CHOICES = DoYouLike.get_choices()
KNOWLEDGE_CHOICES = HowWell.get_choices()


if settings.LINO.user_model:
    from lino.modlib.users import models as users

from lino.modlib.cal.utils import CalendarAction
    
from lino.ui.extjs3 import views

class HtmlRenderer(object):
    """
    Deserves more documentation.
    """
    def __init__(self,ui):
        self.ui = ui
        
    def href(self,url,text):
        return '<a href="%s">%s</a>' % (url,text)
        
    def href_button(self,url,text,title=None):
        if title:
            return '[<a href="%s" title="%s">%s</a>]' % (
                url,cgi.escape(unicode(title)),text)
        return '[<a href="%s">%s</a>]' % (url,text)
        
    def quick_add_buttons(self,ar):
        """
        Returns a HTML chunk that displays "quick add buttons"
        for the given :class:`action request <lino.core.table.TableRequest>`:
        a button  :guilabel:`[New]` followed possibly 
        (if the request has rows) by a :guilabel:`[Show last]` 
        and a :guilabel:`[Show all]` button.
        
        See also :doc:`/tickets/56`.
        
        """
        s = ''
        #~ params = dict(base_params=ar.request2kw(self))
        params = None
        after_show = ar.get_status(self)
        
        #~ params = ar.get_status(self)
        #~ after_show = dict()
        #~ a = ar.actor.get_action('insert')
        a = ar.actor.insert_action
        if a is not None:
            if a.get_action_permission(ar.get_user(),None,None):
                elem = ar.create_instance()
                after_show.update(data_record=views.elem2rec_insert(ar,ar.ah,elem))
                #~ after_show.update(record_id=-99999)
                # see tickets/56
                s += self.action_href_js(a,after_show,_("New"))
                after_show = ar.get_status(self)
        n = ar.get_total_count()
        #~ print 20120702, [o for o in ar]
        if n > 0:
            obj = ar.data_iterator[n-1]
            after_show.update(record_id=obj.pk)
            s += ' ' + self.action_href_js(
                ar.ah.actor.detail_action,after_show,_("Show Last"))
            #~ s += ' ' + self.href_to_request(ar,"[%s]" % unicode(_("Show All")))
            s += ' ' + self.href_to_request(ar,_("Show All"))
        #~ return '<p>%s</p>' % s
        return s
                
    def quick_upload_buttons(self,rr):
        """
        Returns a HTML chunk that displays "quick upload buttons":
        either one button :guilabel:`[Upload]` 
        (if the given :class:`TableTequest <lino.core.table.TableRequest>`
        has no rows)
        or two buttons :guilabel:`[Show]` and :guilabel:`[Edit]` 
        if it has one row.
        
        See also :doc:`/tickets/56`.
        
        """
        #~ params = dict(base_params=rr.request2kw(self))
        #~ params = rr.get_status(self)
        params = None
        after_show = rr.get_status(self)
        #~ after_show = dict(base_params=rr.get_status(self))
        #~ after_show = dict()
        if rr.get_total_count() == 0:
            #~ a = rr.actor.get_action('insert')
            a = rr.actor.insert_action
            if a is not None:
                elem = rr.create_instance()
                after_show.update(data_record=views.elem2rec_insert(rr,rr.ah,elem))
                #~ after_show.update(record_id=-99999)
                # see tickets/56
                return self.action_href_js(a,after_show,_("Upload"))
        if rr.get_total_count() == 1:
            obj = rr.data_iterator[0]
            s = ''
            s += ' [<a href="%s" target="_blank">show</a>]' % (self.ui.media_url(obj.file.name))
            if True:
                after_show.update(record_id=obj.pk)
                s += ' ' + self.action_href_js(rr.ah.actor.detail_action,after_show,_("Edit"))
            else:
                after_show.update(record_id=obj.pk)
                s += ' ' + self.action_href_http(rr.ah.actor.detail_action,_("Edit"),params,after_show)
            return s
        return '[?!]'

  
#~ class PdfRenderer(HtmlRenderer):
    #~ """
    #~ Deserves more documentation.
    #~ """
    #~ def href_to_request(self,rr,text=None):
        #~ return text or ("<b>%s</b>" % cgi.escape(force_unicode(rr.label)))
    #~ def href_to(self,obj,text=None):
        #~ text = text or cgi.escape(force_unicode(obj))
        #~ return "<b>%s</b>" % text
    #~ def instance_handler(self,obj):
        #~ return None
    #~ def request_handler(self,ar,*args,**kw):
        #~ return ''
        

#~ class ExtRendererPermalink(HtmlRenderer):
    #~ """
    #~ Deserves more documentation.
    #~ """
    #~ def href_to_request(self,rr,text=None):
        #~ """
        #~ Returns a HTML chunk with a clickable link to 
        #~ the given :class:`TableTequest <lino.core.table.TableRequest>`.
        #~ """
        #~ return self.href(
            #~ self.get_request_url(rr),
            #~ text or cgi.escape(force_unicode(rr.label)))
    #~ def href_to(self,obj,text=None):
        #~ """
        #~ Returns a HTML chunk with a clickable link to 
        #~ the given model instance.
        #~ """
        #~ return self.href(
            #~ self.get_detail_url(obj),
            #~ text or cgi.escape(force_unicode(obj)))
            
class ExtRenderer(HtmlRenderer):
    """
    Deserves more documentation.
    """
    def href_to(self,ar,obj,text=None):
        h = self.instance_handler(ar,obj)
        if h is None:
            return cgi.escape(force_unicode(obj))
        url = self.js2url(h)
        return self.href(url,text or cgi.escape(force_unicode(obj)))

    def py2js_converter(self,v):
        """
        Additional converting logic for serializing Python values to json.
        """
        if v is LANGUAGE_CHOICES:
            return js_code('LANGUAGE_CHOICES')
        if v is STRENGTH_CHOICES:
            return js_code('STRENGTH_CHOICES')
        if v is KNOWLEDGE_CHOICES:
            return js_code('KNOWLEDGE_CHOICES')
        if isinstance(v,choicelists.Choice):
            """
            This is special. We don't render the text but the value. 
            """
            return v.value
        #~ if isinstance(v,babel.BabelText):
            #~ return unicode(v)
        #~ if isinstance(v,Promise):
            #~ return unicode(v)
        if isinstance(v,dd.Model):
            return v.pk
        if isinstance(v,Exception):
            return unicode(v)
        if isinstance(v,menus.Menu):
            if v.parent is None:
                return v.items
                #kw.update(region='north',height=27,items=v.items)
                #return py2js(kw)
            return dict(text=prepare_label(v),menu=dict(items=v.items))
        if isinstance(v,menus.MenuItem):
            if v.params is not None:
                ar = v.action.actor.request(self.ui,None,v.action,**v.params)
                return handler_item(v,self.request_handler(ar),v.action.help_text)
                #~ return dict(text=prepare_label(v),handler=js_code(handler))
            if v.action:
                if True:
                    #~ handler = self.action_call(v.action,params=v.params)
                    return handler_item(v,self.action_call(None,v.action),v.action.help_text)
                    #~ handler = "function(){%s}" % self.action_call(
                        #~ v.action,None,v.params)
                    #~ return dict(text=prepare_label(v),handler=js_code(handler))
                else:
                    url = self.action_url_http(v.action)
            #~ elif v.params is not None:
                #~ ar = v.action.actor.request(self,None,v.action,**v.params)
                #~ url = self.get_request_url(ar)
            elif v.href is not None:
                url = v.href
            elif v.request is not None:
                url = self.get_request_url(v.request)
            elif v.instance is not None:
                h = self.instance_handler(None,v.instance)
                assert h is not None
                return handler_item(v,h,None)
                #~ handler = "function(){%s}" % self.instance_handler(v.instance)
                #~ return dict(text=prepare_label(v),handler=js_code(handler))
              
                #~ url = self.get_detail_url(v.instance,an='detail')
                #~ url = self.get_detail_url(v.instance)
            else:
                # a separator
                #~ return dict(text=v.label)
                return v.label
                #~ url = self.build_url('api',v.action.actor.app_label,v.action.actor.__name__,fmt=v.action.name)
            if v.parent.parent is None:
                # special case for href items in main menubar
                return dict(
                  xtype='button',text=prepare_label(v),
                  #~ handler=js_code("function() { window.location='%s'; }" % url))
                  handler=js_code("function() { location.replace('%s'); }" % url))
            return dict(text=prepare_label(v),href=url)
        return v
        
    def action_call(self,request,a,after_show={}):
        if a.opens_a_window:
            if request and request.subst_user:
                after_show[ext_requests.URL_PARAM_SUBST_USER] = request.subst_user
            if isinstance(a,actions.ShowEmptyTable):
                after_show.update(record_id=-99998)
            if after_show:
                return "Lino.%s.run(%s)" % (a,py2js(after_show))
            return "Lino.%s.run()" % a
        return "?"

    def js2url(self,js):
        js = cgi.escape(js)
        js = js.replace('"','&quot;')
        return 'javascript:' + js
        
    #~ def action_url_js(self,a,after_show):
        #~ return self.js2url(self.action_call(a,after_show))

    def action_href_js(self,a,after_show={},label=None):
        """
        Return a HTML chunk for a button that will execute this 
        action using a *Javascript* link to this action.
        """
        label = cgi.escape(force_unicode(label or a.get_button_label()))
        #~ url = self.action_url_js(a,after_show)
        url = self.js2url(self.action_call(None,a,after_show))
        return self.href_button(url,label,a.help_text)
        
    def action_button(self,obj,ar,a,label=None):
        if a.opens_a_window:
            after_show = ar.get_status(self)
            after_show.update(record_id=obj.pk)
            return self.action_href_js(a,after_show,label or a.label)
        return self.row_action_button(obj,ar.request,a,label)
        
    def row_action_button(self,obj,request,a,label=None):
        """
        Return a HTML fragment that displays a button-like link 
        which runs the action when clicked.
        """
        label = cgi.escape(unicode(label or a.label))
        url = self.js2url(
            'Lino.%s(%r,%s)' % (
                a,str(request.requesting_panel),
                py2js(obj.pk)))
        return self.href_button(url,label,a.help_text)
        
    def instance_handler(self,ar,obj):
        #~ a = obj.__class__._lino_default_table.get_action('detail')
        a = getattr(obj,'_detail_action',None)
        if a is None:
        #~ if ar is not None and ar.actor.is_valid_row(obj):
            #~ a = ar.actor.detail_action
        #~ else:
            a = obj.__class__._lino_default_table.detail_action
        if a is not None:
            if ar is None or a.get_action_permission(ar.get_user(),obj,None):
                #~ raise Exception("No detail action for %s" % obj.__class__._lino_default_table)
                return self.action_call(None,a,dict(record_id=obj.pk))
        
    def request_handler(self,ar,*args,**kw):
        #~ bp = rr.request2kw(self.ui,**kw)
        st = ar.get_status(self.ui,**kw)
        return self.action_call(ar.request,ar.action,after_show=st)
        
    def href_to_request(self,rr,text=None):
        url = self.js2url(self.request_handler(rr))
        #~ if 'Lino.pcsw.MyPersonsByGroup' in url:
        #~ print 20120618, url
        return self.href(url,text or cgi.escape(force_unicode(rr.label)))
        #~ return self.href_button(url,text or cgi.escape(force_unicode(rr.label)))
            
    def action_href_http(self,a,label=None,**params):
        """
        Return a HTML chunk for a button that will execute 
        this action using a *HTTP* link to this action.
        """
        label = cgi.escape(force_unicode(label or a.get_button_label()))
        return '[<a href="%s">%s</a>]' % (self.action_url_http(a,**params),label)
        
    #~ def get_action_url(self,action,*args,**kw):
    def action_url_http(self,action,*args,**kw):
        #~ if not action is action.actor.default_action:
        if action != action.actor.default_action:
            kw.update(an=action.name)
        return self.build_url("api",action.actor.app_label,action.actor.__name__,*args,**kw)
            
    def get_actor_url(self,actor,*args,**kw):
        return self.build_url("api",actor.app_label,actor.__name__,*args,**kw)
        
    def get_request_url(self,ar,*args,**kw):
        """
        Called from ActionRequest.absolute_url() used in Team.eml.html
        
        http://127.0.0.1:8000/api/cal/MyPendingInvitations?base_params=%7B%7D
        http://127.0.0.1:8000/api/cal/MyPendingInvitations
        
        """
        kw = ar.get_status(self,**kw)
        if not kw['base_params']:
            del kw['base_params']
        #~ kw = self.request2kw(rr,**kw)
        return ar.ui.build_url('api',ar.actor.app_label,ar.actor.__name__,*args,**kw)
        
    def get_detail_url(self,obj,*args,**kw):
        #~ rpt = obj._lino_default_table
        #~ return self.build_url('api',rpt.app_label,rpt.__name__,str(obj.pk),*args,**kw)
        return self.build_url('api',obj._meta.app_label,obj.__class__.__name__,str(obj.pk),*args,**kw)
        
    #~ def request_href_js(self,rr,text=None):
        #~ url = self.request_handler(rr)
        #~ return self.href(url,text or cgi.escape(force_unicode(rr.label)))
        
    
            





def prepare_label(mi):
    return mi.label
    """
    The original idea doesn't work any more with lazy translation.
    See :doc:`/blog/2011/1112`
    """
    #~ label = unicode(mi.label) # trigger translation
    #~ n = label.find(mi.HOTKEY_MARKER)
    #~ if n != -1:
        #~ label = label.replace(mi.HOTKEY_MARKER,'')
        #~ #label=label[:n] + '<u>' + label[n] + '</u>' + label[n+1:]
    #~ return label
    
def handler_item(mi,handler,help_text):
    handler = "function(){%s}" % handler
    #~ d = dict(text=prepare_label(mi),handler=js_code(handler),tooltip="Foo")
    d = dict(text=prepare_label(mi),handler=js_code(handler))
    if settings.LINO.use_quicktips and help_text:
        d.update(listeners=dict(render=js_code(
          "Lino.quicktip_renderer(%s,%s)" % (py2js('Foo'),py2js(help_text)))
        ))
    
    return d


#~ def element_name(elem):
    #~ return u"%s (#%s in %s.%s)" % (elem,elem.pk,elem._meta.app_label,elem.__class__.__name__)


def parse_bool(s):
    return s == 'true'
    
def parse_int(s,default=None):
    if s is None: return None
    return int(s)


    
class ExtUI(base.UI):
    """The central instance of Lino's ExtJS3 User Interface.
    """
    _handle_attr_name = '_extjs3_handle'
    #~ _response = None
    name = 'extjs3'
    verbose_name = "ExtJS with Windows"
    #~ Panel = ext_elems.Panel
    
    
    #~ USE_WINDOWS = False  # If you change this, then change also Lino.USE_WINDOWS in lino.js

    #~ def __init__(self,*args,**kw):
    def __init__(self):
        #~ raise Exception("20120614")
        #~ self.pdf_renderer = PdfRenderer(self) # 20120624
        self.ext_renderer = ExtRenderer(self)
        self.reserved_names = [getattr(ext_requests,n) for n in ext_requests.URL_PARAMS]
        jsgen.register_converter(self.ext_renderer.py2js_converter)
        #~ self.window_configs = {}
        #~ if os.path.exists(self.window_configs_file):
            #~ logger.info("Loading %s...",self.window_configs_file)
            #~ wc = pickle.load(open(self.window_configs_file,"rU"))
            #~ #logger.debug("  -> %r",wc)
            #~ if type(wc) is dict:
                #~ self.window_configs = wc
        #~ else:
            #~ logger.warning("window_configs_file %s not found",self.window_configs_file)
            
        #~ base.UI.__init__(self,*args,**kw) # will create a.window_wrapper for all actions
        base.UI.__init__(self) 
        
        #~ self.welcome_template = get_template('welcome.html')
        
        #~ from django.template.loader import find_template
        #~ source, origin = find_template('welcome.html')
        #~ print source, origin
        
        if False:
            fn = find_config_file('welcome.html')
            logger.info("Using welcome template %s",fn)
            self.welcome_template = CheetahTemplate(file(fn).read())
        
        #~ self.build_site_cache()
            
        #~ self.generate_linolib_messages()
        
    def create_layout_element(self,lh,name,**kw):
        if False: 
            de = lh.get_data_elem(name)
        else:
            try:
                de = lh.get_data_elem(name)
            except Exception, e:
                de = None
                name += " (" + str(e) + ")"
            
        #~ if isinstance(de,fields.FieldSet):
            #~ # return lh.desc2elem(ext_elems.FieldSetPanel,name,de.desc)
            #~ return lh.desc2elem(name,de.desc,**kw)
            
        #~ if isinstance(de,fields.NullField):
            #~ return None
            
        if isinstance(de,fields.DummyField):
            return None
        if isinstance(de,fields.Constant):
            return ext_elems.ConstantElement(lh,de,**kw)
            
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
            
        if isinstance(de,fields.LinkedForeignKey):
            de.primary_key = False # for ext_store.Store()
            lh.add_store_field(de)
            return ext_elems.LinkedForeignKeyElement(lh,de,**kw)
            
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
                  js_code("Lino.show_in_own_window_button(Lino.%s)" % de.default_action)
                  #~ js_code("Lino.report_window_button(Lino.%s)" % de.default_action)
                  #~ js_code("Lino.report_window_button(ww,Lino.%s)" % de.default_action)
                ])
                if de.slave_grid_format == 'grid':
                    if not de.parameters:
                        kw.update(hide_top_toolbar=True)
                    e = ext_elems.GridElement(lh,name,de,**kw)
                    return e
                elif de.slave_grid_format == 'summary':
                    # a Table in a DetailWindow, displayed as a summary in a HtmlBox 
                    o = dict(drop_zone="FooBar")
                    #~ a = de.get_action('insert')
                    a = de.insert_action
                    if a is not None:
                        kw.update(ls_insert_handler=js_code("Lino.%s" % a))
                        kw.update(ls_bbar_actions=[self.a2btn(a)])
                    #~ else:
                        #~ print 20120619, de, 'has no insert_action'
                    field = fields.HtmlBox(verbose_name=de.label,**o)
                    field.name = de.__name__
                    field._return_type_for_method = de.slave_as_summary_meth(self,'<br>')
                    lh.add_store_field(field)
                    e = ext_elems.HtmlBoxElement(lh,field,**kw)
                    return e
                    
                elif de.slave_grid_format == 'html':
                    #~ a = de.get_action('insert')
                    a = de.insert_action
                    if a is not None:
                        kw.update(ls_insert_handler=js_code("Lino.%s" % a))
                        kw.update(ls_bbar_actions=[self.a2btn(a)])
                    field = fields.HtmlBox(verbose_name=de.label)
                    field.name = de.__name__
                    field._return_type_for_method = de.slave_as_html_meth(self)
                    lh.add_store_field(field)
                    e = ext_elems.HtmlBoxElement(lh,field,**kw)
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
            msg = "Unknown element %r referred in layout %s of %s." % (
                name,lh.layout,lh.rh.actor)
            l = [de.name for de in lh.rh.actor.wildcard_data_elems()]
            model = getattr(lh.rh.actor,'model',None) # VirtualTables don't have a model
            if getattr(model,'_lino_slaves',None):
                l += [str(rpt) for rpt in model._lino_slaves.values()]
            msg += " Possible names are %s." % ', '.join(l)
        else:
            msg = "Unknown element %r referred in layout %s." % (
                name,lh.layout)
            msg += "Cannot handle %r" % de
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

  
    def get_urls(self):
        rx = '^'
        urlpatterns = patterns('',
            #~ (rx+'$', self.index_view),
            (rx+'$', views.Index.as_view()),
            #~ (rx+r'grid_config/(?P<app_label>\w+)/(?P<actor>\w+)$', self.grid_config_view),
            (rx+r'api/main_html$', views.MainHtml.as_view()),
            (rx+r'grid_config/(?P<app_label>\w+)/(?P<actor>\w+)$', views.GridConfig.as_view()),
            #~ (rx+r'detail_config/(?P<app_label>\w+)/(?P<actor>\w+)$', self.detail_config_view),
            #~ (rx+r'api/(?P<app_label>\w+)/(?P<actor>\w+)$', self.api_list_view),
            (rx+r'api/(?P<app_label>\w+)/(?P<actor>\w+)$', views.ApiList.as_view()),
            
            #~ (rx+r'api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$', self.api_element_view),
            (rx+r'api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$', views.ApiElement.as_view()),
            #~ (rx+r'restful/(?P<app_label>\w+)/(?P<actor>\w+)$', self.restful_view),
            (rx+r'restful/(?P<app_label>\w+)/(?P<actor>\w+)$', views.Restful.as_view()),
            #~ (rx+r'restful/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$', self.restful_view),
            (rx+r'restful/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$', views.Restful.as_view()),
            #~ (rx+r'choices/(?P<app_label>\w+)/(?P<rptname>\w+)$', self.choices_view),
            (rx+r'choices/(?P<app_label>\w+)/(?P<rptname>\w+)$', views.Choices.as_view()),
            (rx+r'choices/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<fldname>\w+)$', views.Choices.as_view()),
        )
        if settings.LINO.use_tinymce:
            #~ self.templates_view
            urlpatterns += patterns('',
                (rx+r'templates/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>\w+)/(?P<fldname>\w+)$', 
                    views.Templates.as_view()),
                (rx+r'templates/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>\w+)/(?P<fldname>\w+)/(?P<tplname>\w+)$', 
                    views.Templates.as_view()),
            )

        from os.path import exists, join, abspath, dirname
        
        logger.info("Checking /media URLs ")
        prefix = settings.MEDIA_URL[1:]
        assert prefix.endswith('/')
        
        def setup_media_link(short_name,attr_name=None,source=None):
            target = join(settings.MEDIA_ROOT,short_name)
            if exists(target):
                return
            #~ if settings.LINO.extjs_root:
            if attr_name:
                source = getattr(settings.LINO,attr_name)
                if not source:
                    raise Exception(
                      "%s does not exist and LINO.%s is not set." % (
                      target,attr_name))
            if not exists(source):
                raise Exception("LINO.%s (%s) does not exist" % (attr_name,p))
            if is_devserver():
                #~ urlpatterns += patterns('django.views.static',
                urlpatterns.extend(patterns('django.views.static',
                (r'^%s%s/(?P<path>.*)$' % (prefix,short_name), 
                    'serve', {
                    'document_root': source,
                    'show_indexes': False })))
            else:
                logger.info("Setting up symlink %s -> %s.",target,source)
                symlink = getattr(os,'symlink',None)
                if symlink is not None:
                    symlink(source,target)
            
        setup_media_link('extjs','extjs_root')
        if settings.LINO.use_extensible:
            setup_media_link('extensible','extensible_root')
        if settings.LINO.use_tinymce:
            setup_media_link('tinymce','tinymce_root')
            
        #~ lino_root = join(settings.LINO.project_dir,'using','lino')
        #~ if not exists(lino_root):
            #~ lino_root = 
        #~ setup_media_link('lino',source=join(lino_root,'media'))
        setup_media_link('lino',source=join(dirname(lino.__file__),'..','media'))

        if is_devserver():
            urlpatterns += patterns('django.views.static',
                (r'^%s(?P<path>.*)$' % prefix, 'serve', 
                  { 'document_root': settings.MEDIA_ROOT, 
                    'show_indexes': True }),
            )

        return urlpatterns

    def html_page(self,*args,**kw):
        return '\n'.join([ln for ln in self.html_page_lines(*args,**kw)])
        
    def html_page_lines(self,request,title=None,on_ready='',**kw):
        """Generates the lines of Lino's HTML reponse.
        """
        yield '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
        yield '<html><head>'
        yield '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
        yield '<title id="title">%s</title>' % settings.LINO.title
        
        def stylesheet(url):
            url = self.media_url() + url
            return '<link rel="stylesheet" type="text/css" href="%s" />' % url
            
        #~ yield '<link rel="stylesheet" type="text/css" href="%s/extjs/resources/css/ext-all.css" />' % self.media_url()
        yield stylesheet('/extjs/resources/css/ext-all.css')
        #~ yield '<!-- overrides to base library -->'
        if settings.LINO.use_extensible:
            yield stylesheet("/extensible/resources/css/extensible-all.css")
          
        if settings.LINO.use_vinylfox:
            p = self.media_url() + '/lino/vinylfox/'
            yield '<link rel="stylesheet" type="text/css" href="%sresources/css/htmleditorplugins.css" />' % p
          
        if settings.LINO.use_filterRow:
            p = self.media_url() + '/lino/filterRow'
            yield '<link rel="stylesheet" type="text/css" href="%s/filterRow.css" />' % p
            
        if settings.LINO.use_gridfilters:
            yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/statusbar/css/statusbar.css" />' % self.media_url() 
            yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/gridfilters/css/GridFilters.css" />' % self.media_url() 
            yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/gridfilters/css/RangeMenu.css" />' % self.media_url() 
            
        yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/fileuploadfield/css/fileuploadfield.css" />' % self.media_url() 
        
        yield '<link rel="stylesheet" type="text/css" href="%s/lino/extjs/lino.css">' % self.media_url()
        
        if settings.LINO.use_awesome_uploader:
            yield '<link rel="stylesheet" type="text/css" href="%s/lino/AwesomeUploader/AwesomeUploader.css">' % self.media_url()
            yield '<link rel="stylesheet" type="text/css" href="%s/lino/AwesomeUploader/AwesomeUploader Progress Bar.css">' % self.media_url()
         
        def javascript(url):
            url = self.media_url() + url
            return '<script type="text/javascript" src="%s"></script>' % url
            
        if settings.DEBUG:
            yield javascript('/extjs/adapter/ext/ext-base-debug.js')
            yield javascript('/extjs/ext-all-debug.js')
            if settings.LINO.use_extensible:
                yield javascript('/extensible/extensible-all-debug.js')
        else:
            yield javascript('/extjs/adapter/ext/ext-base.js')
            yield javascript('/extjs/ext-all.js')
            if settings.LINO.use_extensible:
                yield javascript('/extensible/extensible-all.js')
                
        if translation.get_language() != 'en':
            yield javascript('/extjs/src/locale/ext-lang-'+translation.get_language()+'.js')
            if settings.LINO.use_extensible:
                yield javascript('/extensible/src/locale/extensible-lang-'+translation.get_language()+'.js')
            
        if False:
            yield '<script type="text/javascript" src="%s/extjs/Exporter-all.js"></script>' % self.media_url() 
            
        if False:
            yield '<script type="text/javascript" src="%s/extjs/examples/ux/CheckColumn.js"></script>' % self.media_url() 

        yield '<script type="text/javascript" src="%s/extjs/examples/ux/statusbar/StatusBar.js"></script>' % self.media_url()
        
        if settings.LINO.use_tinymce:
            p = self.media_url() + '/tinymce'
            #~ yield '<script type="text/javascript" src="Ext.ux.form.FileUploadField.js"></script>'
            yield '<script type="text/javascript" src="%s/tiny_mce.js"></script>' % p
            yield '<script type="text/javascript" src="%s/lino/tinymce/Ext.ux.TinyMCE.js"></script>' % self.media_url()
            yield '''<script language="javascript" type="text/javascript">
tinymce.init({
        theme : "advanced"
        // , mode : "textareas"
});
</script>'''

        yield '<script type="text/javascript" src="%s/lino/extjs/Ext.ux.form.DateTime.js"></script>' % self.media_url()

        if settings.LINO.use_gridfilters:
            p = self.media_url() + '/extjs/examples/ux/gridfilters'
            #~ yield '<script type="text/javascript" src="%s/extjs/examples/ux/RowEditor.js"></script>' % self.media_url()
            yield '<script type="text/javascript" src="%s/menu/RangeMenu.js"></script>' % p
            yield '<script type="text/javascript" src="%s/menu/ListMenu.js"></script>' % p
            yield '<script type="text/javascript" src="%s/GridFilters.js"></script>' % p
            yield '<script type="text/javascript" src="%s/filter/Filter.js"></script>' % p
            yield '<script type="text/javascript" src="%s/filter/StringFilter.js"></script>' % p
            yield '<script type="text/javascript" src="%s/filter/DateFilter.js"></script>' % p
            yield '<script type="text/javascript" src="%s/filter/ListFilter.js"></script>' % p
            yield '<script type="text/javascript" src="%s/filter/NumericFilter.js"></script>' % p
            yield '<script type="text/javascript" src="%s/filter/BooleanFilter.js"></script>' % p
            
        yield '<script type="text/javascript" src="%s/extjs/examples/ux/fileuploadfield/FileUploadField.js"></script>' % self.media_url()
        
        if settings.LINO.use_filterRow:
            p = self.media_url() + '/lino/filterRow'
            yield '<script type="text/javascript" src="%s/filterRow.js"></script>' % p
            
        if settings.LINO.use_vinylfox:
            p = self.media_url() + '/lino/vinylfox/src/Ext.ux.form.HtmlEditor'
            #~ yield '<script type="text/javascript" src="Ext.ux.form.FileUploadField.js"></script>'
            yield '<script type="text/javascript" src="%s.MidasCommand.js"></script>' % p
            yield '<script type="text/javascript" src="%s.Divider.js"></script>' % p
            yield '<script type="text/javascript" src="%s.HR.js"></script>' % p
            yield '<script type="text/javascript" src="%s.Image.js"></script>' % p
            yield '<script type="text/javascript" src="%s.RemoveFormat.js"></script>' % p
            yield '<script type="text/javascript" src="%s.IndentOutdent.js"></script>' % p
            yield '<script type="text/javascript" src="%s.SubSuperScript.js"></script>' % p
            yield '<script type="text/javascript" src="%s.FindAndReplace.js"></script>' % p
            yield '<script type="text/javascript" src="%s.Table.js"></script>' % p
            yield '<script type="text/javascript" src="%s.Word.js"></script>' % p
            yield '<script type="text/javascript" src="%s.Link.js"></script>' % p
            yield '<script type="text/javascript" src="%s.SpecialCharacters.js"></script>' % p
            yield '<script type="text/javascript" src="%s.UndoRedo.js"></script>' % p
            yield '<script type="text/javascript" src="%s.Heading.js"></script>' % p
            yield '<script type="text/javascript" src="%s.Plugins.js"></script>' % p
            
        if settings.LINO.use_awesome_uploader:
            p = self.media_url() + '/lino/AwesomeUploader/'
            #~ yield '<script type="text/javascript" src="Ext.ux.form.FileUploadField.js"></script>'
            yield '<script type="text/javascript" src="%s/Ext.ux.XHRUpload.js"></script>' % p
            yield '<script type="text/javascript" src="%s/swfupload.js"></script>' % p
            yield '<!-- <script type="text/javascript" src="%s/swfupload.swfobject.js"></script> -->' % p
            yield '<script type="text/javascript" src="%s/Ext.ux.AwesomeUploaderLocalization.js"></script>' % p
            yield '<script type="text/javascript" src="%s/Ext.ux.AwesomeUploader.js"></script>' % p

        #~ yield '<!-- overrides to library -->'
        #~ yield '<script type="text/javascript" src="%slino/extjs/lino.js"></script>' % self.media_url()
        
        
        """
        Acting as another user will not give you the access permissions of that user.
        A secretary who has authority to act as her boss in order to manage his calendar
        should not also see e.g. statistic reports to which she has no access.
        For system admins it is different: 
        when a system admin acts as another user, 
        he inherits this user's access permissions. 
        System admins use this feature to test the permissions of other users.
        """
        user = request.user
        if user.profile.level >= dd.UserLevels.admin:
            if request.subst_user:
                user = request.subst_user
        if not settings.LINO.build_js_cache_on_startup:
            self.build_js_cache_for_user(user)
        yield '<script type="text/javascript" src="%s"></script>' % (
            self.media_url(*self.lino_js_parts(user)))
            

        #~ yield '<!-- page specific -->'
        yield '<script type="text/javascript">'

        yield 'Ext.onReady(function(){'
        
        #~ yield "console.time('onReady');"
        
        if request.user.authenticated:
          
            if request.subst_user:
                #~ yield "Lino.subst_user = %s;" % py2js(request.subst_user.id)
                yield "Lino.set_subst_user(%s,%s);" % (
                    py2js(request.subst_user.id),
                    py2js(unicode(request.subst_user)))
                user_text = unicode(request.user) + " (" + _("as") + " " + unicode(request.subst_user) + ")"
            else:
                #~ yield "Lino.subst_user = null;"
                yield "Lino.set_subst_user(null);"
                user_text = unicode(request.user) 
                
            user = request.user
            
            yield "Lino.user = %s;" % py2js(dict(id=user.id,name=unicode(user)))
            
            if user.profile.level >= dd.UserLevels.admin:
                authorities = [(u.id,unicode(u)) 
                    for u in users.User.objects.exclude(profile=dd.UserProfiles.blank_item)]
            else:
                authorities = [(a.user.id,unicode(a.user)) 
                    for a in users.Authority.objects.filter(authorized=user)]
            
            #~ handler = self.ext_renderer.instance_handler(user)
            a = users.MySettings.default_action
            handler = self.ext_renderer.action_call(None,a,dict(record_id=user.pk))
            handler = "function(){%s}" % handler
            if len(authorities):
                mysettings = dict(text=_("My settings"),handler=js_code(handler))
                #~ act_as = [
                    #~ dict(text=unicode(u),handler=js_code("function(){Lino.set_subst_user(%s)}" % i)) 
                        #~ for i,u in user.get_received_mandates()]
                act_as = [
                    dict(text=t,handler=js_code("function(){Lino.set_subst_user(%s,%s)}" % (v,py2js(t)))) 
                        for v,t in authorities]
                        #~ for v,t in user.get_received_mandates()]
                act_as.insert(0,dict(
                    text=_("Myself"),
                    handler=js_code("function(){Lino.set_subst_user(null)}")))
                act_as = dict(text=_("Act as..."),menu=dict(items=act_as))
                login_menu = dict(
                    text=user_text,
                    menu=dict(items=[act_as,mysettings]))
            else:
                login_menu = dict(text=user_text,handler=js_code(handler))
                
            yield "Lino.login_menu = %s;" % py2js(login_menu)
            yield "Lino.main_menu = Lino.main_menu.concat(['->',Lino.login_menu]);"
                
        
        #~ yield "Lino.load_mask = new Ext.LoadMask(Ext.getBody(), {msg:'Immer mit der Ruhe...'});"
          
        main=dict(
          id="main_area",
          xtype='container',
          region="center",
          autoScroll=True,
          layout='fit',
          html=self.get_main_html(request),
        )
        
        win = dict(
          layout='fit',
          #~ maximized=True,
          items=main,
          #~ closable=False,
          bbar=dict(xtype='toolbar',items=js_code('Lino.status_bar')),
          #~ title=self.site.title,
          tbar=js_code('Lino.main_menu'),
          #~ tbar=settings.LINO.get_site_menu(self,request.user),
        )
        jsgen.set_for_user(request.user)
        for ln in jsgen.declare_vars(win):
            yield ln
        #~ yield '  new Ext.Viewport({layout:"fit",items:%s}).render("body");' % py2js(win)
        yield '  Lino.viewport = new Lino.Viewport({items:%s});' % py2js(win)
        yield '  Lino.viewport.render("body");'
            
        #~ yield '  Ext.QuickTips.init();'
        
        yield on_ready
        #~ for ln in on_ready:
            #~ yield ln
        
        #~ yield "console.timeEnd('onReady');"
        yield "}); // end of onReady()"
        yield '</script></head><body>'
        if settings.LINO.use_davlink:
            yield '<applet name="DavLink" code="davlink.DavLink.class"'
            yield '        archive="%s/lino/applets/DavLink.jar"' % self.media_url()
            yield '        width="1" height="1"></applet>'
            # Note: The value of the ARCHIVE attribute is a URL of a JAR file.
        yield '<div id="body"></div>'
        #~ yield '<div id="tbar"/>'
        #~ yield '<div id="main"/>'
        #~ yield '<div id="bbar"/>'
        #~ yield '<div id="konsole"></div>'
        yield "</body></html>"
        
    def get_main_html(self,request):
        html = settings.LINO.get_main_html(request)
        if html:
            html = '<div class="htmlText">%s</div>' % html
        return html
            
    def linolib_intro(self):
        """
        Called from :xfile:`linolib.js`.
        """
        def fn():
            yield """// lino.js --- generated %s by Lino version %s.""" % (time.ctime(),lino.__version__)
            #~ // $site.title ($lino.welcome_text())
            yield "Ext.BLANK_IMAGE_URL = '%s/extjs/resources/images/default/s.gif';" % self.media_url()
            yield "LANGUAGE_CHOICES = %s;" % py2js(list(LANGUAGE_CHOICES))
            # TODO: replace the following lines by a generic method for all ChoiceLists
            yield "STRENGTH_CHOICES = %s;" % py2js(list(STRENGTH_CHOICES))
            yield "KNOWLEDGE_CHOICES = %s;" % py2js(list(KNOWLEDGE_CHOICES))
            yield "MEDIA_URL = %r;" % (self.media_url())
            #~ yield "ROOT_URL = %r;" % settings.LINO.root_url
            yield "ROOT_URL = %r;" % self.root_url
            
            #~ yield "API_URL = %r;" % self.build_url('api')
            #~ yield "TEMPLATES_URL = %r;" % self.build_url('templates')
            #~ yield "Lino.status_bar = new Ext.ux.StatusBar({defaultText:'Lino version %s.'});" % lino.__version__
        
        #~ return '\n'.join([ln for ln in fn()])
        return '\n'.join(fn())



    def parse_params(self,rh,request):
        return rh.store.parse_params(request)
        
    #~ def rest2form(self,request,rh,data):
        #~ d = dict()
        #~ logger.info('20120118 rest2form %r', data)
        #~ for i,f in enumerate(rh.store.list_fields):
        #~ return d
        
    def unused_error_response(self,e=None,message=None,**kw):
        kw.update(success=False)
        #~ if e is not None:
        if isinstance(e,Exception):
            if False: # useful when debugging, but otherwise rather disturbing
                logger.exception(e)
            if hasattr(e,'message_dict'):
                kw.update(errors=e.message_dict)
        #~ kw.update(alert_msg=cgi.escape(message_prefix+unicode(e)))
        #~ 20120628b kw.update(alert=True)
        #~ kw.update(message=message)
        if message is None:
            message = unicode(e)
        kw.update(message=cgi.escape(message))
        #~ kw.update(message=message_prefix+unicode(e))
        #~ logger.debug('error_response %s',kw)
        return self.action_response(kw)
    

    def action_response(self,kw):
        """
        Builds a JSON response from given dict, 
        checking first whether there are only allowed keys 
        (defined in :attr:`ACTION_RESPONSES`)
        """
        self.check_action_response(kw)
        return views.json_response(kw)
            
    def lino_js_parts(self,user):
    #~ def js_cache_name(self):
        #~ return ('cache','js','site.js')
        #~ return ('cache','js','lino.js')
        #~ return ('cache','js','lino_'+user.get_profile()+'_'+translation.get_language()+'.js')
        #~ return ('cache','js','lino_'+(user.profile.name or user.username)+'_'+translation.get_language()+'.js')
        return ('cache','js','lino_' + user.profile.value + '_' + translation.get_language()+'.js')
        
    def build_site_cache(self,force=False):
        """
        Build the site cache files under `/media/cache`,
        especially the :xfile:`lino*.js` files, one per user profile and language.
        """
        if settings.LINO.never_build_site_cache:
            logger.info("Not building site cache because `settings.LINO.never_build_site_cache` is True")
            return 
        if not os.path.isdir(settings.MEDIA_ROOT):
            logger.warning("Not building site cache because "+
            "directory '%s' (settings.MEDIA_ROOT) does not exist.", 
            settings.MEDIA_ROOT)
            return
        
        started = time.time()
        
        settings.LINO.on_each_app('setup_site_cache',force)
        
        makedirs_if_missing(os.path.join(settings.MEDIA_ROOT,'upload'))
        makedirs_if_missing(os.path.join(settings.MEDIA_ROOT,'webdav'))
        
        if force or settings.LINO.build_js_cache_on_startup:
            count = 0
            langs = babel.AVAILABLE_LANGUAGES
            qs = users.User.objects.exclude(profile=dd.UserProfiles.blank_item) # .exclude(level='')
            for lang in langs:
                babel.set_language(lang)
                for user in qs:
                    count += self.build_js_cache_for_user(user,force)
            babel.set_language(None)
                
            logger.info("%d lino*.js files have been built in %s seconds.",
                count,time.time()-started)
          
    def build_js_cache_for_user(self,user,force=False):
        """
        Build the lino*.js file for the specified user and the current language.
        If the file exists and is up to date, don't generate it unless 
        `force=False` is specified.
        
        This is called 
        - on each request if :attr:`lino.Lino.build_js_cache_on_startup` is `False`.
        - with `force=True` by :class:`lino.modles.BuildSiteCache`
        """
        jsgen.set_for_user(user)
        
        fn = os.path.join(settings.MEDIA_ROOT,*self.lino_js_parts(user)) 
        if not force and os.path.exists(fn):
            mtime = os.stat(fn).st_mtime
            if mtime > settings.LINO.mtime:
                if not user.modified or user.modified < datetime.datetime.fromtimestamp(mtime):
                    logger.debug("%s is up to date.",fn)
                    return 0
                    
        logger.info("Building %s ...", fn)
        makedirs_if_missing(os.path.dirname(fn))
        f = codecs.open(fn,'w',encoding='utf-8')
        try:
            self.write_lino_js(f,user)
            #~ f.write(jscompress(js))
            f.close()
            return 1
        except Exception, e:
            """
            If some error occurs, remove the half generated file 
            to make sure that Lino will try to generate it again on next request
            (and report the same error message again).
            """
            f.close()
            os.remove(fn)
            raise
        #~ logger.info("Wrote %s ...", fn)
            
    def write_lino_js(self,f,user):
        tpl = self.linolib_template()
        
        messages = set()
        def mytranslate(s):
            messages.add(s)
            return _(s)
        tpl._ = mytranslate
        f.write(jscompress(unicode(tpl)+'\n'))
        make_dummy_messages_file(self.linolib_template_name(),messages)
        
        actors_list = [
            rpt for rpt in table.master_reports \
               + table.slave_reports \
               + table.generic_slaves.values() \
               + table.custom_tables \
               + table.frames_list ]
               
        """
        Call Ext.namespace for *all* actors because e.g. outbox.Mails.FormPanel 
        is defined in ns outbox.Mails which is not directly used by non-expert users.
        """
        
        f.write("Lino.main_menu = %s;\n" % py2js(settings.LINO.get_site_menu(self,user)))

        for a in actors_list:
            f.write("Ext.namespace('Lino.%s')\n" % a)
            
        # actors with an own `get_handle_name` don't have a js implementation
        #~ print '20120605 dynamic actors',[a for a in actors_list if a.get_handle_name is not None]
        actors_list = [a for a in actors_list if a.get_handle_name is None]

        actors_list = [a for a in actors_list if a.get_view_permission(jsgen._for_user)]
          
        #~ logger.info('20120120 table.all_details:\n%s',
            #~ '\n'.join([str(d) for d in table.all_details]))
        
        details = set()
        def add(actor,fl,nametpl):
            if fl is not None:
                if not fl in details:
                    fl._formpanel_name = nametpl % actor
                    details.add(fl)
                    
        for a in actors_list:
            add(a,a.detail_layout, "Lino.%s.DetailFormPanel")
            add(a,a.insert_layout, "Lino.%s.InsertFormPanel")
            
        for fl in details:
            lh = fl.get_layout_handle(self)
            for ln in self.js_render_FormPanel(lh,user):
                f.write(ln + '\n')
        
        for rpt in actors_list:
            rh = rpt.get_handle(self) 
            if isinstance(rpt,type) and issubclass(rpt,table.AbstractTable):
                #~ if rpt.model is None:
                #~ f.write('// 20120621 %s\n' % rpt)
                    #~ continue
                
                for ln in self.js_render_GridPanel_class(rh,user):
                    f.write(ln + '\n')
                
            for a in rpt.get_actions():
                if a.opens_a_window:
                    if isinstance(a,(actions.ShowDetailAction,actions.InsertRow)):
                        for ln in self.js_render_detail_action_FormPanel(rh,a):
                              f.write(ln + '\n')
                    for ln in self.js_render_window_action(rh,a,user):
                        f.write(ln + '\n')
                elif a.show_in_workflow:
                    for ln in self.js_render_workflow_action(rh,a,user):
                        f.write(ln + '\n')
        return 1
          
        
    #~ def make_linolib_messages(self):
        #~ """
        #~ Called from :term:`dtl2py`.
        #~ """
        #~ from lino.utils.config import make_dummy_messages_file
        #~ tpl = self.linolib_template()
        #~ messages = set()
        #~ def mytranslate(s):
            #~ messages.add(s)
            #~ return _(s)
        #~ tpl._ = mytranslate
        #~ unicode(tpl) # just to execute the template. result is not needed
        #~ return make_dummy_messages_file(self.linolib_template_name(),messages)
        
    #~ def make_dtl_messages(self):
        #~ from lino.core.kernel import make_dtl_messages
        #~ return make_dtl_messages(self)
        
    def linolib_template_name(self):
        return os.path.join(os.path.dirname(__file__),'linolib.js')
        
    def linolib_template(self):
        def docurl(ref):
            if not ref.startswith('/'):
                raise Exception("Invalid docref %r" % ref)
            # todo: check if file exists...
            return "http://lino.saffre-rumma.net" + ref + ".html"
            
        libname = self.linolib_template_name()
        tpl = CheetahTemplate(codecs.open(libname,encoding='utf-8').read())
        tpl.ui = self
            
        tpl._ = _
        #~ tpl.user = request.user
        tpl.site = settings.LINO
        tpl.settings = settings
        tpl.lino = lino
        tpl.docurl = docurl
        tpl.ui = self
        tpl.ext_requests = ext_requests
        for k in ext_requests.URL_PARAMS:
            setattr(tpl,k,getattr(ext_requests,k))
        return tpl
            

    #~ def quicklink(self,request,app_label,actor,**kw):
        #~ rpt = self.requested_report(request,app_label,actor)
        #~ return self.action_href(rpt.default_action,**kw)

    def setup_handle(self,h,ar):
        """
        ar is usually None, except for actors with dynamic handle
        """
        #~ logger.info('20120621 ExtUI.setup_handle() %s',h)
        if isinstance(h,tables.TableHandle):
            if issubclass(h.actor,table.Table):
                if h.actor.model is None \
                    or h.actor.model is dd.Model \
                    or h.actor.model._meta.abstract:
                    #~ logger.info('20120621 %s : no real table',h)
                    return
            ll = layouts.ListLayout(h.actor.get_column_names(ar),h.actor,hidden_elements=h.actor.hidden_columns)
            #~ h.list_layout = layouts.ListLayoutHandle(h,ll,hidden_elements=h.actor.hidden_columns)
            h.list_layout = ll.get_layout_handle(self)
        else:
            h.list_layout = None
                
        if h.actor.parameters:
            if h.actor.params_template:
                params_template = h.actor.params_template
            else:
                #~ params_template= ' '.join([pf.name for pf in h.actor.params])
                params_template= ' '.join(h.actor.parameters.keys())
            pl = layouts.ParamsLayout(params_template,h.actor)
            h.params_layout = pl.get_layout_handle(self)
            #~ h.params_layout.main.update(hidden = h.actor.params_panel_hidden)
            #~ h.params_layout = layouts.LayoutHandle(self,pl)
            #~ logger.info("20120121 %s params_layout is %s",h,h.params_layout)
        
        h.store = ext_store.Store(h)
        
        #~ if h.store.param_fields:
            #~ logger.info("20120121 %s param_fields is %s",h,h.store.param_fields)
        
        #~ 20120614 if h.list_layout:
            #~ h.on_render = self.build_on_render(h.list_layout.main)
            
        #~ elif isinstance(h,table.FrameHandle):
            #~ if issubclass(h.report,table.EmptyTable):
                #~ h.store = ext_store.Store(h)
          
                
                      
    def source_dir(self):
        return os.path.abspath(os.path.dirname(__file__))
        
    def a2btn(self,a,**kw):
        if isinstance(a,actions.SubmitDetail):
            kw.update(panel_btn_handler=js_code('function(panel){panel.save()}'))
            
        elif isinstance(a,actions.ShowDetailAction):
            kw.update(panel_btn_handler=js_code('Lino.show_detail'))
        elif isinstance(a,actions.InsertRow):
            kw.update(must_save=True)
            kw.update(panel_btn_handler=js_code(
                'function(panel){Lino.show_insert(panel)}'))
        elif isinstance(a,actions.DuplicateRow):
            kw.update(panel_btn_handler=js_code(
                'function(panel){Lino.show_insert_duplicate(panel)}'))
        elif isinstance(a,actions.DeleteSelected):
            kw.update(panel_btn_handler=js_code("Lino.delete_selected"))
                #~ "Lino.delete_selected" % a))
        elif isinstance(a,actions.RowAction):
            if a.url_action_name is None:
                raise Exception("Action %r has no url_action_name" % a)
            kw.update(must_save=True)
            kw.update(
              panel_btn_handler=js_code("Lino.row_action_handler(%r)" % a.url_action_name))
        elif isinstance(a,actions.ListAction):
            if a.url_action_name is None:
                raise Exception("Action %r has no url_action_name" % a)
            kw.update(
              panel_btn_handler=js_code("Lino.list_action_handler(%r)" % a.url_action_name))
            kw.update(must_save=True)
        else:
            kw.update(panel_btn_handler=js_code("Lino.%s" % a))
        kw.update(
          text=a.label,
          #~ name=a.name,
          auto_save=a.auto_save,
          itemId=a.name,
          #~ text=unicode(a.label),
        )
        if a.help_text:
            kw.update(tooltip=a.help_text)
        return kw
        
    def unused_setup_detail_handle(self,dh):
        """
        Adds UI-specific information to a DetailHandle.
        """
        lh_list = dh.lh_list
        if len(lh_list) == 1:
            dh.tabbed = False
            lh = lh_list[0]
            #~ lh.label = None
            dh.main = lh.main
            #~ main.update(autoScroll=True)
        else:
            dh.tabbed = True
            tabs = [lh.main for lh in lh_list]
            #~ for t in tabs: t.update(autoScroll=True)
            dh.main = ext_elems.TabPanel(tabs)
            
        dh.on_render = self.build_on_render(dh.main)
            
    def build_on_render(self,main):
        "dh is a FormLayout or a ListLayout"
        on_render = []
        elems_by_field = {}
        field_elems = []
        for e in main.active_children:
            if isinstance(e,ext_elems.FieldElement):
                field_elems.append(e)
                l = elems_by_field.get(e.field.name,None)
                if l is None:
                    l = []
                    elems_by_field[e.field.name] = l
                l.append(e)
            
        for e in field_elems:
            #~ if isinstance(e,FileFieldElement):
                #~ kw.update(fileUpload=True)
            chooser = choosers.get_for_field(e.field)
            if chooser:
                #~ logger.debug("20100615 %s.%s has chooser", self.lh.layout, e.field.name)
                for f in chooser.context_fields:
                    for el in elems_by_field.get(f.name,[]):
                        #~ if main.has_field(f):
                        #~ varname = varname_field(f)
                        #~ on_render.append("%s.on('change',Lino.chooser_handler(%s,%r));" % (varname,e.ext_name,f.name))
                        on_render.append(
                            "%s.on('change',Lino.chooser_handler(%s,%r));" % (
                            el.as_ext(),e.as_ext(),f.name))
        return on_render
        
    #~ def formpanel_name(self,layout):
        #~ if isinstance(layout,layouts.FormLayout
            #~ return "Lino.%s.InsertFormPanel" % self._table
        #~ elif isinstance(layout,layouts.FormLayout):
            #~ return "Lino.%s.DetailFormPanel" % self._table
        #~ raise Exception("Unknown Form Layout %s" % layout)
      
        
      
    def js_render_FormPanel(self,dh,user):
        
        tbl = dh.layout._table
        
        yield ""
        yield "%s = Ext.extend(Lino.FormPanel,{" % dh.layout._formpanel_name
        yield "  layout: 'fit',"
        yield "  auto_save: true,"
        if dh.layout.window_size and dh.layout.window_size[1] == 'auto':
            yield "  autoHeight: true,"
        if settings.LINO.is_installed('contenttypes') and issubclass(tbl,table.Table):
            yield "  content_type: %s," % py2js(ContentType.objects.get_for_model(tbl.model).pk)
        yield "  initComponent : function() {"
        yield "    var containing_panel = this;"
        for ln in jsgen.declare_vars(dh.main):
            yield "    " + ln
        yield "    this.items = %s;" % dh.main.as_ext()
        yield "    this.before_row_edit = function(record) {"
        for ln in ext_elems.before_row_edit(dh.main):
            yield "      " + ln
        yield "    }"
        on_render = self.build_on_render(dh.main)
        if on_render:
            yield "    this.onRender = function(ct, position) {"
            for ln in on_render:
                yield "      " + ln
            #~ yield "      Lino.%s.FormPanel.superclass.onRender.call(this, ct, position);" % tbl
            yield "      %s.superclass.onRender.call(this, ct, position);" % dh.layout._formpanel_name
            yield "    }"

        #~ yield "    Lino.%s.FormPanel.superclass.initComponent.call(this);" % tbl
        yield "    %s.superclass.initComponent.call(this);" % dh.layout._formpanel_name
        
        if tbl.active_fields:
            yield '    // active_fields:'
            for name in tbl.active_fields:
                e = dh.main.find_by_name(name)
                if e is not None: # 20120715
                    yield '    %s.on("%s",function(){this.save()},this);' % (py2js(e),e.active_change_event)
                    """
                    Seems that checkboxes don't emit a change event when they are changed.
                    http://www.sencha.com/forum/showthread.php?43350-2.1-gt-2.2-OPEN-Checkbox-missing-the-change-event
                    """
        yield "  }"
        yield "});"
        yield ""
        
        
    def js_render_detail_action_FormPanel(self,rh,action):
        rpt = rh.actor
        yield ""
        #~ yield "// js_render_detail_action_FormPanel %s" % action
        dtl = action.get_window_layout()
        #~ dtl = rpt.detail_layout
        if dtl is None:
            raise Exception("action %s on table %r == %r without detail?" % (action,action.actor,rpt))
        #~ yield "Lino.%sPanel = Ext.extend(Lino.%s.FormPanel,{" % (action,dtl._table)
        yield "Lino.%sPanel = Ext.extend(%s,{" % (action,dtl._formpanel_name)
        yield "  empty_title: %s," % py2js(action.get_button_label())
        #~ if not isinstance(action,actions.InsertRow):
        if action.hide_navigator:
            yield "  hide_navigator: true,"
            
        if rh.actor.params_panel_hidden:
            yield "  params_panel_hidden: true,"

        yield "  ls_bbar_actions: %s," % py2js([
            rh.ui.a2btn(a) for a in rpt.get_actions(action) 
                if a.show_in_bbar and a.get_action_permission(jsgen._for_user,None,None)]) 
        yield "  ls_url: %s," % py2js(ext_elems.rpt2url(rpt))
        if action != rpt.default_action:
            yield "  action_name: %s," % py2js(action.url_action_name)
        #~ yield "  active_fields: %s," % py2js(rpt.active_fields)
        yield "  initComponent : function() {"
        a = rpt.detail_action
        if a:
            yield "    this.ls_detail_handler = Lino.%s;" % a
        a = rpt.insert_action
        if a:
            yield "    this.ls_insert_handler = Lino.%s;" % a
            
        yield "    Lino.%sPanel.superclass.initComponent.call(this);" % action
        yield "  }"
        yield "});"
        yield ""
        
    def js_render_GridPanel_class(self,rh,user):
        
        yield ""
        #~ yield "// js_render_GridPanel_class"
        yield "Lino.%s.GridPanel = Ext.extend(Lino.GridPanel,{" % rh.actor
        
        kw = dict()
        #~ kw.update(empty_title=%s,rh.actor.get_button_label()
        kw.update(ls_url=ext_elems.rpt2url(rh.actor))
        kw.update(ls_store_fields=[js_code(f.as_js()) for f in rh.store.list_fields])
        if rh.store.pk is not None:
            kw.update(ls_id_property=rh.store.pk.name)
            kw.update(pk_index=rh.store.pk_index)
            #~ if settings.LINO.use_contenttypes:
            if settings.LINO.is_installed('contenttypes'):
                kw.update(content_type=ContentType.objects.get_for_model(rh.actor.model).pk)
        kw.update(ls_quick_edit=rh.actor.cell_edit)
        kw.update(ls_bbar_actions=[
            rh.ui.a2btn(a) 
              for a in rh.actor.get_actions(rh.actor.default_action) 
                  if a.show_in_bbar and a.get_action_permission(jsgen._for_user,None,None)])
        kw.update(ls_grid_configs=[gc.data for gc in rh.actor.grid_configs])
        kw.update(gc_name=ext_elems.DEFAULT_GC_NAME)
        #~ if action != rh.actor.default_action:
            #~ kw.update(action_name=action.name)
        #~ kw.update(content_type=rh.report.content_type)
        
        vc = dict(emptyText=_("No data to display."))
        if rh.actor.editable:
            vc.update(getRowClass=js_code('Lino.getRowClass'))
        kw.update(viewConfig=vc)
        
        
        
        kw.update(page_length=rh.actor.page_length)
        kw.update(stripeRows=True)

        #~ if rh.actor.master:
        kw.update(title=rh.actor.label)
        kw.update(disabled_actions_index=rh.store.column_index('disabled_actions'))
        
        for k,v in kw.items():
            yield "  %s : %s," % (k,py2js(v))
        
        yield "  initComponent : function() {"
        
        #~ a = rh.actor.get_action('detail')
        a = rh.actor.detail_action
        if a:
            yield "    this.ls_detail_handler = Lino.%s;" % a
        #~ a = rh.actor.get_action('insert')
        a = rh.actor.insert_action
        if a:
            yield "    this.ls_insert_handler = Lino.%s;" % a
        
        
        yield "    var ww = this.containing_window;"
        for ln in jsgen.declare_vars(rh.list_layout.main.columns):
            yield "    " + ln
            
            
        yield "    this.before_row_edit = function(record) {"
        for ln in ext_elems.before_row_edit(rh.list_layout.main):
            yield "      " + ln
        yield "    };"
        
        #~ if rh.on_render:
        on_render = self.build_on_render(rh.list_layout.main)        
        if on_render:
            yield "    this.onRender = function(ct, position) {"
            for ln in on_render:
                yield "      " + ln
            yield "      Lino.%s.GridPanel.superclass.onRender.call(this, ct, position);" % rh.actor
            yield "    }"
            
            
        yield "    this.ls_columns = %s;" % py2js([ 
            ext_elems.GridColumn(i,e) for i,e 
                in enumerate(rh.list_layout.main.columns)])
            
        #~ yield "    this.columns = this.apply_grid_config(this.gc_name,this.ls_grid_configs,this.ls_columns);"
        #~ yield "    this.colModel = Lino.ColumnModel({columns:this.apply_grid_config(this.gc_name,this.ls_grid_configs,this.ls_columns)});"

        #~ yield "    this.items = %s;" % rh.list_layout._main.as_ext()
        #~ 20111125 see ext_elems.py too
        #~ if self.main.listeners:
            #~ yield "  config.listeners = %s;" % py2js(self.main.listeners)
        yield "    Lino.%s.GridPanel.superclass.initComponent.call(this);" % rh.actor
        yield "  }"
        yield "});"
        yield ""
      
            
    def js_render_workflow_action(self,rh,action,user):
        """
        Defines the non-window action used by :meth:`row_action_button`
        """
        # 20120723 : removed useless js param "action"
        yield "Lino.%s = function(rp,pk) { " % action
        #~ panel = "Lino.%s.GridPanel.ls_url" % action 
        url = ext_elems.rpt2url(rh.actor)
        yield "  Lino.run_row_action(rp,%s,pk,%s);" % (
            py2js(url),py2js(action.url_action_name))
        yield "};"


    def js_render_window_action(self,rh,action,user):
      
        rpt = rh.actor
        
        if isinstance(action,actions.ShowDetailAction):
            mainPanelClass = "Lino.%sPanel" % action
        elif isinstance(action,actions.InsertRow): 
            mainPanelClass = "Lino.%sPanel" % action
        elif isinstance(action,actions.GridEdit):
            mainPanelClass = "Lino.%s.GridPanel" % rpt
        elif isinstance(action,CalendarAction):
            mainPanelClass = "Lino.CalendarPanel"
            #~ mainPanelClass = "Lino.CalendarAppPanel"
            #~ mainPanelClass = "Ext.ensible.cal.CalendarPanel"
        else:
            return 
        if action.actor is None:
            raise Exception("20120524 %s %s actor is None" % (rh.actor,action))
        if rpt.parameters:
            params = rh.params_layout.main
            #~ assert params.__class__.__name__ == 'ParameterPanel'
        else:
            params = None
            
        windowConfig = dict()
        #~ ws = action.actor.window_size
        wl = action.get_window_layout()
        if wl is not None:
            ws = wl.window_size
            if ws:
                windowConfig.update(
                    #~ width=ws[0],
                    width=js_code('Lino.chars2width(%d)' % ws[0]),
                    maximized=False,
                    draggable=True, 
                    maximizable=True, 
                    modal=True)
                if ws[1] == 'auto':
                    windowConfig.update(autoHeight=True)
                elif isinstance(ws[1],int):
                    #~ windowConfig.update(height=ws[1])
                    windowConfig.update(height=js_code('Lino.rows2height(%d)' % ws[1]))
                else:
                    raise ValueError("height")
                #~ print 20120629, action, windowConfig
                
        #~ yield "var fn = function() {" 
        #~ yield "};" 
        yield "Lino.%s = new Lino.WindowAction(%s,function(){" % (action,py2js(windowConfig))
        #~ yield "  console.log('20120625 fn');" 
        if isinstance(action,CalendarAction):
            yield "  return Lino.calendar_app.get_main_panel();"
        else:
            p = dict()
            if action is settings.LINO.get_main_action(user):
                p.update(is_home_page=True)
            #~ yield "  var p = {};" 
            if action.hide_top_toolbar:
                p.update(hide_top_toolbar=True)
                #~ yield "  p.hide_top_toolbar = true;" 
            if action.actor.hide_window_title:
                #~ yield "  p.hide_window_title = true;" 
                p.update(hide_window_title=True)
            #~ yield "  p.is_main_window = true;" # workaround for problem 20111206
            p.update(is_main_window=True) # workaround for problem 20111206
            yield "  var p = %s;"  % py2js(p)
            #~ if isinstance(action,CalendarAction):
                #~ yield "  p.items = Lino.CalendarAppPanel_items;" 
            if params:
                for ln in jsgen.declare_vars(params):
                    yield '  '  + ln
                yield "  p.params_panel = %s;" % params
                yield "  p.params_panel.fields = %s;" % py2js(
                  [e for e in params.walk() if isinstance(e,ext_elems.FieldElement)])
            
            yield "  return new %s(p);" % mainPanelClass
        #~ yield "  console.log('20120625 rv is',rv);" 
        #~ yield "  return rv;"
        yield "});" 
        
    
    def table2xhtml(self,ar,max_row_count=300):
        doc = xghtml.Document(force_unicode(ar.get_title()))
        t = doc.add_table()
        self.ar2html(ar,t)
        return xghtml.E.tostring(t.as_element())
        
    def ar2html(self,ar,tble):
        """
        Using lino.utils.xmlgen.html
        """
        tble.attrib.update(cellspacing="3px",bgcolor="#ffffff", width="100%")
        
        fields = ar.ah.store.list_fields
        headers = [force_unicode(col.label or col.name) for col in ar.ah.list_layout.main.columns]
        cellwidths = None
        columns = ar.ah.list_layout.main.columns
        
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
                    for e in ar.ah.list_layout.main.columns:
                        if e.name == cn:
                            col = e
                            break
                    #~ col = ar.ah.list_layout._main.find_by_name(cn)
                    #~ col = ar.ah.list_layout._main.columns[ci]
                    if col is None:
                        #~ names = [e.name for e in ar.ah.list_layout._main.walk()]
                        raise Exception("No column named %r in %s" % (cn,ar.ah.list_layout.main.columns))
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
          
        
        sums  = [fld.zero for fld in fields]
        #~ cellattrs = dict(align="center",valign="middle",bgcolor="#eeeeee")
        cellattrs = dict(align="left",valign="top",bgcolor="#eeeeee")
        hr = tble.add_header_row(*headers,**cellattrs)
        if cellwidths:
            for i,td in enumerate(hr): 
                td.attrib.update(width=cellwidths[i])
        #~ print 20120623, ar.actor
        recno = 0
        for row in ar.data_iterator:
            recno += 1
            cells = [x for x in ar.ah.store.row2html(ar,fields,row,sums)]
            #~ print 20120623, cells
            tble.add_body_row(*cells,**cellattrs)
                
        has_sum = False
        for i in sums:
            if i:
                has_sum = True
                break
        if has_sum:
            tble.add_body_row(*ar.ah.store.sums2html(ar,fields,sums),**cellattrs)
            
            
            
    
    def create_layout_panel(self,lh,name,vertical,elems,**kw):
        pkw = dict()
        pkw.update(labelAlign=kw.pop('label_align','top'))
        pkw.update(hideCheckBoxLabels=kw.pop('hideCheckBoxLabels',True))
        pkw.update(label=kw.pop('label',None))
        pkw.update(width=kw.pop('width',None))
        pkw.update(height=kw.pop('height',None))
        if kw:
            raise Exception("Unknown panel attributes %r" % kw)
        if name == 'main':
            if isinstance(lh.layout,layouts.ListLayout):
                #~ return ext_elems.GridMainPanel(lh,name,vertical,*elems,**pkw)
                #~ return ext_elems.GridMainPanel(lh,name,lh.layout._table,*elems,**pkw)
                return ext_elems.GridElement(lh,name,lh.layout._table,*elems,**pkw)
            if isinstance(lh.layout,layouts.ParamsLayout) : 
                return ext_elems.ParamsPanel(lh,name,vertical,*elems,**pkw)
                #~ fkw = dict(layout='fit', autoHeight= True, frame= True, items=pp)
                #~ if lh.layout._table.params_panel_hidden:
                    #~ fkw.update(hidden=True)
                #~ return ext_elems.FormPanel(**fkw)
            if isinstance(lh.layout,layouts.FormLayout): 
                if len(elems) == 1 or vertical:
                    return ext_elems.DetailMainPanel(lh,name,vertical,*elems,**pkw)
                else:
                    return ext_elems.TabPanel(lh,name,*elems,**pkw)
            raise Exception("No element class for layout %r" % lh.layout)
        return ext_elems.Panel(lh,name,vertical,*elems,**pkw)


    def row_action_button(self,*args,**kw):
        return self.ext_renderer.row_action_button(*args,**kw)
