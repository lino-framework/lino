# -*- coding: UTF-8 -*-
# Copyright 2009-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Defines the classes :class:`AbstractTable` and
:class:`VirtualTable`.

"""
import logging ; logger = logging.getLogger(__name__)

import os
import yaml

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from lino.core import actors
from lino.core import actions
from lino.core import fields
from lino.core.utils import resolve_fields_list
from lino.core.tablerequest import TableRequest


class InvalidRequest(Exception):
    pass


if False:  # 20130710

    from lino.utils.config import Configured

    class GridConfig(Configured):

        def __init__(self, report, data, *args, **kw):
            self.report = report
            self.data = data
            self.label_en = data.get('label')
            self.data.update(label=_(self.label_en))
            super(GridConfig, self).__init__(*args, **kw)
            must_save = self.validate()
            if must_save:
                msg = self.save_config()
                #~ msg = self.save_grid_config()
                logger.debug(msg)

        def validate(self):
            """
            Removes unknown columns
            """
            must_save = False
            gc = self.data
            columns = gc['columns']
            col_count = len(columns)
            widths = gc.get('widths', None)
            hiddens = gc.get('hiddens', None)
            if widths is None:
                widths = [None for x in columns]
                gc.update(widths=widths)
            elif col_count != len(widths):
                raise Exception("%d columns, but %d widths" %
                                (col_count, len(widths)))
            if hiddens is None:
                hiddens = [False for x in columns]
                gc.update(hiddens=hiddens)
            elif col_count != len(hiddens):
                raise Exception("%d columns, but %d hiddens" %
                                (col_count, len(hiddens)))

            valid_columns = []
            valid_widths = []
            valid_hiddens = []
            for i, colname in enumerate(gc['columns']):
                f = self.report.get_data_elem(colname)
                if f is None:
                    logger.debug(
                        "Removed unknown column %d (%r). Must save.",
                        i, colname)
                    must_save = True
                else:
                    valid_columns.append(colname)
                    valid_widths.append(widths[i])
                    valid_hiddens.append(hiddens[i])
            gc.update(widths=valid_widths)
            gc.update(hiddens=valid_hiddens)
            gc.update(columns=valid_columns)
            return must_save

        def unused_write_content(self, f):
            self.data.update(label=self.label_en)
            f.write(yaml.dump(self.data))
            self.data.update(label=_(self.label_en))

        def write_content(self, f):
            f.write(yaml.dump(self.data))


class TableHandle(object):
    """
    For every table we create one "handle" per renderer.

    See also :meth:`lino.core.actors.Actor.setup_handle` which is called during
    startup and sets more attributes.

    """

    _layouts = None

    def __init__(self, actor):
        self.actor = actor

    def __str__(self):
        return str(self.actor) + 'Handle'

    def setup_layouts(self):
        if self._layouts is not None:
            return
        self._layouts = [self.list_layout]

    def get_actor_url(self, *args, **kw):
        return settings.SITE.kernel.get_actor_url(self.actor, *args, **kw)

    def submit_elems(self):
        return []

    def get_list_layout(self):
        self.setup_layouts()
        return self._layouts[0]

    def get_columns(self):
        lh = self.get_list_layout()
        #~ print 20110315, layout._main.columns
        return lh.main.columns

    def get_slaves(self):
        return [sl.get_handle() for sl in self.actor._slaves]


class Group(object):

    def __init__(self):
        self.sums = []

    def process_row(self, collector, row):
        collector.append(row)

    #~ def add_to_table(self,table):
        #~ self.table = table
        #~ for col in table.computed_columns.values():


class AbstractTable(actors.Actor):
    """An AbstractTable is the definition of a tabular data view, usually
    displayed in a Grid (but it's up to the user interface to decide
    how to implement this).

    Base class for :class:`Table <lino.core.dbtables.Table>` and
    :class:`VirtualTable <lino.core.tables.VirtualTable>`.

    """

    abstract = True

    _handle_class = TableHandle

    hide_zero_rows = False
    """Set this to `True` if you want to remove rows which contain no
    values when rendering this table as plain HTML.  This is ignored
    when rendered as ExtJS.

    """

    column_names = '*'

    tablet_columns = None
    """
    The columns that must remain visible when this table is rendered
    on a tablet device.
    """

    mobile_columns = None
    """
    The columns that must remain visible when this table is rendered
    on a mobile device.
    """

    popin_columns = None
    """
    The columns that must pop in below the first column if there is no
    space to render them on the device.

    If None: All columns not listed in mobile_columns nor Tablet_columns
    will not pop-in.
    """

    # start_at_bottom = False
    # """Set this to `True` if you want your table to *start at the
    # bottom*.  Unlike reverse ordering, the rows remain in their
    # natural order, but when we open a grid on this table, we want it
    # to start on the last page.
    #
    # Use cases would be :class:`lino_xl.lib.sales.InvoicesByJournal` and
    # :class:`lino_xl.lib.ledger.InvoicesByJournal` but the result is not yet
    # satisfying.
    #
    # """

    group_by = None
    """
    A list of field names that define the groups of rows in this table.
    Each group can have her own header and/or total lines.
    """

    custom_groups = []
    """
    Used internally to store :class:`groups <Group>` defined by this Table.
    """

    master_field = None
    """
    For internal use. Automatically set to the field descriptor of the
    :attr:`master_key`.

    """

    get_data_rows = None
    """
    Maybe deprecated.  Use get_request_queryset() instead.

    Virtual tables *must* define this method, model-based tables *may* define
    it. e.g. in case they need local filtering.

    This will be called with a
    :class:`lino.core.requests.TableRequest` object and is expected to
    return or yield the list of "rows"::

        @classmethod
        def get_data_rows(self, ar):
            ...
            yield somerow

    """

    preview_limit = settings.SITE.preview_limit

    row_height = 1
    """
    Number of text rows per data row.

    """

    variable_row_height = False
    """
    Set this to `True` if you want each row to get the height that it
    needs.

    """

    auto_fit_column_widths = settings.SITE.auto_fit_column_widths
    """Set this to `True` if you want to have the column widths adjusted
    to always fill the available width.  This implies that there will
    be no horizontal scrollbar.

    """

    active_fields = frozenset()
    """
    A list of field names that are "active".
    Value and inheritance as for :attr:`hidden_columns`.

    When a field is "active", this means only that it will cause an
    immediate "background" save and refresh of the :term:`detail
    window` when their value was changed. The true "activity"
    (i.e. other fields being updated according to the value of an
    active field) is defined in the model's :meth:`full_clean
    <dd.Model.full_clean>` and :meth:`FOO_changed
    <dd.Model.FOO_changed>` methods.

    Note that active fields are active only in a :term:`detail
    window`, not in an :term:`insert window`.  That's because there
    they would lead to the unexpected behaviour of closing the window.

    """

    hidden_columns = frozenset()

    form_class = None
    help_url = None

    page_length = 20
    """Number of rows to display per page.  Used to control the height of
    a combobox of a ForeignKey pointing to this model

    """

    cell_edit = True
    """`True` (default) to use ExtJS CellSelectionModel, `False` to use
    RowSelectionModel.  When `True`, the users cannot select multiple
    rows.  When `False`, the users cannot edit individual cells using
    the :kbd:`F2` key..

    """

    show_detail_navigator = True
    """
    Whether a Detail view on a row of this table should have a navigator.
    """

    default_group = Group()

    default_layout = 0

    typo_check = True
    """
    True means that Lino shoud issue a warning if a subclass
    defines any attribute that did not exist in the base class.
    Usually such a warning means that there is something wrong.
    """

    display_mode = 'grid'

    max_render_depth = 2
    """
    Used to limit the rendering of slave card views.
    """

    hide_if_empty = False
    """
    In a detail view if a slave table is empty, it's element will be hidden
    """


    stay_in_grid = False
    """Set this to True if Lino should prefer grid mode and not open a
    detail window on a newly created record.  :class:`SubmitDetail
    <lino.core.actions.SubmitDetail>` closes the window when this is
    True.

    Usage example :class:`LanguageKnowledgesByPerson
    <lino_xl.lib.cv.models.LanguageKnowledgesByPerson>`.

    """

    no_phantom_row = False
    """Suppress a phantom row in situations where Lino would otherwise add
    one.

    Used for :class:`lino_xl.lib.ledger.ByJournal` where a phantom row
    is disturbing.

    TODO: Actually this option would not be necessary if the AJAX call
    sent by a grid panel would include an option which says whether it
    is main item or not.

    """

    order_by = None
    """If specified, this must be a tuple or list of field names which
will be passed to Django's `order_by
<https://docs.djangoproject.com/en/1.11/ref/models/querysets/#order-by>`__
method in order to sort the rows of the queryset.

    """

    filter = None
    """If specified, this must be a `models.Q` object (not a dict of
    (fieldname -> value) pairs) which will be passed to Django's
    `filter
    <https://docs.djangoproject.com/en/1.11/ref/models/querysets/#filter>`__
    method.

    Note that if you allow a user to insert rows into a filtered
    table, you should make sure that new records satisfy your filter
    condition, otherwise you can get surprising behaviour if the user
    creates a new row.

    If your filter consists of simple static values on some known
    field, then you might prefer to use
    :attr:`known_values  <lino.core.actors.Actor.known_values>`
    instead because this will add automatic behaviour.

    One advantage of :attr:`filter` over
    :attr:`known_values  <lino.core.actors.Actor.known_values>`
    is that this can use the full range of Django's `field lookup methods
    <https://docs.djangoproject.com/en/1.11/topics/db/queries/#field-lookups>`_

    """

    exclude = None
    """If specified, this must be dict which will be passed to Django's
    `exclude
    <https://docs.djangoproject.com/en/1.11/ref/models/querysets/#exclude>`__
    method on the queryset.

    """

    extra = None
    """
    Examples::

      extra = dict(select=dict(lower_name='lower(name)'))
      # (or if you prefer:)
      # extra = {'select':{'lower_name':'lower(name)'},'order_by'=['lower_name']}

    List of SQL functions and which RDBMS supports them:
    http://en.wikibooks.org/wiki/SQL_Dialects_Reference/Functions_and_expressions/String_functions

    """

    hide_sums = False
    """
    Set this to True if you don't want Lino to display sums in a table
    view.
    """

    use_paging = False
    """
    Set this to True in Extjs6 to not use a Buffered Store, and use a JsonStore with paging instead.
    """

    drag_drop_sequenced_field = None
    """
    Extjs6 only
    Enables drag and drop reordering for a table.
    Set to the field name that is used to track the order.
    Only used in lino.mixins.sequenced.Sequenced. Field name seqno
    """

    focus_on_quick_search = False
    """
    If True , when the grid opens, the initial keyboard focus will be in the quick search field.
    """

    @classmethod
    def class_init(cls):
        super(AbstractTable, cls).class_init()
        resolve_fields_list(cls, 'tablet_columns', set, {})
        resolve_fields_list(cls, 'mobile_columns', set, {})
        resolve_fields_list(cls, 'popin_columns', set, {})
        if cls.model is not None:
            if not issubclass(cls.model, models.Model):
                if cls.model._lino_default_table is None:
                    cls.model._lino_default_table = cls

    # @classmethod
    # def get_request_queryset(self, ar, **filter):
    #     return []

    @classmethod
    def spawn(cls, suffix, **kw):
        kw['app_label'] = cls.app_label
        return type(cls.__name__ + str(suffix), (cls,), kw)

    @classmethod
    def parse_req(self, request, rqdata, **kw):
        """
        This is called when an incoming web request on this actor is being
        parsed.

        If you override :meth:`parse_req`, then keep in mind that it will
        be called *before* Lino checks the requirements.  For example the
        user may be AnonymousUser even if the requirements won't let it be
        executed.  `ar.subst_user.user_type` may be None, e.g. when called
        from `find_appointment` in :class:`welfare.pcsw.Clients`.

        """
        return kw

    @classmethod
    def get_row_by_pk(self, ar, pk):
        """
        `dbtables.Table` overrides this.
        """
        try:
            return ar.data_iterator[int(pk)-1]
        except (ValueError, IndexError):
            return None

    @classmethod
    def get_default_action(cls):
        return actions.ShowTable()

    @classmethod
    def get_actor_editable(self):
        if self._editable is None:
            return (self.get_data_rows is None)
        return self._editable

    @classmethod
    def setup_columns(self):
        pass

    @classmethod
    def get_column_names(self, ar):
        """Dynamic tables can subclass this method and return a value for
        :attr:`column_names` which depends on the request.

        """
        # if settings.SITE.mobile_view:
        #     return self.column_names_m or self.column_names
        # else:
        #     return self.column_names
        return self.column_names

    @classmethod
    def group_from_row(self, row):
        return self.default_group

    @classmethod
    def wildcard_data_elems(self):
        for cc in self.virtual_fields.values():
            yield cc
        #~ return []

    @classmethod
    def get_filter_kw(self, ar, **kw):
        """
        Return a dict with the "master keywords" for this table
        and a given `master_instance`.

        For example, if you have two models :class:`Book` and
        :class:`Author`, and a foreign key :attr:`Book.author` which
        points to the author of the book, and a table `BooksByAuthor`
        having `master_key` set to ``'author'``, then `get_filter_kw`
        would return a dict `{'author': <PK>}` where PK is the primary
        key of the action request's :attr:`master_instance
        <lino.core.requests.BaseRequest.master_instance>`.

        Another example is
        :class:`lino_xl.lib.tickets.EntriesBySession`, where blog
        entries are not directly linked to a session, but in the
        detail of a session we want to display a table of related blog
        entries.

        :class:`lino_xl.lib.households.SiblingsByPerson` Household
        members are not directly linked to a Person, but usually a
        Person is member of exactly one household, and in the Detail
        of a Person we want to display the members of that household.
        """
        from lino.core.gfks import gfk2lookup, GenericForeignKey
        master_instance = ar.master_instance
        if self.master is None:
            pass
            # master_instance may be e.g. a lino.core.actions.EmptyTableRow
            # UsersWithClients as "slave" of the "table" Home
        elif self.master is models.Model:
            pass

        elif isinstance(self.master_field, GenericForeignKey):
            kw = gfk2lookup(self.master_field, master_instance, **kw)
        elif self.master_field is not None:
            if master_instance is None:
                if not self.master_field.null:
                    #~ logger.info('20120519 %s.get_filter_kw()--> None',self)
                    return  # cannot add rows to this table
            else:
                master_instance = master_instance.get_typed_instance(
                    self.master)
                if not isinstance(master_instance, self.master):
                    # e.g. a ByUser table descendant called by AnonymousUser
                    msg = "%r is not a %s (%s.master_key = '%s')" % (
                        master_instance.__class__,
                        self.master, self,
                        self.master_key)
                    logger.warning(msg)
                    # raise Exception(msg)
                    # raise PermissionDenied(msg)
                    # master_instance = None
                    return  # cannot add rows to this table
            kw[self.master_field.name] = master_instance
        # else:
        #     msg = "20150322 Cannot handle master {0}".format(master_instance)
        #     raise Exception(msg)
        return kw

    #~ @classmethod
    #~ def request(cls,ui=None,request=None,action=None,**kw):
        #~ self = cls
        #~ if action is None:
            #~ action = self.default_action
        #~ return TableRequest(ui,self,request,action,**kw)

    # @fields.displayfield(_("Details"))
    # def detail_pointer(cls, obj, ar):
    #     # print("20181230 detail_pointer() {}".format(cls))
    #     return obj.obj2href(ar)

    @classmethod
    def request(self, master_instance=None, **kw):
        """Return a new :class:`TableRequest
        <lino.core.tablerequest.TableRequest>` on this table.

        If this is a slave table, the :attr:`master_instance
        <lino.core.tablerequest.TableRequest.master_instance>` can be
        specified as optional first positional argument.

        """
        kw.update(actor=self)
        if master_instance is not None:
            kw.update(master_instance=master_instance)
        return TableRequest(**kw)

    @classmethod
    def run_action_from_console(self, pk=None, an=None):
        """
        Not yet stable. Used by print_tx25.py.
        To be combined with the `show` management command.
        """
        settings.SITE.startup()
        ba = None
        if pk is not None:
            if an is None:
                # an = self.default_elem_action_name
                ba = self.detail_action
        elif an is None:
            an = self.default_list_action_name
        if ba is None:
            ba = self.get_action_by_name(an)
        #~ print ba
        if pk is None:
            ar = self.request(action=ba)
        else:
            ar = self.request(action=ba, selected_pks=[pk])

        ba.action.run_from_ui(ar)
        kw = ar.response
        msg = kw.get('message')
        if msg:
            print(msg)
        url = kw.get('open_url') or kw.get('open_webdav_url')
        if url:
            os.startfile(url)

    @classmethod
    def add_quick_search_filter(cls, data, search_text):
        """Add a filter to the given data iterator in order to apply a quick
        search for the given `search_text`.

        """
        return data


