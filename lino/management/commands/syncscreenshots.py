# -*- coding: UTF-8 -*-
## Copyright 2012-2013 Luc Saffre
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
Not yet implemented.
Compares screenshots below DIR1 with those below DIR2.
Fails and writes a comprehensible report if one of the mismatches.

Intended use is to run this as a test case, 
specifying 
the output of the last makescreenshots run 
(demo/media/cache/screenshots)
as DIR1 and `userdocs/scrennshots` 
("official", "confirmed" screenshots) as DIR2.

"""

import logging
logger = logging.getLogger(__name__)

import os
import errno
#~ import codecs
import sys
from optparse import make_option 
from os.path import join


from multiprocessing import Process

from django.db import models
from django.utils.translation import ugettext as _
from django.utils import translation
from django.utils.encoding import force_unicode
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.core.servers.basehttp import WSGIServerException, get_internal_wsgi_application
from django.core.servers.basehttp import WSGIRequestHandler

from django.conf import settings
#~ from django.test import LiveServerTestCase
from django.test.testcases import StoppableWSGIServer

from lino.core.dbutils import obj2str, full_model_name, sorted_models_list, app_labels
from lino.utils import screenshots
from atelier.utils import SubProcessParent



class Command(BaseCommand):
    help = __doc__
    args = "output_dir"
    
    
    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Required argument: output_dir")
            
        output_dir = args[0]
            
        #~ print settings.SITE.__class__
        settings.SITE.startup()
        #~ translation.activate(settings.LANGUAGE_CODE)
        
        sync_screenshots(output_dir,force=True)
        
