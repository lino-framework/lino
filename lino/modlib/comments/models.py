# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
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
The :xfile:`models.py` file for :mod:`lino.modlib.notes`.
"""

import logging
logger = logging.getLogger(__name__)

import os
import sys
import cgi
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy 
from django.contrib.humanize.templatetags.humanize import naturaltime

#~ from django.contrib.contenttypes.models import ContentType
#~ from django.contrib.contenttypes import generic
from django.db import IntegrityError
from django.utils.encoding import force_unicode


from lino import dd
from lino.utils.restify import restify
from lino import mixins
from django.conf import settings


system = dd.resolve_app('system')
#~ outbox = dd.resolve_app('outbox')
#~ postings = dd.resolve_app('postings')
#~ contacts = dd.resolve_app('contacts')


class Comment(
        dd.CreatedModified,
        dd.UserAuthored,
        dd.Hierarizable,
        dd.Controllable,
      ):
    "The model definition."
    
    class Meta:
        abstract = settings.SITE.is_abstract_model('comments.Comment')
        verbose_name = _("Comment")
        verbose_name_plural = _("Comment")
        
    #~ text = dd.RichTextField(_("Text"),blank=True,format='html')
    text = dd.RichTextField(_("Text"),format='plain')
    
    
    def __unicode__(self):
        return u'%s #%s' % (self._meta.verbose_name,self.pk)

dd.update_field(Comment,'user',editable=False)
    
    
class Comments(dd.Table):
    required = dd.required(user_level='admin')
    slave_grid_format = "summary"
    
    model = 'comments.Comment'
    
    insert_layout = dd.FormLayout("""
    text
    """,window_size=(40,10))
    
    detail_layout = """
    id user created modified owner
    text
    """
    
    #~ column_names = "id date user type event_type subject * body_html"
    #~ column_names = "id date user event_type type project subject * body"
    #~ hide_columns = "body"
    #~ hidden_columns = frozenset(['body'])
    #~ order_by = ["id"]
    #~ label = _("Notes")


class MyComments(mixins.ByUser,Comments):
    required = dd.required()
    auto_fit_column_widths =  True
    #~ master_key = 'user'
    #~ column_names = "date event_type type subject project body *"
    #~ column_names = "date event_type type subject body *"
    #~ column_names = "date type event_type subject body_html *"
    #~ can_view = perms.is_authenticated
    #~ label = _("My notes")
    order_by = ["created"]
    

  
    
class CommentsByX(Comments):
    required = dd.required()
    #~ column_names = "date event_type type subject body user *"
    order_by = ["-created"]
    
    
class CommentsByController(CommentsByX):
    master_key = 'owner'
    column_names = "text created user *"
    
    @classmethod
    def summary_row(cls,ar,obj,**kw): 
        yield obj.text
        yield " ("
        yield ar.obj2html(obj,naturaltime(obj.created))
        yield _(" by ")
        yield ar.obj2html(obj.user)
        yield ")"
    

def setup_main_menu(site,ui,profile,m):
    m  = m.add_menu("office",system.OFFICE_MODULE_LABEL)
    m.add_action('comments.MyComments')
  
def setup_explorer_menu(site,ui,profile,m):
    m  = m.add_menu("office",system.OFFICE_MODULE_LABEL)
    m.add_action('comments.Comments')
  
