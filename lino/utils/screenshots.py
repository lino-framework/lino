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
"""

import logging
logger = logging.getLogger(__name__)

import os
import subprocess

from django.conf import settings

from atelier.sphinxconf import Django2rstDirective

from djangosite.dbutils import set_language


SCREENSHOTS = dict()

class ScreenshotDirective(Django2rstDirective):
    def get_rst(self):
        #~ lng = self.state.document.settings.env.config.language
        #~ set_language(lng)
        assert len(self.content) == 0
        assert len(self.arguments) == 1
        ss = SCREENSHOTS[self.arguments[0]]
        return "\n\n.. image:: %s\n\n" % ss.get_filename(set_language())
        

class Screenshot(object):
    def __init__(self,name,url,username=None):
        self.name = name
        self.url = url
        self.username = username
        
    def get_filename(self,root,language):
        return '%s/%s/%s.jpg' % (root,language,self.name)
        
    def get_url(self,root,language):
        return '%s%s?lng=%s' % (root,self.url,language)

def register_screenshot(*args,**kw):
    ss = Screenshot(*args,**kw)
    SCREENSHOTS[ss.name] = ss
    return ss
    

def setup(app):
    app.add_directive('screenshot', ScreenshotDirective)
