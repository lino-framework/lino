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
Calls :mod:`initdb <djangosite.management.commands.initdb>` with 
:attr:`demo_fixtures <lino.site.Site.demo_fixtures>`.

Introduction see :ref:`lino.tutorial.quickstart`.

"""

from django.conf import settings
from djangosite.management.commands.initdb import Command as BaseCommand
from djangosite.management.commands.initdb import CommandError

class Command(BaseCommand):
    help = __doc__

    def handle(self, *args, **options):
        if len(args) > 0:
            raise CommandError("This command takes no arguments (got %r)" % args)
            
        args = settings.SITE.demo_fixtures
        if isinstance(args,basestring):
            args = args.split()
        super(Command,self).handle(*args, **options)
      
