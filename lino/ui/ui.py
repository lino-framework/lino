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

#~ from django.http import HttpResponse
#~ from django.utils import functional
from django.utils.encoding import force_unicode
#~ from django.utils.functional import Promise

#~ from django.template.loader import get_template
#~ from django.template import RequestContext

from django.utils.translation import ugettext as _
#~ from django.utils import simplejson as json
#~ from django.utils import translation

from django.conf.urls import patterns, url, include


import lino
from lino.core import constants as ext_requests
from . import store as ext_store

from lino.core import actions 
#~ from lino.core.actions import action2str
#~ from lino.core import dbtables
from lino.core import layouts
from lino.core import tables
#~ from lino.utils.xmlgen import xhtml as xhg
#~ from lino.core import fields
from lino.ui import base
from lino.core import actors
    
from lino.utils.xmlgen import html as xghtml
from lino.utils.config import make_dummy_messages_file


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
    The central instance of Lino's User Interface.
    Not only ExtJS (despite the name).
    
    """
    #~ _handle_attr_name = '_extjs3_handle'
    #~ _handle_attr_name = '_lino_ui_handle'
    #~ _response = None
    #~ name = 'extjs3'
    #~ verbose_name = "ExtJS with Windows"
    #~ Panel = ext_elems.Panel
    
    
    #~ USE_WINDOWS = False  # If you change this, then change also Lino.USE_WINDOWS in lino.js
    
    #~ def __init__(self,*args,**kw):
    def __init__(self,site):
        
        #~ site.logger.info('20130418 lino.ui.ui.ExtUI.__init__()')
        super(ExtUI,self).__init__(site)
        #~ pass
        
        #~ def before_site_startup(self,site):
        #~ logger.info('20130404 on_site_startup')
        #~ site.ui = self

        #~ logger.info("20130221 lino.ui.ExtUI.__init__()")
        pre_ui_build.send(self)
        
        #~ raise Exception("20120614")
        #~ self.pdf_renderer = PdfRenderer(self) # 20120624
        from lino.ui.render import PlainRenderer, TextRenderer
        self.plain_renderer = PlainRenderer(self)
        self.text_renderer = TextRenderer(self)
        self.reserved_names = [getattr(ext_requests,n) for n in ext_requests.URL_PARAMS]
          
        if site.use_extjs:
            from lino.extjs import ExtRenderer
            self.default_renderer = self.ext_renderer = ExtRenderer(self)
        else:
            self.default_renderer = self.plain_renderer
          
        names = set()
        for n in self.reserved_names:
            if n in names:
                raise Exception("Duplicate reserved name %r" % n)
            names.add(n)
        #~ base.UI.__init__(self)
        
        #~ trigger creation of params_layout.params_store
        #~ for res in actors.actors_list:
            #~ for ba in res.get_actions():
                #~ if ba.action.parameters:
                    #~ ba.action.params_layout.get_layout_handle(self)
        
        from lino.utils import codetime
        self.mtime = codetime()
        #~ logger.info("20130610 codetime is %s", datetime.datetime.fromtimestamp(self.mtime))
        
        post_ui_build.send(self)
        
        #~ """
        #~ setup_columns() methods may access the database
        #~ """
        #~ for res in actors.actors_list:
            #~ res.setup_columns()

        # trigger creation of params_layout.params_store
        for res in actors.actors_list:
            for ba in res.get_actions():
                if ba.action.parameters:
                    ba.action.params_layout.get_layout_handle(self)
    
        
        
    #~ def get_patterns(self):
        #~ """
        #~ """
        #~ self.ext_renderer.build_site_cache()
        #~ return super(ExtUI,self).get_patterns()
        
        

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
          
    def render_action_response(self,rv):
        """
        Builds a JSON response from given dict, 
        checking first whether there are only allowed keys 
        (defined in :attr:`ACTION_RESPONSES`)
        """
        #~ if isinstance(rv,models.Model):
            #~ js = self.ui.ext_renderer.instance_handler(None,invoice)
            #~ rv = dict(eval_js=js)
        
        rv = self.check_action_response(rv)
        return views.json_response(rv)
    

    def row_action_button(self,*args,**kw):
        """
        See :meth:`ExtRenderer.row_action_button`
        """
        return self.ext_renderer.row_action_button(*args,**kw)
