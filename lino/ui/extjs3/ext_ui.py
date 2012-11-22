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
from django.conf import settings
from django.http import HttpResponse, Http404
from django.utils import functional
from django.utils.encoding import force_unicode
#~ from django.utils.functional import Promise

from django.template.loader import get_template
from django.template import RequestContext

from django.utils.translation import ugettext as _
#~ from django.utils import simplejson as json
from django.utils import translation

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf.urls.defaults import patterns, url, include


import lino
from lino.ui.extjs3 import ext_elems
from lino.ui.extjs3 import ext_store
#~ from lino.ui.extjs3 import ext_windows
from lino.ui import requests as ext_requests

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
from lino.core.modeltools import makedirs_if_missing
from lino.core.modeltools import full_model_name
from lino.core.modeltools import is_devserver
    
from lino.utils import choosers
from lino.utils import babel
from lino.utils import choicelists
from lino.core import menus
from lino.utils import jsgen
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

#~ from lino.utils.choicelists import DoYouLike, HowWell
#~ STRENGTH_CHOICES = DoYouLike.get_choices()
#~ KNOWLEDGE_CHOICES = HowWell.get_choices()

NOT_GIVEN = object()

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
        
          
    def href_button_action(self,ba,*args,**kw):
        if ba.action.icon_file is not None:
            kw.update(icon_file=ba.action.icon_file)
            kw.update(style="vertical-align:-30%;")
        return self.href_button(*args,**kw)
        
    def href_button(self,url,text,title=None,target=None,icon_file=None,**kw):
        """
        Returns an elementtree object of a "button-like" ``<a href>`` tag.
        """
        #~ logger.info('20121002 href_button %r',unicode(text))
        if target:
            kw.update(target=target)
        if title:
            # Remember that Python 2.6 doesn't like if title is a Promise
            kw.update(title=unicode(title))
            #~ return xghtml.E.a(text,href=url,title=title)
        kw.update(href=url)
        #~ if icon_name:
        if icon_file:
            #~ btn = xghtml.E.button(type='button',class_='x-btn-text '+icon_name)
            #~ btn = xghtml.E.button(
                #~ type='button',
                #~ class_='x-btn-text '+icon_name,
                #~ onclick='function() {console.log(20121024)}')
            #~ return btn
            #~ return xghtml.E.a(btn,**kw)
            #~ kw.update(class_='x-btn-text '+icon_name)
            img = xghtml.E.img(src=self.ui.media_url('lino','extjs','images','mjames',icon_file))
            return xghtml.E.a(img,**kw)
        else:
            #~ return xghtml.E.span('[',xghtml.E.a(text,**kw),']')
            #~ kw.update(style='border-width:1px; border-color:black; border-style:solid;')
            return xghtml.E.a(text,**kw)
        
    def quick_add_buttons(self,ar):
        """
        Returns a HTML chunk that displays "quick add buttons"
        for the given :class:`action request <lino.core.dbtables.TableRequest>`:
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
        #~ a = ar.actor.get_url_action('insert_action')
        buttons = []
        a = ar.actor.insert_action
        if a is not None:
            if a.get_bound_action_permission(ar,ar.master_instance,None):
                elem = ar.create_instance()
                after_show.update(data_record=views.elem2rec_insert(ar,ar.ah,elem))
                #~ after_show.update(record_id=-99999)
                # see tickets/56
                #~ s += self.window_action_button(a,after_show,_("New"))
                buttons.append(self.window_action_button(ar.request,a,after_show,_("New")))
                #~ buttons.append(self.action_button(ar.request,a,after_show,_("New")))
                buttons.append(' ')
                after_show = ar.get_status(self)
        n = ar.get_total_count()
        #~ print 20120702, [o for o in ar]
        if n > 0:
            obj = ar.data_iterator[n-1]
            after_show.update(record_id=obj.pk)
            #~ a = ar.actor.get_url_action('detail_action')
            a = ar.actor.detail_action
            buttons.append(self.window_action_button(
                ar.request,a,after_show,_("Show Last"),
                icon_file = 'application_form.png',
                title=_("Show the last record in a detail window")))
            buttons.append(' ')
            #~ s += ' ' + self.window_action_button(
                #~ ar.ah.actor.detail_action,after_show,_("Show Last"))
            #~ s += ' ' + self.href_to_request(ar,"[%s]" % unicode(_("Show All")))
            buttons.append(self.href_to_request(None,ar,
              _("Show All"),
              icon_file = 'application_view_list.png',
              title=_("Show all records in a table window")))
        #~ return '<p>%s</p>' % s
        return xghtml.E.p(*buttons)
                
    def quick_upload_buttons(self,rr):
        """
        Returns a HTML chunk that displays "quick upload buttons":
        either one button :guilabel:`[Upload]` 
        (if the given :class:`TableTequest <lino.core.dbtables.TableRequest>`
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
            #~ a = rr.actor.get_url_action('insert_action')
            a = rr.actor.insert_action
            if a is not None:
                elem = rr.create_instance()
                after_show.update(data_record=views.elem2rec_insert(rr,rr.ah,elem))
                #~ after_show.update(record_id=-99999)
                # see tickets/56
                return self.window_action_button(rr.request,a,after_show,_("Upload"),
                  #~ icon_file='attach.png',
                  #~ icon_file='world_add.png',
                  icon_file='page_add.png',
                  title=_("Upload a file from your PC to the server."))
                  #~ icon_name='x-tbar-upload')
        if rr.get_total_count() == 1:
            obj = rr.data_iterator[0]
            chunks = []
            #~ chunks.append(xghtml.E.a(_("show"),
              #~ href=self.ui.media_url(obj.file.name),target='_blank'))
            chunks.append(self.href_button(
                self.ui.media_url(obj.file.name),_("show"),
                target='_blank',
                #~ icon_file='world_go.png',
                icon_file='page_go.png',
                title=_("Open the uploaded file in a new browser window")))
            chunks.append(' ')
            after_show.update(record_id=obj.pk)
            chunks.append(self.window_action_button(rr.request,
                rr.ah.actor.detail_action,
                after_show,
                _("Edit"),icon_file='application_form.png',title=_("Edit metadata of the uploaded file.")))
            return xghtml.E.p(*chunks)
            
            #~ s = ''
            #~ s += ' [<a href="%s" target="_blank">show</a>]' % (self.ui.media_url(obj.file.name))
            #~ if True:
                #~ after_show.update(record_id=obj.pk)
                #~ s += ' ' + self.window_action_button(rr.ah.actor.detail_action,after_show,_("Edit"))
            #~ else:
                #~ after_show.update(record_id=obj.pk)
                #~ s += ' ' + self.action_href_http(rr.ah.actor.detail_action,_("Edit"),params,after_show)
            #~ return s
        return '[?!]'

  
    def obj2html(self,ar,obj,text=None):
        url = self.instance_handler(ar,obj)
        if text is None: text = force_unicode(obj)
        if url is None:
            return xghtml.E.b(text)
        return xghtml.E.a(text,href=url)
        
class TextRenderer(HtmlRenderer):
    def instance_handler(self,ar,obj):
        return None
    def pk2url(self,ar,pk,**kw):
        return None
    def get_request_url(self,ar,*args,**kw):
        return None
    def href_to_request(self,sar,tar,text=None):
        if text is None:
            text = '#'
        return text
  
class PlainRenderer(HtmlRenderer):
    def instance_handler(self,ar,obj):
        a = getattr(obj,'_detail_action',None)
        if a is None:
            a = obj.__class__._lino_default_table.detail_action
        if a is not None:
            if ar is None or a.get_bound_action_permission(ar,obj,None):
                return self.get_detail_url(obj)
  
    def pk2url(self,ar,pk,**kw):
        if pk is not None:
            kw[ext_requests.URL_PARAM_FORMAT] = ext_requests.URL_FORMAT_PLAIN
            return self.ui.build_url('api',
                ar.actor.model._meta.app_label,
                ar.actor.model.__name__,
                str(pk),**kw)
            
    def get_detail_url(self,obj,*args,**kw):
        kw[ext_requests.URL_PARAM_FORMAT] = ext_requests.URL_FORMAT_PLAIN
        return self.ui.build_url('api',obj._meta.app_label,obj.__class__.__name__,str(obj.pk),*args,**kw)
        
    def get_request_url(self,ar,*args,**kw):
        kw.setdefault(ext_requests.URL_PARAM_FORMAT,ext_requests.URL_FORMAT_PLAIN)
        if ar.offset is not None:
            kw.setdefault(ext_requests.URL_PARAM_START,ar.offset)
        if ar.limit is not None:
            kw.setdefault(ext_requests.URL_PARAM_LIMIT,ar.limit)
        if ar.order_by is not None:
            sc = ar.order_by[0]
            if sc.startswith('-'):
                sc = sc[1:]
                kw.setdefault(ext_requests.URL_PARAM_SORTDIR,'DESC')
            kw.setdefault(ext_requests.URL_PARAM_SORT,sc)
        #~ print '20120901 TODO get_request_url'
        return ar.ui.build_url('api',ar.actor.app_label,ar.actor.__name__,*args,**kw)
        
    def request_handler(self,ar,*args,**kw):
        return ''
  
    def action_button(self,obj,ar,ba,label=None,**kw):
        label = label or ba.action.label
        return label
      
class ExtRenderer(HtmlRenderer):
    """
    Deserves more documentation.
    """
    def pk2url(self,ar,pk,**kw):
        return None
        
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
        #~ if v is STRENGTH_CHOICES:
            #~ return js_code('STRENGTH_CHOICES')
        #~ if v is KNOWLEDGE_CHOICES:
            #~ return js_code('KNOWLEDGE_CHOICES')
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
                #~ ar = v.action.actor.request(self.ui,None,v.action,**v.params)
                ar = v.bound_action.request(self.ui,**v.params)
                return handler_item(v,self.request_handler(ar),v.bound_action.action.help_text)
                #~ return dict(text=prepare_label(v),handler=js_code(handler))
            if v.bound_action:
                return handler_item(v,self.action_call(None,v.bound_action,{}),v.bound_action.action.help_text)
                #~ ar = v.action.request(self.ui)
                #~ return handler_item(v,self.request_handler(ar),v.action.help_text)
            elif v.javascript is not None:
                return handler_item(v,v.javascript,None)
            elif v.href is not None:
                url = v.href
            elif v.request is not None:
                raise Exception("20120918 request %r still used?" % v.request)
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
                  handler=js_code("function() { Lino.load_url('%s'); }" % url))
            return dict(text=prepare_label(v),href=url)
        return v
        
    def js2url(self,js):
        js = cgi.escape(js)
        js = js.replace('"','&quot;')
        return 'javascript:' + js
        
    #~ def action_url_js(self,a,after_show):
        #~ return self.js2url(self.action_call(a,after_show))

    def action_button(self,obj,ar,ba,label=None,**kw):
        """
        ``kw`` may contain additional html attributes like `style`
        """
        if ba.action.parameters:
            st = ar.get_action_status(ba,obj)
            #~ st.update(record_id=obj.pk)
            return self.window_action_button(ar.request,ba,st,label or ba.action.label,**kw)
        if ba.action.opens_a_window:
            st = ar.get_status(self)
            st.update(record_id=obj.pk)
            return self.window_action_button(ar.request,ba,st,label or ba.action.label,**kw)
        return self.row_action_button(obj,ar.request,ba,label,**kw)
        
    def window_action_button(self,request,ba,after_show={},label=None,title=None,**kw):
        """
        Return a HTML chunk for a button that will execute this 
        action using a *Javascript* link to this action.
        """
        label = unicode(label or ba.get_button_label())
        url = 'javascript:'+self.action_call(request,ba,after_show)
        #~ logger.info('20121002 window_action_button %s %r',a,unicode(label))
        return self.href_button_action(ba,url,label,title or ba.action.help_text,**kw)
        #~ if a.action.help_text:
            #~ return self.href_button(url,label,a.action.help_text)
        #~ return self.href_button(url,label)
        
    def row_action_button(self,obj,request,ba,label=None,title=None,**kw):
        """
        Return a HTML fragment that displays a button-like link 
        which runs the action when clicked.
        """
        #~ label = unicode(label or ba.get_button_label())
        label = label or ba.action.label
        url = 'javascript:Lino.%s(%r,%s)' % (
                ba.full_name(),str(request.requesting_panel),
                py2js(obj.pk))
        return self.href_button_action(ba,url,label,title or ba.action.help_text,**kw)
        #~ if a.action.help_text:
            #~ return self.href_button(url,label,a.action.help_text)
        #~ return self.href_button(url,label)
        
    def action_call(self,request,bound_action,after_show):
        if bound_action.action.opens_a_window or bound_action.action.parameters:
        #~ if a.opens_a_window:
            #~ if after_show is None:
                #~ after_show = {}
            if request and request.subst_user:
                after_show[ext_requests.URL_PARAM_SUBST_USER] = request.subst_user
            if isinstance(bound_action.action,actions.ShowEmptyTable):
                after_show.update(record_id=-99998)
            if request is None or request.requesting_panel is None:
                rp = 'null'
            else:
                rp = "'" + request.requesting_panel + "'"
            if after_show:
                #~ return "Lino.%s.run(%s)" % (action.full_name(a.actor),py2js(after_show))
                return "Lino.%s.run(%s,%s)" % (
                  bound_action.full_name(),
                  rp,
                  py2js(after_show))
            return "Lino.%s.run(%s)" % (bound_action.full_name(),rp)
        return "?"

    def instance_handler(self,ar,obj):
        a = getattr(obj,'_detail_action',None)
        if a is None:
            #~ a = obj.get_default_table(ar).get_url_action('detail_action')
            a = obj.get_default_table(ar).detail_action
            #~ a = obj.__class__._lino_default_table.get_url_action('detail_action')
        if a is not None:
            if ar is None or a.get_bound_action_permission(ar,obj,None):
                return self.action_call(None,a,dict(record_id=obj.pk))
                
    def obj2html(self,ar,obj,text=None):
        h = self.instance_handler(ar,obj)
        if text is None: text = force_unicode(obj)
        if h is None:
            return xghtml.E.b(text)
        url = 'javascript:' + h
        return xghtml.E.a(text,href=url)
        
        
    def request_handler(self,ar,*args,**kw):
        #~ bp = rr.request2kw(self.ui,**kw)
        st = ar.get_status(self.ui,**kw)
        return self.action_call(ar.request,ar.bound_action,st)
        
    def href_to_request(self,sar,tar,text=None,**kw):
        #~ url = self.js2url(self.request_handler(tar))
        url = 'javascript:'+self.request_handler(tar)
        #~ if 'Lino.pcsw.MyPersonsByGroup' in url:
        #~ print 20120618, url
        #~ return self.href(url,text or cgi.escape(force_unicode(rr.label)))
        #~ if text is None:
            #~ text = unicode(tar.get_title())
        #~ return xghtml.E.a(text,href=url)
        return self.href_button_action(tar.bound_action,url,text or tar.get_title(),**kw)
        #~ return self.href_button(url,text or tar.get_title(),**kw)
        #~ return self.href_button(url,text or cgi.escape(force_unicode(rr.label)))
            
    def unused_action_href_http(self,a,label=None,**params):
        """
        Return a HTML chunk for a button that will execute 
        this action using a *HTTP* link to this action.
        """
        label = cgi.escape(force_unicode(label or a.get_button_label()))
        return '[<a href="%s">%s</a>]' % (self.action_url_http(a,**params),label)
        
    def get_actor_url(self,actor,*args,**kw):
        return self.ui.build_url("api",actor.app_label,actor.__name__,*args,**kw)
        
    def get_request_url(self,ar,*args,**kw):
        """
        Called from ActionRequest.absolute_url() used in `Team.eml.html`
        
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
        #~ the given :class:`TableTequest <lino.core.dbtables.TableRequest>`.
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
    if mi.bound_action and mi.bound_action.action.icon_name:
        d.update(iconCls=mi.bound_action.action.icon_name)
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
        self.plain_renderer = PlainRenderer(self)
        self.text_renderer = TextRenderer(self)
        self.reserved_names = [getattr(ext_requests,n) for n in ext_requests.URL_PARAMS]
        names = set()
        for n in self.reserved_names:
            if n in names:
                raise Exception("Duplicate reserved name %r" % n)
            names.add(n)
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
        
        #~ cause creation of the params_layout.params_store
        for res in actors.actors_list:
            for ba in res.get_actions():
                if ba.action.parameters:
                  ba.action.params_layout.get_layout_handle(self)
        
        
        
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
        #~ required.update(lh.layout._actor.required)
        #~ todo: requirements sind eine negativ-liste. aber auth=True muss in eine positiv-liste
        v = kw.pop('required',NOT_GIVEN)
        if v is not NOT_GIVEN:
            pkw.update(required=v)
        if kw:
            raise Exception("Unknown panel attributes %r for %s" % (kw,lh))
        if name == 'main':
            if isinstance(lh.layout,layouts.ListLayout):
                #~ return ext_elems.GridMainPanel(lh,name,vertical,*elems,**pkw)
                #~ return ext_elems.GridMainPanel(lh,name,lh.layout._actor,*elems,**pkw)
                e = ext_elems.GridElement(lh,name,lh.layout._actor,*elems,**pkw)
            elif isinstance(lh.layout,layouts.ActionParamsLayout) : 
                e = ext_elems.ActionParamsPanel(lh,name,vertical,*elems,**pkw)
            elif isinstance(lh.layout,layouts.ParamsLayout) : 
                e = ext_elems.ParamsPanel(lh,name,vertical,*elems,**pkw)
                #~ fkw = dict(layout='fit', autoHeight= True, frame= True, items=pp)
                #~ if lh.layout._actor.params_panel_hidden:
                    #~ fkw.update(hidden=True)
                #~ return ext_elems.FormPanel(**fkw)
            elif isinstance(lh.layout,layouts.FormLayout): 
                if len(elems) == 1 or vertical:
                    e = ext_elems.DetailMainPanel(lh,name,vertical,*elems,**pkw)
                else:
                    e = ext_elems.TabPanel(lh,name,*elems,**pkw)
            else:
                raise Exception("No element class for layout %r" % lh.layout)
            #~ actions.loosen_requirements(e,**lh.layout._actor.required)
            #~ e.debug_permissions = True
            return e
        return ext_elems.Panel(lh,name,vertical,*elems,**pkw)

    def create_layout_element(self,lh,name,**kw):
        """
        Create a layout element from the named data element.
        """
        #~ if True: 
        if settings.LINO.catch_layout_exceptions: 
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
                if de.slave_grid_format == 'grid':
                    #~ if not de.parameters:
                    kw.update(hide_top_toolbar=True)
                    e = ext_elems.GridElement(lh,name,de,**kw)
                    return e
                elif de.slave_grid_format == 'summary':
                    # a Table in a DetailWindow, displayed as a summary in a HtmlBox 
                    o = dict(drop_zone="FooBar")
                    #~ a = de.get_action('insert')
                    a = de.insert_action
                    if a is not None:
                        kw.update(ls_insert_handler=js_code("Lino.%s" % a.full_name()))
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
                    if de.editable:
                        a = de.insert_action
                        if a is not None:
                            kw.update(ls_insert_handler=js_code("Lino.%s" % a.full_name()))
                            kw.update(ls_bbar_actions=[self.a2btn(a)])
                    field = fields.HtmlBox(verbose_name=de.label)
                    field.name = de.__name__
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
            #~ logger.info("20121023 create_layout_element %r",lh.layout._actor)
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

  
    def get_urls(self):
        #~ print "20121110 get_urls"
        rx = '^'
        urlpatterns = patterns('',
            (rx+'$', views.AdminIndex.as_view()),
            (rx+r'api/main_html$', views.MainHtml.as_view()),
            (rx+r'auth$', views.Authenticate.as_view()),
            (rx+r'grid_config/(?P<app_label>\w+)/(?P<actor>\w+)$', views.GridConfig.as_view()),
            (rx+r'api/(?P<app_label>\w+)/(?P<actor>\w+)$', views.ApiList.as_view()),
            (rx+r'api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$', views.ApiElement.as_view()),
            (rx+r'restful/(?P<app_label>\w+)/(?P<actor>\w+)$', views.Restful.as_view()),
            (rx+r'restful/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$', views.Restful.as_view()),
            (rx+r'choices/(?P<app_label>\w+)/(?P<rptname>\w+)$', views.Choices.as_view()),
            (rx+r'choices/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<fldname>\w+)$', views.Choices.as_view()),
        )
        urlpatterns += settings.LINO.get_urls()
        if settings.LINO.use_eid_applet:
            urlpatterns += patterns('',
                (rx+r'eid-applet-service$', views.EidAppletService.as_view()),
            )
        if settings.LINO.use_jasmine:
            urlpatterns += patterns('',
                (rx+r'run-jasmine$', views.RunJasmine.as_view()),
            )
        if settings.LINO.use_tinymce:
            urlpatterns += patterns('',
                (rx+r'templates/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>\w+)/(?P<fldname>\w+)$', 
                    views.Templates.as_view()),
                (rx+r'templates/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>\w+)/(?P<fldname>\w+)/(?P<tplname>\w+)$', 
                    views.Templates.as_view()),
            )

        return urlpatterns
        
    def get_media_urls(self):
        #~ print "20121110 get_urls"
        urlpatterns = []
        from os.path import exists, join, abspath, dirname
        
        logger.info("Checking /media URLs ")
        prefix = settings.MEDIA_URL[1:]
        assert prefix.endswith('/')
        
        def setup_media_link(short_name,attr_name=None,source=None):
            target = join(settings.MEDIA_ROOT,short_name)
            if exists(target):
                return
            if attr_name:
                source = getattr(settings.LINO,attr_name)
                if not source:
                    raise Exception(
                      "%s does not exist and LINO.%s is not set." % (
                      target,attr_name))
            if not exists(source):
                raise Exception("LINO.%s (%s) does not exist" % (attr_name,source))
            if is_devserver():
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
        if settings.LINO.use_jasmine:
            setup_media_link('jasmine','jasmine_root')
        if settings.LINO.use_extensible:
            setup_media_link('extensible','extensible_root')
        if settings.LINO.use_tinymce:
            setup_media_link('tinymce','tinymce_root')
        if settings.LINO.use_eid_jslib:
            setup_media_link('eid-jslib','eid_jslib_root')
            
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
        
    def html_page_lines(self,request,title=None,on_ready='',run_jasmine=False):
        """Generates the lines of Lino's HTML reponse.
        """
        #~ logger.info("20121003 html_page_lines %r",on_ready)
        yield '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
        yield '<html><head>'
        yield '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
        yield '<title id="title">%s</title>' % settings.LINO.title or settings.LINO.short_name
        
        def stylesheet(*args):
            url = self.media_url(*args) #  + url
            return '<link rel="stylesheet" type="text/css" href="%s" />' % url
        def javascript(url):
            url = self.media_url() + url
            return '<script type="text/javascript" src="%s"></script>' % url
            
        if run_jasmine: 
            yield stylesheet("jasmine","jasmine.css")
        yield stylesheet('extjs','resources','css','ext-all.css')
        
        #~ yield '<!-- overrides to base library -->'
        
        if settings.LINO.use_extensible:
            yield stylesheet("extensible","resources","css","extensible-all.css")
          
        if settings.LINO.use_vinylfox:
            yield stylessheet('/lino/vinylfox/resources/css/htmleditorplugins.css')
            #~ p = self.media_url() + '/lino/vinylfox/resources/css/htmleditorplugins.css'
            #~ yield '<link rel="stylesheet" type="text/css" href="%s" />' % p
          
        if settings.LINO.use_filterRow:
            #~ p = self.media_url() + '/lino/filterRow'
            #~ yield '<link rel="stylesheet" type="text/css" href="%s/filterRow.css" />' % p
            yield stylesheet('lino','filterRow','filterRow.css')
            
        if settings.LINO.use_gridfilters:
            #~ yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/statusbar/css/statusbar.css" />' % self.media_url() 
            #~ yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/gridfilters/css/GridFilters.css" />' % self.media_url() 
            #~ yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/gridfilters/css/RangeMenu.css" />' % self.media_url() 
            yield stylesheet("extjs","examples","ux","statusbar","css/statusbar.css")
            yield stylesheet("extjs","examples","ux","gridfilters","css/GridFilters.css")
            yield stylesheet("extjs","examples","ux","gridfilters","css","RangeMenu.css")
            
        yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/fileuploadfield/css/fileuploadfield.css" />' % self.media_url() 
        
        #~ yield '<link rel="stylesheet" type="text/css" href="%s/lino/extjs/lino.css">' % self.media_url()
        yield stylesheet("lino","extjs","lino.css")
        
        if settings.LINO.use_awesome_uploader:
            yield '<link rel="stylesheet" type="text/css" href="%s/lino/AwesomeUploader/AwesomeUploader.css">' % self.media_url()
            yield '<link rel="stylesheet" type="text/css" href="%s/lino/AwesomeUploader/AwesomeUploader Progress Bar.css">' % self.media_url()
         
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
            #~ yield '<script type="text/javascript" src="%s/tiny_mce.js"></script>' % p
            yield javascript("/tinymce/tiny_mce.js")
            #~ yield '<script type="text/javascript" src="%s/lino/tinymce/Ext.ux.TinyMCE.js"></script>' % self.media_url()
            yield javascript("/lino/tinymce/Ext.ux.TinyMCE.js")
            yield '''<script language="javascript" type="text/javascript">
tinymce.init({
        theme : "advanced"
        // , mode : "textareas"
});
</script>'''

        #~ yield '<script type="text/javascript" src="%s/lino/extjs/Ext.ux.form.DateTime.js"></script>' % self.media_url()
        yield javascript("/lino/extjs/Ext.ux.form.DateTime.js")
        
        if run_jasmine: # settings.LINO.use_jasmine:
            yield javascript("/jasmine/jasmine.js")
            yield javascript("/jasmine/jasmine-html.js")
            
            yield javascript("/lino/jasmine/specs.js")
            
        if settings.LINO.use_eid_jslib:
            yield javascript('/eid-jslib/be_belgium_eid.js')
            yield javascript('/eid-jslib/hellerim_base64.js')
            
            
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
            self.build_js_cache_for_profile(user.profile,False)
        yield '<script type="text/javascript" src="%s"></script>' % (
            self.media_url(*self.lino_js_parts(user.profile)))
            
        #~ yield '<!-- page specific -->'
        yield '<script type="text/javascript">'

        yield 'Ext.onReady(function(){'
        
        #~ yield "console.time('onReady');"
        
        if request.user.profile.authenticated:
          
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
                    #~ for u in users.User.objects.exclude(profile=dd.UserProfiles.blank_item)] 20120829
                    #~ for u in users.User.objects.filter(profile__isnull=False)]
                    for u in users.User.objects.exclude(profile='').exclude(id=user.id)]
                    #~ for u in users.User.objects.filter(profile__gte=dd.UserLevels.guest)]
            else:
                authorities = [(a.user.id,unicode(a.user)) 
                    for a in users.Authority.objects.filter(authorized=user)]
            
            #~ handler = self.ext_renderer.instance_handler(user)
            #~ a = users.MySettings.get_url_action('default_action')
            a = users.MySettings.default_action
            handler = self.ext_renderer.action_call(None,a,dict(record_id=user.pk))
            handler = "function(){%s}" % handler
            mysettings = dict(text=_("My settings"),handler=js_code(handler))
            login_menu_items = [mysettings]
            if len(authorities):
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
                
                login_menu_items.insert(0,act_as)
                #~ login_menu_items = [act_as,mysettings]
                
            if settings.LINO.remote_user_header is None:
                login_menu_items.append(dict(text=_("Log out"),handler=js_code('Lino.logout')))
                login_menu_items.append(dict(text=_("Change password"),handler=js_code('Lino.change_password')))
                login_menu_items.append(dict(text=_("Forgot password"),handler=js_code('Lino.forgot_password')))
            
            login_menu = dict(
                text=user_text,
                menu=dict(items=login_menu_items))
            #~ else:
                #~ login_menu = dict(text=user_text,handler=js_code(handler))
                
            #~ yield "Lino.login_menu = %s;" % py2js(login_menu)
            #~ yield "Lino.main_menu = Lino.main_menu.concat(['->',Lino.login_menu]);"
            yield "Lino.main_menu = Lino.main_menu.concat(['->',%s]);" % py2js(login_menu)
                
        elif settings.LINO.user_model is not None: # 20121103
            login_buttons = [
              #~ dict(xtype="textfield",emptyText=_('Enter your username')),
              #~ dict(xtype="textfield",emptyText=_('Enter your password'),inputType="password"),
              dict(xtype="button",text="Login",handler=js_code('Lino.show_login_window')),
              #~ dict(xtype="button",text="Register",handler=Lino.register),
              ]
            yield "Lino.main_menu = Lino.main_menu.concat(['->',%s]);" % py2js(login_buttons)
                
                
        
        #~ yield "Lino.load_mask = new Ext.LoadMask(Ext.getBody(), {msg:'Immer mit der Ruhe...'});"
          
        main=dict(
          id="main_area",
          xtype='container',
          region="center",
          autoScroll=True,
          layout='fit'
        )
        
        if not on_ready:
            #~ print "20121115 foo"
            main.update(html=settings.LINO.get_main_html(request))
        
        win = dict(
          layout='fit',
          #~ maximized=True,
          items=main,
          #~ closable=False,
          bbar=dict(xtype='toolbar',items=js_code('Lino.status_bar')),
          #~ title=self.site.title,
          tbar=js_code('Lino.main_menu'),
        )
        jsgen.set_for_user_profile(request.user.profile)
        for ln in jsgen.declare_vars(win):
            yield ln
        #~ yield '  new Ext.Viewport({layout:"fit",items:%s}).render("body");' % py2js(win)
        #~ yield '  Lino.body_loadMask = new Ext.LoadMask(Ext.getBody(),{msg:"Please wait..."});'
        #~ yield '  Lino.body_loadMask.show();'
        yield '  Lino.viewport = new Lino.Viewport({items:%s});' % py2js(win)
        
        if run_jasmine: # settings.LINO.use_jasmine:
            yield '  jasmine.getEnv().addReporter(new jasmine.TrivialReporter());'
            yield '  jasmine.getEnv().execute();'
        else:
            yield '  Lino.viewport.render("body");'
        
            
            yield on_ready
        #~ for ln in on_ready:
            #~ yield ln
        
        #~ yield "console.timeEnd('onReady');"
        yield "}); // end of onReady()"
        yield '</script></head><body>'

        if settings.LINO.use_eid_jslib:
            p = self.media_url('eid-jslib')
            #~ print p
            yield '<applet code="org.jdesktop.applet.util.JNLPAppletLauncher"'
            yield 'codebase = "%s/"' % p
            yield 'width="1" height="1"'
            yield 'name   = "BEIDAppletLauncher"'
            yield 'id   = "BEIDAppletLauncher"'
            yield 'archive="applet-launcher.jar,beid35libJava.jar,BEID_Applet.jar">'
    
            yield '<param name="codebase_lookup" value="false">'
            yield '<param name="subapplet.classname" value="be.belgium.beid.BEID_Applet">'
            yield '<param name="progressbar" value="true">'
            yield '<param name="jnlpNumExtensions" value="1">'
            yield '<param name="jnlpExtension1" value= "' + p + '/beid.jnlp">'

            yield '<param name="debug" value="false"/>'
            yield '<param name="Reader" value=""/>'
            yield '<param name="OCSP" value="-1"/>'
            yield '<param name="CRL" value="-1"/>'
            yield '<param name="jnlp_href" value="' + p + '/beid_java_plugin.jnlp" />'
            yield '</applet>'


          
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
            #~ yield "STRENGTH_CHOICES = %s;" % py2js(list(STRENGTH_CHOICES))
            #~ yield "KNOWLEDGE_CHOICES = %s;" % py2js(list(KNOWLEDGE_CHOICES))
            yield "MEDIA_URL = %r;" % (self.media_url())
            yield "ADMIN_URL = %r;" % settings.LINO.admin_url
            #~ if settings.LINO.admin_url:
                #~ yield "ADMIN_URL = '/%s';" % settings.LINO.admin_url
            #~ else:
                #~ yield "ADMIN_URL = '';" 
            
            #~ yield "API_URL = %r;" % self.build_url('api')
            #~ yield "TEMPLATES_URL = %r;" % self.build_url('templates')
            #~ yield "Lino.status_bar = new Ext.ux.StatusBar({defaultText:'Lino version %s.'});" % lino.__version__
        
        #~ return '\n'.join([ln for ln in fn()])
        return '\n'.join(fn())



    #~ def parse_params(self,rh,request):
        #~ return rh.store.parse_params(request)
        
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
            
    def lino_js_parts(self,profile):
        return ('cache','js','lino_' + profile.value + '_' + translation.get_language()+'.js')
        
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
            for lang in langs:
                babel.set_language(lang)
                for profile in dd.UserProfiles.objects():
                    count += self.build_js_cache_for_profile(profile,force)
            #~ qs = users.User.objects.exclude(profile='')
            #~ for lang in langs:
                #~ babel.set_language(lang)
                #~ for user in qs:
                    #~ count += self.build_js_cache_for_user(user,force)
            babel.set_language(None)
                
            logger.info("%d lino*.js files have been built in %s seconds.",
                count,time.time()-started)
          
    #~ def build_js_cache_for_user(self,user,force=False):
    def build_js_cache_for_profile(self,profile,force):
        """
        Build the lino*.js file for the specified user and the current language.
        If the file exists and is up to date, don't generate it unless 
        `force=False` is specified.
        
        This is called 
        - on each request if :attr:`lino.Lino.build_js_cache_on_startup` is `False`.
        - with `force=True` by :class:`lino.models.BuildSiteCache`
        """
        jsgen.set_for_user_profile(profile)
        
        fn = os.path.join(settings.MEDIA_ROOT,*self.lino_js_parts(profile)) 
        if not force and os.path.exists(fn):
            mtime = os.stat(fn).st_mtime
            if mtime > settings.LINO.mtime:
                #~ if not user.modified or user.modified < datetime.datetime.fromtimestamp(mtime):
                logger.debug("%s is up to date.",fn)
                return 0
                    
        logger.info("Building %s ...", fn)
        makedirs_if_missing(os.path.dirname(fn))
        f = codecs.open(fn,'w',encoding='utf-8')
        try:
            self.write_lino_js(f,profile)
            #~ f.write(jscompress(js))
            f.close()
            return 1
        except Exception, e:
            """
            If some error occurs, remove the partly generated file 
            to make sure that Lino will try to generate it again 
            (and report the same error message) on next request.
            """
            f.close()
            os.remove(fn)
            raise
        #~ logger.info("Wrote %s ...", fn)
            
    #~ def write_lino_js(self,f,user):
    def write_lino_js(self,f,profile):
        
        tpl = self.linolib_template()
        
        messages = set()
        def mytranslate(s):
            messages.add(s)
            return _(s)
        tpl._ = mytranslate
        f.write(jscompress(unicode(tpl)+'\n'))
        
        """
        Make the dummy messages file.
        But only when generating for root user.
        """
        if jsgen._for_user_profile == dd.UserProfiles.admin:
            make_dummy_messages_file(self.linolib_template_name(),messages)
        
        #~ assert user == jsgen._for_user
        assert profile == jsgen._for_user_profile
        
        f.write("Lino.main_menu = %s;\n" % py2js(settings.LINO.get_site_menu(self,profile)))

        actors_list = [
            rpt for rpt in dbtables.master_reports \
               + dbtables.slave_reports \
               + dbtables.generic_slaves.values() \
               + dbtables.custom_tables \
               + dbtables.frames_list ]
               
        actors_list.extend(choicelists.CHOICELISTS.values())
               
        """
        Call Ext.namespace for *all* actors because e.g. outbox.Mails.FormPanel 
        is defined in ns outbox.Mails which is not directly used by non-expert users.
        """
        for a in actors_list:
            f.write("Ext.namespace('Lino.%s')\n" % a)
                
        #~ assert user == jsgen._for_user
        assert profile == jsgen._for_user_profile
        
        """
        actors with their own `get_handle_name` don't have a js implementation
        """
        #~ print '20120605 dynamic actors',[a for a in actors_list if a.get_handle_name is not None]
        actors_list = [a for a in actors_list if a.get_handle_name is None]

        #~ new_actors_list = []
        #~ for a in actors_list:
            #~ if a.get_view_permission(jsgen._for_user_profile):
                #~ new_actors_list.append(a)
        #~ actors_list = new_actors_list
        
        actors_list = [a for a in actors_list if a.get_view_permission(jsgen._for_user_profile)]
        
        #~ actors_list = [a for a in actors_list if a.get_view_permission(jsgen._for_user)]
          
        f.write("\n// ChoiceLists: \n")
        for a in choicelists.CHOICELISTS.values():
            #~ if issubclass(a,choicelists.ChoiceList):
            f.write("Lino.%s = %s;\n" % (a.actor_id,py2js(a.get_choices())))
                
        #~ logger.info('20120120 dbtables.all_details:\n%s',
            #~ '\n'.join([str(d) for d in dbtables.all_details]))
        
        form_panels = set()
        param_panels = set()
        action_param_panels = set()
        def add(res,collector,fl,formpanel_name):
            # fl : a FormLayout
            if fl is not None:
                lh = fl.get_layout_handle(self)
                for e in lh.main.walk():
                    e.loosen_requirements(res)
                if fl in collector:
                    pass
                    #~ fl._using_actors.append(actor)
                else:
                    fl._formpanel_name = formpanel_name
                    #~ fl._using_actors = [actor]
                    collector.add(fl)
                    
        #~ assert user == jsgen._for_user
        assert profile == jsgen._for_user_profile
        
        for res in actors_list:
            add(res,form_panels,res.detail_layout, "%s.DetailFormPanel" % res)
            add(res,form_panels,res.insert_layout, "%s.InsertFormPanel" % res)
            add(res,param_panels,res.params_layout, "%s.ParamsPanel" % res)
            
            for ba in res.get_actions():
                if ba.action.parameters:
                    add(res,action_param_panels,ba.action.params_layout, 
                      "%s.%s_ActionFormPanel" % (res,ba.action.action_name))

        if False:
            logger.debug('FormPanels')
            for fl in details:
                logger.debug('- ' + fl._formpanel_name + ' : ' + ','.join([a.actor_id for a in fl._using_actors]))
            
        #~ f.write('\n/* Application FormPanel subclasses */\n')
        for fl in param_panels:
            lh = fl.get_layout_handle(self)
            for ln in self.js_render_ParamsPanelSubclass(lh):
                f.write(ln + '\n')
                
        for fl in action_param_panels:
            lh = fl.get_layout_handle(self)
            for ln in self.js_render_ActionFormPanelSubclass(lh):
                f.write(ln + '\n')
                
        for fl in form_panels:
            lh = fl.get_layout_handle(self)
            for ln in self.js_render_FormPanelSubclass(lh):
                f.write(ln + '\n')
        
        actions_written = set()
        for rpt in actors_list:
            rh = rpt.get_handle(self) 
            for ba in rpt.get_actions():
                if ba.action.parameters:
                    if not ba.action in actions_written:
                        #~ logger.info("20121005 %r is not in %r",a,actions_written)
                        actions_written.add(ba.action)
                        for ln in self.js_render_window_action(rh,ba,profile):
                            f.write(ln + '\n')
          
        for rpt in actors_list:
            rh = rpt.get_handle(self) 
            if isinstance(rpt,type) and issubclass(rpt,(tables.AbstractTable,choicelists.ChoiceList)):
                #~ if rpt.model is None:
                #~ f.write('// 20120621 %s\n' % rpt)
                    #~ continue
                
                for ln in self.js_render_GridPanel_class(rh):
                    f.write(ln + '\n')
                
            #~ for a in rpt.get_actions():
                #~ if a.opens_a_window or a.parameters:
                    #~ if isinstance(a,(actions.ShowDetailAction,actions.InsertRow)):
                        #~ for ln in self.js_render_detail_action_FormPanel(rh,a):
                              #~ f.write(ln + '\n')
                    #~ for ln in self.js_render_window_action(rh,a,user):
                        #~ f.write(ln + '\n')
                #~ elif a.custom_handler:
                    #~ for ln in self.js_render_custom_action(rh,a,user):
                        #~ f.write(ln + '\n')
        
            for ba in rpt.get_actions():
                if ba.action.parameters:
                    pass
                elif ba.action.opens_a_window:
                    if isinstance(ba.action,(actions.ShowDetailAction,actions.InsertRow)):
                        for ln in self.js_render_detail_action_FormPanel(rh,ba):
                              f.write(ln + '\n')
                    for ln in self.js_render_window_action(rh,ba,profile):
                        f.write(ln + '\n')
                #~ elif a.show_in_workflow:
                elif ba.action.custom_handler:
                    for ln in self.js_render_custom_action(rh,ba):
                        f.write(ln + '\n')
            
        
        #~ assert user == jsgen._for_user
        assert profile == jsgen._for_user_profile
        
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
        if h.actor.is_abstract():
            return
            
        #~ logger.info('20121010 ExtUI.setup_handle() %s',h.actor)
            
        if isinstance(h,tables.TableHandle):
            #~ if issubclass(h.actor,dbtables.Table):
            ll = layouts.ListLayout(h.actor.get_column_names(ar),h.actor,hidden_elements=h.actor.hidden_columns)
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
          
                
                      
    def source_dir(self):
        return os.path.abspath(os.path.dirname(__file__))
        
    def a2btn(self,ba,**kw):
        a = ba.action
        if a.parameters:
            kw.update(panel_btn_handler=js_code("Lino.param_action_handler(Lino.%s)" % ba.full_name()))
        elif isinstance(a,actions.SubmitDetail):
            #~ kw.update(tabIndex=1)
            js = 'function(panel){panel.save(null,%s,%r)}' % (
                py2js(a.switch_to_detail),a.action_name)
            kw.update(panel_btn_handler=js_code(js))
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
        elif isinstance(a,actions.RowAction):
            #~ if a.url_action_name is None:
                #~ raise Exception("Action %r has no url_action_name" % a)
            kw.update(must_save=True)
            kw.update(
              panel_btn_handler=js_code("Lino.row_action_handler(%r)" % a.action_name))
              #~ panel_btn_handler=js_code("Lino.row_action_handler(%r)" % a.url_action_name))
        elif isinstance(a,actions.ListAction):
            #~ if a.url_action_name is None:
                #~ raise Exception("Action %r has no url_action_name" % a)
            #~ kw.update(
              #~ panel_btn_handler=js_code("Lino.list_action_handler(%r)" % a.action_name))
            kw.update(panel_btn_handler=js_code(ba.get_panel_btn_handler(self)))
            kw.update(must_save=True)
        else:
            kw.update(panel_btn_handler=js_code("Lino.%s" % a))
            
        if a.icon_name:
            kw.update(iconCls=a.icon_name) # 'x-tbar-delete'
        else:
            kw.update(text=a.label)
        kw.update(
          #~ name=a.name,
          menu_item_text=a.label,
          overflowText=a.label,
          auto_save=a.auto_save,
          itemId=a.action_name,
          #~ text=unicode(a.label),
        )
        if a.help_text:
            kw.update(tooltip=a.help_text)
        elif a.icon_name:
            kw.update(tooltip=a.label)
        return kw
        
    def build_on_render(self,main):
        "dh is a FormLayout or a ListLayout"
        on_render = []
        elems_by_field = {}
        field_elems = []
        for e in main.active_children:
            if isinstance(e,ext_elems.FieldElement):
                if e.get_view_permission(jsgen._for_user_profile):
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
        
        
      
    #~ def js_render_ParamsPanelSubclass(self,dh,user):
    def js_render_ParamsPanelSubclass(self,dh):
        tbl = dh.layout._actor
        
        yield ""
        #~ yield "Lino.%s = Ext.extend(Lino.FormPanel,{" % dh.layout._formpanel_name
        yield "Lino.%s = Ext.extend(Ext.form.FormPanel,{" % dh.layout._formpanel_name
        for k,v in dh.main.ext_options().items():
            if k != 'items':
                yield "  %s: %s," % (k,py2js(v))
        #~ yield "  layout: 'fit',"
        #~ yield "  auto_save: true,"
        if dh.layout.window_size and dh.layout.window_size[1] == 'auto':
            yield "  autoHeight: true,"
        yield "  initComponent : function() {"
        yield "    var containing_panel = this;"
        lc = 0
        for ln in jsgen.declare_vars(dh.main.elements):
            yield "    " + ln
            lc += 1
        if lc == 0:
            raise Exception("%r of %s has no variables" % (dh.main,dh))
        yield "    this.items = %s;" % py2js(dh.main.elements)
        yield "    this.fields = %s;" % py2js(
          [e for e in dh.main.walk() if isinstance(e,ext_elems.FieldElement)])
        yield "    Lino.%s.superclass.initComponent.call(this);" % dh.layout._formpanel_name
        yield "  }"
        yield "});"
        yield ""
      
    #~ def js_render_ActionFormPanelSubclass(self,dh,user):
    def js_render_ActionFormPanelSubclass(self,dh):
        tbl = dh.layout._actor
        #~ logger.info("20121007 js_render_ActionFormPanelSubclass %s",dh.layout._formpanel_name)
        yield ""
        yield "Lino.%s = Ext.extend(Lino.ActionFormPanel,{" % dh.layout._formpanel_name
        for k,v in dh.main.ext_options().items():
            if k != 'items':
                yield "  %s: %s," % (k,py2js(v))
        if tbl.action_name is None:
            raise Exception("20121009 action_name of %r is None" % tbl)
        yield "  action_name: '%s'," % tbl.action_name
        yield "  window_title: %s," % py2js(tbl.label)
        #~ yield "  layout: 'fit',"
        #~ yield "  auto_save: true,"
        if dh.layout.window_size and dh.layout.window_size[1] == 'auto':
            yield "  autoHeight: true,"
        yield "  initComponent : function() {"
        yield "    var containing_panel = this;"
        lc = 0
        for ln in jsgen.declare_vars(dh.main.elements):
            yield "    " + ln
            lc += 1
        # 20121116
        #~ if lc == 0:
            #~ raise Exception("%s (%r of %s) has no variables" % (dh.layout._formpanel_name,dh.main,dh))
        yield "    this.items = %s;" % py2js(dh.main.elements)
        yield "    this.fields = %s;" % py2js(
          [e for e in dh.main.walk() if isinstance(e,ext_elems.FieldElement)])
        yield "    Lino.%s.superclass.initComponent.call(this);" % dh.layout._formpanel_name
        yield "  }"
        yield "});"
        yield ""
      
    #~ def js_render_FormPanelSubclass(self,dh,user):
    def js_render_FormPanelSubclass(self,dh):
        
        tbl = dh.layout._actor
        if not dh.main.get_view_permission(jsgen._for_user_profile):
            msg = "No view permission for main panel of %s :" % dh.layout._formpanel_name
            msg += " actor %s requires %s, but main requires %s)" % (tbl,tbl.required,dh.main.required)
            raise Exception(msg)
        
        yield ""
        yield "Lino.%s = Ext.extend(Lino.FormPanel,{" % dh.layout._formpanel_name
        yield "  layout: 'fit',"
        yield "  auto_save: true,"
        if dh.layout.window_size and dh.layout.window_size[1] == 'auto':
            yield "  autoHeight: true,"
        if settings.LINO.is_installed('contenttypes') and issubclass(tbl,dbtables.Table):
            yield "  content_type: %s," % py2js(ContentType.objects.get_for_model(tbl.model).pk)
        if not tbl.editable:
            yield "  disable_editing: true," 
        yield "  initComponent : function() {"
        yield "    var containing_panel = this;"
        lc = 0
        for ln in jsgen.declare_vars(dh.main):
            yield "    " + ln
            lc += 1
        if lc == 0:
            raise Exception("%r of %s has no variables" % (dh.main,dh))
        yield "    this.items = %s;" % dh.main.as_ext()
        #~ if issubclass(tbl,tables.AbstractTable):
        if True:
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
            yield "      Lino.%s.superclass.onRender.call(this, ct, position);" % dh.layout._formpanel_name
            yield "    }"

        #~ yield "    Lino.%s.FormPanel.superclass.initComponent.call(this);" % tbl
        yield "    Lino.%s.superclass.initComponent.call(this);" % dh.layout._formpanel_name
        
        if tbl.active_fields:
        #~ if issubclass(tbl,tables.AbstractTable) and tbl.active_fields:
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
        #~ logger.info('20121005 js_render_detail_action_FormPanel(%s,%s)',rpt,action.full_name(rpt))
        yield ""
        #~ yield "// js_render_detail_action_FormPanel %s" % action
        dtl = action.get_window_layout()
        #~ dtl = rpt.detail_layout
        if dtl is None:
            raise Exception("action %s without detail?" % action.full_name())
        #~ yield "Lino.%sPanel = Ext.extend(Lino.%s.FormPanel,{" % (action,dtl._actor)
        yield "Lino.%sPanel = Ext.extend(Lino.%s,{" % (action.full_name(),dtl._formpanel_name)
        yield "  empty_title: %s," % py2js(action.get_button_label())
        #~ if not isinstance(action,actions.InsertRow):
        if action.action.hide_navigator:
            yield "  hide_navigator: true,"
            
        if rh.actor.params_panel_hidden:
            yield "  params_panel_hidden: true,"

        yield "  ls_bbar_actions: %s," % py2js([
            rh.ui.a2btn(ba) for ba in rpt.get_actions(action.action) 
                if ba.action.show_in_bbar and ba.get_view_permission(jsgen._for_user_profile)]) 
        yield "  ls_url: %s," % py2js(ext_elems.rpt2url(rpt))
        if action.action != rpt.default_action.action:
            yield "  action_name: %s," % py2js(action.action.action_name)
        #~ yield "  active_fields: %s," % py2js(rpt.active_fields)
        yield "  initComponent : function() {"
        a = rpt.detail_action
        if a:
            yield "    this.ls_detail_handler = Lino.%s;" % a.full_name()
        a = rpt.insert_action
        if a:
            yield "    this.ls_insert_handler = Lino.%s;" % a.full_name()
            
        yield "    Lino.%sPanel.superclass.initComponent.call(this);" % action.full_name()
        yield "  }"
        yield "});"
        yield ""
        
    #~ def js_render_GridPanel_class(self,rh,user):
    def js_render_GridPanel_class(self,rh):
        
        yield ""
        yield "// js_render_GridPanel_class %s" % rh
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
            rh.ui.a2btn(ba) 
              for ba in rh.actor.get_actions(rh.actor.default_action.action) 
                  if ba.action.show_in_bbar and ba.get_view_permission(jsgen._for_user_profile)])
        kw.update(ls_grid_configs=[gc.data for gc in rh.actor.grid_configs])
        kw.update(gc_name=ext_elems.DEFAULT_GC_NAME)
        #~ if action != rh.actor.default_action:
            #~ kw.update(action_name=action.name)
        #~ kw.update(content_type=rh.report.content_type)
        
        vc = dict(emptyText=_("No data to display."))
        if rh.actor.editable:
            vc.update(getRowClass=js_code('Lino.getRowClass'))
        kw.update(viewConfig=vc)
        
        
        if not rh.actor.editable:
            kw.update(disable_editing=True)
        if rh.actor.params_panel_hidden:
            kw.update(params_panel_hidden=True)
        
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
            yield "    this.ls_detail_handler = Lino.%s;" % a.full_name()
        #~ a = rh.actor.get_action('insert')
        a = rh.actor.insert_action
        if a:
            yield "    this.ls_insert_handler = Lino.%s;" % a.full_name()
        
        
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
      
            
    def js_render_custom_action(self,rh,action):
        """
        Defines the non-window action handler used by :meth:`row_action_button`
        """
        
        # 20120723 : removed useless js param "action"
        yield "Lino.%s = function(rp,pk) { " % action.full_name()
        #~ panel = "Lino.%s.GridPanel.ls_url" % action 
        url = ext_elems.rpt2url(rh.actor)
        yield "  Lino.run_row_action(rp,%s,pk,%s);" % (
            py2js(url),py2js(action.action.action_name))
        yield "};"


    #~ def js_render_window_action(self,rh,action,user):
    def js_render_window_action(self,rh,action,profile):
      
        rpt = rh.actor
        
        if rpt.parameters and action.action.use_param_panel:
            params_panel = rh.params_layout_handle
        else:
            params_panel = None
        
        if isinstance(action.action,actions.ShowDetailAction):
            mainPanelClass = "Lino.%sPanel" % action.full_name()
        elif isinstance(action.action,actions.InsertRow): 
            mainPanelClass = "Lino.%sPanel" % action.full_name()
        elif isinstance(action.action,actions.GridEdit):
            mainPanelClass = "Lino.%s.GridPanel" % rpt
            #~ if rh.actor.parameters:
                #~ params_panel = rh.params_layout_handle.main
        elif isinstance(action.action,CalendarAction):
            mainPanelClass = "Lino.CalendarPanel"
            #~ mainPanelClass = "Lino.CalendarAppPanel"
            #~ mainPanelClass = "Ext.ensible.cal.CalendarPanel"
        elif action.action.parameters:
            #~ mainPanelClass = "Lino.ActionParamsPanel"
            params_panel = action.action.make_params_layout_handle(self)
            #~ logger.info("20121003 %r %s", action, params_panel)
        else:
            return 
        #~ if action.defining_actor is None:
            #~ raise Exception("20120524 %s %r actor is None" % (rh.actor,action))
        windowConfig = dict()
        wl = action.get_window_layout()
        #~ if action.action_name == 'wf1':
            #~ logger.info("20121005 %r --> %s",action,wl)
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
                
        yield "Lino.%s = new Lino.WindowAction(%s,function(){" % (action.full_name(),py2js(windowConfig))
        #~ yield "  console.log('20120625 fn');" 
        if isinstance(action.action,CalendarAction):
            yield "  return Lino.calendar_app.get_main_panel();"
        else:
            p = dict()
            if action.action is settings.LINO.get_main_action(profile):
                p.update(is_home_page=True)
            #~ yield "  var p = {};" 
            if action.action.hide_top_toolbar or action.actor.hide_top_toolbar or action.action.parameters:
                p.update(hide_top_toolbar=True)
                #~ yield "  p.hide_top_toolbar = true;" 
            if rpt.hide_window_title:
                #~ yield "  p.hide_window_title = true;" 
                p.update(hide_window_title=True)
            #~ yield "  p.is_main_window = true;" # workaround for problem 20111206
            p.update(is_main_window=True) # workaround for problem 20111206
            yield "  var p = %s;"  % py2js(p)
            #~ yield "  Lino.insert_subst_user(p);" # 20121010 : 
            #~ if isinstance(action,CalendarAction):
                #~ yield "  p.items = Lino.CalendarAppPanel_items;" 
            if params_panel:
                #~ for ln in jsgen.declare_vars(params_panel):
                    #~ yield '  '  + ln
                if action.action.parameters:
                    #~ yield "  return %s;" % params_panel
                    yield "  return new Lino.%s({});" % wl._formpanel_name
                else:
                    #~ yield "  p.params_panel = %s;" % params_panel
                    yield "  p.params_panel = new Lino.%s({});" % params_panel.layout._formpanel_name
                    yield "  return new %s(p);" % mainPanelClass
            else:
                yield "  return new %s(p);" % mainPanelClass
        #~ yield "  console.log('20120625 rv is',rv);" 
        #~ yield "  return rv;"
        yield "});" 
        
    
    def table2xhtml(self,ar,max_row_count=300):
        doc = xghtml.Document(force_unicode(ar.get_title()))
        t = doc.add_table()
        self.ar2html(ar,t,ar.data_iterator)
        return xghtml.E.tostring(t.as_element())
        
    def ar2html(self,ar,tble,data_iterator):
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
          
        if True:
            #~ print 20120901, ar.order_by
            for i,e in enumerate(columns):
                if e.sortable and ar.order_by != [e.name]:
                    kw = {ext_requests.URL_PARAM_SORT:e.name}
                    url = ar.renderer.get_request_url(ar,**kw)
                    if url is not None:
                        headers[i] = xghtml.E.a(headers[i],href=url)
        
        sums  = [fld.zero for fld in fields]
        #~ cellattrs = dict(align="center",valign="middle",bgcolor="#eeeeee")
        cellattrs = dict(align="left",valign="top",bgcolor="#eeeeee")
        hr = tble.add_header_row(*headers,**cellattrs)
        if cellwidths:
            for i,td in enumerate(hr): 
                td.attrib.update(width=cellwidths[i])
        #~ print 20120623, ar.actor
        recno = 0
        for row in data_iterator:
            recno += 1
            cells = [x for x in ar.ah.store.row2html(ar,fields,row,sums)]
            #~ print 20120623, cells
            tble.add_body_row(*cells,**cellattrs)
            
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
                tble.add_body_row(*ar.ah.store.sums2html(ar,fields,sums),**cellattrs)
            
            
            
    

    def row_action_button(self,*args,**kw):
        """
        See :meth:`ExtRenderer.row_action_button`
        """
        return self.ext_renderer.row_action_button(*args,**kw)


    def unused_action_url_http(self,action,*args,**kw):
        #~ if not action is action.actor.default_action:
        if action != action.actor.default_action:
            kw.update(an=action.name)
        return self.build_url("api",action.actor.app_label,action.actor.__name__,*args,**kw)
            
