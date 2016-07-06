# -*- coding: UTF-8 -*-
# Copyright 2009-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"Defines the :class:`Model` class."

from __future__ import unicode_literals
from __future__ import print_function
# import six
# str = six.text_type
from builtins import str
from past.builtins import basestring
from builtins import object

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from lino import AFTER18
from lino.core.utils import obj2str, full_model_name
from lino.core.utils import ChangeWatcher

from lino.core import fields
from lino.core import signals
from lino.core import actions
from lino.core.utils import error2str
from lino.core.utils import resolve_model
from lino.utils.xmlgen.html import E
from lino.utils import get_class_attr


class Model(models.Model):
    """Lino adds a series of features to Django's `Model
    <https://docs.djangoproject.com/en/dev/ref/models/class/>`_
    class.  If a Lino application includes plain Django Model
    classes, Lino will "extend" these by adding the attributes and
    methods defined here to these classes.

    .. attribute:: workflow_buttons

        A virtual field that displays the workflow buttons for this
        row and the given action request.

    .. method:: full_clean

        This is defined by Django.

    .. method:: FOO_changed

        Called when field FOO of an instance of this model has been
        modified through the user interface.

        For every field named "FOO", if the model has a method called
        "FOO_changed", then this method will be installed as a field-level
        post-edit trigger.

        Example::

          def city_changed(self,oldvalue):
              print("City changed from %s to %s!" % (oldvalue, self.city))

    .. method:: FOO_choices

        Return a queryset or list of allowed choices for field FOO.

        For every field named "FOO", if the model has a method called
        "FOO_choices" (which must be decorated by :func:`dd.chooser`),
        then this method will be installed as a chooser for this
        field.

        Example of a context-sensitive chooser method::

          country = dd.ForeignKey(
              'countries.Country', blank=True, null=True)
          city = dd.ForeignKey(
              'countries.City', blank=True, null=True)

          @chooser()
          def city_choices(cls,country):
              if country is not None:
                  return country.place_set.order_by('name')
              return cls.city.field.rel.model.objects.order_by('name')


    .. method:: create_FOO_choice

        For every field named "FOO" (which must have a chooser), if
        the model has a method called "create_FOO_choice", then this
        chooser will be a "learning" chooser.  That is, users can
        enter text into the combobox, and Lino will create a new
        database object from it.


    """

    class Meta(object):
        abstract = True

    allow_cascaded_delete = frozenset()
    """A set of names of `ForeignKey` or `GenericForeignKey` fields of
    this model that allow for cascaded delete.

    If this is a simple string, Lino expects it to be a
    space-separated list of filenames and convert it into a set at
    startup.
    
    Lino by default forbids to delete any object that is referenced by
    other objects. Users will get a message of type "Cannot delete X
    because n Ys refer to it".
    
    Example: Lino should not refuse to delete a Mail just because it
    has some Recipient.  When deleting a Mail, Lino should also delete
    its Recipients.  That's why
    :class:`lino_xl.lib.outbox.models.Recipient` has
    ``allow_cascaded_delete = 'mail'``.
    
    This is also used by :class:`lino.mixins.duplicable.Duplicate` to
    decide whether slaves of a record being duplicated should be
    duplicated as well.

    A startup (in :meth:`kernel_startup
    <lino.core.kernel.Kernel.kernel_startup>`) Lino automatically sets
    `on_delete
    <https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey.on_delete>`_
    to ``PROTECT`` for all FK fields that are not listed in the
    ``allow_cascaded_delete`` of their model.
    
    """

    grid_post = actions.CreateRow()
    submit_insert = actions.SubmitInsert()
    """This is the action represented by the "Create" button of an Insert
    window. See :mod:`lino.modlib.dedupe` for an example of how to
    override it.

    """

    quick_search_fields = None
    """Explicitly specify the fields to be included in queries with a
    quick search value.

    In your model declarations this should be either `None` or a
    `string` containing a space-separated list of field names.

    This is being resolved during server startup into a frozenset of
    field names. If it is `None`, Lino builds a list of all CharFields
    on the model.

    If you want to not inherit this field from a parent using standard
    MRO, then you must set that field explictly to `None`.

    This is also used when a gridfilter has been set on a foreign key
    column which points to this model.

    """

    quick_search_fields_digit = None
    """Same as :attr:`quick_search_fields`, but this list is used when the
    search text contains only digits (and does not start with '0').

    """

    active_fields = frozenset()
    """If specified, this is the default value for
    :attr:`active_fields<lino.core.tables.AbstractTable.active_fields>`
    of every `Table` on this model.

    """

    hidden_columns = frozenset()
    """If specified, this is the default value for
    :attr:`hidden_columns<lino.core.tables.AbstractTable.hidden_columns>`
    of every `Table` on this model.

    """

    hidden_elements = frozenset()
    """If specified, this is the default value for
    :attr:`hidden_elements<lino.core.tables.AbstractTable.hidden_elements>`
    of every `Table` on this model.

    """

    # simple_parameters = frozenset()
    # """If specified, this is the default value for :attr:`simple_parameters
    # <lino.core.tables.AbstractTable.simple_parameters>` of every `Table`
    # on this model.

    # """

    preferred_foreignkey_width = None
    """The default preferred width (in characters) of widgets that
    display a ForeignKey to this model.

    If not specified, the default default `preferred_width`
    for ForeignKey fields is *20*.

    """

    workflow_state_field = None
    """If this is set on a Model, then it will be used as default value
    for
    :attr:`workflow_state_field<lino.core.table.Table.workflow_state_field>`
    of all tables based on this Model.

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

    _widget_options = {}

    def as_list_item(self, ar):
        return E.li(str(self))

    @classmethod
    def get_param_elem(model, name):
        # This is called by :meth:`Chooser.get_data_elem` when
        # application code defines a chooser with an argument that
        # does not match any field. There is currently no usage
        # example for this on database models.
        return None

    @classmethod
    def get_data_elem(cls, name):
        """Return the named data element. This can be a database field, a
        :class:`lino.core.fields.RemoteField`, a
        :class:`lino.core.fields.VirtualField` or a Django-style
        virtual field (GenericForeignKey).

        """
        #~ logger.info("20120202 get_data_elem %r,%r",model,name)
        if not name.startswith('__'):
            parts = name.split('__')
            if len(parts) > 1:
                # It's going to be a RemoteField
                # logger.warning("20151203 RemoteField %s in %s", name, cls)

                from lino.core import store

                model = cls
                field_chain = []
                for n in parts:
                    if model is None:
                        raise Exception(
                            "Invalid remote field {0} for {1}".format(name, cls))

                    if isinstance(model, basestring):
                        model = resolve_model(model)
                        # logger.warning("20151203 %s", model)
                        # Django 1.9 no longer resolves the
                        # rel.model of ForeignKeys on abstract
                        # models.

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
                    if getattr(fld, 'rel', None):
                        if AFTER18:
                            model = fld.rel.model
                        else:
                            model = fld.rel.to
                    else:
                        model = None

                def func(obj, ar=None):
                    try:
                        for fld in field_chain:
                            if obj is None:
                                return obj
                            obj = fld._lino_atomizer.full_value_from_object(
                                obj, ar)
                        return obj
                    except Exception as e:
                        raise Exception(
                            "Error while computing %s: %s" % (name, e))
                        # ~ if False: # only for debugging
                        if True:  # see 20130802
                            logger.exception(e)
                            return str(e)
                        return None
                return fields.RemoteField(func, name, fld)

        try:
            return cls._meta.get_field(name)
        except models.FieldDoesNotExist:
            pass

        v = get_class_attr(cls, name)
        if v is not None:
            return v

        for vf in cls._meta.virtual_fields:
            if vf.name == name:
                return vf

    def get_choices_text(self, request, actor, field):
        """
        Return the text to be displayed when an instance of this model
        is being used as a choice in a combobox of a ForeignKey field
        pointing to this model).
        `request` is the web request,
        `actor` is the requesting actor.

        The default behavious is to simply return `unicode(self)`.

        Usage example is :class:`lino_xl.lib.countries.models.Place`.
        """
        return str(self)

    def disable_delete(self, ar=None):
        """Decide whether this database object may be deleted.  Return `None`
        if it is okay to delete this object, otherwise a nonempty
        translatable string with a message that explains why this
        object cannot be deleted.

        The argument `ar` contains the action request which is trying
        to delete. `ar` is possibly `None` when this is being called
        from a script or batch process.

        The default behaviour checks whether there are any related
        objects which would not get cascade-deleted and thus produce a
        database integrity error.

        You can override this method e.g. for defining additional
        conditions.  Example::

          def disable_delete(self, ar=None):
              msg = super(MyModel, self).disable_delete(ar)
              if msg is not None:
                  return msg
              if self.is_imported:
                  return _("Cannot delete imported records.")

        When overriding, be careful to not skip the `super` method.

        Note that :class:`lino.mixins.polymorphic.Polymorphic`
        overrides this.

        """
        # In case of MTI, every concrete model has its own ddh.
        # Deleting an Invoice will also delete the Voucher. Ask all MTI
        # parents whether they have a veto (other than self).
        
        for b in self.__class__.__bases__:
            if issubclass(b, models.Model) \
               and b is not models.Model and not b._meta.abstract:
                msg = b._lino_ddh.disable_delete_on_object(
                    self, [self.__class__])
                if msg is not None:
                    return msg
        return self.__class__._lino_ddh.disable_delete_on_object(self)

    @classmethod
    def get_default_table(self):
        """Used internally. Lino chooses during the kernel startup, for each
        model, one of the discovered Table subclasses as the "default
        table".

        """
        return self._lino_default_table  # set in dbtables.py

    def disabled_fields(self, ar):
        """Return a set of names of fields that should be disabled (not
        editable) for this record.

        Usage example::

          def disabled_fields(self,request):
              if self.user == request.user: return []
              df = ['field1']
              if self.foo:
                df.append('field2')
              return df

        """
        return set()

    def delete(self, **kw):
        """
        Double-check to avoid "murder bug" (20150623).
        
        """
        msg = self.disable_delete(None)
        if msg is not None:
            raise Warning(msg)
        super(Model, self).delete(**kw)

    def delete_veto_message(self, m, n):
        """Return the message :message:`Cannot delete X because N Ys refer to
        it.`

        """
        msg = _(
            "Cannot delete %(model)s %(self)s "
            "because %(count)d %(refs)s refer to it."
        ) % dict(
            self=self, count=n,
            model=self._meta.verbose_name,
            refs=m._meta.verbose_name_plural or m._meta.verbose_name + 's')
        #~ print msg
        return msg

    @classmethod
    def define_action(cls, **kw):
        """
        Adds one or several actions to this model.
        Actions must be specified using keyword arguments.

        Used e.g. by :mod:`lino_xl.lib.cal` to add the `UpdateReminders`
        action to :class: `lino.modlib.users.models.User`.

        """
        for k, v in list(kw.items()):
            if k in cls.__dict__:
                raise Exception("Tried to redefine %s.%s" % (cls, k))
            setattr(cls, k, v)

    @classmethod
    def add_active_field(cls, names):
        if isinstance(cls.active_fields, basestring):
            cls.active_fields = frozenset(
                fields.fields_list(cls, cls.active_fields))
        cls.active_fields = cls.active_fields | fields.fields_list(cls, names)

    @classmethod
    def hide_elements(self, *names):
        """Mark the named data elements (fields) as hidden.  They remain in
        the database but are not visible in the user interface.

        """
        for name in names:
            if self.get_data_elem(name) is None:
                raise Exception("%s has no element '%s'" % (self, name))
        self.hidden_elements = self.hidden_elements | set(names)

    def on_create(self, ar):
        """
        Used e.g. by :class:`lino_xl.lib.notes.models.Note`.
        on_create gets the action request as argument.
        Didn't yet find out how to do that using a standard Django signal.

        """
        pass

    def after_ui_create(self, ar):
        """Like :meth:`after_ui_save`, but only on a **new** instance.

        Usage example: the :class:`households.Household
        <lino_welfare.modlib.households.models.Household>` model in
        :ref:`welfare` overrides this in order to call its `populate`
        method.

        """
        pass

    def before_ui_save(self, ar):
        """A hook for adding customized code to be executed each time an
        instance of this model gets updated via the user interface and
        **before** the changes are written to the database.

        Deprecated.  Use the :data:`pre_ui_save
        <lino.core.signals.pre_ui_save>` signal instead.

        Example in :class:`lino_xl.lib.cal.models_event.Event` to mark
        the event as user modified by setting a default state.

        """
        pass

    def after_ui_save(self, ar, cw):
        """Like :meth:`before_ui_save`, but
        **after** the changes are written to the database.

        Arguments:

            ar: the action request 
  
            cw: the :class:`ChangeWatcher` object, or `None` if this is
                a new instance.
        
        Called after a PUT or POST on this row,
        and after the row has been saved.
        
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
        pass

    def get_row_permission(self, ar, state, ba):
        """Returns True or False whether this row instance gives permission
        to the ActionRequest `ar` to run the specified action.

        """
        return ba.get_bound_action_permission(ar, self, state)

    def update_owned_instance(self, controllable):
        """
        Called by :class:`lino.modlib.gfks.Controllable`.
        """
        #~ print '20120627 tools.Model.update_owned_instance'
        pass

    def after_update_owned_instance(self, controllable):
        """
        Called by :class:`lino.modlib.gfks.Controllable`.
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

        from lino.utils.mldbc.fields import BabelCharField

        #~ logger.info("2013011 lookup_or_create")
        fkw = dict()
        fkw.update(known_values)

        if isinstance(lookup_field, basestring):
            lookup_field = model._meta.get_field(lookup_field)
        if isinstance(lookup_field, BabelCharField):
            flt = settings.SITE.lookup_filter(
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
        except ValidationError as e:
            raise ValidationError("Failed to auto_create %s : %s" %
                                  (obj2str(obj), e))
        obj.save()
        signals.auto_create.send(obj, known_values=known_values)
        return obj

    @classmethod
    def quick_search_filter(model, search_text, prefix=''):
        """Return the filter expression to apply when a quick search text is
        specified.

        """
        # logger.info(
        #     "20160610 quick_search_filter(%s, %r, %r)",
        #     model, search_text, prefix)
        q = models.Q()

        if search_text.isdigit() and not search_text.startswith('0'):
            for fn in model.quick_search_fields_digit:
                kw = {prefix + fn: int(search_text)}
                q = q | models.Q(**kw)
        else:
            for fn in model.quick_search_fields:
                kw = {prefix + fn + "__icontains": search_text}
                q = q | models.Q(**kw)
        return q

    @classmethod
    def setup_table(cls, t):
        """Called during site startup once on each Table that uses this
        model. Note that this is a class method.

        """
        pass

    def on_duplicate(self, ar, master):
        """Called by :class:`lino.mixins.duplicable.Duplicate` on
        the new row instance and on all related objects.

        `ar` is the action request that asked to duplicate.

        If `master` is not None, then this is a cascaded duplicate
        initiated be a :meth:`duplicate` on the specified `master`.

        Note that this is called *before* saving the object for the
        first time.

        Obsolete: On the master (i.e. when `master` is `None`), this
        is called *after* having saved the new object for a first
        time, and for related objects (`master` is not `None`) it is
        called *before* saving the object.  But even when an
        overridden :meth:`on_duplicate` method modifies a master, you
        don't need to :meth:`save` because Lino checks for
        modifications and saves the master a second time when needed.

        Note also that "related objects" means only those which point
        to the master using a FK which is listed in
        :attr:`allow_cascaded_delete
        <lino.core.model.Model.allow_cascaded_delete>`.

        """
        pass

    def before_state_change(self, ar, old, new):
        """Called by :meth:`set_workflow_state` before a state change."""
        pass

    def after_state_change(self, ar, old, new):
        """Called by :meth:`set_workflow_state` after a state change."""
        ar.set_response(refresh=True)

    def set_workflow_state(row, ar, state_field, target_state):
        """Called by workflow actions (:class:`ChangeStateAction
        <lino.core.workflows.ChangeStateAction>`) to perform the
        actual state change.

        """
        watcher = ChangeWatcher(row)
        old = getattr(row, state_field.attname)
        target_state.choicelist.before_state_change(row, ar, old, target_state)
        row.before_state_change(ar, old, target_state)
        setattr(row, state_field.attname, target_state)
        row.save()
        target_state.choicelist.after_state_change(row, ar, old, target_state)
        row.after_state_change(ar, old, target_state)
        watcher.send_update(ar.request)
        row.after_ui_save(ar, watcher)

    def after_send_mail(self, mail, ar, kw):
        """
        Called when an outbox email controlled by self has been sent
        (i.e. when the :class:`lino_xl.lib.outbox.models.SendMail`
        action has successfully completed).
        """
        pass

    def summary_row(self, ar, **kw):
        """Return or yield a series of HTML elements that describes this
        record in a :func:`lino.core.tables.summary`.

        Usage example::

            def summary_row(self, ar):
                elems = [ar.obj2html(self)]
                if self.city:
                    elems. += [" (", ar.obj2html(self.city), ")"]
                return E.p(*elems)

        """
        yield ar.obj2html(self)

    @fields.displayfield(_("Description"))
    def description_column(self, ar):
        if ar is None:
            return ''
        return ar.obj2html(self)

    @fields.displayfield(_("Workflow"))
    def workflow_buttons(obj, ar):
        #~ logger.info('20120930 workflow_buttons %r', obj)
        l = []
        if ar is not None:
            actor = ar.actor
            state = actor.get_row_state(obj)
            if state is not None:
                #~ l.append(E.b(unicode(state),style="vertical-align:middle;"))
                # if state.button_text:
                #     l.append(E.b(state.button_text))
                # else:
                #     l.append(E.b(str(state)))
                l.append(E.b(str(state)))
                #~ l.append(u" » ")
                #~ l.append(u" \u25b8 ")
                #~ l.append(u" \u2192 ")
                #~ sep = u" \u25b8 "
                sep = u" \u2192 "
            else:
                # logger.info('20150602 no state for %s in %s (%s)',
                #             obj, actor, actor.model)
                sep = ''

            for ba in actor.get_actions():
                if ba.action.show_in_workflow:
                    if actor.get_row_permission(obj, ar, state, ba):
                        l.append(sep)
                        l.append(ar.action_button(ba, obj))
                        sep = ' '
        return E.span(*l)

    def error2str(self, e):
        return error2str(self, e)

    def __repr__(self):
        return obj2str(self)

    def get_related_project(self):
        if settings.SITE.project_model:
            if isinstance(self, settings.SITE.project_model):
                return self

    def get_system_note_type(self, request):
        """Used when :mod:`lino_xl.lib.notes` is installed. Expected to return
        either `None` (the default) or an existing :class:`NoteType
        <lino_xl.lib.notes.models.NoteType>` instance. If this is not
        `None`, then the system note will also be stored in the
        database as a :class:`lino_xl.lib.notes.models.Note`.

        """
        return None

    def get_system_note_recipients(self, request, silent):
        """
        Return a list of email recipients for a system note on this
        object. Used by :meth:`rt.ar.add_system_note`.

        Every recipient must be a string with a valid email recipient like
        "john@example.com" or "John Doe <john@example.com>".
        """

        return []

    def to_html(self, **kw):
        import lino.ui.urls  # hack: trigger ui instantiation
        actor = self.get_default_table()
        kw.update(renderer=settings.SITE.kernel.text_renderer)
        ar = actor.request(**kw)
        return self.preview(ar)
        #~ username = kw.pop('username',None)

    def get_typed_instance(self, model):
        """
        Used when implementing :ref:`polymorphism`.
        """
        return self

    def get_detail_action(self, ar):
        """Return the detail action to use for this object with the given
        action request.

        If `self` has a special attribute `_detail_action` defined,
        return this.  This magic is used by
        :meth:`Menu.add_instance_action
        <lino.core.menus.Menu.add_instance_action>`.

        If the action requests's actor can be used for this object,
        then use its `detail_action`. Otherwise use the
        `detail_action` of this object's default table.

        Return `None` if no detail action is defined, or if the
        request has no view permission.

        Once upon a time we wanted that e.g. for a `pcsw.Client` the
        detail_action depends on the user profile.  This feature is
        currently not used.

        """
        a = getattr(self, '_detail_action', None)
        if a is None:
            if ar and ar.actor and ar.actor.model \
               and self.__class__ is ar.actor.model:
                a = ar.actor.detail_action
            else:
                a = self.__class__.get_default_table().detail_action
        if a is None or ar is None:
            return a
        if a.get_view_permission(ar.get_user().profile):
            return a

    def is_attestable(self):
        """Override this to disable the :class:`lino_xl.lib.excerpts.CreateExcerpt`
