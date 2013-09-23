## Copyright 2010-2013 Luc Saffre
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

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


import datetime

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
#~ from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.core.exceptions import ValidationError


from lino.core import auth
from lino.core.dbutils import full_model_name
from lino.core import frames
from lino.core import actions
from lino.core import fields
from lino.core import dbtables
from lino.core import model
from lino.core.requests import VirtualRow
from lino.core.actors import Actor
from lino.utils.choosers import chooser
from lino.mixins.duplicable import Duplicable, Duplicate
from lino.core.dbutils import navinfo
from lino.utils import AttrDict
from lino.utils import curry
from north.dbutils import BabelCharField
from lino.utils.xmlgen.html import E

#~ class Owned(dd.Model):
class Controllable(model.Model):
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
        
    owner_type = fields.ForeignKey(ContentType,
        editable=True,
        blank=controller_is_optional,null=controller_is_optional,
        verbose_name=string_concat(owner_label,' ',_('(type)')))
    owner_id = fields.GenericForeignKeyIdField(
        owner_type,
        editable=True,
        blank=controller_is_optional,null=controller_is_optional,
        verbose_name=string_concat(owner_label,' ',_('(object)')))
    owner = fields.GenericForeignKey(
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
        if settings.SITE.loading_from_dump:
            super(Controllable,self).save(*args,**kw)
        else:
            if self.owner: #  and not self.is_user_modified():
                self.owner.update_owned_instance(self)
            super(Controllable,self).save(*args,**kw)
            if self.owner: #  and self.is_user_modified():
                self.owner.after_update_owned_instance(self)



class UserAuthored(model.Model):
    """
    Mixin for models that have a `user` field which is automatically 
    set to the requesting user.
    Also defines a `ByUser` base table which fills the master instance 
    from the web request.
    """
    required = dict(auth=True)
    class Meta:
        abstract = True
        
    if settings.SITE.user_model: 
      
        workflow_owner_field = 'user' 
        
        user = models.ForeignKey(settings.SITE.user_model,
            verbose_name=_("Author"),
            related_name="%(app_label)s_%(class)s_set_by_user",
            blank=True,null=True
            )
            
    else:
      
        user = fields.DummyField()
        
    #~ def on_duplicate(self,ar):
        #~ self.user = ar.get_user()
        #~ super(AutoUser,self).on_duplicate(ar)
        
    def on_create(self,ar):
        """
        Adds the requesting user to the `user` field.
        
        When acting as another user, the default implementation
        still inserts the real user, not subst_user. 
        This is important for cal.Event.
        """
        if self.user_id is None:
            #~ u = ar.get_user() 
            u = ar.user
            if u is not None:
                self.user = u
        super(UserAuthored,self).on_create(ar)
        
    #~ def update_owned_instance(self,other):
        #~ print '20120627 AutoUser.update_owned_instance'
        #~ other.user = self.user
        #~ super(UserAuthored,self).update_owned_instance(other)
        
    manager_level_field = 'level'
    """
    Only system managers can edit other users' work. 
    But if the application defines customized UserGroups, 
    then we may want to permit it also to department managers.
    If an application defines a UserGroup `foo`, 
    then it can set this attribute to `'foo_level'` 
    on a model to specify that a manager level for 
    the foo department is enough to get edit permission on other users' instances.
    
    Usage examples see 
    :class:`lino.modlib.notes.models.Note`
    or
    :class:`lino.modlib.cal.models.Component`.
    """
    
    def get_row_permission(self,ar,state,ba):
        """
        Only system managers can edit other users' work.
        """
        if not super(UserAuthored,self).get_row_permission(ar,state,ba):
            #~ logger.info("20120919 no permission to %s on %s for %r",action,self,user)
            return False
        user = ar.get_user()
        if self.user != user and getattr(user.profile,self.manager_level_field) < auth.UserLevels.manager:
            return ba.action.readonly
        return True

AutoUser = UserAuthored # backwards compatibility

class AuthorAction(actions.Action):
    """
    """
    manager_level_field = 'level'
    
    def get_action_permission(self,ar,obj,state):
        user = ar.get_user()
        if obj.user != user and getattr(user.profile,self.manager_level_field) < auth.UserLevels.manager:
            return self.readonly
        return super(actions.AuthorAction,self).get_action_permission(ar,obj,state)
        
        
class RegisterAction(actions.Action):
    label = _("Register")
    show_in_workflow = True
    readonly = False
    
    #~ icon_file = 'flag_green.png'
    #~ required = dict(states='draft')
    help_text = _("Register this object.")
    
    def attach_to_actor(self,actor,name):
        if not issubclass(actor.model,Registrable):
            raise Exception("%s is not a Registrable" % actor.model)
        if actor.workflow_state_field is None:
            # e.g. ledger.Voucher is an "abstract Registrable"
            return False
        self.target_model = actor.model
        self.required = self.target_model.required_to_register
        return super(RegisterAction,self).attach_to_actor(actor,name)
  
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        #~ ar.confirm(self.help_text,_("Are you sure?"))
        obj.register(ar)
        obj.save()
        kw.update(refresh=True)
        return kw
    
    
        
class DeregisterAction(actions.Action):
    label = _("Deregister")
    show_in_workflow = True
    readonly = False
    
    #~ icon_file = 'cancel.png'
    #~ required = dict(states='registered paid')
    help_text=_("Deregister this object.")
    
    def attach_to_actor(self,actor,name):
        if not issubclass(actor.model,Registrable):
            raise Exception("%s is not a Registrable" % actor.model)
        if actor.workflow_state_field is None:
            # e.g. ledger.Voucher is an "abstract Registrable"
            return False
        self.target_model = actor.model
        self.required = self.target_model.required_to_deregister
        #~ logger.info("20121208 DeregisterAction.attach_to_actor() %s %s",actor,actor.model.required_to_deregister)
        return super(DeregisterAction,self).attach_to_actor(actor,name)
  
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        #~ ar.confirm(self.help_text,_("Are you sure?"))
        obj.deregister(ar)
        obj.save()
        kw.update(refresh=True)
        return kw


class Registrable(model.Model):
    """
    Base class to anything that may be "registered" and "deregistered".
    E.g. Invoices, Vouchers, Declarations are candidates. 
    "Registered" in general means "this object has been taken account of". 
    Registered objects generally are not editable.
    """
    class Meta:
        abstract = True
        
    workflow_state_field = 'state'
    
    required_to_register = dict(states='draft')
    #~ required_to_deregister = dict(states='registered paid')
    required_to_deregister = dict(states='registered')
    
    register_action = RegisterAction()
    deregister_action = DeregisterAction()
    
    _registrable_fields = None
    
    @classmethod
    def get_registrable_fields(cls,site):
        return
        yield 'date'
        
        
    @classmethod
    def on_analyze(cls,site):
        super(Registrable,cls).on_analyze(site)
        cls._registrable_fields = set(cls.get_registrable_fields(site))
        #~ logger.info("20130128 %s %s",cls,cls._registrable_fields)
    
    def disabled_fields(self,ar):
        if not self.state.editable:
            return self._registrable_fields
        return super(Registrable,self).disabled_fields(ar)
    
    
    def get_row_permission(self,ar,state,ba):
        """
        Only invoices in an editable state may be edited.
        """
        #~ if isinstance(ba.action,actions.DeleteSelected):
            #~ logger.info("20130128 Registrable.get_row_permission %s %s %s %s",
                #~ self,state,ba.action,ar.bound_action.action.readonly)
        if state and not state.editable:
            if not ar.bound_action.action.readonly:
                return False
        return super(Registrable,self).get_row_permission(ar,state,ba)
    
        
    def register(self,ar):
        """
        Register this item. 
        The base implementation just sets the state to "registered".
        Subclasses may override this to add custom behaviour.
        """
        state_field = self._meta.get_field('state')
        self.state = state_field.choicelist.registered
        
    def deregister(self,ar):
        """
        Deregister this item. 
        The base implementation just sets the state to "draft".
        Subclasses may override this to add custom behaviour.
        """
        state_field = self._meta.get_field('state')
        self.state = state_field.choicelist.draft
        
    def before_printable_build(self,bm):
        state_field = self._meta.get_field('state')
        if self.state != state_field.choicelist.registered:
            self.register(None)
            self.save()



if settings.SITE.user_model: 
  
    class ByUser(dbtables.Table):
        master_key = 'user'
        #~ can_view = perms.is_authenticated
        
        @classmethod
        def get_actor_label(self):
            if self.model is None: 
                return self._label or self.__name__
            #~ return self._label or string_concat(_("My "),self.model._meta.verbose_name_plural)
            return self._label or _("My %s") % self.model._meta.verbose_name_plural
            #~ return _("My %s") % self.model._meta.verbose_name_plural
            
        @classmethod
        def setup_request(self,ar):
            #~ logger.info("mixins.ByUser.setup_request")
            if ar.master_instance is None:
                ar.master_instance = ar.get_user()
                
                
else:
  
    # dummy Table for userless sites
    class ByUser(dbtables.Table): pass 
  



class CreatedModified(model.Model):
    """
    Adds two timestamp fields `created` and `modified`.    
    
    We don't use Django's `auto_now` and `auto_now_add` features because:
    
    - 20110829 the modified field did not get updated after save()
      didn't investigate further since the workaround shown at
      http://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add
      is ok for me.
      
    - `/blog/2011/0901`
    
    """
    class Meta:
        abstract = True
        
    created = models.DateTimeField(_("Created"),editable=False)
    modified = models.DateTimeField(_("Modified"),editable=False)
    
    def save(self, *args, **kwargs):
        '''
        On save, update timestamps.
        '''
        if not settings.SITE.loading_from_dump:
            #~ if not self.pk:
            if self.created is None:
                self.created = datetime.datetime.now()
            self.modified = datetime.datetime.now()
        super(CreatedModified, self).save(*args, **kwargs)



class MoveUp(actions.Action):
    label = _("Up")
    #~ label = "\u2191" thin arrow up
    #~ label = "\u25b2" # triangular arrow up
    custom_handler = True
    icon_name = 'arrow_up'
    #~ icon_file = 'arrow_up.png'
    help_text = _("Move this row one row upwards")
    
    def get_action_permission(self,ar,obj,state):
        #~ return False
        if ar.data_iterator is None: return False
        if ar.data_iterator.count() == 0: return False
        if ar.data_iterator[0] == obj: return False
        return super(MoveUp,self).get_action_permission(ar,obj,state)
    
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        obj.swap_seqno(ar,-1)
        #~ obj.move_up()
        kw = dict()
        #~ kw.update(refresh=True)
        kw.update(refresh_all=True)
        kw.update(message=_("Moved up."))
        return ar.success(**kw)
        
class MoveDown(actions.Action):
    label = _("Down")
    #~ label = "\u2193"
    #~ label = "\u25bc" # triangular arrow down
    custom_handler = True
    icon_name = 'arrow_down'
    #~ icon_file = 'arrow_down.png'
    help_text = _("Move this row one row downwards")
    
    def get_action_permission(self,ar,obj,state):
        if ar.data_iterator is None: return False
        if ar.data_iterator.count() == 0: return False
        if ar.data_iterator[ar.data_iterator.count()-1] == obj: return False
        #~ if obj.__class__.__name__=='Entry' and obj.seqno == 25:
            #~ print 20130706, ar.data_iterator.count(), ar.data_iterator
        return super(MoveDown,self).get_action_permission(ar,obj,state)
    
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        obj.swap_seqno(ar,1)
        #~ obj.move_down()
        kw = dict()
        #~ kw.update(refresh=True)
        kw.update(refresh_all=True)
        kw.update(message=_("Moved down."))
        return ar.success(**kw)
        

class DuplicateSequenced(Duplicate):
  
    def run_from_code(self,ar,**kw):
        obj = ar.selected_rows[0]
  
        #~ print '20120605 duplicate', self.seqno, self.account
        seqno = obj.seqno
        qs = obj.get_siblings().filter(seqno__gte=seqno).reverse()
        if qs is None:
            raise Exception("20121227 TODO: Tried to duplicate a root element?")
        for s in qs:
            #~ print '20120605 duplicate inc', s.seqno, s.account
            s.seqno += 1
            s.save()
        kw.update(seqno=seqno)
        return super(DuplicateSequenced,self).run_from_code(ar,**kw)
  

class Sequenced(Duplicable):
    """
    Abstract base class for models that have a field `seqno`
    containing a "sequence number".
    """
  
    class Meta:
        abstract = True
        ordering = ['seqno']
        
    seqno = models.IntegerField(
        blank=True,null=False,
        verbose_name=_("Seq.No."))
        
    duplicate = DuplicateSequenced()
    move_up = MoveUp()
    move_down = MoveDown()
        
    def __unicode__(self):
        return unicode(_("Row # %s") % self.seqno)
    
    def get_siblings(self):
        """
        Return a Django Queryset with all siblings of this,
        or `None` if this is a root element which cannot have anu siblings.
        The queryset will of course include self.
        The default implementation sets a global sequencing
        by returning all objects of self's model.
        Overridden e.g. in 
        :class:`lino.modlib.thirds.models.Third`
        or
        :class:`lino_welfare.modlib.debts.models.Entry`.
        """
        return self.__class__.objects.order_by('seqno')      
        
    def set_seqno(self):
        """
        Initialize `seqno` to the `seqno` of eldest sibling + 1.
        """
        qs = self.get_siblings()
        if qs is None:
            self.seqno = 0
        else:
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
        
    #~ def move_up(self)
        #~ """
        #~ Move this row "one position up" within its siblings
        #~ """
        #~ qs = self.get_siblings()
        #~ if qs is None:
            #~ return
        #~ nav = AttrDict(**navinfo(qs,self))
        #~ if not nav.recno:
            #~ return
        #~ if not nav.prev:
            #~ return
        #~ prev = qs.get(pk=nav.prev)
        #~ if self.seqno == prev.seqno:
            #~ return
        #~ prev_seqno  = prev.seqno 
        #~ prev.seqno = self.seqno
        #~ self.seqno = prev_seqno 
        #~ self.save()
        #~ prev.save()
        
    def swap_seqno(self,ar,offset):
        """
        Move this row "up or down" within its siblings
        """
        #~ qs = self.get_siblings()
        qs = ar.data_iterator
        if qs is None:
            return
        nav = AttrDict(**navinfo(qs,self))
        if not nav.recno:
            return
        new_recno = nav.recno + offset
        if new_recno <= 0:
            return
        if new_recno > qs.count():
            return
        other = qs[new_recno-1]
        prev_seqno  = other.seqno 
        other.seqno = self.seqno
        self.seqno = prev_seqno 
        self.save()
        other.save()
        
    @fields.displayfield(_("Move"),preferred_width=5)
    def move_buttons(obj,ar):
        """
        Displays the buttons for this row and this user.
        """
        actor = ar.actor
        l = []
        state = None # TODO: support a possible state?
        for n in ('move_up','move_down'):
            ba = actor.get_action_by_name(n)
            if ba.get_bound_action_permission(ar,obj,state):
                l.append(ar.renderer.action_button(obj,ar,ba))
                l.append(' ')
        return E.p(*l)
        
  

class Hierarizable(Sequenced):
    """
    Abstract model mixin for things that have a "parent" and "siblings".
    """
    class Meta:
        abstract = True
        
    parent = models.ForeignKey('self',
        verbose_name=_("Parent"),
        null=True,blank=True,
        related_name='children')
    
    def get_siblings(self):
        if self.parent:
            return self.parent.children.all()
        return self.__class__.objects.filter(parent__isnull=True)
    
    #~ def save(self, *args, **kwargs):
        #~ super(Hierarizable, self).save(*args, **kwargs)
    def full_clean(self, *args, **kwargs):
        p = self.parent
        while p is not None:
            if p == self:
                raise ValidationError("Cannot be your own ancestor")
            p = p.parent
        super(Hierarizable, self).full_clean(*args, **kwargs)
        
    def is_parented(self,other):
        if self == other: return True
        p = self.parent
        while p is not None:
            if p == other: 
                return True
            p = p.parent
        
        
    def get_parents(self):
        rv = []
        p = self.parent
        while p is not None:
            rv.insert(p)
            p = p.parent
        return rv
        

class ProjectRelated(model.Model):
    """
    Mixin for Models that are automatically 
    related to a "project". 
    A project means here 
    "the central most important thing that is used to classify most other things".
    For example in lino.projects.pcsw, the "project" is a Client.
    
    Whether an application has such a concept of "project", 
    and which model has this privileged status, 
    is set in :attr:`lino.Lino.project_model`.
    
    """
    
    class Meta:
        abstract = True
        
    if settings.SITE.project_model:
        project = models.ForeignKey(
            settings.SITE.project_model,
            blank=True,null=True,
            related_name="%(app_label)s_%(class)s_set_by_project",
            )
    else:
        project = fields.DummyField()

    def get_related_project(self,ar):
        if settings.SITE.project_model:
            return self.project
        
    #~ def summary_row(self,ui,rr,**kw):
    def summary_row(self,ar,**kw):
        s = [ar.obj2html(self)]
        #~ s = ui.ext_renderer.obj2html(self)
        if settings.SITE.project_model:
            #~ if self.project and not dd.has_fk(rr,'project'):
            if self.project:
                #~ s += " (" + ui.obj2html(self.project) + ")"
                s += [" (",ar.obj2html(self.project), ")"]
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
        if isinstance(self.project,settings.SITE.modules.contacts.Partner):
            if self.project.email:
                yield ('to',self.project)
        for r in super(ProjectRelated,self).get_mailable_recipients():
            yield r

    def get_postable_recipients(self):
        if isinstance(self.project,settings.SITE.modules.contacts.Partner):
            yield self.project
        for p in super(ProjectRelated,self).get_postable_recipients():
            yield p


from lino.mixins.printable import (Printable, PrintableType, 
    CachedPrintable, TypedPrintable, 
    DirectPrintAction)
    
from lino.mixins.uploadable import Uploadable
from lino.mixins.human import Human, Born, Genders
#~ from lino.mixins.mails import Recipient, Mail
#~ from lino.utils.dblogger import DiffingMixin
#~ from lino.mixins.personal import SexField, PersonMixin

from lino.core import actions
from lino.mixins import printable


class Referrable(model.Model):
    """
    Mixin for things that have a unique `ref` field and a `get_by_ref` method.
    """
    class Meta:
        abstract = True
        
    ref = fields.NullCharField(_("Reference"),
        max_length=40,
        blank=True,null=True,
        unique=True)
    
    @classmethod
    def get_by_ref(cls,ref,default=models.NOT_PROVIDED):
        try:
            return cls.objects.get(ref=ref)
        except cls.DoesNotExist,e:
            if default is models.NOT_PROVIDED:
                raise cls.DoesNotExist(
                  "No %s with reference %r" % (unicode(cls._meta.verbose_name),ref))
            return default

    def __unicode__(self):
        return self.ref or unicode(_('(Root)'))




class EmptyTableRow(VirtualRow,Printable):
    """
    Base class for virtual rows of an :class:`EmptyTable`.
    An EmptyTableRow instance 
    """
    pk = -99998
    def __init__(self,table,**kw):
        self._table = table
        VirtualRow.__init__(self,**kw)
        
    def __unicode__(self):
        return unicode(self._table.label)
        
    def get_print_language(self):
        return settings.SITE.DEFAULT_LANGUAGE.django_code
        
    def get_templates_group(self):
        return self._table.app_label + '/' + self._table.__name__
    
    def filename_root(self):
        return self._table.app_label + '.' + self._table.__name__
        
    def __getattr__(self,name):
        """
        Since there is only one EmptyTableRow class, we simulate a 
        getter here by manually creating an InstanceAction.
        """
        v = getattr(self._table,name)
        if isinstance(v,actions.Action):
            return actions.InstanceAction(v,self._table,self,None)
        # 20130525 dd.Report calls `get_story` on `self`, not on the `cls`
        if callable(v):
            return curry(v,self)
        #~ return v 
        #~ raise Exception("")
        raise AttributeError("EmptyTableRow on %s has no action and no callable '%s'" % (self._table,name))



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
        return actions.ShowEmptyTable()
    
    
    @classmethod
    def create_instance(self,ar,**kw):
        if self.parameters:
            kw.update(ar.param_values)

        #~ for k,v in req.param_values.items():
            #~ kw[k] = v
        #~ for k,f in self.parameters.items():
            #~ kw[k] = f.value_from_object(None)
        obj = EmptyTableRow(self,**kw)
        kw = ar.ah.store.row2dict(ar,obj)
        obj._data = kw
        obj.update(**kw)
        return obj
    
    @classmethod
    def get_data_elem(self,name):
        de = super(EmptyTable,self).get_data_elem(name)
        if de is not None:
            return de
        a = name.split('.')
        if len(a) == 2:
            return getattr(getattr(settings.SITE.modules,a[0]),a[1])
            
            
class Report(EmptyTable):
    
    detail_layout = "body"
    
    @fields.virtualfield(fields.HtmlBox())
    def body(cls,self,ar):
        html = []
        #~ for item in self.get_story(self,ar):
        for item in self.get_story(ar):
            if E.iselement(item):
                html.append(item)
            elif isinstance(item,type) and issubclass(item,Actor):
                html.append(ar.show(item,master_instance=self))
            else:
                raise Exception("Cannot handle %r" % item)
                
        return E.div(*html)

    @classmethod
    def as_appy_pod_xml(cls,self,apr):
        from lino.utils.html2odf import html2odf, toxml

        chunks = []
        for item in self.get_story(apr.ar):
            if E.iselement(item):
                chunks.append(toxml(html2odf(item)))
            elif isinstance(item,type) and issubclass(item,Actor):
                sar = apr.ar.spawn(item,master_instance=self)
                chunks.append(apr.insert_table(sar))
            else:
                raise Exception("Cannot handle %r" % item)
                
        return ''.join(chunks)
    
            
            


if True: # not yet convinced that it is necessary.
  
  from north.dbutils import BabelNamed
  
else: 

  class BabelNamed(model.Model):
    """
    Same as :class:`north.dbutils.BabelNamed` except that we now inherit 
    from Lino's extended `Model` instead of Django's plain `Model`.
    
    The advantage is that subclasses can call super() when they 
    override one of methods in :class:`dd.Model <lino.core.model.Model>`.
    
    """
    
    class Meta:
        abstract = True
        
    name = BabelCharField(max_length=200,verbose_name=_("Designation"))
    
    def __unicode__(self):
        return babelattr(self,'name')
    


#~ from lino.models import Workflowable
