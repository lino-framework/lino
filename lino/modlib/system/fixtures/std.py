# -*- coding: UTF-8 -*-
## Copyright 2011-2013 Luc Saffre
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

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from lino.utils.instantiator import Instantiator
from lino.core.dbutils import resolve_model

def objects():
    if settings.SITE.user_model:
        tft = Instantiator('system.TextFieldTemplate',"name description text").build
        
        yield tft("hello","Inserts 'Hello, world!'","""<div>Hello, world!</div>""")
        #~ yield tft("mfg","",'<p>Mit freundlichen Gr&uuml;&szlig;en<br><p class="data_field">root</p>')
        yield tft("mfg","",'<p>Mit freundlichen Gr&uuml;&szlig;en<br><p>{{request.subst_user or request.user}}</p>')
    
    if settings.SITE.is_installed('contenttypes'):
        HelpText = resolve_model('system.HelpText')
        HT = Instantiator(HelpText,"content_type field help_text").build
        yield HT(ContentType.objects.get_for_model(HelpText),'field',"The name of the field.")
    
