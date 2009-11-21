## Copyright 2009 Luc Saffre
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


from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from lino import reports
from lino import layouts
from lino.utils import perms


class Property(models.Model):
    short = models.CharField(max_length=40)
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name
        

class PropValue(models.Model):
    prop = models.ForeignKey(Property)
    value = models.CharField(max_length=200)
    owner_t = models.ForeignKey(ContentType)
    owner_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('owner_t', 'owner_id')
  

class PropsByOwner(reports.Report):
    master = models.Model
    columnNames = "prop value"
    can_delete = True
    model = PropValue
    order_by = "prop.short"
