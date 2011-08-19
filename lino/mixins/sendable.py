# -*- coding: UTF-8 -*-
## Copyright 2009-2011 Luc Saffre
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
"""
This defines a model mixin that adds a "Send email" button.
"""

raise "moved to lino.modlib.mails"

import logging
logger = logging.getLogger(__name__)

import os
import sys
import datetime
import traceback
import cStringIO
import glob
from fnmatch import fnmatch

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string, get_template, select_template, Context, TemplateDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.encoding import force_unicode

try:
    import ho.pisa as pisa
    #pisa.showLogging()
except ImportError:
    pisa = None

import lino
from lino import reports
from lino import fields
#~ from lino import actions

#~ from lino.tools import full_model_name
from lino.utils import iif
from lino.utils import babel

from lino.utils.config import find_config_file
from Cheetah.Template import Template as CheetahTemplate

#~ from django.template.loader import get_template
#~ from django.template import Context



class SendMailAction(reports.RowAction):
    "Deserves more documentation."
  
    name = 'send'
    label = _('Send email')
    callable_from = None
            
    def run(self,rr,elem,**kw):
        #~ if False: 
            #~ if elem.time_sent:
                #~ return rr.ui.error_response(
                    #~ message="%s has already been sent (%s)" % (elem,elem.time_sent))
          
        tplname = elem._meta.app_label + '/' + elem.__class__.__name__ + '/email.html'
        
        
        fn = find_config_file(tplname)
        logger.info("Using email template %s",fn)
        tpl = CheetahTemplate(file(fn).read())
        tpl.instance = elem
        html_content = unicode(tpl)
        
        from lino.modlib.mails.models import OutMail
        m = OutMail(user=rr.get_user(),subject=elem.get_subject(),body=html_content)
        m.full_clean()
        m.save()
        for t,n,a in elem.get_recipients():
            m.recipient_set.create(type=t,address=a,name=n)
        kw.update(open_url=rr.ui.get_detail_url(m))
        return rr.ui.success_response(**kw)
        
    
class Sendable(models.Model):
    "Deserves more documentation."
    class Meta:
        abstract = True
        
    #~ time_sent = models.DateTimeField(null=True,editable=False)
    
    @classmethod
    def setup_report(cls,rpt):
        rpt.add_action(SendMailAction())
        
    def get_print_language(self,pm):
        return babel.DEFAULT_LANGUAGE
        
    def get_templates_group(self):
        return model_group(self)
        
    def get_subject(self):
        return unicode(self)
        
    def get_recipients(self):
        "return or yield a list of (type,name,address) tuples"
        raise NotImplementedError()
        
