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


from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _

from lino.modlib import fields
from lino.modlib import tools
from lino import reports
from lino import layouts

tools.requires_apps('auth','contenttypes')

class Link(models.Model):
    user = models.ForeignKey("auth.User")
    date = models.DateTimeField(auto_now=True) 
    owner_type = models.ForeignKey(ContentType)
    owner_id = models.PositiveIntegerField()
    owner = generic.GenericForeignKey('owner_type', 'owner_id')
    url = models.URLField(verify_exists=True)
    desc = models.CharField(max_length=200,blank=True,null=True,
        verbose_name='Description')
    
    def __unicode__(self):
        return self.desc or self.url or u""
        
        
class LinkDetail(layouts.DetailLayout):
    datalink = 'links.Link'
    main = """
    url
    desc
    user date owner
    """
        

class Links(reports.Report):
    model = 'links.Link'
    column_names = "id date user owner desc"
    order_by = "id"

class MyLinks(Links):
    fk_name = 'user'
    column_names = "date desc owner"

class LinksByOwner(Links):
    button_label = _("Links")
    title = _("Links by owner")
    fk_name = 'owner'
    column_names = "url date desc user"
    order_by = "date"
  
