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


#~ from north.babel import LANGUAGE_CHOICES
from lino.modlib.cal.utils import CalendarAction

from django.db import models
from django.conf import settings
from django.http import HttpResponse, Http404
from django.utils import functional
from django.utils import translation
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
from lino.ui import elems as ext_elems
from lino.ui import store as ext_store
from lino.ui.render import HtmlRenderer

from lino import dd
from lino.core import actions 
#~ from lino.core.actions import action2str
from lino.core import dbtables
from lino.core import layouts
from lino.core import tables
#~ from lino.utils.xmlgen import xhtml as xhg
#~ from lino.core.dbutils import makedirs_if_missing
#~ from lino.core.dbutils import full_model_name
    
from lino.utils import AttrDict
from lino.utils import choosers
from lino.core import choicelists
from lino.core import menus
from lino.utils import jsgen
from lino.utils.jsgen import py2js, js_code, id2js
from lino.utils.xmlgen import html as xghtml
from lino.utils.xmlgen.html import E
from lino.utils.config import make_dummy_messages_file

if False:
    from lino.utils.jscompressor import JSCompressor
    jscompress = JSCompressor().compress
else:    
    def jscompress(s): return s
      
from lino.mixins import printable


if settings.SITE.user_model:
    from lino.modlib.users import models as users

AFTER_20130725 = True
USE_DAVLINK_JNLP = False

#~ from lino.utils.choicelists import DoYouLike, HowWell
#~ STRENGTH_CHOICES = DoYouLike.get_choices()
#~ KNOWLEDGE_CHOICES = HowWell.get_choices()

#~ NOT_GIVEN = object()



def prepare_label(mi):
    return mi.label
    """
    The original idea doesn't work any more with lazy translation.
    See `/blog/2011/1112`
    """
    #~ label = unicode(mi.label) # trigger translation
    #~ n = label.find(mi.HOTKEY_MARKER)
    #~ if n != -1:
        #~ label = label.replace(mi.HOTKEY_MARKER,'')
        #~ #label=label[:n] + '<u>' + label[n] + '</u>' + label[n+1:]
    #~ return label
    



