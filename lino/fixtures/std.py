# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
## This file is part of the Lino-DSBE project.
## Lino-DSBE is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino-DSBE is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino-DSBE; if not, see <http://www.gnu.org/licenses/>.


#~ from django.contrib.contenttypes.models import ContentType
from lino.utils.instantiator import Instantiator, i2d
from lino.tools import resolve_model
from django.utils.translation import ugettext_lazy as _


from django.db import models
from lino.utils.babel import babel_values, babelitem

#~ TextFieldTemplate = resolve_model('lino.TextFieldTemplate')

#~ from lino.modlib.properties import models as properties 

def objects():
  
    tft = Instantiator('lino.TextFieldTemplate',"name description text").build
    
    yield tft("hello","Inserts 'Hello, world!'","""<div>Hello, world!</div>""")
    yield tft("mfg","",'<p>Mit freundlichen Gr&uuml;&szlig;en<br><p class="data_field">root</p>')
    
