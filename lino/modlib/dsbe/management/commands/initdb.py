# -*- coding: UTF-8 -*-
## Copyright 2009-2010 Luc Saffre
## This file is part of the TimTools project.
## TimTools is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## TimTools is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with TimTools; if not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from lino.core.coretools import app_labels

from lino.utils import *

class Command(BaseCommand):
    args = '<fixtur1>, ...'
    help = 'Performs a database reset and loads the specified fixtures'

    def handle(self, *args, **options):
            
        dbname = settings.DATABASES['default']['NAME']
        if not confirm("Gonna reset your database (%s).\nAre you sure (y/n) ?" % dbname):
            raise CommandError("User abort.")
        options.update(interactive=False)
        apps = app_labels()
        call_command('reset',*apps,**options)
        call_command('syncdb',**options)
        call_command('loaddata',*args,**options)
            
