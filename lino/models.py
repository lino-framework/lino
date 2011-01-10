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

#~ import logging
#~ logger = logging.getLogger(__name__)
from lino.utils import dblogger

from django.conf import settings
from django.contrib.auth import models as auth
from django.contrib.sessions import models as sessions
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
from lino.utils import perms
#~ from lino import choices_method, simple_choices_method

class SiteConfig(models.Model):
    site_company = models.ForeignKey('contacts.Company',blank=True,null=True,
        verbose_name=_("The company that runs this site"))
    next_partner_id = models.IntegerField(
        default=1,
        verbose_name=_("The next automatic id for Person or Company"))
    # base_currency 
    
    def __unicode__(self):
        return force_unicode(_("Site Configuration"))

class SiteConfigs(reports.Report):
    model = SiteConfig
    #~ default_action_class = reports.OpenDetailAction
    has_navigator = False
    can_delete = perms.never
    
    
def get_site_config():
    try:
        return SiteConfig.objects.get(pk=1)
    except SiteConfig.DoesNotExist:
        dblogger.info("Creating SiteConfig record")
        sc = SiteConfig(pk=1)
        #~ from lino.lino_site import lino_site
        #~ lino_site.init_site_config(sc)
        settings.LINO_SITE.init_site_config(sc)
        sc.save()
        return sc

class Permissions(reports.Report):
    model = auth.Permission
    order_by = 'content_type__app_label codename'.split()
  
class Users(reports.Report):
    model = auth.User
    #~ order_by = "last_name first_name".split()
    order_by = ["username"]
    column_names = 'username first_name last_name is_active id is_superuser is_staff last_login'

class Groups(reports.Report):
    model = auth.Group
    order_by = ["name"]
    #~ display_field = 'name'

class Sessions(reports.Report):
    model = sessions.Session
    #~ display_field = 'session_key'


class ContentTypes(reports.Report):
    model = contenttypes.ContentType



def add_site_menu(site):
    m = site.add_menu("site",_("~Site"))
    #~ m.add_action('system.SiteConfigs',can_view=perms.is_staff,params=dict(pk=1))
    m.add_action('lino.SiteConfigs.detail',
      label=_('Site Configuration'),
      can_view=perms.is_staff,
      params=dict(record_id=1))
