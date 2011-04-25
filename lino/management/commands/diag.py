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

import logging
logger = logging.getLogger(__name__)

import os
import errno
import codecs
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
from lino.tools import obj2str

  

class Command(BaseCommand):
    help = """Writes a diagnostic report about this Site.
    """
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
        
        fd = codecs.open("diag.rst","w",encoding="utf-8")
        
        def writeln(ln):
            fd.write(ln + "\n")
            #~ print s
        
        
        writeln("Lino %s" % lino.__version__)
        writeln(settings.LINO.title)
        
        models_list = models.get_models() # trigger django.db.models.loading.cache._populate()

        apps = app_labels()
        writeln("%d applications: %s." % (len(apps), ", ".join(apps)))
        writeln("%d models:" % len(models_list))
        i = 0
        headers = ["No.","Name",
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
            cells.append(str(i))
            cells.append("%s.%s" % (model._meta.app_label, model._meta.object_name))
            #~ cells.append(str(model))
            if model._meta.managed:
                cells.append('X')
            else:
                cells.append('')
            cells.append(str(len(model._meta.fields)))
            qs = model.objects.all()
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
        
        fd.close()
        
