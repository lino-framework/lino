## Copyright 2010-2011 Luc Saffre
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

import logging
logger = logging.getLogger(__name__)

import datetime
import os

from django.utils.translation import ugettext as _
from django.db import models
from django.conf import settings

from lino import reports
from lino.tools import obj2str
from lino.utils import ispure
#~ from lino import layouts
    
class Uploadable(models.Model):
    """
    Represents an uploadable file.
    """
    
    class Meta:
        abstract = True
        verbose_name = _("upload")
        verbose_name_plural = _("uploads")
        
    file = models.FileField(_("File"),upload_to='uploads/%Y/%m')
    #~ user = models.ForeignKey('auth.User',verbose_name=_("Owner"))
    #~ timestamp = models.TimeField(_("Timestamp"),auto_now=True)
    mimetype = models.CharField(_("MIME type"),max_length=64, editable=False)
    created = models.DateTimeField(_("Created"),auto_now_add=True, editable=False)
    modified = models.DateTimeField(_("Modified"),auto_now=True, editable=False)
    description = models.CharField(_("Description"),max_length=200,blank=True,null=True)
    
    #~ def show_date(self):
        #~ if self.timestamp:
            #~ return unicode(self.timestamp.date)
        #~ return u''
    #~ show_date.return_type = models.CharField(_("Date"),max_length=10)
    
    #~ def show_time(self):
        #~ if self.timestamp:
            #~ return unicode(self.timestamp.time)
        #~ return u''
    #~ show_time.return_type = models.CharField(_("Time"),max_length=8)
    
    def __unicode__(self):
        return self.description or self.file.name

    def handle_uploaded_files(self,request):
        #~ from django.core.files.base import ContentFile
        uf = request.FILES['file'] # an UploadedFile instance
        #~ cf = ContentFile(request.FILES['file'].read())
        #~ print f
        #~ raise NotImplementedError
        #~ dir,name = os.path.split(f.name)
        #~ if name != f.name:
            #~ print "Aha: %r contains a path! (%s)" % (f.name,__file__)
            
        #~ name = os.path.join(settings.MEDIA_ROOT,'uploads',name)
        
        self.size = uf.size
        self.mimetype = uf.content_type
        
        if not ispure(uf.name):
            raise Exception('uf.name is a %s!' % type(uf.name))
        
        # Django magics: 
        self.file = uf.name # assign a string
        ff = self.file  # get back a FileField instance !
        #~ print 'uf=',repr(uf),'ff=',repr(ff)
        
        if not ispure(uf.name):
            raise Exception('uf.name is a %s!' % type(uf.name))
            
        ff.save(uf.name,uf,save=False)
        
        # The expression `self.file` 
        # now yields a FieldFile instance that has been created from `uf`.
        # see Django FileDescriptor.__get__()
        
        logger.info("Wrote uploaded file %s", ff.path)
        #~ print obj2str(self,True)
        
        #~ raise NotImplementedError
        
        #~ destination = ff.open('wb+')
        #~ for chunk in uf.chunks():
            #~ destination.write(chunk)
        #~ destination.close()
        
