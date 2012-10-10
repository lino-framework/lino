## Copyright 2010-2012 Luc Saffre
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

import logging
logger = logging.getLogger(__name__)


import datetime

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
#~ from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

from lino import dd
#~ from lino.models import Workflow
#~ from lino.utils import perms
from lino.core.modeltools import full_model_name
from lino.core import frames
from lino.core import actions
from lino.utils.choosers import chooser
from lino.mixins.duplicable import Duplicable


#~ class Owned(dd.Model):
class Controllable(dd.Model):
    """
    Mixin for models that are "controllable" by another database object.
    
    Defines three fields `owned_type`, `owned_id` and `owned`.
    And a class attribute :attr:`owner_label`.
    
    For example in :mod:`lino.modlibs.cal`, the owner of a Task or Event 
    is some other database object that caused the task's or event's 
    creation.
    
    Or in :mod:`lino.modlib.sales` and :mod:`lino.modlib.purchases`,
    an invoice may cause one or several Tasks 
    to be automatically generated when a certain payment mode 
    is specified.
    
    Controllable objects are "governed" or "controlled"
    by their controller:
    If the controller gets modified, it may decide to delete or 
    modify some or all of her controlled objects.
    
    Non-automatic tasks always have an empty `controller` field.
    Some fields are read-only on an automatic Task because 
    it makes no sense to modify them.
    
    """
    # Translators: will also be concatenated with '(type)' '(object)'
    owner_label = _('Controlled by')
    """
    The labels (`verbose_name`) of the fields 
    `owned_type`, `owned_id` and `owned`
    are derived from this attribute which 
    may be overridden by subclasses.
    """
    
    controller_is_optional = True
    """
    Whether the controller is optional (may be NULL)
    """
    
    class Meta:
        abstract = True
        
    owner_type = dd.ForeignKey(ContentType,
        editable=True,
        blank=controller_is_optional,null=controller_is_optional,
        verbose_name=string_concat(owner_label,' ',_('(type)')))
    owner_id = dd.GenericForeignKeyIdField(
        owner_type,
        editable=True,
        blank=controller_is_optional,null=controller_is_optional,
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
      
    def get_owner_id_display(self,value):
        if self.owner_type:
            try:
                return unicode(self.owner_type.get_object_for_this_type(pk=value))
            except self.owner_type.model_class().DoesNotExist,e:
                return "%s with pk %r does not exist" % (
                    full_model_name(self.owner_type.model_class()),value)
            
            
    def update_owned_instance(self,controllable):
        """
        If this (acting as a controller) is itself controlled, 
        forward the call to the controller.
        """
        if self.owner:
            self.owner.update_owned_instance(controllable)
        #~ m = getattr(self.owner,'update_owned_instance',None)
        #~ if m:
            #~ m(controllable)

    def save(self,*args,**kw):
        if self.owner: #  and not self.is_user_modified():
            self.owner.update_owned_instance(self)
            #~ print "20120627 called update_owned_instance of ", self.owner.__class__
            #~ m = getattr(self.owner,'update_owned_instance',None)
            #~ if m:
                #~ m(self)
        super(Controllable,self).save(*args,**kw)
        if self.owner: #  and self.is_user_modified():
            self.owner.after_update_owned_instance(self)
            #~ m = getattr(self.owner,'after_update_owned_instance',None)
            #~ if m:
                #~ m(self)



class UserAuthored(dd.Model):
    """
    Mixin for models that have a `user` field which is automatically 
    set to the requesting user.
    Also defines a `ByUser` base table which fills the master instance 
    from the web request.
    """
    class Meta:
        abstract = True
        
    #~ user = models.ForeignKey('contacts.Partner',
        #~ verbose_name=_("user"),
        #~ related_name="%(app_label)s_%(class)s_set_by_user",
        #~ blank=True,null=True
        #~ )
            
    if settings.LINO.user_model: 
      
        workflow_owner_field = 'user' # used by :mod:`lino.modlib.workflows.models`
        
        user = models.ForeignKey(settings.LINO.user_model,
            verbose_name=_("Author"),
            related_name="%(app_label)s_%(class)s_set_by_user",
            blank=True,null=True
            )
        
    #~ def on_duplicate(self,ar):
        #~ self.user = ar.get_user()
        #~ super(AutoUser,self).on_duplicate(ar)
        
        
    def on_create(self,ar):
        """
        Adds the requesting user to the `user` field.
        """
        if self.user_id is None:
            u = ar.get_user()
            if u is not None:
                self.user = u
        super(UserAuthored,self).on_create(ar)
        
    #~ def update_owned_instance(self,other):
        #~ print '20120627 AutoUser.update_owned_instance'
        #~ other.user = self.user
        #~ super(UserAuthored,self).update_owned_instance(other)
        

    def get_row_permission(self,user,state,ba):
        """
        Only system managers can edit other users' work.
        """
        if not super(UserAuthored,self).get_row_permission(user,state,ba):
            #~ logger.info("20120919 no permission to %s on %s for %r",action,self,user)
            return False
        if self.user != user and user.profile.level < dd.UserLevels.manager:
            #~ logger.info("20120919 no permission to %s on %r because %r != %r",action,self,self.user,user)
            return ba.action.readonly
        return True

AutoUser = UserAuthored # backwards compatibility


if settings.LINO.user_model: 
  
    class ByUser(dd.Table):
        master_key = 'user'
        #~ can_view = perms.is_authenticated
        
        @classmethod
        def get_actor_label(self):
            return string_concat(
                _("My "),self.model._meta.verbose_name_plural)
            #~ return _("My %s") % self.model._meta.verbose_name_plural
            
        @classmethod
        def setup_request(self,ar):
            #~ logger.info("mixins.ByUser.setup_request")
            if ar.master_instance is None:
                ar.master_instance = ar.get_user()
                
                
else:
  
    # dummy Table for userless sites
    class ByUser(dd.Table): pass 
  



class CreatedModified(dd.Model):
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
        
    created = models.DateTimeField(_("Created"),editable=False)
    modified = models.DateTimeField(_("Modified"),editable=False)
    
    def save(self, *args, **kwargs):
        '''
        On save, update timestamps.
        '''
        if not settings.LINO.loading_from_dump:
            if not self.pk:
                self.created = datetime.datetime.now()
            self.modified = datetime.datetime.now()
        super(CreatedModified, self).save(*args, **kwargs)


class Sequenced(Duplicable):
    """
    Abstract base class for models that have a sequence number `seqno`.
    """
  
    class Meta:
        abstract = True
        ordering = ['seqno']
        
    seqno = models.IntegerField(
        blank=True,null=False,
        verbose_name=_("Seq.No."))
        
        
    @dd.action(_("Duplicate"))
    def duplicate_row(self,ar):
        #~ print '20120605 duplicate_row', self.seqno, self.account
        seqno = self.seqno
        qs = self.get_siblings().filter(seqno__gte=seqno).reverse()
        for s in qs:
            #~ print '20120605 duplicate_row inc', s.seqno, s.account
            s.seqno += 1
            s.save()
        return super(Sequenced,self).duplicate_row.run(self,ar,seqno=seqno)
        
    def __unicode__(self):
        return unicode(_("Row # %s") % self.seqno)
        
    
    def get_siblings(self):
        """
        The default implementation sets a global sequencing
        by returning all objects of this model.
        Overridden in :class:`lino.modlib.thirds.models.Third`.
        """
        return self.__class__.objects.order_by('seqno')      
        
    def set_seqno(self):
        """
        Initialize `seqno` to the `seqno` of eldest sibling + 1.
        """
        qs = self.get_siblings()
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
  

class ProjectRelated(dd.Model):
    """
    Mixin for Models that are automatically 
    related to a "project". 
    A project means here 
    "the central most important thing that is used to classify most other things".
    For example in lino.apps.pcsw, the "project" is a Client.
    
    Whether an application has such a concept of "project", 
    and which model has this privileged status, 
    is set in :attr:`lino.Lino.project_model`.
    
    """
    
    class Meta:
        abstract = True
        
    if settings.LINO.project_model:
        project = models.ForeignKey(
            settings.LINO.project_model,
            blank=True,null=True,
            related_name="%(app_label)s_%(class)s_set_by_project",
            )

    #~ def summary_row(self,ui,rr,**kw):
    def summary_row(self,ar,**kw):
        s = ar.href_to(self)
        #~ s = ui.ext_renderer.href_to(self)
        if settings.LINO.project_model:
            #~ if self.project and not dd.has_fk(rr,'project'):
            if self.project:
                #~ s += " (" + ui.href_to(self.project) + ")"
                s += " (" + ar.href_to(self.project) + ")"
        return s
            
    def update_owned_instance(self,other):
        """
        When a :class:`project-related <ProjectRelated>` 
        object controls another project-related object, 
        then the controlled automatically inherits 
        the `project` of its controller.
        """
        if isinstance(other,ProjectRelated):
            other.project = self.project
        super(ProjectRelated,self).update_owned_instance(other)
        
    def get_mailable_recipients(self):
        if isinstance(self.project,settings.LINO.modules.contacts.Partner):
            if self.project.email:
                yield ('to',self.project)
        for r in super(ProjectRelated,self).get_mailable_recipients():
            yield r

    def get_postable_recipients(self):
        if isinstance(self.project,settings.LINO.modules.contacts.Partner):
            yield self.project
        for p in super(ProjectRelated,self).get_postable_recipients():
            yield p


from lino.mixins.printable import Printable, PrintableType, CachedPrintable, TypedPrintable, DirectPrintAction
from lino.mixins.uploadable import Uploadable
#~ from lino.mixins.mails import Recipient, Mail
#~ from lino.utils.dblogger import DiffingMixin
#~ from lino.mixins.personal import SexField, PersonMixin

from lino.core import actions
from lino.mixins import printable


class EmptyTable(frames.Frame):
    """
    A "Table" that has exactly one virtual row and thus is visible 
    only using a Detail view on that row.
    """
    #~ debug_permissions = True
    #~ has_navigator = False
    #~ hide_top_toolbar = True
    hide_navigator = True
    default_list_action_name = 'show'
    default_elem_action_name =  'show'
    #~ default_action = actions.ShowEmptyTable()
    
    do_print = DirectPrintAction()
    #~ show = actions.ShowEmptyTable()
    
    @classmethod
    def get_default_action(cls):
        #~ return actions.BoundAction(cls,cls.show)
        #~ return 'show'
        return actions.ShowEmptyTable()
        
    
    
    #~ @classmethod
    #~ def do_setup(self):
        #~ # logger.info("%s.__init__()",self.__class__)
        #~ # if not self.__class__ is Frame:
        #~ if self is not EmptyTable:
            #~ # assert self.default_action_class is None
            #~ # if self.label is None:
                #~ # raise Exception("%r has no label" % self)
            #~ # self.default_action = actions.ShowEmptyTable()
            #~ # self.default_action = self.add_action(actions.ShowEmptyTable())
            #~ super(Frame,self).do_setup()
            #~ # self.setup_actions()
            #~ # self.add_action(self.default_action)

    #~ @classmethod
    #~ def setup_actions(self):
        #~ super(EmptyTable,self).setup_actions()
        #~ from lino.mixins.printable import DirectPrintAction
        #~ self.add_action(DirectPrintAction())
        
            
    @classmethod
    def create_instance(self,req,**kw):
        #~ if self.known_values:
            #~ kw.update(self.known_values)
        if self.parameters:
            kw.update(req.param_values)

        #~ for k,v in req.param_values.items():
            #~ kw[k] = v
        #~ for k,f in self.parameters.items():
            #~ kw[k] = f.value_from_object(None)
        obj = actions.EmptyTableRow(self,**kw)
        kw = req.ah.store.row2dict(req,obj)
        obj._data = kw
        obj.update(**kw)
        return obj
    
    #~ @classmethod
    #~ def elem_filename_root(self,elem):
        #~ return self.app_label + '.' + self.__name__

    @classmethod
    def get_data_elem(self,name):
        de = super(EmptyTable,self).get_data_elem(name)
        if de is not None:
            return de
        a = name.split('.')
        if len(a) == 2:
            return getattr(getattr(settings.LINO.modules,a[0]),a[1])
            


#~ from lino.models import Workflowable