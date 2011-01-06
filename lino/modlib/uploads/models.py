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

class UploadType(models.Model):
    
    class Meta:
        verbose_name = _("upload type")
        verbose_name_plural = _("upload types")
        
    name = models.CharField(max_length=200,verbose_name=_('Name'))
    
    def __unicode__(self):
        return self.name
        
class UploadTypes(reports.Report):
    model = 'uploads.UploadType'
    column_names = "name *"
    order_by = ["name"]
    
        
DELAY_CHOICES = [
  ('D', _("days")),
  ('W', _("weeks")),
  ('M', _("months")),
  ('Y', _("years")),
]
  
class Upload(mixins.Uploadable,mixins.PartnerDocument,mixins.Reminder):
    type = models.ForeignKey("uploads.UploadType",
      blank=True,null=True)
      #~ verbose_name=_('upload type'))
    delay_value = models.IntegerField(_("Delay"),default=0)
    delay_unit = models.CharField(_("Unit"),max_length=1,default='D',choices=DELAY_CHOICES)
      

    def __unicode__(self):
        if self.description:
            s = self.description
        else:
            s = self.file.name
            i = s.rfind('/')
            if i != -1:
                s = s[i+1:]
        if self.type:
            s = unicode(self.type) + ' ' + s
        return s
        
class Uploads(reports.Report):
    model = Upload
    order_by = ["modified"]
    column_names = "file user created modified *"
    

class UploadsByPerson(Uploads):
    fk_name = 'person'
    column_names = "file user company created modified"
    show_slave_grid = False
    
class UploadsByCompany(Uploads):
    fk_name = 'company'
    column_names = "file user person created modified"
    show_slave_grid = False
    
    
class MyUploads(mixins.ByUser,Uploads):
    column_names = "file user company created modified"
    label = _("My uploads")
    order_by = ["modified"]
