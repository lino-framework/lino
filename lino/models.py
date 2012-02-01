## Copyright 2009-2012 Luc Saffre
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
Defines some system models, especially the :class:`SiteConfig` model.
Expected to be installed in every Lino application.
"""

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
from lino import mixins
from lino import dd
#~ from lino import commands
from lino.mixins import printable
from lino.utils import babel
from lino.utils import perms
#~ from lino import choices_method, simple_choices_method
from lino.tools import obj2str, sorted_models_list
from lino.tools import resolve_field

class SiteConfig(models.Model):
    """
    This model should have exactly one instance, 
    used to store persistent global site parameters.
    Application code sees this as ``settings.LINO.config``.
    """
        
    default_build_method = models.CharField(max_length=20,
      verbose_name=_("Default build method"),
      default='appyodt',
      choices=printable.build_method_choices(),blank=True)
        
    #~ def save(self,*args,**kw):
        #~ settings.LINO.configure(self)
        #~ r = super(SiteConfig,self).save(*args,**kw)
        #~ return r
   
    def __unicode__(self):
        return force_unicode(_("Global Site Parameters"))

class SiteConfigs(dd.Table):
    model = SiteConfig
    #~ default_action_class = dd.OpenDetailAction
    has_navigator = False
    #~ can_delete = perms.never
    
    
def get_site_config():
    try:
        return SiteConfig.objects.get(pk=1)
    #~ except SiteConfig.DoesNotExist:
    except Exception,e:
        kw = dict(pk=1)
        kw.update(settings.LINO.site_config_defaults)
        dblogger.debug("Creating SiteConfig record (%s)",e)
        sc = SiteConfig(**kw)
        #~ do NOT save the instance here
        #~ sc.save()
        return sc

def update_site_config(**kw):
    sc = get_site_config()
    for k,v in kw.items():
        setattr(sc,k,v)
    sc.save()


class ContentTypes(dd.Table):
    model = contenttypes.ContentType
    
    
  
class DataControlListing(mixins.Listing):
    """Performs a "soft integrity test" on the database. 
    Prints 
    """
    class Meta:
        verbose_name = _("Data Control Listing") 
    
    def body(self):
        items = []
        for model in sorted_models_list():
            m = getattr(model,'data_control',None)
            if m is not None:
                for i in model.objects.all():
                    msgs = i.data_control()
                    if msgs:
                        if len(msgs) == 1:
                            items.append("<b>%s</b> : %s" % (unicode(i),msgs[0]))
                        else:
                            items.append("<b>%s</b> : %s" % (
                              unicode(i),
                              "\n".join(
                                ["<br>(%d) %s" % (x[0]+1,x[1])
                                  for x in enumerate(msgs)])))
        #~ html = "<ol>"
        #~ html += "\n".join(["<li>%s</li>" % ln for ln in items])
        #~ html += "</ol>"
        html = "\n".join(["<p>%s</p>" % ln for ln in items])
        html = '<div class="htmlText">%s</div>' % html
        return html
        
from lino.utils.choosers import chooser
    
class HelpText(models.Model):
    
    class Meta:
        verbose_name = _("Help Text")
        verbose_name_plural = _("Help Texts")
        
    content_type = models.ForeignKey(contenttypes.ContentType,
        verbose_name=_("Model"))
    field = models.CharField(_("Field"),
        max_length=200)

    help_text = dd.RichTextField(_("HelpText"),
        blank=True,null=True,format='plain')
    
    def __unicode__(self):
        return self.content_type.app_label + '.' + self.content_type.name + '.' + self.field
        
    @chooser(simple_values=True)
    def field_choices(cls,content_type):
        l = []
        if content_type is not None:
            meta = content_type.model_class()._meta
            #~ for f in meta.fields: yield f.name
            #~ for f in meta.many_to_many: yield f.name
            #~ for f in meta.virtual_fields: yield f.name
            for f in meta.fields: 
                if not getattr(f,'_lino_babel_field',False):
                    l.append(f.name)
            for f in meta.many_to_many: l.append(f.name)
            for f in meta.virtual_fields: l.append(f.name)
        return l
        
    #~ def get_field_display(cls,fld):
        #~ return fld

    @dd.virtualfield(models.CharField(_("Verbose name"),max_length=200))
    def verbose_name(self,request):
        return resolve_field(unicode(self)).verbose_name
            
            
            
class HelpTexts(dd.Table):
    model = HelpText
    column_names = "field verbose_name help_text id content_type"
    
class HelpTextsByModel(HelpTexts):
    master_key = 'content_type'

if settings.LINO.user_model: 
  
    class TextFieldTemplate(mixins.AutoUser):
        """A reusable block of text that can be selected from a text editor to be 
        inserted into the text being edited.
        """
      
        class Meta:
            verbose_name = _("Text Field Template")
            verbose_name_plural = _("Text Field Templates")
            
        name = models.CharField(_("Designation"),max_length=200)
        description = dd.RichTextField(_("Description"),
            blank=True,null=True,format='html')
        text = dd.RichTextField(_("Template Text"),
            blank=True,null=True,format='html')
        
        def __unicode__(self):
            return self.name
            
    class MyTextFieldTemplates(mixins.ByUser):
        model = TextFieldTemplate
        
    class TextFieldTemplates(dd.Table):
        model = TextFieldTemplate


def add_site_menu(site):
    m = site.add_menu("site",_("~Site"))
    #~ m.add_action('system.SiteConfigs',can_view=perms.is_staff,params=dict(pk=1))
    m.add_instance_action(site.config,
        label=_('Global Site Parameters'),
        can_view=perms.is_staff)
    return m
    #~ m.add_action('lino.SiteConfigs.detail',
      #~ label=_('Site Configuration'),
      #~ can_view=perms.is_staff,
      #~ params=dict(record_id=1))
