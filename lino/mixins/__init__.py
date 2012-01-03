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

import datetime

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
#~ from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

from lino import dd
from lino.utils import perms
from lino.tools import full_model_name
from lino.utils.choosers import chooser
    

class AutoUser(models.Model):
    """
    Mixin for models that have a `user` field which is automatically 
    set to the requesting user.
    Also defines a `ByUser` base table which fills the master instance 
    from the web request.
    """
    class Meta:
        abstract = True
        
    if settings.LINO.user_model: 
      
        user = models.ForeignKey(settings.LINO.user_model,
            verbose_name=_("user"),
            related_name="%(app_label)s_%(class)s_set_by_user",
            blank=True,null=True
            )
        
        def on_create(self,req):
            if self.user is None:
                u = req.get_user()
                if u is not None:
                    self.user = u
            
        def update_owned_instance(self,task):
            task.user = self.user

if settings.LINO.user_model: 
  
    class ByUser(dd.Table):
        master_key = 'user'
        can_view = perms.is_authenticated
        
        @classmethod
        def init_label(self):
            return _("My %s") % self.model._meta.verbose_name_plural
            
        @classmethod
        def setup_request(self,rr):
            if rr.master_instance is None:
                rr.master_instance = rr.get_user()
else:
    # dummy report for userless sites
    class ByUser(dd.Table): pass 
  


class CreatedModified(models.Model):
    """
    Adds two timestamp fields `created` and `modified`.    
    
    We don't use Djangos auto_now and auto_now_add features because:
    
    - 20110829 the modified field did not get updated after save()
      didn't investigate further since the workaround shown at
      http://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add
      is ok for me.
      
    - :doc:`/blog/2011/0901`
    
    """
    class Meta:
        abstract = True
        
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)
    
    def save(self, *args, **kwargs):
        '''
        On save, update timestamps.
        '''
        if not settings.LINO.loading_from_dump:
            if not self.pk:
                self.created = datetime.datetime.now()
            self.modified = datetime.datetime.now()
        super(CreatedModified, self).save(*args, **kwargs)

        


class Sequenced(models.Model):
    """Abstract base class for models that have a sequence number `seqno`
    """
  
    class Meta:
        abstract = True
        ordering = ['seqno']
        
    seqno = models.IntegerField(
        blank=True,null=False,
        verbose_name=_("Seq.No."))
    
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
    """
    Mixin for models that are "owned" by other database objects.
    
    Defines three fields `owned_type`, `owned_id` and `owned`.
    And a class attribute :attr:`owner_label`.
    
    """
    # Translators: will also be concatenated with '(type)' '(object)'
    owner_label = _('Owned by')
    """
    The labels (`verbose_name`) of the fields 
    `owned_type`, `owned_id` and `owned`
    are derived from this attribute which 
    may be overridden by subclasses.
    
    """
    
    class Meta:
        abstract = True
        
    owner_type = models.ForeignKey(ContentType,
        editable=True,
        blank=True,null=True,
        verbose_name=string_concat(owner_label,' ',_('(type)')))
    owner_id = dd.GenericForeignKeyIdField(
        owner_type,
        editable=True,
        blank=True,null=True,
        verbose_name=string_concat(owner_label,' ',_('(object)')))
    owner = dd.GenericForeignKey(
        'owner_type', 'owner_id',
        verbose_name=owner_label)
        
    #~ owner_panel= dd.FieldSet(_("Owner"),
        #~ "owner_type owner_id",
        #~ owner_type=_("Model"),
        #~ owner_id=_("Instance"))
    
    
    @chooser(instance_values=True)
    def owner_id_choices(cls,owner_type):
        if owner_type:
            return owner_type.model_class().objects.all()
        return []
      
    #~ owner_id_choices.instance_values = True
    #~ owner_id_choices = classmethod(owner_id_choices)
        
    def get_owner_id_display(self,value):
        if self.owner_type:
            try:
                return unicode(self.owner_type.get_object_for_this_type(pk=value))
            except self.owner_type.model_class().DoesNotExist,e:
                return "%s with pk %r does not exist" % (
                    full_model_name(self.owner_type.model_class()),value)
            
            
    def update_owned_instance(self,task):
        m = getattr(self.owner,'update_owned_instance',None)
        if m:
            m(task)

    #~ def data_control(self):
        #~ "Used by :class:`lino.models.DataControlListing`."
        #~ msgs = []
        #~ ct = ContentType.objects.get_for_id()
        #~ ...
        #~ msgs.append(unicode(e))
        #~ return msgs


class ProjectRelated(models.Model):
    """Related to a project. 
    Deserves more documentation.
    """
    
    class Meta:
        abstract = True
        
    if settings.LINO.project_model:
        project = models.ForeignKey(settings.LINO.project_model,blank=True,null=True)

    def summary_row(self,ui,rr,**kw):
        s = ui.href_to(self)
        if settings.LINO.project_model:
            if self.project and not dd.has_fk(rr,'project'):
                s += " (" + ui.href_to(self.project) + ")"
        return s
            


from lino.mixins.printable import Printable, PrintableType, CachedPrintable, TypedPrintable, Listing
from lino.mixins.uploadable import Uploadable
from lino.utils.dblogger import DiffingMixin
#~ from lino.mixins.personal import SexField, PersonMixin