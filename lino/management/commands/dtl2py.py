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

import logging
logger = logging.getLogger(__name__)

#~ from django.db import models
#~ from django.conf import settings
#~ from django.utils.translation import ugettext as _
#~ from django.utils.encoding import force_unicode 
#~ from django.core.management import call_command

from django.core.management.base import BaseCommand, CommandError
#~ from django.db.models import loading
#~ from django.db import models
#~ from django.contrib.contenttypes.models import ContentType
#~ from lino.core import actors
#~ from lino.utils import get_class_attr

import lino

class Command(BaseCommand):
    help = """Generates a .py file for each .dtl file.
    """
    requires_model_validation = False
    
    def handle(self, *args, **options):
        if len(args) != 0:
            raise CommandError("This command takes no arguments.")
            
        logger.info("Running %s.", self)
        from lino.ui.extjs3 import UI
        #~ UI = settings.LINO.get_ui_class
        ui = UI(make_messages=True)
        #~ # install Lino urls under root location (`/`)
        #~ ui = urlpatterns = ui.get_patterns()
        #~ settings.LINO.setup()
        ui.make_dtl_messages()
        ui.make_linolib_messages()
        
        logger.info("%s done.", self)
