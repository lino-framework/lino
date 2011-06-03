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

"""Performs a database reset and loads the specified fixtures for all applications.  
It is a combination of Django's `syncdb`, `flush` and `loaddata` commands.
It also writes log entries to your dblogger.
"""

import logging
from optparse import make_option 

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

import lino
from lino.core.coretools import app_labels
from lino.utils import *
from lino.utils import dblogger

class Command(BaseCommand):
    help = __doc__
    
    args = "fixture [fixture ...]"
    
    option_list = BaseCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Do not prompt for input of any kind.'),
    ) 

    def handle(self, *args, **options):
            
        if not dblogger.logger.isEnabledFor(logging.INFO):
            raise CommandError("System logger must be enabled for INFO")
        dbname = settings.DATABASES['default']['NAME']
        if options.get('interactive'):
            if not confirm("Gonna flush your database (%s).\nAre you sure (y/n) ?" % dbname):
                raise CommandError("User abort.")
        #~ logLevel = dblogger.logger.level
        #~ if logLevel > logging.DEBUG:
            #~ dblogger.logger.setLevel(logging.DEBUG)
        
        dblogger.info("Lino initdb %s started on database %s.", args, dbname)
        dblogger.info(lino.welcome_text())
        options.update(interactive=False)
        apps = app_labels()
        #~ call_command('reset',*apps,**options)
        call_command('syncdb',load_initial_data=False,**options)
        call_command('flush',**options)
        call_command('loaddata',*args,**options)
        #~ if logLevel > logging.DEBUG:
            #~ dblogger.logger.setLevel(logLevel)
        dblogger.info("Lino initdb done %s on database %s.", args, dbname)