class ExtRenderer(HtmlRenderer):
    """
    A HTML renderer that uses the ExtJS Javascript toolkit.
    
    """
    is_interactive = True
    
    def __init__(self,ui):
        HtmlRenderer.__init__(self,ui)
        jsgen.register_converter(self.py2js_converter)
        
        
        
        for s in 'green blue red yellow'.split():
            self.row_classes_map[s] = 'x-grid3-row-%s' % s
        
        
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
        if v is settings.SITE.LANGUAGE_CHOICES:
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
            if v.instance is not None:
                h = self.instance_handler(None,v.instance)
                assert h is not None
                js = "function() {%s}" % h
                return self.handler_item(v,js,None)
                #~ handler = "function(){%s}" % self.instance_handler(v.instance)
                #~ return dict(text=prepare_label(v),handler=js_code(handler))
              
                #~ url = self.get_detail_url(v.instance,an='detail')
                #~ url = self.get_detail_url(v.instance)
            elif v.bound_action is not None:
                if v.params:
                    ar = v.bound_action.request(**v.params)
                    js = self.request_handler(ar)
                else:
                    js = self.action_call(None,v.bound_action,{})
                js = "function() {%s}" % js
                return self.handler_item(v,js,v.help_text)
                
            elif v.javascript is not None:
                js = "function() {%s}" % v.javascript
                return self.handler_item(v,js,v.help_text)
            elif v.href is not None:
                url = v.href
            #~ elif v.request is not None:
                #~ raise Exception("20120918 request %r still used?" % v.request)
                #~ url = self.get_request_url(v.request)
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
        
        
    def get_action_status(self,ar,ba,obj,**kw):
        #~ logger.info("get_action_status %s",ba.full_name())
        if ba.action.parameters:
            if ba.action.params_layout.params_store is None:
                raise Exception("20121016 %s has no store" % ba.action.params_layout)
            kw.update(field_values=ba.action.params_layout.params_store.pv2dict(
                ba.action.action_param_defaults(ar,obj)))
        return kw
      
        
        
    def action_button(self,obj,ar,ba,label=None,**kw):
        """
        ``kw`` may contain additional html attributes like `style`
        """
        if ba.action.parameters:
            st = self.get_action_status(ar,ba,obj)
            #~ st.update(record_id=obj.pk)
            return self.window_action_button(ar.request,ba,st,label or ba.action.label,**kw)
        if ba.action.opens_a_window:
            st = ar.get_status()
            if obj is not None:
                st.update(record_id=obj.pk)
            return self.window_action_button(ar.request,ba,st,label or ba.action.label,**kw)
        return self.row_action_button(obj,ar.request,ba,label,**kw)
        
    def request_handler(self,ar,*args,**kw):
        st = ar.get_status(**kw)
        return self.action_call(ar.request,ar.bound_action,st)
        
    def window_action_button(self,request,ba,after_show={},label=None,title=None,**kw):
        """
        Return a HTML chunk for a button that will execute this 
        action using a *Javascript* link to this action.
        """
        label = unicode(label or ba.get_button_label())
        url = 'javascript:' + self.action_call(request,ba,after_show)
        #~ logger.info('20121002 window_action_button %s %r',a,unicode(label))
        return self.href_button_action(ba,url,label,title or ba.action.help_text,**kw)
        #~ if a.action.help_text:
            #~ return self.href_button(url,label,a.action.help_text)
        #~ return self.href_button(url,label)
        
    def row_action_button(self,obj,request,ba,label=None,title=None,**kw):
        """
        Return a HTML fragment that displays a button-like link 
        which runs the bound action `ba` when clicked.
        """
        #~ label = unicode(label or ba.get_button_label())
        label = label or ba.action.label
        if AFTER_20130725:
            #~ url = 'javascript:%s(%s)' % (ba.get_panel_btn_handler(),py2js(rp))
            #~ url = 'javascript:' + ba.get_js_call(request,obj)
            #~ url = 'javascript:' + self.action_call_on_instance(obj,request,ba,**kw) # until 20130905
            url = 'javascript:' + self.action_call_on_instance(obj,request,ba)
        else:
            if request is None:
                rp = None
            else:
                rp = request.requesting_panel
            url = 'javascript:Lino.%s(%s,%s)' % (
                    ba.full_name(),py2js(rp),py2js(obj.pk))
        #~ return self.href_button_action(ba,url,label,title or ba.action.help_text) # until 20130905
        return self.href_button_action(ba,url,label,title or ba.action.help_text,**kw)
        #~ if a.action.help_text:
            #~ return self.href_button(url,label,a.action.help_text)
        #~ return self.href_button(url,label)
        
    def action_call_on_instance(self,obj,request,ba,**st):
        if request is None:
            rp = None
        else:
            rp = request.requesting_panel
            
        if ba.action.opens_a_window or ba.action.parameters:
            ar = ba.request(request=request)
            #~ after_show = ar.get_status(settings.SITE.ui)
            st.update(self.get_action_status(ar,ba,obj))
            st.update(record_id=obj.pk)
            return "Lino.%s.run(%s,%s)" % (
              ba.full_name(),
              py2js(rp),
              py2js(st))
        # it's a custom ajax action generated by js_render_custom_action()
        return "Lino.%s(%s,%s)" % (ba.full_name(),py2js(rp),py2js(obj.pk))
        
    def action_call(self,request,bound_action,after_show):
        
        if bound_action.action.opens_a_window or bound_action.action.parameters:
            if request and request.subst_user:
                after_show[ext_requests.URL_PARAM_SUBST_USER] = request.subst_user
            if isinstance(bound_action.action,actions.ShowEmptyTable):
                after_show.update(record_id=-99998)
            if request is None:
                rp = None
            else:
                rp = request.requesting_panel
            if after_show:
                return "Lino.%s.run(%s,%s)" % (
                  bound_action.full_name(),
                  py2js(rp),
                  py2js(after_show))
            return "Lino.%s.run(%s)" % (bound_action.full_name(),py2js(rp))
        return "%s()" % self.get_panel_btn_handler(bound_action)

    def get_panel_btn_handler(self,ba):
        if ba.action.select_rows:
            h  = 'Lino.row_action_handler('
        else:
            h  = 'Lino.list_action_handler('
            #~ ls_url = '/' + ba.actor.app_label + '/' + ba.actor.__name__
            h += "'/%s/%s'," % (ba.actor.app_label,ba.actor.__name__)
        h += "'%s'" % ba.action.action_name
        h += ",'%s'" % ba.action.http_method
        if ba.action.preprocessor:
            h += "," + ba.action.preprocessor
        h += ")"
        return h 
        
    def row_action_handler(self,ba,obj,ar=None):
        if ar is None or ba.get_bound_action_permission(ar,obj,None):
            return self.action_call(None,ba,dict(record_id=obj.pk))
            
    def instance_handler(self,ar,obj):
        a = getattr(obj,'_detail_action',None)
        if a is None:
            a = obj.get_default_table().detail_action
        if a is not None:
            if ar is None or a.get_bound_action_permission(ar,obj,None):
                return self.action_call(None,a,dict(record_id=obj.pk))
                
    def obj2html(self,ar,obj,text=None):
        h = self.instance_handler(ar,obj)
        if text is None: text = force_unicode(obj)
        if h is None:
            return xghtml.E.b(text)
        url = 'javascript:' + h
        e = xghtml.E.a(text,href=url)
        #~ print 20130802, xghtml.E.tostring(e)
        return e
        
        
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
        return settings.SITE.build_admin_url("api",actor.app_label,actor.__name__,*args,**kw)
        
    def get_request_url(self,ar,*args,**kw):
        """
        Called from ActionRequest.absolute_url() used in `Team.eml.html`
        
        http://127.0.0.1:8000/api/cal/MyPendingInvitations?base_params=%7B%7D
        http://127.0.0.1:8000/api/cal/MyPendingInvitations
        
        """
        kw = ar.get_status(**kw)
        if not kw['base_params']:
            del kw['base_params']
        #~ kw = self.request2kw(rr,**kw)
        if ar.bound_action != ar.actor.default_action:
            kw[ext_requests.URL_PARAM_ACTION_NAME] = ar.bound_action.action.action_name
        return settings.SITE.build_admin_url('api',ar.actor.app_label,ar.actor.__name__,*args,**kw)
        
    def get_detail_url(self,obj,*args,**kw):
        return settings.SITE.build_admin_url('api',obj._meta.app_label,obj.__class__.__name__,str(obj.pk),*args,**kw)
        
    #~ def request_href_js(self,rr,text=None):
        #~ url = self.request_handler(rr)
        #~ return self.href(url,text or cgi.escape(force_unicode(rr.label)))
        
    def show_request(self,ar,**kw):
        """
        Returns a HTML element representing this request as a table.
        Used by appy_pod rendered.
        """
        return ar.table2xhtml(**kw)
        #~ return E.tostring(ar.table2xhtml())
        
    def handler_item(self,mi,handler,help_text):
        #~ handler = "function(){%s}" % handler
        #~ d = dict(text=prepare_label(mi),handler=js_code(handler),tooltip="Foo")
        d = dict(text=prepare_label(mi),handler=js_code(handler))
        if mi.bound_action and mi.bound_action.action.icon_name:
            d.update(iconCls='x-tbar-'+mi.bound_action.action.icon_name)
        if settings.SITE.use_quicktips and help_text:
            d.update(listeners=dict(render=js_code(
              "Lino.quicktip_renderer(%s,%s)" % (py2js('Foo'),py2js(help_text)))
            ))
        return d


    def html_page(self,*args,**kw):
        return '\n'.join([ln for ln in self.html_page_lines(*args,**kw)])
        
    def html_page_lines(self,request,title=None,on_ready='',run_jasmine=False):
        """
        Generates the lines of Lino's HTML reponse.
        """
        site = settings.SITE
        
        #~ logger.info("20121003 html_page_lines %r",on_ready)
        yield '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
        yield '<html><head>'
        yield '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
        yield '<title id="title">%s</title>' % site.title or site.verbose_name
        
        def stylesheet(url):
            return '<link rel="stylesheet" type="text/css" href="%s" />' % url
        def javascript(url):
            return '<script type="text/javascript" src="%s"></script>' % url
            
        if run_jasmine: 
            yield stylesheet(site.build_media_url("jasmine/jasmine.css"))
        yield stylesheet(site.build_extjs_url('resources/css/ext-all.css'))
        
        #~ yield '<!-- overrides to base library -->'
        
        if site.use_extensible:
            #~ yield stylesheet(site.build_media_url("extensible/resources/css/extensible-all.css"))
            yield stylesheet(site.build_extensible_url('resources/css/extensible-all.css'))
          
        if site.use_vinylfox:
            yield stylesheet(site.build_media_url('lino/vinylfox/resources/css/htmleditorplugins.css'))
            #~ p = self.media_url() + '/lino/vinylfox/resources/css/htmleditorplugins.css'
            #~ yield '<link rel="stylesheet" type="text/css" href="%s" />' % p
          
        if site.use_filterRow:
            #~ p = self.media_url() + '/lino/filterRow'
            #~ yield '<link rel="stylesheet" type="text/css" href="%s/filterRow.css" />' % p
            yield stylesheet(site.build_media_url('lino/filterRow/filterRow.css'))
            
        if site.use_gridfilters:
            #~ yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/statusbar/css/statusbar.css" />' % self.media_url() 
            #~ yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/gridfilters/css/GridFilters.css" />' % self.media_url() 
            #~ yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/gridfilters/css/RangeMenu.css" />' % self.media_url() 
            yield stylesheet(site.build_extjs_url("examples/ux/statusbar/css/statusbar.css"))
            yield stylesheet(site.build_extjs_url("examples/ux/gridfilters/css/GridFilters.css"))
            yield stylesheet(site.build_extjs_url("examples/ux/gridfilters/css/RangeMenu.css"))
            
        yield stylesheet(site.build_extjs_url("examples/ux/fileuploadfield/css/fileuploadfield.css"))
            
        #~ yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/fileuploadfield/css/fileuploadfield.css" />' % site.build_media_url() 
        
        #~ yield '<link rel="stylesheet" type="text/css" href="%s/lino/extjs/lino.css">' % self.media_url()
        yield stylesheet(site.build_media_url("lino/extjs/lino.css"))
        
        if site.use_awesome_uploader:
            yield stylesheet(site.build_media_url("lino/AwesomeUploader/AwesomeUploader.css"))
            yield stylesheet(site.build_media_url("lino/AwesomeUploader/AwesomeUploader Progress Bar.css"))
         
        if settings.DEBUG:
            yield javascript(site.build_extjs_url('adapter/ext/ext-base-debug.js'))
            yield javascript(site.build_extjs_url('ext-all-debug.js'))
            if site.use_extensible:
                #~ yield javascript(site.build_media_url('extensible/extensible-all-debug.js'))
                yield javascript(site.build_extensible_url('extensible-all-debug.js'))
        else:
            yield javascript(site.build_extjs_url('adapter/ext/ext-base.js'))
            yield javascript(site.build_extjs_url('ext-all.js'))
            if site.use_extensible:
                #~ yield javascript(site.build_media_url('extensible/extensible-all.js'))
                yield javascript(site.build_extensible_url('extensible-all.js'))
                
        if translation.get_language() != 'en':
            yield javascript(site.build_extjs_url('src/locale/ext-lang-'+translation.get_language()+'.js'))
            if site.use_extensible:
                yield javascript(site.build_media_url('extensible/src/locale/extensible-lang-'+translation.get_language()+'.js'))
            
        if False:
            yield '<script type="text/javascript" src="%s/extjs/Exporter-all.js"></script>' % site.build_media_url() 
            
        if False:
            yield '<script type="text/javascript" src="%s/extjs/examples/ux/CheckColumn.js"></script>' % site.build_media_url() 

        yield javascript(site.build_extjs_url('examples/ux/statusbar/StatusBar.js'))
        
        if site.use_spinner:
            yield javascript(site.build_extjs_url('examples/ux/Spinner.js'))
        
        if site.use_tinymce:
            #~ p = self.media_url() + '/tinymce'
            #~ p = site.build_media_url('tinymce')
            #~ yield '<script type="text/javascript" src="Ext.ux.form.FileUploadField.js"></script>'
            #~ yield '<script type="text/javascript" src="%s/tiny_mce.js"></script>' % p
            yield javascript(site.build_tinymce_url("tiny_mce.js"))
            #~ yield '<script type="text/javascript" src="%s/lino/tinymce/Ext.ux.TinyMCE.js"></script>' % self.media_url()
            yield javascript(site.build_media_url("lino/tinymce/Ext.ux.TinyMCE.js"))
            yield '''<script language="javascript" type="text/javascript">
tinymce.init({
        theme : "advanced"
        // , mode : "textareas"
});
</script>'''

        #~ yield '<script type="text/javascript" src="%s/lino/extjs/Ext.ux.form.DateTime.js"></script>' % self.media_url()
        yield javascript(site.build_media_url("lino/extjs/Ext.ux.form.DateTime.js"))
        
        if run_jasmine: # site.use_jasmine:
            yield javascript(site.build_media_url("jasmine/jasmine.js"))
            yield javascript(site.build_media_url("jasmine/jasmine-html.js"))
            
            yield javascript(site.build_media_url("lino/jasmine/specs.js"))
            
        if site.use_eid_jslib:
            yield javascript(site.build_media_url('eid-jslib/be_belgium_eid.js'))
            yield javascript(site.build_media_url('eid-jslib/hellerim_base64.js'))
            
        #~ if site.use_bootstrap:
            #~ yield '<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>'
            
            
        if site.use_gridfilters:
            #~ p = self.media_url() + '/extjs/examples/ux/gridfilters'
            p = site.build_extjs_url('examples/ux/gridfilters')
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
            
        yield javascript(site.build_extjs_url("examples/ux/fileuploadfield/FileUploadField.js"))
        
        if site.use_filterRow: 
            p = site.build_media_url('lino','filterRow') 
            yield '<script type="text/javascript" src="%s/filterRow.js"></script>' % p
            
        if site.use_vinylfox:
            p = site.build_media_url() + '/lino/vinylfox/src/Ext.ux.form.HtmlEditor'
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
            
        if site.use_awesome_uploader:
            p = site.build_media_url() + '/lino/AwesomeUploader/'
            #~ yield '<script type="text/javascript" src="Ext.ux.form.FileUploadField.js"></script>'
            yield '<script type="text/javascript" src="%s/Ext.ux.XHRUpload.js"></script>' % p
            yield '<script type="text/javascript" src="%s/swfupload.js"></script>' % p
            yield '<!-- <script type="text/javascript" src="%s/swfupload.swfobject.js"></script> -->' % p
            yield '<script type="text/javascript" src="%s/Ext.ux.AwesomeUploaderLocalization.js"></script>' % p
            yield '<script type="text/javascript" src="%s/Ext.ux.AwesomeUploader.js"></script>' % p

        #~ yield '<!-- overrides to library -->'
        #~ yield '<script type="text/javascript" src="%slino/extjs/lino.js"></script>' % self.media_url()
        
        
        """
        Acting as another user won't give you the access permissions of that user.
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
        if not site.build_js_cache_on_startup:
            self.build_js_cache_for_profile(user.profile,False)
        yield '<script type="text/javascript" src="%s"></script>' % (
            site.build_media_url(*self.lino_js_parts(user.profile)))
            
        #~ yield '<!-- page specific -->'
        
        if USE_DAVLINK_JNLP:
            #~ http://docs.oracle.com/javase/tutorial/deployment/deploymentInDepth/deployingWithoutCodebase.html
            yield '<script src="http://www.java.com/js/deployJava.js"></script>'
            if False:
                p = site.build_media_url('lino/applets/DavLink.jar')
                yield """\
