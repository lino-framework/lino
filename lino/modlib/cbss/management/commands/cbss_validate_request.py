# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from lino import dd

class Command(BaseCommand):
    args = '<model> <id>'
    help = 'Locally validates an existing CBSS request.'

    def handle(self, *args, **options):
        model = dd.resolve_model('cbss.'+args[0])
        pk = int(args[1])
        req = model.objects.get(pk=pk)
        req.validate_request()
        print req.logged_messages
      
