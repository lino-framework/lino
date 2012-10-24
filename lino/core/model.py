# -*- coding: UTF-8 -*-
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

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _

from django.db.models.base import signals, ModelState, DeferredAttribute, ManyToOneRel, izip

from lino.core import fields
from lino.core import modeltools
from lino.utils.xmlgen import html as xghtml


class Model(models.Model):
    """
    Adds Lino specific features to Django's Model base class. 
    If a Lino application uses simple Django Models,
    the attributes and methods defined here are added to these 
    modules during :func:`lino.core.kernel.analyze_models`.
    """
    class Meta:
        abstract = True
        
    allow_cascaded_delete = []
    """
    A list of names of ForeignKey fields of this model 
    that allow for cascaded delete.
    
    When deleting an object through the user interface, 
    Lino by default forbids to delete an object that is 
    referenced by other objects. Users will get a message 
    of type "Cannot delete X because n Ys refer to it".
    
    Example: Lino should not refuse to delete 
    a Mail just because it has some Recipient. 
    When deleting a Mail, Lino should also delete its Recipients.
    That's why :class:`lino.modlib.outbox.models.Recipient` 
    has ``allow_cascaded_delete = ['mail']``.
    
    Note that this currently is also consulted by
    :meth:`lino.mixins.duplicable.Duplicable.duplicate_row`
    to decide whether slaves of a record being duplicated
    should be duplicated as well.
    
    This mechanism doesn't depend on nor influence Django's
    `on_delete
    <https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey.on_delete>`_
    option.
    But of course you should not allow_cascaded_delete for fields
    which have e.g. `on_delete=PROTECT`.

    
    """
    
    quick_search_fields = None
    """
    When quick_search text is given for a table on this model, 
    Lino by default searches the query text in all CharFields.
    But on models with `quick_search_fields` will search only those fields.
    
    This is also used when a gridfilter has been set on a 
    foreign key column which points to this model. 
    
    """
    
    #~ grid_search_field = None
    #~ """
    #~ The name of the field to be used when a gridfilter has been set on a 
    #~ foreign key column which points to this model. Capito?
    #~ """

    
    workflow_state_field = None
    """
    If this is set on a Model, then it will be used as default 
    value for :attr:`lino.core.table.Table.workflow_state_field` 
    on all tables based on this Model.
    """
    
    workflow_owner_field = None
    """
    If this is set on a Model, then it will be used as default 
    value for :attr:`lino.core.table.Table.workflow_owner_field` 
    on all tables based on this Model.
    """
    
    #~ _watch_changes_specs = None
    _change_watcher_spec = None
    """
    Internally used by :meth:`watch_changes`
    """
    
    #~ _change_summary = ''
    #~ """
    #~ Internally used by :meth:`watch_changes`
    #~ """
    
    @classmethod
    def watch_changes(cls,*args,**kw):
        """
        Declare this model to be "observed" or "watched" for changes.
        Each change to an object comprising at least one watched field
        will lead to an entry to the `Changes` table.
        
        All calls to watch_changes will be grouped by model.
        
        See also :mod:`lino.core.changes`.
        """
        from lino.core import changes
        changes.add_watcher_spec(cls,*args,**kw)
        
    #~ def get_watcher(self,*args,**kw):
        #~ from lino.core import changes
        #~ return changes.Watcher(self,*args,**kw)
        
    #~ def update_system_note(self,note):
        #~ pass
        
    #~ def set_change_summary(self,text):
        #~ self._change_summary = text
    
    def disable_delete(self,ar):
        """
        Return None if it is okay to delete this object,
        otherwise a nonempty string explaining why.
        The argument `ar` contains the :class:`lino.core.actions.ActionRequest` 
        which is trying to delete. `ar` is possibly `None` when this is 
        being called from a script or batch process.
        """
        return self._lino_ddh.disable_delete_on_object(self)
        
    def get_default_table(self,ar):
        return self._lino_default_table
        
    def disabled_fields(self,ar):
        return []
        
    def on_create(self,ar):
        """
        Used e.g. by modlib.notes.Note.on_create().
        on_create gets the action request as argument.
        Didn't yet find out how to do that using a standard Django signal.
        """
        pass
        
    def before_ui_save(self,ar):
        """
        Called after a PUT or POST on this row, and before saving the row.
        Example in :class:`lino.modlib.cal.models.Event` to mark the 
        event as user modified by setting a default state.
        """
        pass
        
    def after_ui_save(self,ar,**kw):
        """
        Called after a PUT or POST on this row, 
        and after the row has been saved.
        It must return (and may modify) the `kw` which will become 
        the Ajax response to the save() call.
        Used by 
        :class:`lino_welfare.modlib.debts.models.Budget` 
        to fill default entries to a new Budget,
        or by :class:`lino_welfare.modlib.cbss.models.CBSSRequest` 
        to execute the request,
        or by 
        :class:`lino_welfare.modlib.jobs.models.Contract` 
        :class:`lino_welfare.modlib.pcsw.models.Coaching` 
        """
        return kw
        
    def get_row_permission(self,ar,state,ba):
        """
        Returns True or False whether this row instance 
        gives permission the specified action request `ar` 
        to run the specified action.
        """
        #~ logger.info("20121020 Model.get_row_permission %s",unicode(ba.action.label))
        return ba.get_bound_action_permission(ar,self,state)

    def update_owned_instance(self,controllable):
        """
        Called by :class:`lino.mixins.Controllable`.
        """
        #~ print '20120627 tools.Model.update_owned_instance'
        pass
                
    def after_update_owned_instance(self,controllable):
        """
        Called by :class:`lino.mixins.Controllable`.
        """
        pass
        
    def get_mailable_recipients(self):
        """
        Return or yield a list of (type,partner) tuples to be 
        used as recipents when creating an outbox.Mail from this object.
        """
        return []
        
    def get_postable_recipients(self):
        """
        Return or yield a list of Partners to be 
        used as recipents when creating a posting.Post from this object.
        """
        return []
        
    @classmethod
    def site_setup(self,site):
        pass
        
    @classmethod
    def setup_table(cls,t):
        """
        Called during site startup once on each Table that 
        uses this model.
        """
        pass
        
    def on_duplicate(self,ar,master):
        """
        Called by :meth:`lino.mixins.duplicable.Duplicable.duplicate_row`.
        `ar` is the action request that asked to duplicate.
        If `master` is not None, then this is a cascaded duplicate initiated
        be a duplicate() on the specifie `master`.
        """
        pass
        
    def before_state_change(self,ar,kw,old,new):
        """
        Called before a state change.
        """
        pass
  
    def after_state_change(self,ar,kw,old,new):
        """
        Called after a state change.
        """
        kw.update(refresh=True)
        
    def after_send_mail(self,mail,ar,kw):
        """
        Called when an outbox email controlled by self has been sent
        (i.e. when the :class:`lino.modlib.outbox.models.SendMail` 
        action has successfully completed).
        """
        pass
  
    def summary_row(self,ar,**kw):
        return ar.href_to(self)
        
    #~ @fields.displayfield(_("ACtions"))
    #~ def action_buttons(obj,ar):
        #~ l = []
        #~ for a in ar.actor.get_custom_actions(ar,obj):
            #~ l.append(ar.renderer.action_button(obj,ar,a))
            #~ l.append(' ')
        #~ return xghtml.E.p(*l)
      
    @fields.displayfield(_("Workflow"))
    def workflow_buttons(obj,ar):
        """
        Displays the workflow buttons for this row and this user.
        """
        #~ logger.info('20120930 workflow_buttons %r', obj)
        actor = ar.actor
        #~ print 20120621 , actor,  self
        #~ print 20120618, ar
        l = []
        state = actor.get_row_state(obj)
        if state:
            #~ l.append(xghtml.E.b(unicode(state),style="vertical-align:middle;"))
            l.append(xghtml.E.b(unicode(state)))
            #~ l.append(u" » ")
            #~ l.append(u" \u25b8 ")
            l.append(u" \u2192 ")
        for a in ar.actor.get_workflow_actions(ar,obj):
            l.append(ar.renderer.action_button(obj,ar,a))
            l.append(' ')
        #~ return ', '.join(l)
        return xghtml.E.p(*l)
        
        
    def __repr__(self):
        return modeltools.obj2str(self)


    def get_related_project(self,ar):
        if settings.LINO.project_model:
            if isinstance(self,settings.LINO.project_model):
                return self
        
    def get_system_note_type(self,ar):
        return None
        
    def get_system_note_recipients(self,ar,silent):
        """
        Called from :meth:`lino.Lino.get_system_note_recipients`.
        """
        return []
        
