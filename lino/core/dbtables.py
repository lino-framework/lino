# Copyright 2009-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
This defines the :class:`Table` class.
"""

import logging ; logger = logging.getLogger(__name__)

import datetime

from django.conf import settings
from django.db.models.fields import NOT_PROVIDED
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.db.models.query import QuerySet

from django.apps import apps ; get_models = apps.get_models

from lino.core import fields
from lino.core import actions
from lino.core.model import Model
from lino.core import actors
from lino.core import constants

from lino.core.choicelists import ChoiceListField
from .utils import models_by_base
# from .fields import get_data_elem_from_model


from lino.core.utils import resolve_model, get_field, UnresolvedModel
from lino.core.tables import AbstractTable, TableRequest
from lino.core.gfks import ContentType, GenericForeignKey


INVALID_MK = "Invalid master_key '{0}' in {1} : {2}"


def base_attrs(cl):
    # if cl is Table or len(cl.__bases__) == 0:
        # return
    # myattrs = set(cl.__dict__.keys())
    for b in cl.__bases__:
        for k in base_attrs(b):
            yield k
        for k in list(b.__dict__.keys()):
            yield k


def add_gridfilters(qs, gridfilters):
    """Converts a `filter` request in the format used by
    :extux:`Ext.ux.grid.GridFilters` into a `Django field lookup
    <https://docs.djangoproject.com/en/1.11/ref/models/querysets/#field-lookups>`_
    on a :class:`django.db.models.query.QuerySet`.

    :param qs: the queryset to be modified.
    :param gridfilters: a list of dictionaries, each having 3 keys
                        `field`, `type` and `value`.

    """
    if not isinstance(qs, QuerySet):
        raise NotImplementedError('TODO: filter also simple lists')
    q = models.Q()
    # logger.info("20160610 %s", gridfilters)
    # raise Exception("20160610 %s" % gridfilters)
    for flt in gridfilters:
        field = get_field(qs.model, flt.get('field', None) or flt.get("property"))
        flttype = flt['type']
        kw = {}
        if flttype == 'string':
            if isinstance(field, models.CharField):
                kw[field.name + "__icontains"] = flt['value']
                q = q & models.Q(**kw)
            elif isinstance(field, models.ForeignKey):
                qf = field.remote_field.model.quick_search_filter(
                    flt['value'], prefix=field.name + "__")
                # logger.info("20160610 %s %s", field.remote_field.model, qf)
                q = q & qf
                # rq = models.Q()
                # search_field = field.remote_field.model.grid_search_field
                # for search_field in field.remote_field.model.quick_search_fields:
                # search_field = getattr(field.rel.model,'grid_search_field',None)
                # if search_field is not None:
                    # rq = rq | models.Q(**{field.name+"__%s__icontains" % search_field : flt['value']})
                # q = q & rq
            else:
                raise NotImplementedError(repr(flt))
        elif flttype == 'numeric':
            cmp = str(flt.get('comparison', None) or flt.get('operator', None))
            if cmp == 'eq':
                cmp = 'exact'
            kw[field.name + "__" + cmp] = flt['value']
            q = q & models.Q(**kw)
        elif flttype == 'boolean':
            kw[field.name] = flt['value']
            # kw[field.name + "__equals"] = flt['value']
            q = q & models.Q(**kw)
        elif flttype == 'date':
            v = datetime.date(*settings.SITE.parse_date(flt['value']))
            # v = parse_js_date(flt['value'],field.name)
            cmp = str(flt.get('comparison', None) or flt.get('operator', None))
            if cmp == 'eq':
                cmp = 'exact'
            kw[field.name + "__" + cmp] = v
            q = q & models.Q(**kw)
            # print kw
        elif flttype == 'list':
            if isinstance(field, ChoiceListField):
                choices = []
                for x in field.choices:
                    if x[1] in flt['value']:
                        choices.append(x[0])
                kw[field.name + "__in"] = choices
                q = q & models.Q(**kw)
            else:
                raise NotImplementedError(repr(flt))
        else:
            raise NotImplementedError(repr(flt))
    return qs.filter(q)


def rc_name(rptclass):
    return rptclass.app_label + '.' + rptclass.__name__



def has_fk(rr, name):
    if isinstance(rr, TableRequest):
        return rr.actor.master_key == name
    return False


def model2actor(m):
    def f(table, *args, **kwargs):
        return m(*args, **kwargs)
    return classmethod(f)


class Table(AbstractTable):
    """An :class:`AbstractTable <lino.core.tables.AbstractTable>` that works
    on a Django Model using a QuerySet.

    A Table inherits from :class:`AbstractTable
    <lino.core.tables.AbstractTable>` and adds attributes like
    :attr:`model` and :attr:`master` and :attr:`master_key` who are
    important because Lino handles relations automagically.

    Another class of attributes are `filter`, `exclude` and `sort_order`
    which are thin wrappers to Django's query lookup parameters of same
    name.

    See :class:`dd.Table`.

    """

    abstract = True

    model = None
    """See :attr:`lino.core.actors.Actor.model`

    """

    debug_sql = False

    show_detail_navigator = True

    screenshot_profiles = ['admin']
    """
    The user user_type(s) for which we want a screenshot of this table.
    """

    use_as_default_table = True
    """ Set this to `False` if this Table should *not* become the
    Model's default table.

    """

    expand_memos = False
    """(No longer used; see :srcref:`docs/tickets/44`).  Whether multi-line text
    fields in Grid views should be expanded in by default or not.

    """

    use_detail_params_value = False
    """If when in a detail view will override default param values with the detail's pv values.
    """

    react_responsive = True
    """If viewing the grid view on a mobile, should the grid use responsive mode
    Default: True"""

    react_big_search = False
    """If True will position the quick search input to the bottom of the header and have it full width.
    Default: False"""

    @classmethod
    def add_quick_search_filter(cls, qs, search_text):
        """Add a filter to the given queryset `qs` in order to apply a quick
        search for the given `search_text`.

        """
        flt = qs.model.quick_search_filter(search_text)
        if len(flt) == 0:
            return qs.model.objects.none()
        return qs.filter(flt)

    @classmethod
    def get_chooser_for_field(self, fieldname):
        ch = super(Table, self).get_chooser_for_field(fieldname)
        if ch is not None:
            return ch
        if self.model is not None:
            return self.model.get_chooser_for_field(fieldname)

    @classmethod
    def request(self, master_instance=None, **kw):  # 20130327
        kw.update(actor=self)
        if master_instance is not None:
            kw.update(master_instance=master_instance)
        kw.setdefault('action', self.default_action)
        return TableRequest(**kw)

    @classmethod
    def column_choices(self):
        return [de.name for de in self.wildcard_data_elems()]

    @classmethod
    def get_screenshot_requests(self, language):
        if self.model is None:
            return
        if self.model._meta.abstract:
            return
        if self is not self.model._lino_default_table:
            return

        profiles2user = dict()
        for u in settings.SITE.user_model.objects.filter(language=language):
            if u.user_type and u.user_type.name in self.screenshot_profiles and not u.user_type in profiles2user:
                profiles2user[u.user_type] = u
        for user in list(profiles2user.values()):
            # if user.profile.name != 'admin': return
            # yield self.default_action.request(user=user)
            # and self.default_action is not self.detail_action:
            if self.detail_action:
                yield self.detail_action.request(user=user)

    # @classmethod
    # def elem_filename_root(cls,elem):
        # return elem._meta.app_label + '.' + elem.__class__.__name__ + '-' + str(elem.pk)
    @classmethod
    def get_detail_sets(self):
        """
        Yield a list of (app_label,name) tuples for which the kernel
        should try to create a Detail Set.
        """
        if self.model is not None:
            def yield_model_detail_sets(m):
                for b in m.__bases__:
                    if issubclass(b, models.Model) and b is not models.Model:
                        for ds in yield_model_detail_sets(b):
                            yield ds
                yield m._meta.app_label + '/' + m.__name__

            for ds in yield_model_detail_sets(self.model):
                yield ds

        for s in super(Table, self).get_detail_sets():
            yield s

    # @classmethod
    # def find_field(cls,model,name):
        # for vf in cls.model._meta.virtual_fields:
            # if vf.name == name:
                # return vf
        # return cls.model._meta.get_field(name)

    @classmethod
    def get_actions_hotkeys(cls):
        return cls.model.get_actions_hotkeys()

    @classmethod
    def get_widget_options(cls, name, **options):
        return cls.model.get_widget_options(name, **options)

    @classmethod
    def get_pk_field(self):
        return self.model._meta.pk

    @classmethod
    def get_row_by_pk(self, ar, pk):
        """Implements :meth:`get_row_by_pk
        <lino.core.actors.Actor.get_row_by_pk>` for a database
        table.

        Note: `ar` may not be None.

        """
        try:
            return self.model.get_user_queryset(ar.get_user()).get(pk=pk)
        except ValueError:
            return None
        except self.model.DoesNotExist:
            return None

    # @classmethod
    # def disabled_actions(self, ar, obj):  # no longer used since 20170909
    #     d = dict()
    #     if obj is not None:
    #         state = self.get_row_state(obj)
    #         # u = ar.get_user()
    #         for ba in self.get_actions(ar.bound_action.action):
    #             if ba.action.action_name:
    #                 if ba.action.show_in_bbar and not self.get_row_permission(obj, ar, state, ba):
    #                 # if ba.action.show_in_bbar and not obj.get_row_permission(u,state,ba.action):
    #                 # if a.show_in_bbar and not a.get_action_permission(ar.get_user(),obj,state):
    #                     d[ba.action.action_name] = True
    #             # if ba.action.action_name == 'do_clear_cache':
    #                 # logger.info("20121127 %s %s", obj, d)
    #         # if obj.__class__.__name__ == 'Note':
    #             # logger.info("20120920 %s %s %r", obj, d,obj.__class__.get_row_permission)
    #     return d

    @classmethod
    def wildcard_data_elems(self):
        return fields.wildcard_data_elems(self.model)

    @classmethod
    def is_valid_row(self, row):
        return isinstance(row, self.model)

    @classmethod
    def get_actor_label(self):
        if self.model is None:
            # return self._label or self.__name__
            return super(Table, self).get_actor_label()
        return self._label or self.model._meta.verbose_name_plural

    @classmethod
    def class_init(self):

        if self.model is not None:
            model = resolve_model(self.model, self.app_label)
            if isinstance(model, UnresolvedModel):
                # if settings.SITE.is_installed(self.app_label):
                raise Exception(
                    "Invalid model {} on table {}".format(
                        self.model, self))
            self.model = model

        if isinstance(self.model, UnresolvedModel):
            self.model = None

        if self.model is not None:
            if isinstance(self.hidden_columns, str):
                self.hidden_columns = frozenset(
                    fields.fields_list(self.model, self.hidden_columns))
            self.hidden_columns |= self.model.hidden_columns

            if isinstance(self.active_fields, str):
                self.active_fields = frozenset(
                    fields.fields_list(self.model, self.active_fields))
            self.active_fields |= self.model.active_fields
            self.hidden_elements |= self.model.hidden_elements

            # self.simple_parameters |= self.model.simple_parameters

            for b in self.model.mro():
                for k, v in b.__dict__.items():
                    if isinstance(v, actions.Action):
                        existing_value = self.__dict__.get(k, NOT_PROVIDED)
                        if existing_value is NOT_PROVIDED:
                            # settings.SITE.install_help_text(
                            #     v, v.__class__)
                            setattr(self, k, v)
                        else:
                            if existing_value is None:  # 20130820
                                pass
                                # logger.info("%s disables model action '%s'",self,k)
                            else:
                                if not isinstance(
                                        existing_value, actions.Action):
                                    raise Exception(
                                        "%s cannot install model action %s "
                                        "because name is already used "
                                        "for %r" % self, k, existing_value)

            for name in ('workflow_state_field', 'workflow_owner_field'):
                if getattr(self, name) is None:
                    setattr(self, name, getattr(self.model, name))

            for name in (  # 'disabled_fields',
                'handle_uploaded_files',
                # 'get_row_permission',
                # 'disable_editing',
            ):
                if getattr(self, name) is None:
                    m = getattr(self.model, name, None)
                    if m is not None:
                        # logger.debug('20120731 Install model method %s from %r to %r',name,self.model,self)
                        setattr(self, name, model2actor(m))
                        # 'dictproxy' object does not support item assignment:
                        # self.__dict__[name] = model2actor(m)

            if self.master_key:

                master_model = None
                try:
                    fk = self.model.get_data_elem(self.master_key)
                    # fk = self.model._meta.get_field(self.master_key)
                    # fk, remote, direct, m2m = x
                    # assert direct
                    # assert not m2m
                    if fk is None:
                        raise Exception(
                            "Invalid master_key {} on {}".format(
                                self.master_key, self))
                    if fk.remote_field:
                        master_model = fk.remote_field.model
                    elif isinstance(fk, ChoiceListField):
                        master_model = fk.choicelist.item_class
                    elif isinstance(fk, GenericForeignKey):
                        master_model = ContentType
                    elif isinstance(fk, fields.DummyField):
                        pass
                    else:
                        raise Exception(
                            "Unsupported master_key {0}.{1} ({2})".format(
                                self, fk, fk.__class__))
                except models.FieldDoesNotExist:
                    for vf in self.model._meta.private_fields:
                        if vf.name == self.master_key:
                            fk = vf
                            master_model = ContentType
                            break
                if master_model is None:
                    df = getattr(self.model, self.master_key, None)
                    if df is None:
                        msg = "No field '{0}' in {1}".format(
                            self.master_key, self.model)
                        raise Exception(INVALID_MK.format(
                            self.master_key, self, msg))
                    elif isinstance(df, fields.DummyField):
                        self.abstract = True
                    else:
                        msg = "Cannot handle master key {0}".format(df)
                        msg += " (20150820 virtual fields: {0})".format(
                            [vf.name for vf in
                             self.model._meta.private_fields])
                        raise Exception(INVALID_MK.format(
                            self.master_key, self, msg))
                        # raise Exception(
                        #     "%s : invalid master class for master_key "
                        #     "%r in %s" % (
                        #         self, self.master_key, self.model))
                else:
                    self.master = master_model
                    self.master_field = fk
                    # self.hidden_columns |= set([fk.name])

        super(Table, self).class_init()

        if self.order_by is not None:
            if not isinstance(self.order_by, (list, tuple)):
                raise Exception("%s.order_by is %r (must be a list or tuple)" %
                                (self, self.order_by))
            if False:
                # good idea, but doesn't yet work for foreign fields,
                # e.g. order_by = ['content_type__app_label']
                for fieldname in self.order_by:
                    if fieldname.startswith('-'):
                        fieldname = fieldname[1:]
                    try:
                        fk, remote, direct, m2m = self.model._meta.get_field_by_name(
                            fieldname)
                        assert direct
                        assert not m2m
                    except models.FieldDoesNotExist:
                        raise Exception("Unknown fieldname %r in %s.order_by" %
                                        (fieldname, self))

    @classmethod
    def do_setup(self):

        super(Table, self).do_setup()
        # AbstractTable.do_setup(self)
        if self.model is None:
            return

        if hasattr(self.model, '_lino_slaves'):
            self._slaves = list(self.model._lino_slaves.values())
        else:
            self._slaves = []

    @classmethod
    def is_abstract(self):
        if self.model is None or self.model is Model:
            # or self.model._meta.abstract:
            # logger.info('20120621 %s : no real table',h)
            return True
        return self.abstract

    @classmethod
    def make_disabled_fields(cls, obj, ar):
        s = super(Table, cls).make_disabled_fields(obj, ar)

        if obj is not None and ar is not None:
            s |= obj.disabled_fields(ar)
            if settings.SITE.user_types_module is None:
                return s
            state = cls.get_row_state(obj)
            parent = ar.bound_action.action
            if not parent.opens_a_window:
                return s
            for ba in cls.get_button_actions(parent):
                a = ba.action
                if a.action_name and a.show_in_bbar:
                    if not cls.get_row_permission(obj, ar, state, ba):
                        s.add(a.action_name)
        return s

    @classmethod
    def get_row_permission(cls, obj, ar, state, ba):
        """Returns True if the given action is allowed for the given instance
        `obj` and the given user.

        """
        if obj is None:
            return True
        return obj.get_row_permission(ar, state, ba)

    @classmethod
    def disable_delete(self, obj, ar):
        """
        Return either `None` if the given `obj` *is allowed*
        to be deleted by action request `ar`,
        or a string with a message explaining why, if not.
        """
        # logger.info("20130225 dbtables.disable_delete")
        if self.delete_action is None:
            return "No delete_action"
        if not self.get_row_permission(obj, ar, self.get_row_state(obj), self.delete_action):
            # print "20130222 ar is %r" % ar
            # logger.info("20130225 dbtables.disable_delete no permission")
            return _("You have no permission to delete this row.")
        return obj.disable_delete(ar)

    @classmethod
    def get_layout_aliases(cls):
        return cls.model.get_layout_aliases()

    # @classmethod
    # def get_data_elem(self, name):
    #     """
    #     Adds the possibility to specify
    #     :class:`remote fields <lino.core.fields.RemoteField>`
    #     in a layout template.
    #     """
    #     # cc = AbstractTable.get_data_elem(self,name)
    #
    #     # if self.model is not None:
    #     if isinstance(self.model, type) and issubclass(self.model, models.Model):
    #         # logger.info("20120202 Table.get_data_elem found nothing")
    #         for m in models_by_base(self.model):
    #             de = m.get_data_elem(name)
    #             if de is not None:
    #                 return de
    #     return super(Table, self).get_data_elem(name)
    #
    @classmethod
    def get_request_queryset(self, ar, **filter):
        """
        Return the iterable of Django database objects for the specified
        action request.

        The default implementation calls :meth:`get_user_queryset` and then
        applies request parameters.
        """
        # print("20181121b get_request_queryset", self)

        def apply(qs):

            # print("20160329 {}".format(qs.query))
            if qs is None:
                return self.model.objects.none()
            kw = self.get_filter_kw(ar)
            if kw is None:
                return self.model.objects.none()
            if len(kw):
                qs = qs.filter(**kw)

            if ar.exclude:
                qs = qs.exclude(**ar.exclude)
                # qs = qs.exclude(ar.exclude)

            # 20200425
            spv = dict()
            for k in self.simple_parameters:
                v = getattr(ar.param_values, k)
                # if "room" in k:
                # print("20200423", k, v, self.simple_parameters, ar.param_values)
                if v == constants.CHOICES_BLANK_FILTER_VALUE:
                    spv[k+"__isnull"] = True
                elif v == constants.CHOICES_NOT_BLANK_FILTER_VALUE:
                    spv[k+"__isnull"] = False
                elif v is not None:
                    spv[k] = v

            qs = self.model.add_param_filter(qs, **spv)
            # qs = self.model.add_param_filter(qs, **ar.param_values)

            if self.filter:
                qs = qs.filter(self.filter)

            if ar.filter:
                qs = qs.filter(ar.filter)

            if ar.known_values:
                # logger.info("20120111 known values %r", ar.known_values)
                d = {}
                for k, v in list(ar.known_values.items()):
                    if v is None:
                        d[k + "__isnull"] = True
                    else:
                        # d[k+"__exact"] = v
                        d[k] = v
                    qs = qs.filter(**d)

            if self.exclude:
                qs = qs.exclude(**self.exclude)
                # TODO: use Q object instead of dict

            if ar.quick_search:
                qs = self.add_quick_search_filter(qs, ar.quick_search)
            if ar.gridfilters is not None:
                qs = add_gridfilters(qs, ar.gridfilters)
            extra = ar.extra or self.extra
            if extra is not None:
                qs = qs.extra(**extra)
            order_by = ar.order_by or self.order_by
            if order_by:
                # logger.info("20120122 order_by %s",order_by)
                qs = qs.order_by(*order_by)
            if self.debug_sql:
                logger.info("%s %s", self.debug_sql, qs.query)
            return qs

        if self.model._meta.abstract:
            # Django's UNION feature is a pseudo feature because
            # count() doesn't work and because it doesn't work on
            # mysql (Django ticket #28281).  So here we emulate a
            # union and return an iteration over the different models
            # which implement the abstract model. One limitation is of
            # course that they are ordered only within their model.
            # There is no known in production usage of this feature.
            def func():
                for m in models_by_base(self.model):
                    qs = m.get_request_queryset(ar, **filter)
                    qs = apply(qs)
                    for obj in qs:
                        yield obj
            return func()
        assert not filter
        qs = self.get_queryset(ar)
        return apply(qs)

    @classmethod
    def get_queryset(self, ar, **filter):
        """Return the Django Queryset processed by this table.

        The default implementation forwards the call to the model's
        :meth:`get_request_queryset
        <lino.core.model.Model.get_request_queryset>`.

        Override this to use e.g. select_related() or to return a list.

        Example::

          def get_queryset(self, **ar):
              return self.model.objects.select_related('country', 'city')

        """
        assert not self.model._meta.abstract
        # if self.model._meta.abstract:
        #     lst = list(models_by_base(self.model))
        #     qs = lst[0].get_request_queryset(ar, **filter)
        #     if len(lst) > 1:
        #         flds = self.get_handle().store.list_fields
        #         flds = set([
        #             f.name for f in flds
        #             if isinstance(f.field, models.Field)])
        #         flds |= self.hidden_elements
        #         # flds = self.column_names.split()
        #         qs = qs.only(*flds)
        #         for m in lst[1:]:
        #             qs = qs.union(m.get_request_queryset(ar, **filter).only(*flds))
        #         # raise Exception("20170905 {} {}".format(flds, qs.query))
        #     return qs
        return self.model.get_request_queryset(ar, **filter)

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Table, self).get_title_tags(ar):
            yield t
        for t in self.model.get_title_tags(ar):
            yield t

    @classmethod
    def create_instance(self, ar, **kw):
        """
        Create a model instance using the specified keyword args,
        calling also :meth:`lino.core.model.Model.on_create`.
        """
        # print 20120630, "Actor.create_instance", kw
        instance = self.model(**kw)
        instance.on_create(ar)
        return instance

    @classmethod
    def after_create_instance(cls, obj, ar):
        """

        A hook for code to be executed when a new instance has been created in
        this table.

        This is for actor-specific behaviour.  You can do the equivalent for
        every table on a model by defining an :meth:`after_ui_create
        <lino.core.model.Model.after_ui_create>` method on the model.

        Usage example: :class:`lino_xl.lib.cal.GuestsByPartner`.

        """
        pass

    # @classmethod
    # def ajax_update(self,request):
        # print request.POST
        # return HttpResponse("1", mimetype='text/x-json')


def table_factory(model):
    """
    Automatically define a Table class for the specified model.
    This is used during kernel setup to create default tables for
    models who have no Table.
    """
    # logger.info('table_factory(%s)',model.__name__)
    bases = (Table,)
    for b in model.__bases__:
        rpt = getattr(b, '_lino_default_table', None)
        if rpt is not None:
            if issubclass(model, rpt.model):
            # if issubclass(rpt.model,model):
                bases = (rpt,)
                # bases = (rpt.__class__,)
    # logger.info('table_factory(%s) : bases is %s',model.__name__,bases)
    app_label = model._meta.app_label
    name = model.__name__ + "Table"
    cls = type(name, bases, dict(model=model, app_label=app_label))
    return actors.register_actor(cls)


def column_choices(rptname):
    rpt = actors.get_actor(rptname)
    return rpt.column_choices()
