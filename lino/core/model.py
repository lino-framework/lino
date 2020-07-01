# -*- coding: UTF-8 -*-
# Copyright 2009-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"Defines the :class:`Model` class."

import logging ; logger = logging.getLogger(__name__)
import copy

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from etgen.html import E, forcetext, tostring

from lino.core import fields
from lino.core import signals
from lino.core import actions
from .fields import make_remote_field, RichTextField
from .utils import error2str
from .utils import obj2str
from .diff import ChangeWatcher
from .utils import obj2unicode
from .utils import class_dict_items
from .signals import on_ui_created, pre_ui_delete, pre_ui_save
from .workflows import ChangeStateAction

try:
    import bleach
except ImportError:
    bleach = None




class Model(models.Model, fields.TableRow):
    """Lino adds a series of features to Django's `Model
    <https://docs.djangoproject.com/en/dev/ref/models/class/>`_
    class.  If a Lino application includes plain Django Model
    classes, Lino will "extend" these by adding the attributes and
    methods defined here to these classes.

    .. attribute:: workflow_buttons

        A virtual field that displays the **workflow actions** for
        this row.  This is a compact but intuitive representation of
        the current workflow state, together with a series of
        clickable actions.

    .. attribute:: overview

        A fragment of HTML describing this object in a customizable story of
        paragraphs.

        Customizable using :meth:`get_overview_elems`.

    .. attribute:: detail_link

        A virtual field which displays this database row as a clickable link
        which opens the detail window.  Functionally equivalent to a double
        click, but more intuitive in some places.

    .. method:: full_clean

        This is defined by Django.

    .. method:: FOO_changed

        Called when field FOO of an instance of this model has been
        modified through the user interface.

        Example::

          def city_changed(self, ar):
              print("User {} changed city of {} to {}!".format(
                  ar.get_user(), self, self.city))

        Note: If you want to know the old value when reacting to a change,
        consider writing :meth:`after_ui_save` instead.

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
              return cls.city.field.remote_field.model.objects.order_by('name')


    .. method:: create_FOO_choice

        For every field named "FOO" for which a chooser exists, if the model
        also has a method called "create_FOO_choice", then this chooser will be
        a :term:`learning chooser`. That is, users can enter text into the
        combobox, and Lino will create a new database object from it.

        This works only if FOO is (1) a foreign key and (2) has a chooser.
        See also :term:`learning foreign key`.

    """

    class Meta(object):
        abstract = True

    allow_cascaded_copy = frozenset()
    """A set of names of `ForeignKey` or `GenericForeignKey` fields of
    this model that cause objects to be automatically duplicated when
    their master gets duplicated.

    If this is a simple string, Lino expects it to be a
    space-separated list of filenames and convert it into a set at
    startup.

    """

    allow_cascaded_delete = frozenset()
    """A set of names of `ForeignKey` or `GenericForeignKey` fields of
    this model that allow for cascaded delete.

    Unlike with Dango's `on_delete
    <https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.ForeignKey.on_delete>`__
    attribute you control cascaded delete behaviour on the model whose instances
    are going to be deleted.

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

    At startup (in :meth:`kernel_startup
    <lino.core.kernel.Kernel.kernel_startup>`) Lino automatically sets
    `on_delete
    <https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.ForeignKey.on_delete>`__
    to ``PROTECT`` for all FK fields that are not listed in the
    ``allow_cascaded_delete`` of their model.

    """

    grid_post = actions.CreateRow()
    submit_insert = actions.SubmitInsert()
    """This is the action represented by the "Create" button of an Insert
    window. See :mod:`lino.mixins.dupable` for an example of how to
    override it.

    """

    allow_merge_action = False
    """Whether this model should have a merge action.

    See :class:`lino.core.merge.MergeAction`
    """

    show_in_site_search = True
    """Set this to `False` if you really don't want this model to occur
    in the site-wide search
    (:class:`lino.modlib.about.SiteSearch`).

    """

    quick_search_fields = None
    """
    Explicitly specify the fields to be included in queries with a
    quick search value.

    In your model declarations this should be either `None` or a
    `string` containing a space-separated list of field names.  During
    server startup resolves it into a tuple of data elements.

    If it is `None`, Lino installs a list of all CharFields on the
    model.

    If you want to not inherit this field from a parent using standard
    MRO, then you must set that field explictly to `None`.

    This is also used when a gridfilter has been set on a foreign key
    column which points to this model.

    **Special quick search strings**

    If the search string starts with "#", then Lino searches for a row
    with that *primary key*.

    If the search string starts with "*", then Lino searches for a row
    with that *reference*.
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
    for :attr:`workflow_state_field
    <lino.core.table.Table.workflow_state_field>` of all tables based
    on this Model.

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

    disable_create_choice = False
    """Whether to disable any automatic creation by learning choosers.
    """

    summary_row_template = None
    """
    An optional name of a template to use for :meth:`as_summary_row`.
    """

    _widget_options = {}
    _lino_tables = []
    _bleached_fields = []

    def as_list_item(self, ar):
        return E.li(str(self))

    @classmethod
    def collect_virtual_fields(model):
        """Declare every virtual field defined on this model to Django.

        We use Django's undocumented :meth:`add_field` method.

        Make a copy if the field is inherited, in order to avoid side effects
        like #2592.

        Raise an exception if the model defines both a database field and a
        virtual field of same name.

        """
        if model._meta.abstract:  # 20181023
            return
        # print("201906274 collect_virtual_fields a ", model, model._meta.fields)
        # fieldnames = {f.name for f in model._meta.get_fields()}
        # inject_field() can call this when Models aren't loaded yet.
        fieldnames = {f.name for f in
                      model._meta.private_fields + model._meta.local_fields}
        # print("201906274 collect_virtual_fields b ", fieldnames)
        for m, k, v in class_dict_items(model):
            if isinstance(v, fields.VirtualField):
                # print("201906274 collect_virtual_fields c", m, k, v)
                if k in fieldnames:
                    # There are different possible reasons for this case.  E.g.
                    # a copy of virtual field in parent has already been
                    # attached.
                    continue
                    # f = model._meta.get_field(k)
                    # if f.__class__ is v.__class__:
                    #     # print("20190627 ignoring", m, k, v, f)
                    #     continue
                    # raise ChangedAPI(
                    #     "Virtual field {}.{} hides {} "
                    #     "of same name.".format(
                    #         full_model_name(model), k, f.__class__.__name__))
                if m is not model:
                    # if k == "overview" and model.__name__ == "DailyPlannerRow":
                    #     print("20181022", m, model)
                    # settings.SITE.VIRTUAL_FIELDS.pop(v)
                    v = copy.deepcopy(v)
                settings.SITE.register_virtual_field(v)
                v.attach_to_model(model, k)
                model._meta.add_field(v, private=True)
                fieldnames.add(k)

    @classmethod
    def get_param_elem(model, name):
        # This is called by :meth:`Chooser.get_data_elem` when
        # application code defines a chooser with an argument that
        # does not match any field. There is currently no usage
        # example for this on database models.
        return None

    @classmethod
    def get_data_elem(cls, name):

        if not name.startswith('__'):
            rf = make_remote_field(cls, name)
            if rf:
                return rf
        try:
            return cls._meta.get_field(name)
        except models.FieldDoesNotExist:
            pass

        for vf in cls._meta.private_fields:
            if vf.name == name:
                return vf
        return getattr(cls, name, None)

        # we cannot return super(Model, cls).get_data_elem(name) here because
        # get_data_elem is grafted also to pure Django models which don't
        # inherit from TableRow


    def disable_delete(self, ar=None):
        """
        Decide whether this database object may be deleted.  Return `None`
        if it is okay to delete this object, otherwise a nonempty
        translatable string with a message that explains in user
        language why this object cannot be deleted.

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
        # Deleting an Invoice will also delete the Voucher. Ask all
        # MTI parents (other than self) whether they have a veto .

        for b in self.__class__.__bases__:
            if issubclass(b, models.Model) \
               and b is not models.Model and not b._meta.abstract:
                msg = b._lino_ddh.disable_delete_on_object(
                    self, [self.__class__])
                if msg is not None:
                    return msg
        return self.__class__._lino_ddh.disable_delete_on_object(self)

    def disabled_fields(self, ar):
        """
        Return a set of names of fields that should be disabled (not
        editable) for this record.

        See :doc:`/dev/disabled_fields`.
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
        """Adds one or several actions or other class attributes to this
        model.

        Attributes must be specified using keyword arguments, the
        specified keys must not yet exist on the model.

        Used e.g. in :mod:`lino_xl.lib.cal` to add the `UpdateReminders`
        action to :class: `lino.modlib.users.models.User`.

        Or in :mod:`lino_xl.lib.invoicing.models` for defining a
        custom chooser.

        """
        for k, v in list(kw.items()):
            if k in cls.__dict__:
                raise Exception("Tried to redefine %s.%s" % (cls, k))
            setattr(cls, k, v)

    @classmethod
    def add_active_field(cls, names):
        if isinstance(cls.active_fields, str):
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

    @classmethod
    def add_param_filter(cls, qs, lookup_prefix='', **kwargs):
        """Add filters to queryset using table parameter fields.

        This is called for every simple parameter.

        Usage examples: :class:`DeploymentsByTicket
        <lino_xl.lib.deploy.desktop.DeploymentsByTicket>`, :mod:`lino_book.projects.min3.lib.contacts`.

        """
        # print("20200425", kwargs)
        return qs.filter(**kwargs)
        # if len(kwargs):
        #     raise Exception(
        #         "{}.add_param_filter got unknown argument {}".format(
        #             str(cls.__name__), kwargs))
        # return qs

    @classmethod
    def on_analyze(cls, site):

        if isinstance(cls.workflow_owner_field, str):
            cls.workflow_owner_field = cls.get_data_elem(
                cls.workflow_owner_field)
        if isinstance(cls.workflow_state_field, str):
            cls.workflow_state_field = cls.get_data_elem(
                cls.workflow_state_field)
        # for vf in cls._meta.private_fields:
        #     if vf.name == 'detail_link':
        #         if vf.verbose_name is None:
        #
        #             # note that the verbose_name of a virtual field is a copy
        #             # of the verbose_name of its return_type (see
        #             # VirtualField.lino_resolve_type)
        #
        #             # vf.verbose_name = model._meta.verbose_name
        #             vf.return_type.verbose_name = cls._meta.verbose_name
        #             # if model.__name__ == "Course":
        #             #     print("20181212", model)
        #             break
        bleached_fields = []
        for f in cls._meta.get_fields():
            if isinstance(f, RichTextField):
                if f.editable and \
                    (f.bleached is True or
                        f.bleached is None and settings.SITE.textfield_bleached):
                    bleached_fields.append(f)
        cls._bleached_fields = tuple(bleached_fields)
        if hasattr(cls, 'bleached_fields'):
            raise ChangedAPI("Replace bleached_fields by bleached=True on each field")


    @classmethod
    def lookup_or_create(model, lookup_field, value, **known_values):
        """
        Look up whether there is a model instance having
        `lookup_field` with value `value`
        (and optionally other `known_values` matching exactly).

        If it doesn't exist, create it and emit an
        :attr:`auto_create <lino.core.signals.auto_create>` signal.

        """

        from lino.utils.mldbc.fields import BabelCharField

        # ~ logger.info("2013011 lookup_or_create")
        fkw = dict()
        fkw.update(known_values)

        if isinstance(lookup_field, str):
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
            # ~ flt = models.Q(**{self.lookup_field.name: value})
        qs = model.objects.filter(flt)
        if qs.count() > 0:  # if there are multiple objects, return the first
            if qs.count() > 1:
                logger.warning(
                    "%d %s instances having %s=%r (I'll return the first).",
                    qs.count(), model.__name__, lookup_field.name, value)
            return qs[0]
        # ~ known_values[lookup_field.name] = value
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
        flt = models.Q()
        for w in search_text.split():
            q = models.Q()
            char_search = True
            if w.startswith("#") and w[1:].isdigit():
                w = w[1:]
                char_search = False
            if w.isdigit():
                for fn in model.quick_search_fields_digit:
                    kw = {prefix + fn.name: int(w)}
                    q = q | models.Q(**kw)
            if char_search:
                for fn in model.quick_search_fields:
                    kw = {prefix + fn.name + "__icontains": w}
                    q = q | models.Q(**kw)
            flt &= q
        return flt

    def on_create(self, ar):
        """
        Override this to set default values that depend on the request.

        The difference with Django's `pre_init
        <https://docs.djangoproject.com/en/1.11/ref/signals/#pre-init>`__
        and `post_init
        <https://docs.djangoproject.com/en/1.11/ref/signals/#post-init>`__
        signals is that (1) you override the method instead of binding
        a signal and (2) you get the action request as argument.

        Used e.g. by :class:`lino_xl.lib.notes.Note`.
        """
        pass

    def before_ui_save(self, ar):
        """A hook for adding custom code to be executed each time an
        instance of this model gets updated via the user interface and
        **before** the changes are written to the database.

        Deprecated.  Use the :data:`pre_ui_save
        <lino.core.signals.pre_ui_save>` signal instead.

        Example in :class:`lino_xl.lib.cal.Event` to mark the
        event as user modified by setting a default state.

        """
        for f, old, new in self.fields_to_bleach():
            setattr(self, f.name, new)

    def fields_to_bleach(self):

        if bleach:
            for f in self._bleached_fields:
                old = getattr(self, f.name)
                if old is None:
                    continue
                # print("20190626", self, f, old)
                if not old.startswith("<"):
                    continue
                try:
                    new = bleach.clean(
                        old, tags=settings.SITE.bleach_allowed_tags, strip=True)
                except TypeError as e:
                    logger.warning(
                        "Could not bleach %r : %s (%s)", old, e, self)
                    continue
                if old != new:
                    logger.debug(
                        "Bleaching %s from %r to %r", f.name, old, new)
                    yield f, old, new


    def after_ui_save(self, ar, cw):
        """Like :meth:`before_ui_save`, but
        **after** the changes are written to the database.

        Arguments:

            ar: the action request

            cw: the :class:`ChangeWatcher <lino.core.diff.ChangeWatcher>`
                object, or `None` if this is a new instance.

        Called after a PUT or POST on this row, and after the row has
        been saved.

        Used by
        :class:`lino_welfare.modlib.debts.models.Budget`
        to fill default entries to a new Budget,
        or by :class:`lino_welfare.modlib.cbss.models.CBSSRequest`
        to execute the request,
        or by
        :class:`lino_welfare.modlib.jobs.models.Contract`
        :class:`lino_welfare.modlib.pcsw.models.Coaching`
        :class:`lino.modlib.vat.models.Vat`.
        Or :class:`lino_welfare.modlib.households.models.Household`
        overrides this in order to call its `populate` method.

        """
        # Invalidate disabled_fields cache
        self._disabled_fields = None

    def after_ui_create(self, ar):
        """
        Hook to define custom behaviour to run when a user has created a new instance
        of this model.
        """
        # print(19062017, "Ticket 1910")
        pass

    def save_new_instance(elem, ar):
        """Save this instance and fire related behaviour."""
        pre_ui_save.send(sender=elem.__class__, instance=elem, ar=ar)
        elem.before_ui_save(ar)
        elem.save(force_insert=True)
        # yes, `on_ui_created` comes *after* save()
        on_ui_created.send(elem, request=ar.request)
        ar.selected_rows.append(elem)
        elem.after_ui_create(ar)
        if ar and ar.actor:
            ar.actor.after_create_instance(elem, ar)
        elem.after_ui_save(ar, None)

    def save_watched_instance(elem, ar, watcher):
        if watcher.is_dirty():
            pre_ui_save.send(sender=elem.__class__, instance=elem, ar=ar)
            elem.before_ui_save(ar)
            elem.save(force_update=True)
            watcher.send_update(ar)
            ar.success(_("%s has been updated.") % obj2unicode(elem))
        else:
            ar.success(_("%s : nothing to save.") % obj2unicode(elem))
        elem.after_ui_save(ar, watcher)

    def delete_instance(self, ar):
        pre_ui_delete.send(sender=self, request=ar.request)
        self.delete()

    def get_row_permission(self, ar, state, ba):
        """Returns True or False whether this database object gives permission
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

    # moved to TableRow
    # def get_overview_elems(self, ar):
    #     """This is expected to return a list of HTML elements to be wrapped
    #     into a `<DIV>`.
    #
    #     """
    #     # return [ar.obj2html(self)]
    #     return [self.obj2href(ar)]

    def on_duplicate(self, ar, master):
        """
        Called after duplicating a row on the new row instance.

        Also called recursively on all related objects.  Where "related
        objects" means those which point to the master using a FK which is
        listed in :attr:`allow_cascaded_delete
        <lino.core.model.Model.allow_cascaded_delete>`.

        Called by the :class:`lino.mixins.duplicable.Duplicate` action.

        `ar` is the action request that asked to duplicate.

        If `master` is not None, then this is a cascaded duplicate
        initiated by a :meth:`duplicate` on the specified `master`.

        Note that this is called *before* saving the object for the
        first time.

        Obsolete: On the master (i.e. when `master` is `None`), this
        is called *after* having saved the new object for a first
        time, and for related objects (`master` is not `None`) it is
        called *before* saving the object.  But even when an
        overridden :meth:`on_duplicate` method modifies a master, you
        don't need to :meth:`save` because Lino checks for
        modifications and saves the master a second time when needed.


        """
        pass

    def after_duplicate(self, ar, master):
        """Called by :class:`lino.mixins.duplicable.Duplicate` on
        the new copied row instance, after the row and it's related fields
        have been saved.

        `ar` is the action request that asked to duplicate.

        `ar.selected_rows[0]` contains the original row that is being
        copied, which is the `master` parameter """
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
        # assert hasattr(row, state_field.attname)
        old = getattr(row, state_field.attname)
        target_state.choicelist.before_state_change(row, ar, old, target_state)
        row.before_state_change(ar, old, target_state)
        setattr(row, state_field.attname, target_state)
        row.save()
        target_state.choicelist.after_state_change(row, ar, old, target_state)
        row.after_state_change(ar, old, target_state)
        watcher.send_update(ar)
        row.after_ui_save(ar, watcher)

    def after_send_mail(self, mail, ar, kw):
        """
        Called when an outbox email controlled by self has been sent
        (i.e. when the :class:`lino_xl.lib.outbox.models.SendMail`
        action has successfully completed).
        """
        pass

    def as_summary_row(self, ar):
        """
        Return a raw HTML string representing this object in a data view as a
        single paragraph.

        The string should represent a single ``<p>``.

        If :attr:`summary_row_template` is set, this will render this object
        using the named template, otherwise it will call :meth:`summary_row` and
        wrap the result into a paragraph.


        """
        if self.summary_row_template:
            # not tested
            env = settings.SITE.plugins.jinja.renderer.jinja_env
            template = env.get_template(self.summary_row_template)
            context = ar.get_printable_context(obj=self)
            return template.render(**context)
        return tostring(E.p(*self.summary_row(ar)))

    def summary_row(self, ar, **kw):
        """
        Yield a sequence of ElementTree elements that represent this database
        object in a summary panel.

        The elements will be wrapped into a `<p>` by :meth:`as_summary_row`.

        The default representation is the text returned by :meth:`__str__` in a
        link that opens the detail view on this database object.

        The description may vary depending on the given action request.

        For example a partner model of a given application may want to always
        show the city of a partner unless city is among the known values::

            def summary_row(self, ar):
                elems = [ar.obj2html(self)]
                if self.city and not "city" in ar.known_values:
                    elems += [" (", ar.obj2html(self.city), ")"]
                return E.p(*elems)

        Note that this is called by the class method of same name on
        :class:`lino.core.actors.Actor`, which can potentially be customized and
        can potentially decide to not call the model method.

        TODO: rename this to `get_row_description` and write documentation.

        """
        yield ar.obj2html(self)

    @fields.displayfield(_("Name"), max_length=15)
    def name_column(self, ar):
        return str(self)

    # @fields.displayfield(_("Description"))
    # def mobile_item(self, ar):
    #     if ar is None:
    #         return ''
    #     return E.div(*forcetext(self.get_mobile_list_item_elems(ar)))
    #
    # def get_mobile_list_item_elems(self, ar):
    #     return [self.obj2href(ar)]

    # @fields.displayfield(_("Description"))
    # @fields.htmlbox(_("Overview"))
    @fields.htmlbox()
    def overview(self, ar):
        if ar is None:
            return ''
        return E.div(*forcetext(self.get_overview_elems(ar)))

    @fields.displayfield(_("Workflow"))
    def workflow_buttons(self, ar):
        if ar is None:
            return ''
        return self.get_workflow_buttons(ar)

    def get_workflow_buttons(obj, ar):
        l = []
        actor = ar.actor
        # print(20170102, actor)
        state = actor.get_row_state(obj)
        sep = ''
        show = True  # whether to show the state
        # logger.info('20161219 workflow_buttons %r', state)

        def show_state():
            l.append(sep)
            #~ l.append(E.b(unicode(state),style="vertical-align:middle;"))
            if state.button_text:
                l.append(E.b(u"{} {}".format(state.button_text, state)))
            else:
                l.append(E.b(str(state)))
            # l.append(E.b(str(state)))
            #~ l.append(u" » ")
            #~ l.append(u" \u25b8 ")
            #~ l.append(u" \u2192 ")
            #~ sep = u" \u25b8 "

        df = actor.get_disabled_fields(obj, ar)
        # print(20170909, df)
        for ba in actor.get_actions():
            assert ba.actor == actor  # 20170102
            if ba.action.show_in_workflow:
                # if actor.model.__name__ == 'Vote':
                #     if ba.action.__class__.__name__ == 'MarkVoteAssigned':
                #         print(20170115, actor, ar.get_user())
                if ba.action.action_name not in df:
                  if actor.get_row_permission(obj, ar, state, ba):
                    if show and isinstance(ba.action, ChangeStateAction):
                        show_state()
                        sep = u" \u2192 "  # "→"
                        show = False
                    l.append(sep)
                    l.append(ar.action_button(ba, obj))
                    sep = ' '
        if state and show:
            show_state()
        return E.span(*l)

    def error2str(self, e):
        return error2str(self, e)

    def __repr__(self):
        return obj2str(self)

    def get_related_project(self):
        if settings.SITE.project_model:
            if isinstance(self, settings.SITE.project_model):
                return self

    # def to_html(self, **kw):
    #     import lino.ui.urls  # hack: trigger ui instantiation
    #     actor = self.get_default_table()
    #     kw.update(renderer=settings.SITE.kernel.text_renderer)
    #     ar = actor.request(**kw)
    #     return self.preview(ar)
    #     #~ username = kw.pop('username',None)

    def get_typed_instance(self, model):
        """
        Used when implementing :ref:`polymorphism`.
        """
        return self


