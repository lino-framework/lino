## Copyright 2008-2009 Luc Saffre
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


import datetime
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=200)
    isocode = models.CharField(max_length=2,primary_key=True)
    
    class Meta:
        verbose_name_plural = "Countries"
    
    def __unicode__(self):
        return self.name
        
 
    
class Language(models.Model):
    id = models.CharField(max_length=2,primary_key=True)
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name

##
## report definitions
##        
        
from lino import reports

class Countries(reports.Report):
    model = Country
    order_by = "isocode"
    columnNames = "isocode name"
    
class Languages(reports.Report):
    model = Language
    order_by = "id"