action on individual instances.

        """
        return True

    @classmethod
    def get_chooser_for_field(cls, fieldname):
        d = getattr(cls, '_choosers_dict', {})
        return d.get(fieldname, None)

    @classmethod
    def get_template_group(cls):
        # used by excerpts and printable
        return cls._meta.app_label + '/' + cls.__name__

    def get_body_template(self):
        """Return the name of the body template to use when rendering this
        object in a printable excerpt (:mod:`lino_xl.lib.excerpts`).
        An empty string means that Lino should use the default value
        defined on the ExcerptType.

        """
        return ''

    # def get_excerpt_type(self):
    #     "Return the primary ExcerptType for the given model."
    #     ContentType = settings.SITE.modules.contenttypes.ContentType
    #     ct = ContentType.objects.get_for_model(
    #         self.__class__)
    #     return self.__class__.objects.get(primary=True, content_type=ct)

    def get_excerpt_options(self, ar, **kw):
        """Set additional fields of newly created excerpts from this.  Called
        from
        :class:`lino_xl.lib.excerpts.models.ExcerptType.get_or_create_excerpt`.

        """
        return kw

    def get_print_language(self):
        """Return a Django language code to be activated when an instance of
        this is being printed.  The default implementation returns the
        Site's default language.

        """
        # same as EmptyTableRow.get_print_language
        return settings.SITE.DEFAULT_LANGUAGE.django_code

    @classmethod
    def set_widget_options(self, name, **options):
        """Set default values for the widget options of a given element.

        Usage example::

            JobSupplyment.set_widget_options('duration', width=10)

        has the same effect as specifying ``duration:10`` each time
        when using this element in a layout.

        """
        self._widget_options = dict(**self._widget_options)
        d = self._widget_options.setdefault(name, {})
        d.update(options)

    @classmethod
    def get_widget_options(self, name, **options):
        options.update(self._widget_options.get(name, {}))
        return options

    def get_printable_context(self, ar=None, **kw):

        """Adds a series of names to the context used when rendering printable
        documents. See :doc:`/user/templates_api`.

        :class:`lino_xl.lib.notes.models.Note` extends this.

        """
        # same as lino.utils.report.EmptyTableRow.get_printable_context
        if ar is not None:
            kw = ar.get_printable_context(**kw)
        kw.update(this=self)  # for backward compatibility
        kw.update(obj=self)  # preferred in new templates
        kw.update(language=self.get_print_language())
        return kw

    def before_printable_build(self, bm):
        pass

    def filename_root(self):
        return self._meta.app_label + '.' + self.__class__.__name__ \
            + '-' + str(self.pk)

    @classmethod
    def get_parameter_fields(cls, **fields):
        """Inheritable hook for defining parameters.
        Called once per actor at site startup.

        It receives a `dict` object `fields` and is expected to return
        that `dict` which it may update.

        See also :meth:`get_simple_parameters`.

        Usage example: :class:`lino.modlib.users.mixins.UserAuthored`.

        """
        return fields

    @classmethod
    def get_simple_parameters(cls):
        """Return a set of names of simple parameter fields of every
        `Table` on this model.

        """
        return set([])

    @classmethod
    def get_request_queryset(cls, ar):
        return cls.objects.all()

    @classmethod
    def get_title_tags(self, ar):
        return []

    @classmethod
    def django2lino(cls, model):
        """
        A list of the attributes to be copied to Django models which do
        not inherit from :class:`lino.core.model.Model`.  Used by
        :mod:`lino.core.kernel`

        """
        if issubclass(model, cls):
            return

        for k in LINO_MODEL_ATTRIBS:
            if not hasattr(model, k):
                #~ setattr(model,k,getattr(dd.Model,k))
                setattr(model, k, cls.__dict__[k])
                #~ model.__dict__[k] = getattr(dd.Model,k)
                #~ logger.info("20121127 Install default %s for %s",k,model)

    @classmethod
    def get_subclasses_graph(self):
        """
        Returns an internationalized `graphviz` directive representing
        the polymorphic forms of this model.

        Usage example::

          .. django2rst::

              with dd.translation.override('de'):
                  contacts.Partner.print_subclasses_graph()

        """
        from lino.api import rt
        pairs = []
        collected = set()

        def collect(p):
            for c in rt.models_by_base(p):
                # if c is not p and (p in c.__bases__):
                # if c is not m and p in c.__bases__:
                if c is not p:
                    # ok = True
                    # for cb in c.__bases__:
                    #     if cb in p.mro():
                    #         ok = False
                    # if ok:
                    if c not in collected:
                        pairs.append((p, c))
                        collected.add(c)
                    collect(c)
        collect(self)
        s = '\n'.join(
            ['    "%s" -> "%s"' % (
                p._meta.verbose_name, c._meta.verbose_name)
             for p, c in pairs])
        return """