class VirtualTable(AbstractTable):
    """
    An :class:`AbstractTable` that works on an volatile (non
    persistent) list of rows.

    By nature it cannot have database fields, only virtual fields.

    Subclasses must define a :meth:`get_data_rows` method.

    """
    abstract = True


class VentilatedColumns(VirtualTable):
    """
    A mixin for tables that have a series of automatically generated
    columns
    """
    ventilated_column_suffix = ':5'

    column_names_template = ''
    """
    The template to use for :attr:`column_names`.   It should contain a string
    ``{vcolumns}`` which will be replaced by a space-separated list of the column
    names given by :meth:`get_ventilated_columns`.
    """

    abstract = True

    @classmethod
    def setup_columns(self):
        # if not "{vcolumns}" in self.column_names_template:
        #     return
        # self.column_names = 'description '
        names = ''
        for i, vf in enumerate(self.get_ventilated_columns()):
            self.add_virtual_field('vc' + str(i), vf)
            names += ' ' + vf.name + self.ventilated_column_suffix

        self.column_names = self.column_names_template.format(vcolumns=names)

        #~ logger.info("20131114 setup_columns() --> %s",self.column_names)

    @classmethod
    def get_ventilated_columns(self):
        return []

class VentilatingTable(VentilatedColumns):

    abstract = True
    column_names_template = 'description {vcolumns}'

    @fields.virtualfield(models.CharField(_("Description"), max_length=30))
    def description(self, obj, ar):
        return str(obj)


class ButtonsTable(VirtualTable):
    """

    An abstract :class:`VirtualTable` with only one column and whose rows are
    action buttons.

    Subclasses must implement `get_data_rows` to yield action buttons.

    Usage example
    `lino_welfare.modlib.reception.models.FindDateByClientTable`.

    """
    abstract = True
    column_names = 'button'
    auto_fit_column_widths = True
    window_size = (60, 20)
    hide_top_toolbar = True

    @fields.displayfield(_("Button"))
    def button(self, obj, ar):
        return obj


# from lino.core.signals import post_analyze
# from django.db.utils import DatabaseError

# @signals.receiver(post_analyze)
# def setup_ventilated_columns(sender, **kw):
#     # print("20170308 SETUP_VENTILATED_COLUMNS")
#     if actors.actors_list is not None:
#         for a in actors.actors_list:
#             if issubclass(a, AbstractTable) and not a.abstract:
#                 try:
#                     a.setup_columns()
#                 except DatabaseError:
#                     logger.debug(
#                         "Ignoring DatabaseError in %s.setup_ventilated_columns", a)
#     settings.SITE.resolve_virtual_fields()
