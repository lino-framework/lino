## Copyright 2009 Luc Saffre
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


import os
import traceback
#import types
import cgi
from textwrap import TextWrapper
from StringIO import StringIO # cStringIO doesn't support Unicode
import cStringIO


#from django.conf import settings
from django import forms
from django.db import models
from django.db.models.query import QuerySet
from django.template.loader import render_to_string
from django import template 
from django.shortcuts import render_to_response 
from django.forms.models import modelform_factory, modelformset_factory, inlineformset_factory
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.forms.models import ModelForm,ModelFormMetaclass, BaseModelFormSet
from django.db.models.manager import Manager

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.utils import simplejson
from django.template.loader import render_to_string, get_template, select_template, Context


from lino.utils import layouts
from lino.utils.requests import again, get_redirect, redirect_to
from lino.utils import editing, latex

IS_SELECTED = 'IS_SELECTED_%d'


def SPAN(text,style):
    #text = escape(text)
    return """<span class="textinput"
    style="%s">%s</span>
    """ % (style,text)
    
def HREF(href,text):
    text = escape(text)
    return mark_safe('<a href="%s">%s</a>' % (href,text))



def short_link(s):
    return "link"
    
    

    


