# -*- coding: UTF-8 -*-
## Copyright 2011-2012 Luc Saffre
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
from lino.tools import resolve_model

def objects():
    if settings.LINO.user_model:
        tft = Instantiator('lino.TextFieldTemplate',"name description text").build
        
        yield tft("hello","Inserts 'Hello, world!'","""<div>Hello, world!</div>""")
        yield tft("mfg","",'<p>Mit freundlichen Gr&uuml;&szlig;en<br><p class="data_field">root</p>')
    
    # the following is not really useful data, but a fixture needs to deliver at least one object 
    # otherwise Django thinks that our fixture failed
    
    if settings.LINO.is_installed('contenttypes'):
        HelpText = resolve_model('lino.HelpText')
        HT = Instantiator(HelpText,"content_type field help_text").build
        yield HT(ContentType.objects.get_for_model(HelpText),'field',"The name of the field.")
    
