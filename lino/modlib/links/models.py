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

from lino import fields
#~ from lino import tools
from lino import reports
from lino import mixins
from lino.fields import VirtualField
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
        


class LinkField(fields.VirtualField):
    """
    Used to define the two fields 'a' and 'b' on the Link model.
    """
  
    def __init__(self,fk_field,name,*args,**kw):
        self.fk_field = fk_field
        self.typefield_name = name + '_type' 
        self.idfield_name = name + '_id' 
        fields.VirtualField.__init__(self,fields.DynamicForeignKey(self),self.get_value)
    
    def get_contenttype(self,obj):
        if not getattr(obj,self.fk_field.name + "_id"):
            logger.info("20111209 get_contenttype() no type_id in %s", obj2str(obj))
            return None
        link_type = getattr(obj,self.fk_field.name)
        #~ link_type = obj.type
        return getattr(link_type,self.type_field_name)
        
    def to_python(self, value):
        if isinstance(value,models.Model):
            return value
        if not value:
            return value
        raise Exception("Cannot know contenttype for %r" % value)
        #~ ct = self.get_contenttype(obj)
        #~ if ct is None:
            #~ return None
        #~ return ct.get_object_for_this_type(pk=pk)
            
        #~ return value
        
    def get_prep_value(self, value):
        if value:
            return value.pk
        return None
        
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)
        #~ return self.get_db_prep_value(value,connection)
        
    #~ def save_form_data(self, instance, data):
        #~ setattr(instance, self.name, data)
        
    #~ def get_text_for_value(self,value):
        #~ return self.choicelist.get_text_for_value(value.value)
        
    def __get__(self,obj):
        return self.get_value(obj)
        
    def get_value(self,obj,request=None):
        """
        The optional 2nd argument `request` (passed from
        `VirtualField.value_from_object`) is ignored.
        """
        pk = getattr(obj,self.name+'_id')
        if pk is None:
            return None
        ct = self.get_contenttype(obj)
        if ct is None:
            return None
        return ct.get_object_for_this_type(pk=pk)
        
        #~ try:
            #~ return ct.get_object_for_this_type(pk=pk)
        #~ except model.DoesNotExist:
            #~ return None

    def set_value_in_object(self,request,obj,v):
        raise Exception("20111208")
        if not v:
            setattr(obj,self.name,None)
            return 
            
        ct = self.get_contenttype(obj)
        if ct is None:
            raise Exception("20111209")
            return None
        
        if not isinstance(v,ct.model_class()):
            raise Exception("20111209")
        setattr(obj,self.name,v.pk)






#~ class Link(mixins.Reminder):
#~ class Link(mixins.AutoUser):
class Link(models.Model):
    "Implements :class:`links.Link`."
    
    #~ allow_cascaded_delete = True
    
    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")
    
    type = models.ForeignKey("links.LinkType")

    #~ a = fields.DynamicGeneralForeignKey(type,'a_type',blank=True,null=True)
    #~ b = fields.DynamicGeneralForeignKey(type,'b_type',blank=True,null=True)
    
    a_id = models.PositiveIntegerField(
        # editable=True,
        blank=True,null=True,
        verbose_name=_('(a object)'))
    b_id = models.PositiveIntegerField(
        # editable=True,
        blank=True,null=True,
        verbose_name=_('(b object)'))
        
    #~ a = LinkField(type,'a')
    #~ b = LinkField(type,'b')
    
    a = fields.LinkedForeignKey(type,'a')
    b = fields.LinkedForeignKey(type,'b')
    
    
    #~ a = fields.GenericForeignKey(
        #~ 'type__a_type', 'a_id',
        #~ verbose_name=_("Link origin"))
    #~ b = fields.GenericForeignKey(
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
      
    #~ owner_id_choices.instance_values = True
    #~ owner_id_choices = classmethod(owner_id_choices)
        
    def get_a_display(self,value):
        if self.type:
            try:
                return unicode(self.type.a_type.get_object_for_this_type(pk=value))
            except self.type.a_type.model_class().DoesNotExist,e:
                return "%s with pk %r does not exist" % (
                    full_model_name(self.type.a_type.model_class()),value)
    
    def get_b_display(self,value):
        if self.type:
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
        return force_unicode(_("%s is %s of %s")) % (self.b, self.type, self.a)
        

class LinkTypes(reports.Report):
    model = 'links.LinkType'
    column_names = "name *"
    order_by = ["name"]
    
class Links(reports.Report):
    model = 'links.Link'
    #~ column_names = "id date user url name *"
    column_names = "type a b id *"
    order_by = ["id"]

class LinksByType(Links):
    fk_name = 'type'

class LinksFromThis(Links):
    """
    List of Links who relate *from* this (whose a points to this).
    """
    label = _("Links from this")
    master = models.Model
    link_name = 'a'
    #~ master = ContentType # HACK
    column_names = 'type b'
    
    def get_create_kw(self,master_instance,**kw):
        kw[self.link_name+'_id'] = master_instance.pk
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
    column_names = 'type a'
    label = _("Links to this")


def setup_main_menu(site,ui,user,m): pass

def setup_my_menu(site,ui,user,m): pass
  
def setup_config_menu(site,ui,user,m): 
    m  = m.add_menu("links",_("~Links"))
    m.add_action('links.LinkTypes')
  
def setup_explorer_menu(site,ui,user,m):
    m  = m.add_menu("links",_("~Links"))
    m.add_action('links.Links')
  