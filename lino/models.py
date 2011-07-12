## Copyright 2009-2011 Luc Saffre
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

#~ import logging
#~ logger = logging.getLogger(__name__)
from lino.utils import dblogger

from django.conf import settings
#~ from django.contrib.auth import models as auth
#~ from django.contrib.sessions import models as sessions
from django.contrib.contenttypes import models as contenttypes
from django.utils.encoding import force_unicode 

#~ from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

#~ import lino
from lino import reports
#~ from lino import layouts
from lino.core import actors
#~ from lino import commands
from lino.mixins import printable
from lino.utils import perms
#~ from lino import choices_method, simple_choices_method

class SiteConfig(models.Model):
    # moved to contacts.models:
    #~ site_company = models.ForeignKey('contacts.Company',blank=True,null=True,
        #~ verbose_name=_("The company that runs this site"))
    #~ next_partner_id = models.IntegerField(
        #~ default=1,
        #~ verbose_name=_("The next automatic id for Person or Company"))
        
    default_build_method = models.CharField(max_length=20,
      verbose_name=_("Default build method"),
      default='appyodt',
      choices=printable.build_method_choices(),blank=True)
        
    def save(self,*args,**kw):
        settings.LINO.configure(self)
        r = super(SiteConfig,self).save(*args,**kw)
        return r
   
    def __unicode__(self):
        return force_unicode(_("Global Site Parameters"))

class SiteConfigs(reports.Report):
    model = SiteConfig
    #~ default_action_class = reports.OpenDetailAction
    has_navigator = False
    #~ can_delete = perms.never
    
    
def get_site_config():
    try:
        return SiteConfig.objects.get(pk=1)
    except SiteConfig.DoesNotExist:
        dblogger.debug("Creating SiteConfig record")
        sc = SiteConfig(pk=1)
        sc.save()
        return sc

def update_site_config(**kw):
    sc = get_site_config()
    for k,v in kw.items():
        setattr(sc,k,v)
    sc.save()

#~ class Permissions(reports.Report):
    #~ model = auth.Permission
    #~ order_by = 'content_type__app_label codename'.split()
  
#~ class Users(reports.Report):
    #~ model = auth.User
    #~ order_by = ["username"]
    #~ column_names = 'username first_name last_name is_active id is_superuser is_staff last_login'

#~ class Groups(reports.Report):
    #~ model = auth.Group
    #~ order_by = ["name"]

#~ class Sessions(reports.Report):
    #~ model = sessions.Session


class ContentTypes(reports.Report):
    model = contenttypes.ContentType
    
    
    
from lino.tools import obj2str, sorted_models_list
  
class DataControlListing(printable.Listing):
    """Performs a "soft integrity test" on the database. 
    Prints 
    """
    class Meta:
        verbose_name = _("Data Control Listing") 
        
    def body(self):
        items = []
        for model in sorted_models_list():
            m = getattr(model,'soft_integrity_test',None)
            if m is not None:
                for i in model.objects.all():
                    msgs = i.soft_integrity_test()
                    if msgs:
                        items.append("%s : %s" % (obj2str(i),"<br/>".join(msgs)))
        html = "<ol>"
        html += "\n".join(["<li>%s</li>" % ln for ln in items])
        html += "</ol>"
        html = '<div class="htmlText">%s</div>' % html
        return html
    
    



def add_site_menu(site):
    m = site.add_menu("site",_("~Site"))
    #~ m.add_action('system.SiteConfigs',can_view=perms.is_staff,params=dict(pk=1))
    m.add_instance_action(site.config,label=_('Global Site Parameters'),can_view=perms.is_staff)
    return m
    #~ m.add_action('lino.SiteConfigs.detail',
      #~ label=_('Site Configuration'),
      #~ can_view=perms.is_staff,
      #~ params=dict(record_id=1))
