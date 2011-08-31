# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
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

"""Writes a diagnostic report about the data on this Site. 
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
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

import lino
from lino.core.coretools import app_labels
from lino.utils import rstgen
from lino.tools import obj2str, full_model_name, sorted_models_list

class Command(BaseCommand):
    help = __doc__
    args = "output_dir"
    
    option_list = BaseCommand.option_list + (
        make_option('--noinput', action='store_false', 
            dest='interactive', default=True,
            help='Do not prompt for input of any kind.'),
    ) 
    
    def handle(self, *args, **options):
        if args:
            raise CommandError("This command doesn't accept any arguments.")
            
        self.options = options
        
        encoding = self.stdout.encoding or 'utf-8'
        
        def writeln(ln):
            self.stdout.write(ln.encode(encoding,"xmlcharrefreplace") + "\n")
        
        
        writeln("Lino %s" % lino.__version__)
        writeln(settings.LINO.title)
        models_list = sorted_models_list()

        apps = app_labels()
        writeln("%d applications: %s." % (len(apps), ", ".join(apps)))
        writeln("%d models:" % len(models_list))
        i = 0
        headers = [
            #~ "No.",
            "Name",
            #~ "Class",
            "M",
            "#fields",
            "#rows",
            "first","last"
            ]
        rows = []
        for model in models_list:
            i += 1
            cells = []
            #~ cells.append(str(i))
            cells.append(full_model_name(model))
            #~ cells.append(str(model))
            if model._meta.managed:
                cells.append('X')
            else:
                cells.append('')
            cells.append(str(len(model._meta.fields)))
            #~ qs = model.objects.all()
            qs = model.objects.order_by('pk')
            n = qs.count()
            cells.append(str(n))
            if n:
                cells.append(obj2str(qs[0]))
                cells.append(obj2str(qs[n-1]))
            else:
                cells.append('')
                cells.append('')
            rows.append(cells)
        writeln(rstgen.table(headers,rows))
        
