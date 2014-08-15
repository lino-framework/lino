# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"See :class:`dd.Model`."

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from djangosite.dbutils import obj2str, full_model_name
from lino.core import fields
from lino.core import signals
from lino.core import actions
from lino.core import dbutils
from lino.utils.xmlgen.html import E
from lino.utils import get_class_attr


class Model(models.Model):
    "See :class:`dd.Model`."

    class Meta:
        abstract = True

    allow_cascaded_delete = []

    grid_post = actions.CreateRow()
    submit_insert = actions.SubmitInsert()
    """This is the action represented by the "Create" button of an Insert
    window. See :mod:`lino.modlib.dedupe` for an example of how to
    override it.

    """

    quick_search_fields = None
    """When quick_search text is given for a table on this model, Lino by
    default searches the query text in all CharFields.  But on models
    with `quick_search_fields` will search only those fields.
    
    This is also used when a gridfilter has been set on a foreign key
    column which points to this model.

    """

    active_fields = frozenset()
    """If specified, this is the default value for :attr:`active_fields
    <lino.core.tables.AbstractTable.active_fields>` of every `Table`
    on this model.

    """

    hidden_columns = frozenset()
    """If specified, this is the default value for :attr:`hidden_columns
    <lino.core.tables.AbstractTable.hidden_columns>` of every `Table`
    on this model.

    """

    hidden_elements = frozenset()
    """If specified, this is the default value for :attr:`hidden_elements
    <lino.core.tables.AbstractTable.hidden_elements>` of every `Table`
    on this model.

    """

    preferred_foreignkey_width = None
    """The default preferred width (in characters) of widgets that
    display a ForeignKey to this model.

    If not specified, the default default `preferred_width`
    for ForeignKey fields is *20*.

    """

    workflow_state_field = None
    """If this is set on a Model, then it will be used as default value
    for :attr:`lino.core.table.Table.workflow_state_field` on all
    tables based on this Model.

    """

    workflow_owner_field = None
    """If this is set on a Model, then it will be used as default value
    for :attr:`lino.core.table.Table.workflow_owner_field` on all
    tables based on this Model.

    """

    change_watcher_spec = None
    """
    Internally used by :meth:`watch_changes`
    """

    def as_list_item(self, ar):
        return E.li(unicode(self))

    @classmethod
    def get_param_elem(model, name):
        # This is called by :meth:`Chooser.get_data_elem` when
        # application code defines a chooser with an argument that
        # does not match any field. There is currently no usage
        # example for this on database models.
        return None

    @classmethod
    def get_data_elem(model, name):
        #~ logger.info("20120202 get_data_elem %r,%r",model,name)
        if not name.startswith('__'):
            parts = name.split('__')
            if len(parts) > 1:
                """It's going to be a RemoteField
                """
                # logger.warning("20120406 RemoteField %s in %s",name,self)
                #~ model = self.model

                from lino.ui import store

                field_chain = []
                for n in parts:
                    assert model is not None
                    # ~ 20130508 model.get_default_table().get_handle() # make sure that all atomizers of those fields get created.
                    fld = model.get_data_elem(n)
                    if fld is None:
                        # raise Exception("Part %s of %s got None" % (n,model))
                        raise Exception(
                            "Invalid RemoteField %s.%s (no field %s in %s)" %
                            (full_model_name(model), name, n, full_model_name(model)))
                    # make sure that the atomizer gets created.
                    store.get_atomizer(model, fld, fld.name)
                    field_chain.append(fld)
                    if fld.rel:
                        model = fld.rel.to
                    else:
                        model = None

                def func(obj, ar=None):
                    #~ if ar is None: raise Exception(20130802)
                    #~ print '20130422',name,obj, [fld.name for fld in field_chain]
                    try:
                        for fld in field_chain:
                            #~ obj = fld.value_from_object(obj)
                            obj = fld._lino_atomizer.full_value_from_object(
                                obj, ar)
                        #~ for n in parts:
                            #~ obj = getattr(obj,n)
                        #~ print '20130422 %s --> %r', fld.name,obj
                        return obj
                    except Exception, e:
                        # ~ if False: # only for debugging
                        if True:  # see 20130802
                            logger.exception(e)
                            return str(e)
                        return None
                return fields.RemoteField(func, name, fld)

        try:
            return model._meta.get_field(name)
        except models.FieldDoesNotExist:
            pass

        #~ s = name.split('.')
        #~ if len(s) == 1:
            #~ mod = import_module(model.__module__)
            #~ rpt = getattr(mod,name,None)
        #~ elif len(s) == 2:
            #~ mod = getattr(settings.SITE.modules,s[0])
            #~ rpt = getattr(mod,s[1],None)
        #~ else:
            #~ raise Exception("Invalid data element name %r" % name)

        v = get_class_attr(model, name)
        if v is not None:
            return v

        for vf in model._meta.virtual_fields:
            if vf.name == name:
                return vf

    def get_choices_text(self, request, actor, field):
        """
        Return the text to be displayed when an instance of this model
        is being used as a choice in a combobox (i.e. by ForeignKey fields
        pointing to this model).
        `request` is the web request,
        `actor` is the requesting actor.
        Default is to simply return `unicode(self)`.
        One usage example is :class:`lino.modlib.countries.models.Place`.
        """
        return unicode(self)

    def disable_delete(self, ar):
        return self._lino_ddh.disable_delete_on_object(self)

    @classmethod
    def get_default_table(self):
        """
        Used internally. Lino chooses during the kernel startup, for each model, 
        one of the discovered Table subclasses as the "default table".
        """
        return self._lino_default_table

    def disabled_fields(self, ar):
        return set()

    def on_create(self, ar):
        pass

    def before_ui_save(self, ar):
        pass

    @classmethod
    def define_action(cls, **kw):
        for k, v in kw.items():
            if k in cls.__dict__:
            # if hasattr(cls, k):
                raise Exception("Tried to redefine %s.%s" % (cls, k))
            setattr(cls, k, v)

    @classmethod
    def hide_elements(self, *names):
        for name in names:
            if self.get_data_elem(name) is None:
                raise Exception("%s has no element '%s'" % (self, name))
        self.hidden_elements = self.hidden_elements | set(names)

    def after_ui_create(self, ar):
        pass

    def after_ui_save(self, ar):
        pass

    def get_row_permission(self, ar, state, ba):
        #~ if ba.action.action_name == 'wf7':
            #~ logger.info("20130424 Model.get_row_permission() gonna call %r.get_bound_action_permission()",ba)
        return ba.get_bound_action_permission(ar, self, state)

    def update_owned_instance(self, controllable):
        """
        Called by :class:`lino.mixins.Controllable`.
        """
        #~ print '20120627 tools.Model.update_owned_instance'
        pass

    def after_update_owned_instance(self, controllable):
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

    def get_overview_elems(self, ar):
        return []

    @classmethod
    def on_analyze(self, site):
        pass

    @classmethod
    def lookup_or_create(model, lookup_field, value, **known_values):
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

        if isinstance(lookup_field, basestring):
            lookup_field = model._meta.get_field(lookup_field)
        if isinstance(lookup_field, dbutils.BabelCharField):
            flt = dbutils.lookup_filter(
                lookup_field.name, value, **known_values)
        else:
            if isinstance(lookup_field, models.CharField):
                fkw[lookup_field.name + '__iexact'] = value
            else:
                fkw[lookup_field.name] = value
            flt = models.Q(**fkw)
            #~ flt = models.Q(**{self.lookup_field.name: value})
        qs = model.objects.filter(flt)
        if qs.count() > 0:  # if there are multiple objects, return the first
            if qs.count() > 1:
                logger.warning(
                    "%d %s instances having %s=%r (I'll return the first).",
                    qs.count(), model.__name__, lookup_field.name, value)
            return qs[0]
        #~ known_values[lookup_field.name] = value
        obj = model(**known_values)
        setattr(obj, lookup_field.name, value)
        try:
            obj.full_clean()
        except ValidationError, e:
            raise ValidationError("Failed to auto_create %s : %s" %
                                  (obj2str(obj), e))
        signals.auto_create.send(obj, known_values=known_values)
        obj.save()
        return obj

    @classmethod
    def setup_table(cls, t):
        pass

    def on_duplicate(self, ar, master):
        pass

    def before_state_change(self, ar, old, new):
        """
        Called before a state change.
        """
        pass

    def after_state_change(self, ar, old, new):
        """
        Called after a state change.
        """
        ar.set_response(refresh=True)

    def set_workflow_state(row, ar, state_field, target_state):

        watcher = signals.ChangeWatcher(row)

        #~ old = row.state
        old = getattr(row, state_field.attname)

        target_state.choicelist.before_state_change(row, ar, old, target_state)
        row.before_state_change(ar, old, target_state)
        #~ row.state = target_state
        setattr(row, state_field.attname, target_state)
        #~ self.before_row_save(row,ar)
        row.save()
        target_state.choicelist.after_state_change(row, ar, old, target_state)
        row.after_state_change(ar, old, target_state)

        watcher.send_update(ar.request)

        row.after_ui_save(ar)

    def after_send_mail(self, mail, ar, kw):
        """
        Called when an outbox email controlled by self has been sent
        (i.e. when the :class:`lino.modlib.outbox.models.SendMail`
        action has successfully completed).
        """
        pass

    def summary_row(self, ar, **kw):
        yield ar.obj2html(self)

    @fields.displayfield(_("Description"))
    def description_column(self, ar):
        return ar.obj2html(self)

    def __repr__(self):
        return obj2str(self)

    def get_related_project(self, ar):
        if settings.SITE.project_model:
            if isinstance(self, settings.SITE.project_model):
                return self

    def get_system_note_type(self, ar):
        return None

    def get_system_note_recipients(self, ar, silent):
        return []

    def to_html(self, **kw):
        import lino.ui.urls  # hack: trigger ui instantiation
        actor = self.get_default_table()
        kw.update(renderer=settings.SITE.ui.text_renderer)
        #~ ar = settings.SITE.ui.text_renderer.request(**kw)
        ar = actor.request(**kw)
        return self.preview(ar)
        #~ username = kw.pop('username',None)

    def get_typed_instance(self, model):
        """
        Used when implementing :ref:`polymorphism`.
        """
        #~ assert model is self.__class__
        return self

    def get_detail_action(self, ar):
        """Used by instance_handler. E.g. for a `pcsw.Client` the
        detail_action depends on the user profile.

        """
        a = getattr(self, '_detail_action', None)
        if not a is None:
            return a
        return self.__class__.get_default_table().detail_action

    def is_attestable(self):
        """Override this to disable the :class:`ml.excerpts.CreateExcerpt`
action on individual instances.

        """
        return True

    def get_excerpt_options(self, ar, **kw):
        """Set additional fields of newly created excerpts from this.
        Used by :class:`ml.excerpts.CreateExcerpt`.
        """
        return kw

    LINO_MODEL_ATTRIBS = (
        'get_detail_action',
        'get_row_permission',
        'get_excerpt_options',
        'is_attestable',
        'get_data_elem',
        'get_param_elem',
        'after_ui_save',
        'after_ui_create',
        'preferred_foreignkey_width',
        'before_ui_save',
        'allow_cascaded_delete',
        'workflow_state_field',
        'workflow_owner_field',
        'disabled_fields',
        'get_choices_text',
        'summary_row',
        'submit_insert',
        'active_fields',
        'hidden_columns',
        'hidden_elements',
        'get_default_table',
        'get_related_project',
        'get_system_note_recipients',
        'get_system_note_type',
        'quick_search_fields',
        'change_watcher_spec',
        'on_analyze',
        'disable_delete',
        'lookup_or_create',
        'on_duplicate',
        'on_create',
        'get_typed_instance',
        'print_subclasses_graph',
        'grid_post', 'submit_insert')

    @classmethod
    def django2lino(cls, model):
        """
        A list of the attributes to be copied to Django models which do
        not inherit from :class:`lino.core.model.Model`.  Used by
        :mod:`lino.core.kernel`

        """
        if issubclass(model, cls):
            return

        for k in cls.LINO_MODEL_ATTRIBS:
            if not hasattr(model, k):
                #~ setattr(model,k,getattr(dd.Model,k))
                setattr(model, k, cls.__dict__[k])
                #~ model.__dict__[k] = getattr(dd.Model,k)
                #~ logger.info("20121127 Install default %s for %s",k,model)

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
                        pairs.append(
                            (m._meta.verbose_name, c._meta.verbose_name))
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
