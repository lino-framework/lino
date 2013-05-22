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
from django.utils.translation import get_language
#~ from django.utils import simplejson as json
#~ from django.utils import translation

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
from lino.core import choicelists
from lino.core import menus
from lino.utils import jsgen
from lino.utils.jsgen import py2js, js_code, id2js
from lino.utils.xmlgen import html as xghtml
from lino.utils.config import make_dummy_messages_file
from lino.utils import codetime

from lino.utils.jscompressor import JSCompressor
if False:
    jscompress = JSCompressor().compress
else:    
    def jscompress(s): return s
      



#~ from lino.utils.choicelists import DoYouLike, HowWell
#~ STRENGTH_CHOICES = DoYouLike.get_choices()
#~ KNOWLEDGE_CHOICES = HowWell.get_choices()

#~ NOT_GIVEN = object()


from . import views


def add_user_language(kw,ar):
    u = ar.get_user()
    lang = get_language()
    if u and u.language and lang != u.language:
        kw.setdefault(ext_requests.URL_PARAM_USER_LANGUAGE,lang)
    elif lang != settings.SITE.DEFAULT_LANGUAGE.django_code:
        kw.setdefault(ext_requests.URL_PARAM_USER_LANGUAGE,lang)




class HtmlRenderer(object):
    """
    Deserves more documentation.
    """
    is_interactive = False
    
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
            img = xghtml.E.img(src=settings.SITE.build_media_url('lino','extjs','images','mjames',icon_file))
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
                settings.SITE.build_media_url(obj.file.name),_("show"),
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
        if text is None: 
            text = force_unicode(obj)
        if self.is_interactive:
            url = self.instance_handler(ar,obj)
            if url is not None:
                return xghtml.E.a(text,href=url)
        return xghtml.E.b(text)
        
class TextRenderer(HtmlRenderer):
    user = None
    
    def __init__(self,ui):
        HtmlRenderer.__init__(self,ui)
        self.user = None
        
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
        
    def show(self,ar,*args,**kw):
        """
        Returns a string representing this request in reStructuredText markup.
        """
        print ar.to_rst(*args,**kw)
        
    def unused_request(self,actor=None,**kw):
        #~ username = kw.pop('username',None)
        #~ if username:
            #~ self.login(username)
        #~ if self.user:
            #~ kw.setdefault('user',self.user)
        kw.setdefault('user',settings.SITE.console_user)
        kw.update(renderer=self)
        #~ raise Exception(kw)
        return actor.request(**kw)
        
  
class PlainRenderer(HtmlRenderer):
    """
    A "plain" HTML render that uses bootstrap and jQuery.
    It is called "plain" because that's much more lightweight than 
    :class:`lino.extjs.ExtRenderer`.
    """
  
    is_interactive = True
    
    def instance_handler(self,ar,obj,**kw):
        a = getattr(obj,'_detail_action',None)
        if a is None:
            a = obj.__class__._lino_default_table.detail_action
        if a is not None:
            if ar is None or a.get_bound_action_permission(ar,obj,None):
                add_user_language(kw,ar)
                return self.get_detail_url(obj,**kw)
  
    def href_to(self,ar,obj,text=None):
        h = self.instance_handler(ar,obj)
        if h is None:
            return cgi.escape(force_unicode(obj))
        return self.href(url,text or cgi.escape(force_unicode(obj)))
        
    def pk2url(self,ar,pk,**kw):
        if pk is not None:
            #~ kw[ext_requests.URL_PARAM_FORMAT] = ext_requests.URL_FORMAT_PLAIN
            return settings.SITE.build_plain_url(
                ar.actor.model._meta.app_label,
                ar.actor.model.__name__,
                str(pk),**kw)
            
    def get_detail_url(self,obj,*args,**kw):
        #~ since 20121226 kw[ext_requests.URL_PARAM_FORMAT] = ext_requests.URL_FORMAT_PLAIN
        #~ since 20121226 return self.ui.build_url('api',obj._meta.app_label,obj.__class__.__name__,str(obj.pk),*args,**kw)
        return settings.SITE.build_plain_url(obj._meta.app_label,obj.__class__.__name__,str(obj.pk),*args,**kw)
        
    def get_request_url(self,ar,*args,**kw):
        st = ar.get_status(self)
        kw.update(st['base_params'])
        add_user_language(kw,ar)
        #~ since 20121226 kw.setdefault(ext_requests.URL_PARAM_FORMAT,ext_requests.URL_FORMAT_PLAIN)
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
        
        return settings.SITE.build_plain_url(ar.actor.app_label,ar.actor.__name__,*args,**kw)
        
    def request_handler(self,ar,*args,**kw):
        return ''
  
    def action_button(self,obj,ar,ba,label=None,**kw):
        label = label or ba.action.label
        return label
      
    def window_action_button(self,request,ba,after_show={},label=None,title=None,**kw):
        """
        Return a HTML chunk for a button that will execute this action.
        """
        label = unicode(label or ba.get_button_label())
        url = 'javascript:'+self.action_call(request,ba,after_show)
        #~ logger.info('20121002 window_action_button %s %r',a,unicode(label))
        return self.href_button_action(ba,url,label,title or ba.action.help_text,**kw)
        
    def action_call(self,request,bound_action,after_show):  
        return "oops"

