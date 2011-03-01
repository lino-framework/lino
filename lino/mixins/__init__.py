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

"""

"""

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from lino import reports
from lino.utils import perms
    
class MultiTableBase(models.Model):
  
    """
    Mixin for Models that use `Multi-table inheritance 
    <http://docs.djangoproject.com/en/dev/topics/db/models/#multi-table-inheritance>`__.
    Subclassed by :class:`lino.modlib.journals.models.Journaled`.
    """
    class Meta:
        abstract = True
    
    def get_child_model(self):
        return self.__class__
        
    def get_child_instance(self):
        model = self.get_child_model()
        if model is self.__class__:
            return self
        related_name = model.__name__.lower()
        return getattr(self,related_name)
        
class AutoUser(models.Model):
  
    class Meta:
        abstract = True
        
    user = models.ForeignKey("auth.User",verbose_name=_("user")) # ,blank=True,null=True)
    
    def on_create(self,req):
        u = req.get_user()
        if u is not None:
            self.user = u
        
#~ class ByUser(object):
class ByUser(reports.Report):
    fk_name = 'user'
    can_view = perms.is_authenticated
    
    def setup_request(self,req):
        if req.master_instance is None:
            req.master_instance = req.get_user()


class Owned(models.Model):
  
    class Meta:
        abstract = True
        
    owner_type = models.ForeignKey(ContentType,verbose_name=_('Owner type'))
    owner_id = models.PositiveIntegerField(verbose_name=_('Owner'))
    owner = generic.GenericForeignKey('owner_type', 'owner_id')
    
    def owner_id_choices(self,owner_type):
      #~ ct = ContentType.objects.get(pk=owner_type)
      return owner_type.model_class().objects.all()
    owner_id_choices.instance_values = True
    owner_id_choices = classmethod(owner_id_choices)
        
    def get_owner_id_display(self,value):
        return unicode(self.owner_type.get_object_for_this_type(pk=value))
            


class DiffingMixin(object):
    """
    Unmodified copy of http://djangosnippets.org/snippets/1683/
    
    Used by :mod:`lino.utils.dblogger`.
    """
    def __init__(self, *args, **kwargs):
        super(DiffingMixin, self).__init__(*args, **kwargs)
        self._original_state = dict(self.__dict__)
        
    def save(self, *args, **kwargs):
        state = dict(self.__dict__)
        del state['_original_state']
        self._original_state = state
        super(DiffingMixin, self).save()
    def is_dirty(self):
        missing = object()
        result = {}
        for key, value in self._original_state.iteritems():
            if value != self.__dict__.get(key, missing):
                return True
        return False
    def changed_columns(self):
        missing = object()
        result = {}
        for key, value in self._original_state.iteritems():
            if value != self.__dict__.get(key, missing):
                result[key] = {'old':value, 'new':self.__dict__.get(key, missing)}
        return result





from lino.mixins.reminder import Reminder
from lino.mixins.printable import Printable, PrintableType, TypedPrintable
from lino.mixins.uploadable import Uploadable
from lino.mixins.addressable import ContactDocument, PartnerDocument

