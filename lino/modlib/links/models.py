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


import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from lino import fields
from lino import tools
from lino import reports
#~ from lino import layouts

tools.requires_apps('auth','contenttypes')

class LinkType(models.Model):
    "Implements :class:`links.LinkType`."
    name = models.CharField(max_length=200,verbose_name=_('Name'))
    def __unicode__(self):
        return self.name
    
class Link(models.Model):
    "Implements :class:`links.Link`."
    user = models.ForeignKey("auth.User",verbose_name=_('User'))
    type = models.ForeignKey("links.LinkType",
      blank=True,null=True,
      verbose_name=_('Link type'))
    date = models.DateTimeField(verbose_name=_('Date'),default=datetime.date.today) 
    owner_type = models.ForeignKey(ContentType)
    owner_id = models.PositiveIntegerField(verbose_name=_('Owner'))
    owner = generic.GenericForeignKey('owner_type', 'owner_id')
    url = models.URLField(verify_exists=False)
    name = models.CharField(max_length=200,blank=True,null=True,
        verbose_name=_('Name'))
    valid_until = models.DateField(
        blank=True,null=True,
        verbose_name=_("valid until"))
        
    
    def on_create(self,req):
        u = req.get_user()
        if u is not None:
            self.user = u
            
    def __unicode__(self):
        s = self.name or self.url or u""
        if self.type:
            s = unicode(self.type) + ' ' + s
        return s
        

class LinkTypes(reports.Report):
    model = 'links.LinkType'
    column_names = "name *"
    order_by = "name"
    
class Links(reports.Report):
    model = 'links.Link'
    column_names = "id date user url name *"
    order_by = "id"

class MyLinks(Links):
    fk_name = 'user'
    column_names = "name url date *"
    order_by = 'name'

class LinksByOwner(Links):
    button_label = _("Links")
    label = _("Links by owner")
    fk_name = 'owner'
    column_names = "url date name user *"
    order_by = "date"
    show_slave_grid = False
    
    def summary_row(self,rr,obj):
        if obj.url:
            return u'<a href="%s" target="_blank">%s</a>' % (obj.url,unicode(obj))
        return reports.Report.summary_row(self,rr,obj)
    
    def get_title(self,rr):
        return _("Links by %(model)s %(owner)s") % dict(
          model=rr.master_instance._meta.verbose_name,
          owner=rr.master_instance)
    
  
#~ def links_by_owner(owner):
    #~ return Link.objects.filter(owner=owner)