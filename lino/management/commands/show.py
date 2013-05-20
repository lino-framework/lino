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

import sys
from optparse import make_option 

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import models

class Command(BaseCommand):
    help = __doc__
    args = "action_spec [args ...]"
    
    option_list = BaseCommand.option_list + (
        make_option('--username', action='store', 
            dest='username', default='root',
            help='The username to act as. Default is "root".'),
    ) 
    
    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError("I need at least one argument.")
        #~ settings.SITE.startup()
        spec = args[0]
        cl = settings.SITE.modules.resolve(spec)
        
        if issubclass(cl,models.Model):
            cl = cl._lino_default_table
        username = options['username']
        ses = settings.SITE.login(username)
        ses.show(cl)
          
