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
Does the same as the original Django loaddata command,
but calls :func:`lino.core.kernel.analyze_models` first.
This is necessary if your application has its own 
:meth:`lino.Lino.setup_choicelists`.

"""

from django.conf import settings

from django.core.management.commands.loaddata import Command as OriginalCommand

from lino.core.kernel import analyze_models

class Command(OriginalCommand):
  
    def handle(self, *fixture_labels, **options):
        #~ settings.LINO.startup()
        analyze_models()
        # startup would create a SiteConfig object
        return OriginalCommand.handle(self, *fixture_labels, **options)
  
