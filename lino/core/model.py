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
#~ from django.conf import settings
from django.utils.translation import ugettext as _

from django.db.models.base import signals, ModelState, DeferredAttribute, ManyToOneRel, izip

from lino.core import fields
from lino.core import modeltools
from lino.utils.xmlgen import html as xghtml

class WatcherSpec:
    def __init__(self,ignored_fields,master_key):
        self.ignored_fields = ignored_fields
        self.master_key = master_key
    


class Model(models.Model):
    """
    Adds Lino specific features to Django's Model base class. 
    If a Lino application uses simple Django Models,
    the attributes and methods defined here are added to these 
    modules during :func:`lino.core.kernel.analyze_models`.
    """
    class Meta:
        abstract = True
        
    allow_cascaded_delete = False
    """
    Lino, like Django, by default forbids to delete an object that is 
    referenced by other objects.

    Set this to `True` on models whose objects should get automatically 
    deleted if a related object gets deleted. 
    Example: Lino should not refuse to delete 
    a Mail just because it has some Recipient. 
    When deleting a Mail, Lino should also delete its Recipients.
    That's why :class:`lino.modlib.outbox.models.Recipient` 
    has ``allow_cascaded_delete = True``.
    
    Other examples of such models are 
    :class:`lino.modlib.cv.models.PersonProperty`,
    :class:`lino.modlib.cv.models.LanguageKnowledge`,
    :class:`lino.modlib.debts.models.Actor`,
    :class:`lino.modlib.debts.models.Entry`,
    ...
    
    Not that this currently is also consulted by
    :meth:`lino.mixins.duplicable.Duplicable.duplicate_row`
    to decide whether slaves of a record being duplicated
    should be duplicated as well.
    
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
    
    _watch_changes_specs = None
    """
    Internally used by :meth:`watch_changes`
    """
    
    _change_summary = ''
    """
    Internally used by :meth:`watch_changes`
    """
    
    @classmethod
    def watch_changes(model,ignore=[],master_key=None,**options):
        """
        Declare a set of fields of this model to be "observed" or "watched".
        Each change to an object comprising at least one watched 
        will lead to an entry to the ChangesByObject table.
        
        All calls to watch_changes will be grouped by model.
        
        See also :mod:`lino.core.changes`.
        """
        #~ if ignore is None:
            #~ model._watch_changes_specs = None
            #~ return
        from lino import dd
        if isinstance(ignore,basestring):
            ignore = dd.fields_list(model,ignore)
        ignore = set(ignore)
        if model._watch_changes_specs is not None:
            ignore += model._watch_changes_specs
        for f in model._meta.fields:
            if not f.editable:
                ignore.add(f.name)
        model._watch_changes_specs = WatcherSpec(ignore,master_key)
        #~ logger.info("20120924 %s ignore %s", model, ignore)
        #~ model._watch_changes_specs = (fields_spec,options)
        #~ else:
            #~ raise NotImplementedError()
  
        
        
    def set_change_summary(self,text):
        self._change_summary = text
    
    
    
    def disable_delete(self,ar):
        """
        Return None if it is okay to delete this object,
        otherwise a nonempty string explaining why.
        The argument `ar` contains the :class:`lino.core.actions.ActionRequest` 
        which is trying to delete. `ar` is possibly `None` when this is 
        being called from a script or batch process.
        """
        return self._lino_ddh.disable_delete_on_object(self)
        
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
        the ajax response to the save() call.
        Used by :class:`lino.modlib.debts.models.Budget` 
        to fill default entries to a new Budget,
        or by :class:`lino.modlib.cbss.models.CBSSRequest` 
        to execute the request.
        """
        return kw
        
    def get_row_permission(self,user,state,action):
        """
        Returns True or False whether this row instance 
        gives permission the specified user to run the specified action.
        """
        return action.get_action_permission(user,self,state)

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
        state = ar.actor.get_row_state(obj)
        if state:
            l.append("%s : " % state)
        for a in ar.actor.get_workflow_actions(ar,obj):
            l.append(ar.renderer.action_button(obj,ar,a))
            l.append(' ')
        #~ return ', '.join(l)
        return xghtml.E.p(*l)
        
        
    def __repr__(self):
        return modeltools.obj2str(self)
