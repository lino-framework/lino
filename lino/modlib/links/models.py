## Copyright 2011 Luc Saffre
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
import logging
logger = logging.getLogger(__name__)


from django.db import models
from django.contrib.contenttypes.models import ContentType
#~ from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode

from lino import dd
#~ from lino import tools
from lino import mixins
from lino.dd import VirtualField
from lino.tools import obj2str
#~ from lino import layouts
from lino.utils import babel 
from lino.utils.choosers import chooser

#~ tools.requires_apps('auth','contenttypes')

class LinkType(babel.BabelNamed):
    "Implements :class:`links.LinkType`."
    
    class Meta:
        verbose_name = _("Link Type")
        verbose_name_plural = _("Link Types")
        
    a_type = models.ForeignKey(ContentType,
        editable=True,
        related_name='origin_links',
        #~ blank=True,null=True,
        verbose_name=_('(a type)'))
    b_type = models.ForeignKey(ContentType,
        editable=True,
        related_name='target_links',
        #~ blank=True,null=True,
        verbose_name=_('(b type)'))
        



#~ class Link(mixins.Reminder):
#~ class Link(mixins.AutoUser):
class Link(models.Model):
    "Implements :class:`links.Link`."
    
    #~ allow_cascaded_delete = True
    
    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")
    
    type = models.ForeignKey("links.LinkType")

    #~ a = dd.DynamicGeneralForeignKey(type,'a_type',blank=True,null=True)
    #~ b = dd.DynamicGeneralForeignKey(type,'b_type',blank=True,null=True)
    
    a_id = models.PositiveIntegerField(
        # editable=True,
        blank=True,null=True,
        verbose_name=_('(a object)'))
    b_id = models.PositiveIntegerField(
        # editable=True,
        blank=True,null=True,
        verbose_name=_('(b object)'))
        
    a = dd.LinkedForeignKey(type,'a')
    b = dd.LinkedForeignKey(type,'b')
    
    
    #~ a = dd.GenericForeignKey(
        #~ 'type__a_type', 'a_id',
        #~ verbose_name=_("Link origin"))
    #~ b = dd.GenericForeignKey(
        #~ 'type__a_type', 'a_id',
        #~ verbose_name=_("Link target"))
        
    #~ def get_a(self):
        #~ ct = ContentType.objects.get(pk=self.type.a_type)
        #~ return ct.get_object_for_this_type(self.a_id)
    #~ a = property(get_a)
    
    #~ def get_b(self):
        #~ ct = ContentType.objects.get(pk=self.type.b_type)
        #~ return ct.get_object_for_this_type(self.b_id)
    #~ b = property(get_b)
    
    @chooser(instance_values=True)
    def a_choices(cls,type):
        if type:
            return type.a_type.model_class().objects.all()
        return []
      
    @chooser(instance_values=True)
    def b_choices(cls,type):
        if type:
            return type.b_type.model_class().objects.all()
        return []
      
    @chooser(instance_values=True)
    def type_choices(cls,a,b):
        logger.info("20111213 type_choices(%r,%r)",a,b)
        if a:
            ct = ContentType.objects.get_for_model(a.__class__)
            return LinkType.objects.filter(a_type=ct)
        if b:
            ct = ContentType.objects.get_for_model(b.__class__)
            return LinkType.objects.filter(a_type=ct)
        return []
      
    #~ owner_id_choices.instance_values = True
    #~ owner_id_choices = classmethod(owner_id_choices)
        
    def get_a_display(self,value):
        if self.type_id:
            try:
                return unicode(self.type.a_type.get_object_for_this_type(pk=value))
            except self.type.a_type.model_class().DoesNotExist,e:
                return "%s with pk %r does not exist" % (
                    full_model_name(self.type.a_type.model_class()),value)
    
    def get_b_display(self,value):
        if self.type_id:
            try:
                return unicode(self.type.b_type.get_object_for_this_type(pk=value))
            except self.type.b_type.model_class().DoesNotExist,e:
                return "%s with pk %r does not exist" % (
                    full_model_name(self.type.b_type.model_class()),value)
    
        
    #~ date = models.DateTimeField(_('Date'),
      #~ default=datetime.date.today) 
    #~ url = models.URLField(verify_exists=False)
    #~ name = models.CharField(max_length=200,blank=True,#null=True,
        #~ verbose_name=_('Name'))
            
    def __unicode__(self):
        if self.type_id:
            return force_unicode("%s (%s)" % self.b, self.type)
        return force_unicode("%(a)s - %(b)s" % (self.b, self.a))
        

class LinkTypes(dd.Table):
    model = 'links.LinkType'
    column_names = "name *"
    order_by = ["name"]
    
class Links(dd.Table):
    model = 'links.Link'
    #~ column_names = "id date user url name *"
    column_names = "type a b id *"
    order_by = ["id"]

class LinksByType(Links):
    master_key = 'type'

class LinksFromThis(Links):
    """
    List of Links who relate *from* this (whose a points to this).
    """
    label = _("Links from this")
    master = models.Model
    link_name = 'a'
    #~ master = ContentType # HACK
    column_names = 'type b a'
    
    def get_create_kw(self,master_instance,**kw):
        kw[self.link_name+'_id'] = master_instance.pk
        # we *must* store at least one type otherwise Link.type_choices() 
        # won't get the a (or b) instance
        ct = ContentType.objects.get_for_model(master_instance.__class__)
        types = LinkType.objects.filter(**{self.link_name+'_type':ct})
        if types.count() > 0:
            kw.update(type=types[0])
        return kw
        
    def get_filter_kw(self,master_instance,**kw):
        kw = self.get_create_kw(master_instance,**kw)
        ct = ContentType.objects.get_for_model(master_instance.__class__)
        types = LinkType.objects.filter(**{self.link_name+'_type':ct}).values_list('pk', flat=True)
        kw.update(type_id__in=types)
        return kw
      

class LinksToThis(LinksFromThis):
    """
    List of Links who relate *to* this (whose b points to this).
    """
    master = models.Model
    link_name = 'b'
    column_names = 'type a b'
    label = _("Links to this")


def setup_main_menu(site,ui,user,m): pass

def setup_my_menu(site,ui,user,m): pass
  
def setup_config_menu(site,ui,user,m): 
    m  = m.add_menu("links",_("~Links"))
    m.add_action('links.LinkTypes')
  
def setup_explorer_menu(site,ui,user,m):
    m  = m.add_menu("links",_("~Links"))
    m.add_action('links.Links')
  