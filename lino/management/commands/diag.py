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
Writes a diagnostic status report about the data on this Site. 
Used to get a quick overview on the differences in two databases. 
"""

import logging
logger = logging.getLogger(__name__)

import os
import errno
#~ import codecs
import sys
from optparse import make_option 
from os.path import join

from django.db import models
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from django.conf import settings

class Command(BaseCommand):
    help = __doc__
    args = "output_dir"
    
    #~ option_list = BaseCommand.option_list + (
        #~ make_option('--noinput', action='store_false', 
            #~ dest='interactive', default=True,
            #~ help='Do not prompt for input of any kind.'),
    #~ ) 
    
    def handle(self, *args, **options):
        if args:
            raise CommandError("This command doesn't accept any arguments.")
            
        #~ print settings.SITE.__class__
        #~ self.options = options
        
        #~ settings.SITE.startup()
        
        encoding = self.stdout.encoding or 'utf-8'
        
        def writeln(ln):
            self.stdout.write(ln.encode(encoding,"xmlcharrefreplace") + "\n")
        
        settings.SITE.startup()
        writeln(settings.SITE.get_db_overview_rst())
        
