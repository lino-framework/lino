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

from lino import reports, fields
from lino.utils import perms
from lino.tools import full_model_name
from lino.utils.choosers import chooser
    
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
        
    user = models.ForeignKey("users.User",verbose_name=_("user")) # ,blank=True,null=True)
    
    def on_create(self,req):
        u = req.get_user()
        if u is not None:
            self.user = u
        
class ByUser(reports.Report):
    fk_name = 'user'
    can_view = perms.is_authenticated
    
    def setup_request(self,req):
        if req.master_instance is None:
            req.master_instance = req.get_user()


class CreatedModified(models.Model):
    """Adds two timestamp fields `created` and `modified`."""
    class Meta:
        abstract = True
    created = models.DateTimeField(auto_now_add=True,editable=False)   # iCal:DTSTAMP
    modified = models.DateTimeField(auto_now=True,editable=False)   # iCal:LAST-MODIFIED
        


class Sequenced(models.Model):
    """Abstract base class for models that have a 
    sequence number `seqno`
    """
  
    class Meta:
        abstract = True
        
    seqno = models.IntegerField(
        blank=True,null=False,
        verbose_name=_("Seq.No."))
    
    def set_seqno(self):
        raise NotImplementedError
    
    def set_seqno(self):
        """The default implementation sets a global sequencing. 
        Overridden in :class:`lino.modlib.thirds.models.Third`.
        """
        qs = self.__class__.objects.order_by('seqno')
        n = qs.count()
        if n == 0:
            self.seqno = 1
        else:
            last = qs[n-1]
            self.seqno = last.seqno + 1
        
    
    def full_clean(self,*args,**kw):
        if self.seqno is None:
            self.set_seqno()
        super(Sequenced,self).full_clean(*args,**kw)
  
class Owned(models.Model):
  
    class Meta:
        abstract = True
        
    owner_type = models.ForeignKey(ContentType,editable=True,        
        blank=True,null=True,
        verbose_name=_('Owner type'))
    #~ owner_id = models.PositiveIntegerField(editable=True,
        #~ blank=True,null=True,
        #~ verbose_name=_('Owner'))
    owner_id = fields.GenericForeignKeyIdField(owner_type,
        editable=True,
        blank=True,null=True,
        verbose_name=_('Owner'))
    owner = generic.GenericForeignKey('owner_type', 'owner_id')
    
    @chooser(instance_values=True)
    def owner_id_choices(cls,owner_type):
        #~ ct = ContentType.objects.get(pk=owner_type)
        if owner_type:
            return owner_type.model_class().objects.all()
      
    #~ owner_id_choices.instance_values = True
    #~ owner_id_choices = classmethod(owner_id_choices)
        
    def get_owner_id_display(self,value):
        if self.owner_type:
            try:
                return unicode(self.owner_type.get_object_for_this_type(pk=value))
            except self.owner_type.model_class().DoesNotExist,e:
                return "%s with pk %r does not exist" % (
                    full_model_name(self.owner_type.model_class()),value)
            


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
from lino.mixins.printable import Listing
from lino.mixins.uploadable import Uploadable
#~ from lino.mixins.addressable import ContactDocument, PartnerDocument

