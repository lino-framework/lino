# Copyright 2009-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""
This defines the :class:`Table` class.
"""
from __future__ import print_function
from builtins import str
# import six
# str = six.text_type

from past.builtins import basestring

import logging
logger = logging.getLogger(__name__)

import datetime

from django.conf import settings
from django.db.models.fields import NOT_PROVIDED
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.db.models.query import QuerySet

from django.apps import apps
get_models = apps.get_models

from lino.core import fields
from lino.core import actions
from lino.core.model import Model
from lino.core import actors
from lino.core import frames

from lino.core.choicelists import ChoiceListField


from lino.core.utils import resolve_model, get_field, UnresolvedModel
from lino.core.tables import AbstractTable, TableRequest, VirtualTable
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
    <http://docs.djangoproject.com/en/1.2/ref/models/querysets/#field-lookups>`_
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
        field = get_field(qs.model, flt['field'])
        flttype = flt['type']
        kw = {}
        if flttype == 'string':
            if isinstance(field, models.CharField):
                kw[field.name + "__icontains"] = flt['value']
                q = q & models.Q(**kw)
            elif isinstance(field, models.ForeignKey):
                qf = field.rel.model.quick_search_filter(
                    flt['value'], prefix=field.name + "__")
                # logger.info("20160610 %s %s", field.rel.model, qf)
                q = q & qf
                # rq = models.Q()
                # search_field = field.rel.model.grid_search_field
                # for search_field in field.rel.model.quick_search_fields:
                # search_field = getattr(field.rel.model,'grid_search_field',None)
                # if search_field is not None:
                    # rq = rq | models.Q(**{field.name+"__%s__icontains" % search_field : flt['value']})
                # q = q & rq
            else:
                raise NotImplementedError(repr(flt))
        elif flttype == 'numeric':
            cmp = str(flt['comparison'])
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
            cmp = str(flt['comparison'])
            if cmp == 'eq':
                cmp = 'exact'
            kw[field.name + "__" + cmp] = v
            q = q & models.Q(**kw)
            # print kw
        else:
            raise NotImplementedError(repr(flt))
    return qs.filter(q)


def rc_name(rptclass):
    return rptclass.app_label + '.' + rptclass.__name__

# def de_verbose_name(de):
    # if isinstance(de,models.Field):
        # return de.verbose_name
    # return de.name


# TODO : move these global variables to a better place
master_reports = []
slave_reports = []
generic_slaves = {}
frames_list = []
custom_tables = []
# rptname_choices = []

# config_dirs = []


def register_frame(frm):
    frames_list.append(frm)


def is_candidate(T):
    if T.filter or T.exclude or T.known_values:
        return False
    if not T.use_as_default_table:
        return False
    return True


def register_report(rpt):
    # logger.debug("20120103 register_report %s", rpt.actor_id)

    if issubclass(rpt, Table) and rpt.model is None:
        # logger.debug("20111113 %s is an abstract report", rpt)
        return

    # for name,v in rpt.__dict__.items():
    # for name in rpt.__class__.__dict__.keys():
    # for name in dir(rpt):
        # v = getattr(rpt,name)
        # if isinstance(v,Group):
            # v.name = name
            # v.add_to_table(rpt)
            # rpt.custom_groups = rpt.custom_groups + [v]
        # if isinstance(v,ComputedColumn):
            # v.name = name
            # v.add_to_table(rpt)
            # d = dict()
            # d.update(rpt.computed_columns)
            # d[name] = v
            # rpt.computed_columns = d

    # if rpt.model._meta.abstract:

    # rptname_choices.append((rpt.actor_id, rpt.get_label()))
    # rptname_choices.append(rpt.actor_id)
    
    if issubclass(rpt, Table):
        if rpt.master is None:
            if not rpt.model._meta.abstract:
                # logger.debug("20120102 register %s : master report", rpt.actor_id)
                master_reports.append(rpt)
            if not '_lino_default_table' in rpt.model.__dict__:
                if is_candidate(rpt):
                    rpt.model._lino_default_table = rpt
        elif rpt.master is ContentType:
            # logger.debug("register %s : generic slave for %r", rpt.actor_id, rpt.master_key)
            generic_slaves[rpt.actor_id] = rpt
        else:
            # logger.debug("20120102 register %s : slave for %r", rpt.actor_id, rpt.master_key)
            slave_reports.append(rpt)
    elif issubclass(rpt, VirtualTable):
        custom_tables.append(rpt)


def discover():
    """This is being called at startup.
    
    - Each model can receive a number of "slaves".
      Slaves are tables whose data depends on an instance
      of another model (their master).

    - For each model we want to find out the "default table".
      The "choices table" for a foreignkey field is also currently
      simply the pointed model's default table.
      :modattr:`_lino_default_table`

    """

    logger.debug("Analyzing Tables...")
    # logger.debug("20111113 Register Table actors...")
    for rpt in actors.actors_list:
        if issubclass(rpt, Table) and rpt is not Table:
            register_report(rpt)
        elif issubclass(rpt, VirtualTable) and rpt is not VirtualTable:
            register_report(rpt)
        if issubclass(rpt, frames.Frame) and rpt is not frames.Frame:
            register_frame(rpt)

    logger.debug("Instantiate model tables...")
    for model in get_models():

        # Not getattr but __dict__.get because of the mixins.Listings
        # trick.
        rpt = model.__dict__.get('_lino_default_table', None)
        # rpt = getattr(model,'_lino_default_table',None)
        # logger.debug('20111113 %s._lino_default_table = %s',model,rpt)
        if rpt is None:
            rpt = table_factory(model)
            if rpt is None:
                raise Exception("table_factory() failed for %r." % model)
            register_report(rpt)
            rpt.class_init()
            # rpt.collect_actions()
            model._lino_default_table = rpt

    logger.debug("Analyze %d slave tables...", len(slave_reports))
    for rpt in slave_reports:
        if isinstance(rpt.master, basestring):
            raise Exception("20150216 unresolved master")
        if isinstance(rpt.master, UnresolvedModel):
            continue
        if not isinstance(rpt.master, type):
            raise Exception(
                "20160712 invalid master {!r} in {}".format(
                    rpt.master, rpt))
            
        if issubclass(rpt.master, models.Model):
            # rpt.master = resolve_model(rpt.master)
            slaves = getattr(rpt.master, "_lino_slaves", None)
            if slaves is None:
                slaves = {}
                rpt.master._lino_slaves = slaves
            slaves[rpt.actor_id] = rpt
        # logger.debug("20111113 %s: slave for %s",rpt.actor_id, rpt.master.__name__)
    # logger.debug("Assigned %d slave reports to their master.",len(slave_reports))

    # logger.debug("reports.setup() done")


def has_fk(rr, name):
    if isinstance(rr, TableRequest):
        return rr.actor.master_key == name
    return False


# def model2report(m):
def model2actor(m):
    def f(table, *args):
        return m(*args)
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
    
    model = None
    """The model on which this table iterates.

    """

    debug_sql = False

    show_detail_navigator = True

    screenshot_profiles = ['admin']
    """
    The user profile(s) for which we want a screenshot of this table.
    """

    use_as_default_table = True
    """ Set this to `False` if this Table should *not* become the
    Model's default table.

    """

    expand_memos = False
    """(No longer used; see :srcref:`docs/tickets/44`).  Whether multi-line text
    fields in Grid views should be expanded in by default or not.

    """

    handle_uploaded_files = None
    """
    Handler for uploaded files.
    Same remarks as for :attr:`lino.core.actors.Actor.disabled_fields`.
    """

    @classmethod
    def add_quick_search_filter(cls, qs, search_text):
        """Add a filter to the given queryset `qs` in order to apply a quick
        search for the given `search_text`.

        """
        return qs.filter(qs.model.quick_search_filter(search_text))

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
            if u.profile and u.profile.name in self.screenshot_profiles and not u.profile in profiles2user:
                profiles2user[u.profile] = u
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

        """
        try:
            return self.model.objects.get(pk=pk)
        except ValueError:
            return None
        except self.model.DoesNotExist:
            return None

    @classmethod
    def disabled_actions(self, ar, obj):
        d = dict()
        if obj is not None:
            state = self.get_row_state(obj)
            # u = ar.get_user()
            for ba in self.get_actions(ar.bound_action.action):
                if ba.action.action_name:
                    if ba.action.show_in_bbar and not self.get_row_permission(obj, ar, state, ba):
                    # if ba.action.show_in_bbar and not obj.get_row_permission(u,state,ba.action):
                    # if a.show_in_bbar and not a.get_action_permission(ar.get_user(),obj,state):
                        d[ba.action.action_name] = True
                # if ba.action.action_name == 'do_clear_cache':
                    # logger.info("20121127 %s %s", obj, d)
            # if obj.__class__.__name__ == 'Note':
                # logger.info("20120920 %s %s %r", obj, d,obj.__class__.get_row_permission)
        return d

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
            self.model = resolve_model(self.model, self.app_label)

        if isinstance(self.model, UnresolvedModel):
            self.model = None

        if self.model is not None:
            if isinstance(self.hidden_columns, basestring):
                self.hidden_columns = frozenset(
                    fields.fields_list(self.model, self.hidden_columns))
            self.hidden_columns |= self.model.hidden_columns

            if isinstance(self.active_fields, basestring):
                self.active_fields = frozenset(
                    fields.fields_list(self.model, self.active_fields))
            self.active_fields |= self.model.active_fields
            self.hidden_elements |= self.model.hidden_elements

            # self.simple_parameters |= self.model.simple_parameters

            for b in self.model.mro():
                for k, v in list(b.__dict__.items()):
                    if isinstance(v, actions.Action):
                        existing_value = self.__dict__.get(k, NOT_PROVIDED)
                        if existing_value is NOT_PROVIDED:
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
                    fk = self.model._meta.get_field(self.master_key)
                    # x = self.model._meta.get_field_by_name(self.master_key)
                    # fk, remote, direct, m2m = x
                    # assert direct
                    # assert not m2m
                    if fk.rel is not None:
                        master_model = fk.rel.model
                    elif isinstance(fk, ChoiceListField):
                        master_model = fk.choicelist.item_class
                    elif isinstance(fk, GenericForeignKey):
                        master_model = ContentType
                    else:
                        raise Exception(
                            "Unsupported master_key {0} ({1})".format(
                                fk, fk.__class__))
                except models.FieldDoesNotExist:
                    for vf in self.model._meta.virtual_fields:
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
                             self.model._meta.virtual_fields])
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

        m = getattr(self.model, 'setup_table', None)
        if m is not None:
            m(self)

    @classmethod
    def is_abstract(self):
        if self.model is None \
            or self.model is Model \
                or self.model._meta.abstract:
            # logger.info('20120621 %s : no real table',h)
            return True
        return self.abstract

    @classmethod
    def disabled_fields(cls, obj, ar):
        return obj.disabled_fields(ar)

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
    def get_data_elem(self, name):
        """
        Adds the possibility to specify
        :class:`remote fields <lino.core.fields.RemoteField>`
        in a layout template.
        """
        # cc = AbstractTable.get_data_elem(self,name)

        if self.model is not None:
            if not isinstance(self.model, type) or not issubclass(
                    self.model, models.Model):
                raise Exception(
                    "%s.model is %r (and not a Model subclass)" %
                    (self, self.model))

            # logger.info("20120202 Table.get_data_elem found nothing")
            de = self.model.get_data_elem(name)
            if de is not None:
                return de
        return super(Table, self).get_data_elem(name)

    @classmethod
    def get_request_queryset(self, rr):
        """Build a Queryset for the specified ActionRequest on this table.

        Upon first call, this will also lazily install Table.queryset
        which will be reused on every subsequent call.

        The return value is othe of the following:

        - a Django queryset
        - a list or tuple

        - If you override this, you may turn this method into a
          generator. The only advantage of this is syntax, since the
          yeld objects will be stored in a tuple.

        """
        # print("20160329 dbtables.py get_request_queryset({})".format(
        #     rr.param_values))
        qs = self.get_queryset(rr)
        # print("20160329 {}".format(qs.query))
        if qs is None:
            return self.model.objects.none()
        kw = self.get_filter_kw(rr)
        if kw is None:
            return self.model.objects.none()
        if len(kw):
            qs = qs.filter(**kw)

        if rr.exclude:
            qs = qs.exclude(**rr.exclude)
            # qs = qs.exclude(rr.exclude)

        for k in self.simple_parameters:
            v = getattr(rr.param_values, k)
            if v:
                qs = qs.filter(**{k: v})

        if self.filter:
            qs = qs.filter(self.filter)

        if rr.filter:
            qs = qs.filter(rr.filter)

        if rr.known_values:
            # logger.info("20120111 known values %r",rr.known_values)
            d = {}
            for k, v in list(rr.known_values.items()):
                if v is None:
                    d[k + "__isnull"] = True
                else:
                    # d[k+"__exact"] = v
                    d[k] = v
                qs = qs.filter(**d)

        if self.exclude:
            qs = qs.exclude(**self.exclude)
            # TODO: use Q object instead of dict

        if rr.quick_search:
            qs = self.add_quick_search_filter(qs, rr.quick_search)
        if rr.gridfilters is not None:
            qs = add_gridfilters(qs, rr.gridfilters)
        extra = rr.extra or self.extra
        if extra is not None:
            qs = qs.extra(**extra)
        order_by = rr.order_by or self.order_by
        if order_by:
            # logger.info("20120122 order_by %s",order_by)
            qs = qs.order_by(*order_by)
        if self.debug_sql:
            logger.info("%s %s", self.debug_sql, qs.query)
        return qs

    @classmethod
    def get_queryset(self, ar):
        """
        Return an iterable over the items processed by this table.
        Override this to use e.g. select_related() or to return a list.

        Return a customized default queryset
    
        Example::

          def get_queryset(self):
              return self.model.objects.select_related('country', 'city')


        """
        return self.model.get_request_queryset(ar)

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

