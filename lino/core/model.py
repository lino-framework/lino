# -*- coding: UTF-8 -*-
## Copyright 2009-2013 Luc Saffre
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

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

#~ import copy

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _


from django.core.exceptions import ValidationError
#~ from django.core.exceptions import MultipleObjectsReturned


from lino.core import fields
from lino.core import signals
from lino.core import dbutils
from djangosite.dbutils import obj2str, full_model_name
from lino.utils.xmlgen import html as xghtml
E = xghtml.E


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
    :meth:`lino.mixins.duplicable.Duplicable.duplicate`
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
    
    hidden_columns = frozenset()
    """
    If specified, this is the default value for 
    :attr:`hidden_columns <lino.core.tables.AbstractTable.hidden_columns>` 
    of every `Table` on this model.
    """
    
    hidden_elements = frozenset()
    """
    If specified, this is the default value for 
    :attr:`hidden_elements <lino.core.tables.AbstractTable.hidden_elements>` 
    of every `Table` on this model.
    """
    
    preferred_foreignkey_width = None
    """
    The default preferred width (in characters) of widgets that display a 
    ForeignKey to this model
    """

    
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
    change_watcher_spec = None
    """
    Internally used by :meth:`watch_changes`
    """
    
    #~ _custom_actions = dict()
    """
    Internally used to store custom model actions.
    """
    
    #~ _change_summary = ''
    #~ """
    #~ Internally used by :meth:`watch_changes`
    #~ """
    
    #~ def get_watcher(self,*args,**kw):
        #~ from lino.core import changes
        #~ return changes.Watcher(self,*args,**kw)
        
    #~ def update_system_note(self,note):
        #~ pass
        
    #~ def set_change_summary(self,text):
        #~ self._change_summary = text
        
    def as_list_item(self,ar):
        return E.li(unicode(self))
        
        
    
    def get_choices_text(self,request,rpt,field):
        """
        Return the text to be displayed when an instance of this model 
        is being used as a choice in a combobox (i.e. by ForeignKey fields 
        pointing to this model).
        Default is to simply return `unicode(self)`.
        One usage example is :class:`lino.modlib.countries.models.City`.
        """
        return unicode(self)
        
    def disable_delete(self,ar):
        """
        Return None if it is okay to delete this object,
        otherwise a nonempty string explaining why.
        The argument `ar` contains the :class:`lino.core.actions.ActionRequest` 
        which is trying to delete. `ar` is possibly `None` when this is 
        being called from a script or batch process.
        """
        return self._lino_ddh.disable_delete_on_object(self)
        
    @classmethod # classmethod since 20130422
    def get_default_table(self):
        return self._lino_default_table
        
    def disabled_fields(self,ar):
        return set()
        
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
        
    @classmethod
    def define_action(cls,**kw):
        """
        Adds one or several actions to this model.
        Actions must be specified using keyword arguments.
        
        """
        for k,v in kw.items():
            if hasattr(cls,k):
                raise Exception("Tried to redefine %s.%s" % (cls,k))
            setattr(cls,k,v)
        
        
    @classmethod
    def hide_elements(self,*names):
        """
        Call this to mark the named data elements (fields) as hidden.
        They remain in the database but are not visible in the user interface.
        """
        for name in names:
            if fields.get_data_elem(self,name) is None:
                raise Exception("%s has no element '%s'" % (self,name))
        self.hidden_elements = self.hidden_elements | set(names)
        
        
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
        :class:`lino.modlib.vat.models.Vat` 
        """
        return kw
        
    def get_row_permission(self,ar,state,ba):
        """
        Returns True or False whether this row instance 
        gives permission the ActionRequest `ar` 
        to run the specified action.
        """
        #~ if ba.action.action_name == 'wf7':
            #~ logger.info("20130424 Model.get_row_permission() gonna call %r.get_bound_action_permission()",ba)
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
        
    #~ @classmethod
    #~ def site_setup(self,site):
        #~ pass
        
    @classmethod
    def on_analyze(self,site):
        pass
        
    #~ def lookup_or_create(self,*args,**kwargs):
        #~ from lino.utils.instantiator import lookup_or_create
        #~ lookup_or_create(self,*args,**kwargs)
        
        
    @classmethod
    def lookup_or_create(model,lookup_field,value,**known_values):
        """
        Look-up whether there is a model instance having 
        `lookup_field` with value `value`
        (and optionally other `known_values` matching exactly).
        
        If it doesn't exist, create it and emit an 
        :attr:`auto_create <lino.core.signals.auto_create>` signal.
        
        """
        #~ logger.info("2013011 lookup_or_create")
        fkw = dict()
        fkw.update(known_values)
            
        if isinstance(lookup_field,basestring):
            lookup_field = model._meta.get_field(lookup_field)
        if isinstance(lookup_field,dbutils.BabelCharField):
            flt  = dbutils.lookup_filter(lookup_field.name,value,**known_values)
        else:
            if isinstance(lookup_field,models.CharField):
                fkw[lookup_field.name+'__iexact'] = value
            else:
                fkw[lookup_field.name] = value
            flt = models.Q(**fkw)
            #~ flt = models.Q(**{self.lookup_field.name: value})
        qs = model.objects.filter(flt)
        if qs.count() > 0: # if there are multiple objects, return the first
            if qs.count() > 1: 
                logger.warning(
                  "%d %s instances having %s=%r (I'll return the first).",
                  qs.count(),model.__name__,lookup_field.name,value)
            return qs[0]
        #~ known_values[lookup_field.name] = value
        obj = model(**known_values)
        setattr(obj,lookup_field.name,value)
        try:
            obj.full_clean()
        except ValidationError,e:
            raise ValidationError("Failed to auto_create %s : %s" % (obj2str(obj),e))
        signals.auto_create.send(obj,known_values=known_values)
        obj.save()
        return obj
    

        
        
    @classmethod
    def setup_table(cls,t):
        """
        Called during site startup once on each Table that 
        uses this model.
        """
        pass
        
    def on_duplicate(self,ar,master):
        """
        Called by :meth:`lino.mixins.duplicable.Duplicable.duplicate`.
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
            l.append(E.b(unicode(state)))
            #~ l.append(u" » ")
            #~ l.append(u" \u25b8 ")
            #~ l.append(u" \u2192 ")
        #~ sep = u" \u25b8 "
        sep = u" \u2192 "
        for a in ar.actor.get_workflow_actions(ar,obj):
            l.append(sep)
            l.append(ar.renderer.action_button(obj,ar,a))
            sep = ' '
            #~ l.append(' ')
        #~ return ', '.join(l)
        return E.p(*l)
        
        
    def __repr__(self):
        return obj2str(self)


    def get_related_project(self,ar):
        if settings.SITE.project_model:
            if isinstance(self,settings.SITE.project_model):
                return self
        
    def get_system_note_type(self,ar):
        return None
        
    def get_system_note_recipients(self,ar,silent):
        """
        Called from :meth:`lino.Lino.get_system_note_recipients`.
        """
        return []
        

    @classmethod
    def add_model_action(self,**kw):
        """
        Used e.g. by :mod:`lino.modlib.cal` to add the `UpdateReminders` action 
        to :class: `lino.modlib.users.models.User`.
        """
        for k,v in kw.items():
            if hasattr(self,k):
                raise Exception("add_model_action tried to override '%s' in %s" 
                    % (k,self))
            setattr(self,k,v)
        #~ self._custom_actions = dict(self._custom_actions)
        #~ self._custom_actions.update(kw)
        
    #~ @classmethod
    #~ def get_model_actions(self,table):
        #~ """
        #~ Called once for each :class:`lino.core.dbtables.Table` on this model. 
        #~ Yield a list of (name,action) tuples to install on the table.
        #~ """
            
        #~ if full_model_name(self) in settings.SITE.mergeable_models:
            #~ yield ( 'merge_row', MergeAction(self) )
            
    def to_html(self,**kw):
        import lino.ui.urls # hack: trigger ui instantiation
        actor=self.get_default_table()
        kw.update(renderer=settings.SITE.ui.text_renderer)
        #~ ar = settings.SITE.ui.text_renderer.request(**kw)
        ar = actor.request(**kw)
        return self.preview(ar)
        #~ username = kw.pop('username',None)
            

    def get_typed_instance(self,model):
        """
        Used when implementing :ref:`polymorphism`.
        """
        assert model is self.__class__
        return self
        
        
    LINO_MODEL_ATTRIBS = (
              'get_row_permission',
              'after_ui_save',
              #~ 'update_system_note',
              'preferred_foreignkey_width',
              'before_ui_save',
              'allow_cascaded_delete',
              'workflow_state_field',
              'workflow_owner_field',
              'disabled_fields',
              'get_choices_text',
              'summary_row',
              #~ 'get_model_actions',
              #~ '_custom_actions',
              'hidden_columns',
              'hidden_elements',
              'get_default_table',
              'get_related_project',
              'get_system_note_recipients',
              'get_system_note_type',
              'quick_search_fields',
              'change_watcher_spec',
              #~ 'site_setup',
              'on_analyze',
              'disable_delete',
              'lookup_or_create',
              'on_duplicate',
              'on_create',
              'get_typed_instance',
              'print_subclasses_graph')
    """
    A list of the attributes to be copied to Django models which do not inherit from 
    :class:`lino.core.model.Model`.
    Used by :mod:`lino.core.kernel`
    """
    

    @classmethod
    def print_subclasses_graph(self):
        """
        Returns a `graphviz` directive 
        Used in welfare.userdocs to generate a internationalized graphviz::
        
          \.. py2rst:: print contacts.Partner.print_subclasses_graph()
          
        """
        from lino import dd
        pairs = []
        
        def collect(m):
            for c in dd.models_by_base(m):
                #~ if c is not m and (m in c.__bases__):
                #~ if c is not m:
                #~ if m in c.__bases__:
                if c is not m:
                    ok = True
                    #~ for cb in c.__bases__:
                        #~ if cb in m.mro():
                            #~ ok = False
                    if ok:
                        pairs.append((m._meta.verbose_name,c._meta.verbose_name))
                    collect(c)
        collect(self)
        s = '\n'.join(['    "%s" -> "%s"' % x for x in pairs])
        s = """

.. graphviz:: 
   
   digraph foo {
%s   
  }
  
""" % s
        print s
