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
Performs a database reset *for all installed apps* 
and loads the specified fixtures for all applications.  
It is a combination of Django's `syncdb`, `flush` and `loaddata` commands.
It also writes log entries to your dblogger.

Django's `flush` command may fail

"""

import logging
from optparse import make_option 

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from django.core.management.sql import sql_delete
from django.core.management.color import no_style
#~ from django.core.management.sql import sql_reset
from django.db import connections, transaction, DEFAULT_DB_ALIAS
from django.db import models

import lino
from lino.core.coretools import app_labels
from lino.utils import *

class Command(BaseCommand):
    help = __doc__
    
    args = "fixture [fixture ...]"
    
    option_list = BaseCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Do not prompt for input of any kind.'),
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a database to reset. '
                'Defaults to the "default" database.'),
    ) 

    def handle(self, *args, **options):
      
        from lino.utils import dblogger
            
        if not dblogger.logger.isEnabledFor(logging.INFO):
            raise CommandError("System logger must be enabled for INFO")
        using = options.get('database', DEFAULT_DB_ALIAS)
        dbname = settings.DATABASES[using]['NAME']
        if options.get('interactive'):
            if not confirm("We are going to flush your database (%s).\nAre you sure (y/n) ?" % dbname):
                raise CommandError("User abort.")
        #~ logLevel = dblogger.logger.level
        #~ if logLevel > logging.DEBUG:
            #~ dblogger.logger.setLevel(logging.DEBUG)
            
        options.update(interactive=False)
        dblogger.info("Lino initdb %s started on database %s.", args, dbname)
        dblogger.info(lino.welcome_text())
        if True:
            conn = connections[using]
            #~ sql_list = u'\n'.join(sql_reset(app, no_style(), conn)).encode('utf-8')
            app_list = [models.get_app(app_label) for app_label in app_labels()]
            for app in app_list:
                # app_label = app.__name__.split('.')[-2]
                sql_list = sql_delete(app,no_style(),conn)
                # print app_label, ':', sql_list
                try:
                    cursor = conn.cursor()
                    for sql in sql_list:
                        # print sql
                        cursor.execute(sql)
                except Exception, e:
                    transaction.rollback_unless_managed()
                    raise
            transaction.commit_unless_managed()
        
        
        #~ call_command('reset',*apps,**options)
        #~ call_command('syncdb',load_initial_data=False,**options)
        if False:
            call_command('flush',verbosity=0,interactive=False)
        call_command('syncdb',**options)
        #~ call_command('flush',**options)
        call_command('loaddata',*args,**options)
        #~ if logLevel > logging.DEBUG:
            #~ dblogger.logger.setLevel(logLevel)
        dblogger.info("Lino initdb done %s on database %s.", args, dbname)
