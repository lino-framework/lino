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

raise "no longer used. moved to lino_site"

import lino
from django.db import models
from django.db.models import loading

#~ def welcome():

def thanks_to():
    l = ["%s %s <%s>" % (name,version,url) 
          for name,url,version in lino.thanks_to()]
    return '\n'.join(l)
      

def app_labels():
    return [a.__name__.split('.')[-2] for a in loading.get_apps()]
        
