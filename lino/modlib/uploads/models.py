# -*- coding: UTF-8 -*-
## Copyright 2008-2011 Luc Saffre
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

#~ import logging
#~ logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


#~ import lino
#~ logger.debug(__file__+' : started')

from lino import reports
from lino.utils import perms
from lino import mixins
from lino.modlib.contacts import models as contacts
from lino.modlib.cal.models import DurationUnit, update_auto_task

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
    
        
class Upload(
    mixins.Uploadable,
    #~ contacts.PartnerDocument,
    #~ mixins.Reminder, 
    mixins.AutoUser,
    mixins.CreatedModified,
    mixins.Owned):
    
    allow_cascaded_delete = True
    
    type = models.ForeignKey("uploads.UploadType",
      blank=True,null=True)
      #~ verbose_name=_('upload type'))
      
    valid_until = models.DateField(
        blank=True,null=True,
        verbose_name=_("valid until"))
        
    #~ owner_type = models.ForeignKey(ContentType,blank=True,null=True)
    #~ owner_id = models.PositiveIntegerField(blank=True,null=True)
    #~ owner = generic.GenericForeignKey('owner_type', 'owner_id')
    
    description = models.CharField(_("Description"),max_length=200,blank=True) # ,null=True)
    
    #~ def __unicode__(self):
        #~ return self.description or self.file.name

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
        
    def save(self,*args,**kw):
        super(Upload,self).save(*args,**kw)
        self.save_auto_tasks()
        
    def save_auto_tasks(self):
        #~ logger.info("Upload.save_auto_tasks() %s : owner is %s", self.pk, self.owner)
      
        # These constants must be unique for the whole Lino Site.
        # Keep in sync with auto types defined in lino.apps.-dsbe.models.Person
        UPLOAD_VALID_UNTIL = 5
        
        update_auto_task(
          UPLOAD_VALID_UNTIL,
          self.user,
          self.valid_until,
          _("%s expires" % (self.type)),
          self,
          alarm_value=2,alarm_unit=DurationUnit.months)
        
    def update_owned_instance(self,task):
        #~ logger.info("Upload.update_owned_instance() %s : owner is %s", self.pk, self.owner)
        mixins.AutoUser.update_owned_instance(self,task)
        mixins.Owned.update_owned_instance(self,task)
          
        
class Uploads(reports.Report):
    model = Upload
    order_by = ["modified"]
    column_names = "file user created modified *"
    

#~ class UploadsByPerson(Uploads):
    #~ fk_name = 'person'
    #~ column_names = "file user company created modified"
    #~ show_slave_grid = False
    
#~ class UploadsByCompany(Uploads):
    #~ fk_name = 'company'
    #~ column_names = "file user person created modified"
    #~ show_slave_grid = False
    
class UploadsByOwner(Uploads):
    fk_name = 'owner'
    column_names = "file user type * "
    show_slave_grid = False
    
    
class MyUploads(mixins.ByUser,Uploads):
    #~ column_names = "file user person company owner created modified"
    column_names = "file user owner *"
    label = _("My uploads")
    order_by = ["modified"]
