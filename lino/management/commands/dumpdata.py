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
Does the same as the original Django dumpdata command,
but calls `lino.Lino.startup` first.
This is necessary if your application has its 
own :meth:`lino.Lino.setup_choicelists`.

"""

from django.conf import settings

from django.core.management.commands.dumpdata import Command as DumpdataCommand


#~ from lino.core.kernel import analyze_models

class Command(DumpdataCommand):
  
    def handle(self, *app_labels, **options):
        #~ analyze_models()
        settings.LINO.startup()
        
        options.update(format='py')
      
        return DumpdataCommand.handle(self, *app_labels, **options)
  