#     def is_attestable(self):
#         """Override this to disable the :class:`lino_xl.lib.excerpts.CreateExcerpt`
# action on individual instances.

#         """
#         return True

    @classmethod
    def get_chooser_for_field(cls, fieldname):
        d = getattr(cls, '_choosers_dict', {})
        # if fieldname.endswith("__municipality"):
        #     print("20200425 Model.get_chooser_for_field", cls, fieldname, d)
        return d.get(fieldname, None)

    @classmethod
    def set_widget_options(self, name, **options):
        """
        Set default values for the widget options of a given element.

        Usage example::

            JobSupplyment.set_widget_options('duration', width=10)

        has the same effect as specifying ``duration:10`` each time
        when using this element in a layout.

        List of widget options that can be set:

        `width`
        `preferred_width`
        `label`
        `editable`
        `preferred_height`
        `hide_sum`


        """
        # from lino.modlib.extjs.elems import FieldElement
        # for k in options.keys():
        #     if not hasattr(FieldElement, k):
        #         raise Exception("Invalid widget option {}".format(k))
        self._widget_options = dict(**self._widget_options)
        d = self._widget_options.setdefault(name, {})
        d.update(options)

    @classmethod
    def get_widget_options(self, name, **options):
        options.update(self._widget_options.get(name, {}))
        return options

    def filename_root(self):
        return self._meta.app_label + '.' + self.__class__.__name__ \
            + '-' + str(self.pk)

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        """Return the base queryset for tables on this object.

        The optional `filter` keyword arguments, if present, are
        applied as additional filter. This is used only in UNION
        tables on abstract model mixins where filtering cannot be done
        after the join.

        """
        qs = cls.get_user_queryset(ar.get_user(), **filter)
        if ar.actor.only_fields is not None:
            qs = qs.only(ar.actor.only_fields)
        return qs

    @classmethod
    def get_user_queryset(cls, user, **filter):
        """
        Get the base queryset, used for user level row filtering in :class:`lino_xl.lib.tickets.Ticket`
        """
        if filter:
            return cls.objects.filter(**filter)
        return cls.objects.all()

    @classmethod
    def get_title_tags(self, ar):
        return []

    @classmethod
    def resolve_states(cls, states):
        """Convert the given string `states` into a set of state objects.

        The states specifier must be either a set containing state
        objects or a string containing a space-separated list of valid
        state names. If it is a string, convert it to the set.

        """
        if states is None:
            return None
        elif isinstance(states, str):
            fld = cls.workflow_state_field
            return set(
                [fld.choicelist.get_by_name(x) for x in states.split()])
        elif isinstance(states, set):
            return states
        raise Exception(
            "Cannot resolve stateset specifier {!r}".format(states))

    @classmethod
    def get_actions_hotkeys(cls):
        """
        Return or yield a list of hotkeys to be linked to named actions.

        [{'key': key, 'ctrl': Bool, 'shift': Bool, 'ba': action_name}]

        """

    @classmethod
    def get_layout_aliases(cls):
        """

        Yield a series of (ALIAS, repl) tuples that cause a name ALIAS in a
        layout based on this model to be replaced by its replacement `repl`.

        """
        return []

    @classmethod
    def django2lino(cls, model):
        """
        Injects additional methods into a pure Django model that does
        not inherit from :class:`lino.core.model.Model`.  Used by
        :mod:`lino.core.kernel`

        """
        wo = {}
        for b in model.__mro__:
            if issubclass(b, cls):
                wo.update(b._widget_options)
        model._widget_options = wo

        if issubclass(model, cls):
            return

        for k in LINO_MODEL_ATTRIBS:
            if not hasattr(model, k):
                #~ setattr(model,k,getattr(dd.Model,k))
                # if k in cls.__dict__:
                #     setattr(model, k, cls.__dict__[k])
                # else:
                #     setattr(model, k, getattr(cls, k))
                for b in cls.__mro__:
                    if k in b.__dict__:
                        setattr(model, k, b.__dict__[k])
                        break
                # setattr(model, k, getattr(cls, k))
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
    'collect_virtual_fields',
    'define_action',
    'delete_instance',
    'setup_parameters',
    'add_param_filter',
    'save_new_instance',
    'save_watched_instance',
    'save_existing_instance',
    '_widget_options',
    'set_widget_options',
    'get_widget_options',
    'get_chooser_for_field',
    'get_detail_action',
    # 'get_print_language',
    'get_row_permission',
    # 'get_excerpt_options',
    # 'is_attestable',
    'get_data_elem',
    'get_param_elem',
    'after_ui_save',
    'preferred_foreignkey_width',
    'before_ui_save',
    'allow_cascaded_delete',
    'allow_cascaded_copy',
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
    'get_user_queryset',
    'get_title_tags',
    'get_default_table',
    'get_default_table',
    'get_layout_aliases',
    'get_actions_hotkeys',
    'as_summary_row',
    'summary_row_template',
    'get_related_project',
    'obj2href',
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
    'grid_post', 'submit_insert', 'delete_veto_message', '_lino_tables',
    'show_in_site_search', 'allow_merge_action')


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
    <https://docs.djangoproject.com/en/1.11/ref/contrib/contenttypes/#django.contrib.contenttypes.fields.GenericRelation>`_
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
