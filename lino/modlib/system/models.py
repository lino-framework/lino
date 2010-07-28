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

from django.contrib.auth import models as auth
from django.contrib.sessions import models as sessions
from django.contrib.contenttypes import models as contenttypes

#~ from django import forms
from django.db import models
from django.utils.translation import ugettext as _

import lino
from lino import reports
from lino import layouts
#~ from lino import commands
from lino.utils import perms
#~ from lino import choices_method, simple_choices_method

class ReportConfig(models.Model):
  
    rptname = models.CharField(max_length=100)
    """The actor name of the report being customized."""
    
    name = models.CharField(max_length=20)
    """Short name for this Configuration.
    Must be identifying inside a same rptname. 
    """
    
    label = models.CharField(max_length=100)
    """Name presented to user when selecting a Config for a given report."""
    
    #~ @simple_choices_method
    #~ @classmethod
    def rptname_choices(cls):
        """This is a choices_method (and not a `choices` 
        parameter of rptname) because the list isnt' available 
        during model population."""
        #~ print 20100724, __file__
        return reports.rptname_choices
    rptname_choices.simple_values = True
    rptname_choices = classmethod(rptname_choices)
    
    
class ReportColumn(models.Model):
    rptconfig = models.ForeignKey('system.ReportConfig')
    seq = models.IntegerField()
    colname = models.CharField(max_length=30)
    
    #~ @choices_method
    @classmethod
    def colname_choices(cls,rptconfig):
        return reports.column_choices(rptconfig.rptname)
        
class ReportConfigDetail(layouts.DetailLayout):
    datalink = 'system.ReportConfig'
    main = """
    rptname name label
    system.ColumnsByReport
    """
    
class ReportConfigs(reports.Report):
    model = 'system.ReportConfig'
    
class ColumnsByReport(reports.Report):
    model = 'system.ReportColumn'
    fk_name = 'rptconfig'
    
    
    

class SiteConfig(models.Model):
    site_company = models.ForeignKey('contacts.Company',blank=True,null=True,
        verbose_name=_("The company that runs this site"))
    next_partner_id = models.IntegerField(verbose_name=_("The next automatic id for Person or Company"))
    # base_currency 

class SiteConfigDetail(layouts.DetailLayout):
    #~ label = _('Site Configuration')
    datalink = 'system.SiteConfig'
    main = """
    site_company
    next_partner_id
    """

class SiteConfigs(reports.Report):
    model = SiteConfig
    #~ default_action_class = reports.OpenDetailAction

def get_site_config():
    try:
        return SiteConfig.objects.get(pk=1)
    except SiteConfig.DoesNotExist:
        lino.log.info("Creating SiteConfig record")
        sc = SiteConfig(pk=1)
        from lino.lino_site import lino_site
        lino_site.init_site_config(sc)
        return sc

class Permissions(reports.Report):
    model = auth.Permission
    order_by = 'content_type__app_label codename'
  
class Users(reports.Report):
    model = auth.User
    order_by = "username"
    display_field = 'username'
    column_names = 'username first_name last_name is_active id is_superuser is_staff last_login'

class Groups(reports.Report):
    model = auth.Group
    order_by = "name"
    display_field = 'name'

class Sessions(reports.Report):
    model = sessions.Session
    display_field = 'session_key'


class ContentTypes(reports.Report):
    model = contenttypes.ContentType



def add_system_menu(lino):
    m = lino.add_menu("system",_("~System"))
    #~ m.add_action('system.SiteConfigs',can_view=perms.is_staff,params=dict(pk=1))
    m.add_action('system.SiteConfigs.detail',
      label=_('Site Configuration'),
      can_view=perms.is_staff,
      params=dict(record_id=1))
    if False:
        m = lino.add_menu("auth",_("~Authentificate"))
        m.add_action('system.Login',can_view=perms.is_anonymous)
        m.add_action('system.Logout',can_view=perms.is_authenticated)
        m.add_action('system.PasswordReset',can_view=perms.is_authenticated)
