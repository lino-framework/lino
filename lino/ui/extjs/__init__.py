## Copyright 2009-2010 Luc Saffre
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

raise Exception("extjs4 not yet ready")



#~ import os
#~ import traceback

#~ from django.db import models
#~ from django.conf import settings
#from django.utils import html
#~ from django.utils.translation import ugettext as _

#~ import lino
#~ from lino import layouts
#~ from lino.utils import jsgen 
#~ py2js = jsgen.py2js
from . import ext_ui

def get_ui(site):
    return ext_ui.ExtUI(site)
    
#~ ui = ext_ui.ExtUI()
#~ jsgen.register_converter(ui.py2js_converter)

#~ from lino.ui.extjsu.ext_ui import ui