.. graphviz::
   
   digraph foo {
%s
  }
  
""" % s

    @classmethod
    def print_subclasses_graph(self):
        print(self.get_subclasses_graph())

LINO_MODEL_ATTRIBS = (
    'get_parameter_fields',
    '_widget_options',
    'set_widget_options',
    'get_widget_options',
    'get_chooser_for_field',
    'get_detail_action',
    'get_print_language',
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
    'get_simple_parameters',
    'get_request_queryset',
    'get_title_tags',
    'get_default_table',
    'get_template_group',
    'get_related_project',
    'get_system_note_recipients',
    'get_system_note_type',
    'quick_search_fields',
    'quick_search_fields_digit',
    'change_watcher_spec',
    'on_analyze',
    'disable_delete',
    'lookup_or_create',
    'quick_search_filter',
    'on_duplicate',
    'on_create',
    'error2str',
    'get_typed_instance',
    'print_subclasses_graph',
    'grid_post', 'submit_insert', 'delete_veto_message')


from lino.core.signals import receiver
from django.db.models.signals import pre_delete


@receiver(pre_delete)
def pre_delete_handler(sender, instance=None, **kw):
    """Before actually deleting an object, we override Django's behaviour
    concerning related objects via a GFK field.

    In Lino you can configure the cascading behaviour using
    :attr:`allow_cascaded_delete`.

    See also :doc:`/dev/gfks`.

    It seems that Django deletes *generic related objects* only if
    the object being deleted has a `GenericRelation
    <https://docs.djangoproject.com/en/1.7/ref/contrib/contenttypes/#django.contrib.contenttypes.fields.GenericRelation>`_
    field (according to `Why won't my GenericForeignKey cascade
    when deleting?
    <http://stackoverflow.com/questions/6803018/why-wont-my-genericforeignkey-cascade-when-deleting>`_).
    OTOH this statement seems to be wrong: it happens also in my
    projects which do *not* use any `GenericRelation`.  As
    :mod:`test_broken_gfk
    <lino_welfare.projects.eupen.tests.test_broken_gfk>` shows.

    TODO: instead of calling :meth:`disable_delete
    <lino.core.model.Model.disable_delete>` here again (it has
    been called earlier by the delete action before asking for user
    confirmation), Lino might change the `on_delete` attribute of all
    `ForeignKey` fields which are not in
    :attr:`allow_cascaded_delete` from ``CASCADE`` to
    ``PROTECTED`` at startup.

    """

    kernel = settings.SITE.kernel
    # print "20141208 generic related objects for %s:" % obj
    must_cascade = []
    for gfk, fk_field, qs in kernel.get_generic_related(instance):
        if gfk.name in qs.model.allow_cascaded_delete:
            must_cascade.append(qs)
        else:
            if fk_field.null:  # clear nullable GFKs
                for obj in qs:
                    setattr(obj, gfk.name, None)
            elif qs.count():
                raise Warning(instance.delete_veto_message(
                    qs.model, qs.count()))
    for qs in must_cascade:
        if qs.count():
            logger.info("Deleting %d %s before deleting %s",
                        qs.count(),
                        qs.model._meta.verbose_name_plural,
                        obj2str(instance))
            for obj in qs:
                obj.delete()