<script>  
    var attributes = {
        name:"DavLink",
        code:'davlink.DavLink.class', 
        archive:'%s', width:1, height:1}; 
    var parameters = { jnlp_href:'davlink.jnlp' }; 
    var version = '1.6' ; 
    deployJava.runApplet(attributes, parameters, version);      
</script>
""" % p
            else:
                p = site.build_media_url('lino','applets','davlink.jnlp')
                p = request.build_absolute_uri(p)
                yield """\
<script>  
    deployJava.launchWebStartApplication('%s');
</script>
""" % p
            
        
        yield '<script type="text/javascript">'

        yield 'Ext.onReady(function(){'
        
        #~ yield "console.time('onReady');"
        
        if settings.SITE.user_model is not None:

            if request.user.profile.authenticated:
          
                if request.subst_user:
                    #~ yield "Lino.subst_user = %s;" % py2js(request.subst_user.id)
                    yield "Lino.set_subst_user(%s,%s);" % (
                        py2js(request.subst_user.id),
                        py2js(unicode(request.subst_user)))
                    user_text = unicode(request.user) + " (" + _("as") + " " + unicode(request.subst_user) + ")"
                else:
                    #~ yield "Lino.subst_user = null;"
                    yield "Lino.set_subst_user();"
                    user_text = unicode(request.user) 
                    
                user = request.user
                
                yield "Lino.user = %s;" % py2js(dict(id=user.id,name=unicode(user)))
                
                if user.profile.level >= dd.UserLevels.admin:
                    authorities = [(u.id,unicode(u)) 
                        #~ for u in users.User.objects.exclude(profile=dd.UserProfiles.blank_item)] 20120829
                        #~ for u in users.User.objects.filter(profile__isnull=False)]
                        for u in settings.SITE.user_model.objects.exclude(profile='').exclude(id=user.id)]
                        #~ for u in users.User.objects.filter(profile__gte=dd.UserLevels.guest)]
                else:
                    authorities = [(a.user.id,unicode(a.user)) 
                        for a in users.Authority.objects.filter(authorized=user)]
                
                #~ handler = self.ext_renderer.instance_handler(user)
                #~ a = users.MySettings.get_url_action('default_action')
                a = users.MySettings.default_action
                handler = self.action_call(None,a,dict(record_id=user.pk))
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
                    
                if site.remote_user_header is None:
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
                
            else:
                login_buttons = [
                  #~ dict(xtype="textfield",emptyText=_('Enter your username')),
                  #~ dict(xtype="textfield",emptyText=_('Enter your password'),inputType="password"),
                  dict(xtype="button",text=_("Log in"),handler=js_code('Lino.show_login_window')),
                  #~ dict(xtype="button",text="Register",handler=Lino.register),
                  ]
                yield "Lino.main_menu = Lino.main_menu.concat(['->',%s]);" % py2js(login_buttons)
                if on_ready:
                    # anonymous request using permalink: forward request.path as "on_login" URL
                    on_ready = "Lino.show_login_window(%s)" % py2js(request.path)
                    
                
        
        #~ yield "Lino.load_mask = new Ext.LoadMask(Ext.getBody(), {msg:'Immer mit der Ruhe...'});"
        
        dashboard = dict(
            id="dashboard",
            xtype='container',
            autoScroll=True,
            )
          
        main=dict(
            id="main_area",
            xtype='container',
            region="center",
            #~ autoScroll=True,
            layout='fit',
            items=dashboard,
            )
        
        if not on_ready:
            #~ print "20121115 foo"
            dashboard.update(html=site.get_main_html(request))
        
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
        
        if site.use_esteid:
            yield 'Lino.init_esteid();'
        
        
        if run_jasmine: # site.use_jasmine:
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

        if site.use_esteid:
            yield '<object id="esteid" type="application/x-esteid" style="width: 1px; height: 1px;"></object>'
            #~ yield "your browser doesn't support esteid"
            #~ yield '</object>'
            
        if site.use_eid_jslib:
            p = site.build_media_url('eid-jslib')
            p = request.build_absolute_uri(p)
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
            #~ yield '<param name="jnlpExtension1" value= "beid.jnlp">'

            yield '<param name="debug" value="false"/>'
            yield '<param name="Reader" value=""/>'
            yield '<param name="OCSP" value="-1"/>'
            yield '<param name="CRL" value="-1"/>'
            #~ yield '<param name="jnlp_href" value="' + p + '/beid_java_plugin.jnlp" />'
            yield '<param name="jnlp_href" value="beid_java_plugin.jnlp" />'
            yield '<param name="separate_jvm" value="true">' # 20130913
            yield '</applet>'


        if site.use_davlink:
          if not USE_DAVLINK_JNLP:
            p = site.build_media_url('lino','applets','DavLink.jar')
            p = request.build_absolute_uri(p)
            yield '<applet name="DavLink" code="davlink.DavLink.class"'
            #~ yield '        archive="%s/lino/applets/DavLink.jar"' % site.build_media_url()
            yield '        archive="%s"' % p
            yield '        width="1" height="1">'
            yield '<param name="separate_jvm" value="true">' # 20130913
            yield '</applet>'
            # Note: The value of the ARCHIVE attribute is a URL of a JAR file.
            
        if site.use_eidreader:
            p = site.build_media_url('lino','applets','EIDReader.jar')
            p = request.build_absolute_uri(p)
            yield '<applet name="EIDReader" code="lino.eidreader.EIDReader.class"'
            yield '        archive="%s"' % p
            yield '        width="1" height="1">'
            yield '<param name="separate_jvm" value="true">' # 20130913
            yield '</applet>'
            
        yield '<div id="body"></div>'
        #~ yield '<div id="tbar"/>'
        #~ yield '<div id="main"/>'
        #~ yield '<div id="bbar"/>'
        #~ yield '<div id="konsole"></div>'
        yield "</body></html>"
        
        
        
    def build_site_cache(self,force=False):
        """
        Build the site cache files under `/media/cache`,
        especially the :xfile:`lino*.js` files, one per user profile and language.
        """
        if settings.SITE.never_build_site_cache:
            logger.debug("Not building site cache because `settings.SITE.never_build_site_cache` is True")
            return 
        if not os.path.isdir(settings.MEDIA_ROOT):
            logger.debug("Not building site cache because "+
            "directory '%s' (settings.MEDIA_ROOT) does not exist.", 
            settings.MEDIA_ROOT)
            return
        
        started = time.time()
        #~ logger.info("build_site_cache started")
        
        settings.SITE.on_each_app('setup_site_cache',force)
        
        settings.SITE.makedirs_if_missing(os.path.join(settings.MEDIA_ROOT,'upload'))
        settings.SITE.makedirs_if_missing(os.path.join(settings.MEDIA_ROOT,'webdav'))
        
        if force or settings.SITE.build_js_cache_on_startup:
            count = 0
            #~ langs = settings.SITE.AVAILABLE_LANGUAGES
            for lng in settings.SITE.languages:
                with translation.override(lng.django_code):
                #~ dd.set_language(lng.django_code)
                    for profile in dd.UserProfiles.objects():
                        count += self.build_js_cache_for_profile(profile,force)
            #~ qs = users.User.objects.exclude(profile='')
            #~ for lang in langs:
                #~ dd.set_language(lang)
                #~ for user in qs:
                    #~ count += self.build_js_cache_for_user(user,force)
            #~ dd.set_language(None)
                
            logger.info("%d lino*.js files have been built in %s seconds.",
                count,time.time()-started)
          
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
            #~ if mtime > settings.SITE.mtime:
            if mtime > settings.SITE.ui.mtime:
                #~ if not user.modified or user.modified < datetime.datetime.fromtimestamp(mtime):
                #~ logger.info("20130204 %s is up to date.",fn)
                return 0
                    
        logger.info("Building %s ...", fn)
        settings.SITE.makedirs_if_missing(os.path.dirname(fn))
        f = codecs.open(fn,'w',encoding='utf-8')
        try:
            self.write_lino_js(f,profile)
            #~ f.write(jscompress(js))
            f.close()
            #~ logger.info("20130128 USED_NUMBER_FORMATS: %s", ext_elems.USED_NUMBER_FORMATS)
            return 1
        except Exception, e:
            """
            If some error occurs, remove the partly generated file 
            to make sure that Lino will try to generate it again 
            (and report the same error message) on next request.
            """
            f.close()
            #~ os.remove(fn)
            raise
        #~ logger.info("Wrote %s ...", fn)
            
    def write_lino_js(self,f,profile):
        
        tpl = self.linolib_template()
        
        context = dict(
            ext_renderer = self,
            site = settings.SITE,
            settings = settings,
            lino = lino,
            ext_requests = ext_requests,
        )
        
        messages = set()
        def mytranslate(s):
            messages.add(s)
            return _(s)
        context.update(_=mytranslate)
        #~ f.write(jscompress(unicode(tpl)+'\n'))
        f.write(jscompress(tpl.render(**context)+'\n'))
        
        """
        Make the dummy messages file.
        But only when generating for root user.
        """
        #~ if False: # no longer needed because babel extracts them
            #~ if jsgen._for_user_profile == dd.UserProfiles.admin:
                #~ make_dummy_messages_file(self.linolib_template_name(),messages)
        
        #~ assert user == jsgen._for_user
        assert profile == jsgen._for_user_profile
        
        menu = settings.SITE.get_site_menu(self,profile)
        menu.add_item('home',_("Home"),javascript="Lino.close_all_windows()")
        f.write("Lino.main_menu = %s;\n" % py2js(menu))

        actors_list = [
            rpt for rpt in dbtables.master_reports \
               + dbtables.slave_reports \
               + dbtables.generic_slaves.values() \
               + dbtables.custom_tables \
               + dbtables.frames_list ]
               
        actors_list.extend([a for a in choicelists.CHOICELISTS.values() if settings.SITE.is_installed(a.app_label)])
          
        #~ logger.info("20130804 gonna remove %s", [repr(a) for a in actors_list if settings.SITE.modules.resolve(str(a)) is not a])
        #~ actors_list = [a for a in actors_list if settings.SITE.modules.resolve(str(a)) is a]
          
        
        # don't generate JS for abstract actors       
        actors_list = [a for a in actors_list if not a.is_abstract()]
        
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
        
        actors_list = [a for a in actors_list 
            if a.default_action.get_view_permission(jsgen._for_user_profile)]
        
        #~ actors_list = [a for a in actors_list if a.get_view_permission(jsgen._for_user)]
          
        f.write("\n// ChoiceLists: \n")
        for a in choicelists.CHOICELISTS.values():
            if settings.SITE.is_installed(a.app_label):
                #~ if issubclass(a,choicelists.ChoiceList):
                f.write("Lino.%s = %s;\n" % (a.actor_id,py2js(a.get_choices())))
                
        #~ logger.info('20120120 dbtables.all_details:\n%s',
            #~ '\n'.join([str(d) for d in dbtables.all_details]))
        
        form_panels = set()
        param_panels = set()
        action_param_panels = set()
        def add(res,collector,fl,formpanel_name):
            # fl : a FormLayout
            if fl is None: return
            if fl._datasource is None: return # 20130804
            try:
                lh = fl.get_layout_handle(settings.SITE.ui)
            except Exception as e:
                raise Exception("Could not define %s for %r: %s" % (formpanel_name,res,e))
                
            if True: # 20121130 why was this?
                for e in lh.main.walk():
                    e.loosen_requirements(res)
            else:
                lh.main.loosen_requirements(res)
            if fl in collector:
                pass
                #~ fl._using_actors.append(actor)
            else:
                fl._formpanel_name = formpanel_name
                fl._url = ext_elems.rpt2url(res)
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
            lh = fl.get_layout_handle(settings.SITE.ui)
            for ln in self.js_render_ParamsPanelSubclass(lh):
                f.write(ln + '\n')
                
        for fl in action_param_panels:
            lh = fl.get_layout_handle(settings.SITE.ui)
            for ln in self.js_render_ActionFormPanelSubclass(lh):
                f.write(ln + '\n')
                
        for fl in form_panels:
            lh = fl.get_layout_handle(settings.SITE.ui)
            for ln in self.js_render_FormPanelSubclass(lh):
                f.write(ln + '\n')
        
        actions_written = set()
        for rpt in actors_list:
            rh = rpt.get_handle() 
            for ba in rpt.get_actions():
                if ba.action.parameters:
                    if not ba.action in actions_written:
                        #~ logger.info("20121005 %r is not in %r",a,actions_written)
                        actions_written.add(ba.action)
                        for ln in self.js_render_window_action(rh,ba,profile):
                            f.write(ln + '\n')
          
        for rpt in actors_list:
            rh = rpt.get_handle() 
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
                #~ elif ba.action.custom_handler:
                elif ba.action.action_name:
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
        
    def lino_js_parts(self,profile):
        return ('cache','js','lino_' + profile.value + '_' + translation.get_language()+'.js')
        
    #~ def linolib_template_name(self):
        #~ return os.path.join(os.path.dirname(__file__),'linolib.js')
        
    def linolib_template(self):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(
            os.path.dirname(__file__)))
        return env.get_template('linoweb.js')
        #~ fn = self.linolib_template_name()
        #~ return settings.SITE.jinja2_env.Template(file(fn).read())
        #~ return settings.SITE.jinja2_env.Template(file(fn).read())
        #~ return jinja2.Template(file(self.linolib_template_name()).read())
        
        #~ def docurl(ref):
            #~ if not ref.startswith('/'):
                #~ raise Exception("Invalid docref %r" % ref)
            #~ # todo: check if file exists...
            #~ return "http://lino.saffre-rumma.net" + ref + ".html"
            
        #~ libname = self.linolib_template_name()
        
        #~ tpl = CheetahTemplate(codecs.open(libname,encoding='utf-8').read())
        #~ tpl.ui = self
            
        #~ tpl._ = _
        #~ tpl.site = settings.SITE
        #~ tpl.settings = settings
        #~ tpl.lino = lino
        #~ tpl.docurl = docurl
        #~ tpl.ui = self
        #~ tpl.ext_requests = ext_requests
        #~ for k in ext_requests.URL_PARAMS:
            #~ setattr(tpl,k,getattr(ext_requests,k))
        #~ return tpl
            

    def toolbar(self,action_list):
        """
        This also manages action groups
        """
        buttons = []
        combo_map = dict()
        for ba in action_list:
            if ba.action.show_in_bbar and ba.get_view_permission(jsgen._for_user_profile):
                if ba.action.combo_group is None:
                    buttons.append(self.a2btn(ba))
                else:
                    k = ba.action.combo_group
                    combo = combo_map.get(k,None)
                    if combo is None:
                        parent = self.a2btn(ba)
                        menu = [ parent ]
                        combo = AttrDict(menu=menu)
                        combo.update(iconCls=parent.get('iconCls'))
                        combo.update(menu_item_text=parent.get('menu_item_text'))
                        combo.update(text=parent.get('text'))
                        buttons.append(combo)
                        combo_map[k] = combo
                    else:
                        #~ menu = parent.get('menu',None)
                        #~ if menu is None:
                            #~ id_map[k] = menu_btn
                        combo['menu'].append(self.a2btn(ba))
        reduced_buttons = []
        for b in buttons:
            menu = b.get('menu',None)
            if menu is None:
                reduced_buttons.append(b)
            elif len(menu) == 1:
                reduced_buttons.append(menu[0])
            else:
                b.update(xtype='splitbutton')
                b.update(panel_btn_handler=menu[0]['panel_btn_handler'])
                for a in menu:
                    a['text'] = a['menu_item_text']
                    if a.get('iconCls',1) == b.get('iconCls',2):
                        del a['iconCls']
                    
                reduced_buttons.append(b)
        return reduced_buttons
        
    def a2btn(self,ba,**kw):
        a = ba.action
        if a.parameters:
            kw.update(panel_btn_handler=js_code("Lino.param_action_handler(Lino.%s)" % ba.full_name()))
        elif isinstance(a,actions.SubmitDetail):
            js = 'function(panel){panel.save(null,%s,%r)}' % (
                py2js(a.switch_to_detail),a.action_name)
            kw.update(panel_btn_handler=js_code(js))
        elif isinstance(a,actions.ShowDetailAction):
            kw.update(panel_btn_handler=js_code('Lino.show_detail'))
        elif isinstance(a,actions.InsertRow):
            kw.update(must_save=True)
            kw.update(panel_btn_handler=js_code(
                'function(panel){Lino.show_insert(panel)}'))
        #~ elif isinstance(a,actions.DuplicateRow):
            #~ kw.update(panel_btn_handler=js_code(
                #~ 'function(panel){Lino.show_insert_duplicate(panel)}'))
        elif isinstance(a,actions.DeleteSelected):
            kw.update(panel_btn_handler=js_code("Lino.delete_selected"))
        else:
            kw.update(must_save=True)
            kw.update(panel_btn_handler=js_code(self.get_panel_btn_handler(ba)))
            
        if a.icon_name:
            kw.update(iconCls='x-tbar-'+a.icon_name)
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
        
        
    SUPPRESSED = set(('items','layout'))
    
    def js_render_ParamsPanelSubclass(self,dh):
        
        tbl = dh.layout._datasource
        
        yield ""
        yield "Lino.%s = Ext.extend(Ext.form.FormPanel,{" % dh.layout._formpanel_name
        for k,v in dh.main.ext_options().items():
            #~ if k != 'items':
            if not k in self.SUPPRESSED:
                yield "  %s: %s," % (k,py2js(v))
        #~ yield "  collapsible: true,"
        if dh.main.value['layout'] == 'hbox':
            yield "  layout: 'hbox',"
        else:
            yield "  layout: 'form',"
        yield "  autoHeight: true,"
        #~ if dh.layout.window_size and dh.layout.window_size[1] == 'auto':
            #~ yield "  autoHeight: true,"
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
        tbl = dh.layout._datasource
        #~ logger.info("20121007 js_render_ActionFormPanelSubclass %s",dh.layout._formpanel_name)
        yield ""
        yield "Lino.%s = Ext.extend(Lino.ActionFormPanel,{" % dh.layout._formpanel_name
        for k,v in dh.main.ext_options().items():
            if k != 'items':
                yield "  %s: %s," % (k,py2js(v))
        assert tbl.action_name is not None
            #~ raise Exception("20121009 action_name of %r is None" % tbl)
        yield "  action_name: '%s'," % tbl.action_name
        #~ 20131004 yield "  ls_url: %s," % py2js(dh.layout._url)
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
      
    def js_render_FormPanelSubclass(self,dh):
        
        tbl = dh.layout._datasource
        if not dh.main.get_view_permission(jsgen._for_user_profile):
            msg = "No view permission for main panel of %s :" % dh.layout._formpanel_name
            msg += " main requires %s, but actor %s requires %s)" % (dh.main.required,tbl,tbl.required)
            #~ raise Exception(msg)
            logger.warning(msg)
            return 
        
        yield ""
        yield "Lino.%s = Ext.extend(Lino.FormPanel,{" % dh.layout._formpanel_name
        yield "  layout: 'fit',"
        yield "  auto_save: true,"
        if dh.layout.window_size and dh.layout.window_size[1] == 'auto':
            yield "  autoHeight: true,"
        if settings.SITE.is_installed('contenttypes') and issubclass(tbl,dbtables.Table):
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
        #~ yield "Lino.%sPanel = Ext.extend(Lino.%s.FormPanel,{" % (action,dtl._datasource)
        yield "Lino.%sPanel = Ext.extend(Lino.%s,{" % (action.full_name(),dtl._formpanel_name)
        yield "  empty_title: %s," % py2js(action.get_button_label())
        #~ if not isinstance(action,actions.InsertRow):
        if action.action.hide_navigator:
            yield "  hide_navigator: true,"
            
        if rh.actor.params_panel_hidden:
            yield "  params_panel_hidden: true,"

        yield "  ls_bbar_actions: %s," % py2js(self.toolbar(rpt.get_actions(action.action)))
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
        yield "// js_render_GridPanel_class %s" % rh.actor
        yield "Lino.%s.GridPanel = Ext.extend(Lino.GridPanel,{" % rh.actor
        
        kw = dict()
        #~ kw.update(empty_title=%s,rh.actor.get_button_label()
        kw.update(ls_url=ext_elems.rpt2url(rh.actor))
        kw.update(ls_store_fields=[js_code(f.as_js(f.name)) for f in rh.store.list_fields])
        if rh.store.pk is not None:
            kw.update(ls_id_property=rh.store.pk.name)
            kw.update(pk_index=rh.store.pk_index)
            #~ if settings.SITE.use_contenttypes:
            if settings.SITE.is_installed('contenttypes'):
                kw.update(content_type=ContentType.objects.get_for_model(rh.store.pk.model).pk)
                #~ kw.update(content_type=ContentType.objects.get_for_model(rh.actor.model).pk)
        kw.update(cell_edit=rh.actor.cell_edit)
        kw.update(ls_bbar_actions=self.toolbar(rh.actor.get_actions(rh.actor.default_action.action)))
        kw.update(ls_grid_configs=[gc.data for gc in rh.actor.grid_configs])
        kw.update(gc_name=ext_elems.DEFAULT_GC_NAME)
        #~ if action != rh.actor.default_action:
            #~ kw.update(action_name=action.name)
        #~ kw.update(content_type=rh.report.content_type)
        
        vc = dict(emptyText=_("No data to display."))
        if rh.actor.editable:
            vc.update(getRowClass=js_code('Lino.getRowClass'))
        if rh.actor.auto_fit_column_widths:
            vc.update(forceFit=True)
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
            ext_elems.GridColumn(rh.list_layout,i,e) for i,e 
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
        # 20130726 added http_method and preprocessor
        yield "Lino.%s = function(rp,pk) { " % action.full_name()
        url = ext_elems.rpt2url(rh.actor)
        yield "  Lino.run_row_action(rp,%s,%s,pk,%s,%s);" % (
            py2js(url),py2js(action.action.http_method),
            py2js(action.action.action_name),
            action.action.preprocessor)
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
            params_panel = action.action.make_params_layout_handle(settings.SITE.ui)
            #~ logger.info("20121003 %r %s", action, params_panel)
        else:
            return 
        #~ if action.defining_actor is None:
            #~ raise Exception("20120524 %s %r actor is None" % (rh.actor,action))
        windowConfig = dict()
        wl = action.get_window_layout()
        ws = action.get_window_size()
        #~ if wl is not None:
            #~ ws = wl.window_size
        if True:
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
            #~ yield "  return Lino.calendar_app.get_main_panel();"
            yield "  return Lino.CalendarApp().get_main_panel();"
        else:
            p = dict()
            if action.action is settings.SITE.get_main_action(profile):
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
        
    
    def linolib_intro(self):
        """
        Called from :xfile:`linolib.js`.
        """
        
        def fn():
            yield """// lino.js --- generated %s by Lino version %s.""" % (time.ctime(),lino.__version__)
            #~ // $site.title ($lino.welcome_text())
            yield "Ext.BLANK_IMAGE_URL = '%s';" % settings.SITE.build_extjs_url('resources/images/default/s.gif')
            yield "LANGUAGE_CHOICES = %s;" % py2js(list(settings.SITE.LANGUAGE_CHOICES))
            # TODO: replace the following lines by a generic method for all ChoiceLists
            #~ yield "STRENGTH_CHOICES = %s;" % py2js(list(STRENGTH_CHOICES))
            #~ yield "KNOWLEDGE_CHOICES = %s;" % py2js(list(KNOWLEDGE_CHOICES))
            yield "MEDIA_URL = %s;" % py2js(settings.SITE.build_media_url())
            #~ yield "ADMIN_URL = %r;" % settings.SITE.admin_prefix
            
            #~ yield "API_URL = %r;" % self.build_url('api')
            #~ yield "TEMPLATES_URL = %r;" % self.build_url('templates')
            #~ yield "Lino.status_bar = new Ext.ux.StatusBar({defaultText:'Lino version %s.'});" % lino.__version__
        
        #~ return '\n'.join([ln for ln in fn()])
        return '\n'.join(fn())



