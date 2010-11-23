#coding: UTF-8
## Copyright 2008-2010 Luc Saffre
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

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

#~ import lino
#~ logger.debug(__file__+' : started')

from lino import reports
from lino.utils import perms
from lino import mixins

class Upload(mixins.Uploadable,mixins.PartnerDocument,mixins.Reminder):
    pass

class Uploads(reports.Report):
    model = Upload
    order_by = "modified"
    column_names = "file user created modified *"
    

class UploadsByPerson(Uploads):
    fk_name = 'person'
    column_names = "file user company created modified"
    show_slave_grid = False
    
    
class MyUploads(mixins.ByUser,Uploads):
    column_names = "file user company created modified"
    label = _("My uploads")
    order_by = "modified"
