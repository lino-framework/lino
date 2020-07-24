# -*- coding: UTF-8 -*-
# Copyright 2009-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""This defines :class:`Actor` and related classes.

See :doc:`/dev/actors`.


"""
from future.utils import with_metaclass

import logging; logger = logging.getLogger(__name__)

import copy
import traceback

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.core import fields
from lino.core import actions
from lino.core import layouts
from lino.core.requests import ActionRequest
from lino.core.boundaction import BoundAction
from lino.core.exceptions import ChangedAPI
from lino.core.constants import _handle_attr_name
from lino.core.permissions import add_requirements, Permittable
from lino.core.utils import resolve_model
from lino.core.utils import error2str
from lino.core.utils import qs2summary
from lino.core.utils import ParameterPanel
from lino.core.utils import navinfo, dbfield2params_field
from lino.utils import curry, AttrDict, is_string

from etgen.html import E, forcetext, tostring

from .roles import SiteUser

ACTOR_SEP = '.'

actor_classes = []
actors_dict = None
actors_list = None

def discover():
    global actor_classes
    global actors_list
    global actors_dict

    assert actors_list is None
    assert actors_dict is None

    actors_list = []
    actors_dict = AttrDict()

    logger.debug("actors.discover() : registering %d actors",
                 len(actor_classes))
    for cls in actor_classes:
        register_actor(cls)
    actor_classes = None


def register_actor(a):
    #~ logger.debug("register_actor %s",a)
    if not a.abstract:
        if not settings.SITE.is_installed(a.app_label):
            # avoid registering choicelists of non-installed plugins
            # logger.info("20190107 skip register_actor for %s", a)
            return
    old = actors_dict.define(a.app_label, a.__name__, a)
    if old is not None:
        actors_list.remove(old)
    actors_list.append(a)
    return a



#~ class ClassProperty(property):
    #~ def __get__(self, cls, owner):
        #~ return self.fget.__get__(None, owner)()
#~




def field_getter(name):
    def func(cls, obj, ar):
        #~ print 20130910, repr(obj),name
        return getattr(obj, name)
    return func


class ActorMetaClass(type):

    def __new__(meta, classname, bases, classDict):
        #~ if not classDict.has_key('app_label'):
            #~ classDict['app_label'] = cls.__module__.split('.')[-2]
        """
        attributes that are never inherited from base classes:
        """
        # classDict.setdefault('name',classname)
        # ~ classDict.setdefault('label',None) # 20130906
        #~ classDict.setdefault('related_name',None)
        #~ classDict.setdefault('button_label',None)
        classDict.setdefault('title', None)
        classDict.setdefault('help_text', None)
        classDict.setdefault('abstract', False)

        declared_label = classDict.pop('label', None)
        if declared_label is not None:
            classDict.update(_label=declared_label)
        declared_known_values = classDict.pop('known_values', None)
        if declared_known_values is not None:
            classDict.update(_known_values=declared_known_values)
        declared_editable = classDict.pop('editable', None)
        if declared_editable is not None:
            classDict.update(_editable=declared_editable)

        cls = type.__new__(meta, classname, bases, classDict)

        #~ if not classDict.has_key('label'):
            #~ cls.label = ClassProperty(cls.get_actor_label)
            # ~ meta.label = property(cls.get_actor_label.im_func) # 20130906
        #~ if not classDict.has_key('known_values'):
            #~ cls.known_values = ClassProperty(cls.get_known_values)
            # ~ meta.known_values = property(cls.get_known_values.im_func) # 20130906
        """
        On 20110822 I thought "A Table always gets the app_label of its model,
        you cannot set this yourself in a subclass
        because otherwise it gets complex when inheriting reports from other
        app_labels."
        On 20110912 I cancelled change 20110822 because PersonsByOffer
        should clearly get app_label 'jobs' and not 'contacts'.

        """

        if classDict.get('app_label', None) is None:
            # Figure out the app_label by looking one level up.
            # For 'django.contrib.sites.models', this would be 'sites'.
            x = cls.__module__.split('.')
            if len(x) > 1:
                cls.app_label = x[-2]

        cls.actor_id = cls.app_label + '.' + cls.__name__
        cls._setup_done = False
        cls._setup_doing = False
        cls.virtual_fields = {}
        cls._constants = {}
        cls._actions_dict = {}  # AttrDict()
        cls._actions_list = []  # 20121129
        # cls._pending_field_updates = []

        cls.collect_virtual_fields()


        # def register_class_attribute(k, v):
        #     if isinstance(v, fields.Constant):
        #         cls.add_constant(k, v)
        #     elif isinstance(v, fields.VirtualField):  # 20120903b
        #         cls.add_virtual_field(k, v)
        #     elif isinstance(v, models.Field):  # 20130910
        #         # ~ print "20130910 add virtual field " ,k, cls
        #         vf = fields.VirtualField(v, field_getter(k))
        #         cls.add_virtual_field(k, vf)
        #
        # # inherit virtual fields defined on parent actors
        # for b in bases:
        #     for cl in b.__mro__:
        #         for k, v in cl.__dict__.items():
        #             register_class_attribute(k, v)
        # for k, v in classDict.items():
        #     register_class_attribute(k, v)

        #~ if classname == 'Tasks':
            #~ logger.info("20130817 no longer added actor vfs")

        #~ cls.params = []
        #~ for k,v in classDict.items():
            #~ if isinstance(v,models.Field):
                #~ v.set_attributes_from_name(k)
                #~ v.table = cls
                #~ cls.params.append(v)
        #~ cls.install_params_on_actor()
        if actor_classes is not None:
            actor_classes.append(cls)
        # if classname not in (
        #         'Table', 'AbstractTable', 'VirtualTable',
        #         'Action', 'Actor', 'Frame',
        #         'ChoiceList', 'Workflow',
        #         'EmptyTable', 'Dialog'):
        #     elif not cls.__name__.startswith('unused_'):
        #         # ~ cls.class_init() # 20120115
        #         actor_classes.append(cls)
        #     #~ logger.debug("ActorMetaClass.__new__(%s)", cls)
        return cls

    def __str__(cls):
        return cls.actor_id

    def __repr__(cls):
        return cls.__module__ + "." + cls.__name__

    @property
    def label(cls):
        # return cls.get_label()  # 20200307
        return cls.get_actor_label()

    @property
    def known_values(cls):
        return cls.get_known_values()

    @property
    def editable(cls):
        return cls.get_actor_editable()


class Actor(with_metaclass(ActorMetaClass, type('NewBase', (actions.Parametrizable, Permittable), {}))):
    """
    The base class for all actors.  Subclassed by :class:`AbstractTable
    <lino.core.tables.AbstractTable>`, :class:`Table
    <lino.core.dbtables.Table>`, :class:`ChoiceList
    <lino.core.choicelists.ChoiceList>` and :class:`Frame
    <lino.core.frames.Frame>`.

    .. attribute:: label

        The text to appear e.g. on a button that will call the default
        action of an actor.  This attribute is *not* inherited to
        subclasses.  For :class:`Actor` subclasses that don't have a
        label, Lino will call :meth:`get_actor_label`.

    .. attribute:: known_values

        A `dict` of `fieldname` -> `value` pairs that specify "known values".

        Requests will automatically be filtered to show only existing
        records with those values.  This is like :attr:`filter`, but new
        instances created in this Table will automatically have these
        values set.

    .. attribute:: welcome_message_when_count

       Set this to an integer (e.g. 0) to tell Lino to make a generic
       welcome message "You have X items in Y" when the number of rows
       in this table is *greater than* the given integer.

    The following class methods are `None` in the default
    implementation. Subclass can define them.

    .. classmethod:: get_handle_name(self, ar)

        Most actors use the same UI handle for each request.  But
        e.g. :class:`lino_welfare.modlib.debts.models.PrintEntriesByBudget`
        and :class:`lino_xl.lib.events.EventsByType` override this to
        implement dynamic columns depending on it's master_instance.


    .. classmethod:: get_row_classes(self, ar)

        If a method of this name is defined on an actor, then it must
        be a class method which takes an :class:`ar
        <lino.core.requests.BaseRequest>` as single argument and
        returns either None or a string "red", "green" or "blue"
        (todo: add more colors and styles). Example::

            @classmethod
            def get_row_classes(cls,obj,ar):
                if obj.client_state == ClientStates.newcomer:
                    return 'green'

        Defining this method will cause an additional special
        `RowClassStoreField` field in the :class:`lino.core.Store`
        objects of this actor.

    .. classmethod:: get_welcome_messages(self, ar)

        If a method of this name is defined on an actor, then it must
        be a class method which takes an :class:`ar
        <lino.core.requests.BaseRequest>` as single argument and
        returns or yields a list of :term:`welcome messages <welcome
        message>` (messages to be displayed in the welcome block of
        :xfile:`admin_main.html`).

        Note that this handler will be called independently of whether
        the user has permission to view the actor or not.
    """
    required_roles = set([SiteUser])
    """See :attr:`lino.core.permissions.Permittable.required_roles`"""

    model = None
    """The model on which this table iterates.

    The application programmer can specify either the model class
    itself or a string of type ``'app.Model'``.

    This should be `None` on all tables which are not subclass of
    :class:`lino.core.dbtables.Table`.

    """

    actions = None
    """An :class:`AttrDict <atelier.utils.AttrDict>` containing the
    actions available on this actor.

    """

    only_fields = None

    app_label = None
    """
    Specify this if you want to "override" an existing actor.

    The default value is deduced from the module where the subclass is
    defined.

    Note that this attribute is not inherited from base classes.

    :func:`lino.core.table.table_factory` also uses this.
    """

    master = None
    """The class of the "master" for this actor.

    Application code usually doesn't need to specify this because it
    is automatically set on actors whose :attr:`master_key` is
    specified.

    Setting this to something else than `None` will turn the table
    into a :term:`slave table`.

    If the :attr:`master` is something else than a database model
    (e.g. a ChoiceList), then the actor must also define a
    :meth:`get_master_instance` method.

    """

    master_key = None
    """The name of a field of this table's :attr:`model` that
    points to its :attr:`master`.

    The field named by :attr:`master_key` should usually be a
    :class:`ForeignKey` field.

    Special cases: :class:`lino_xl.lib.cal.EntriesByGuest` shows the entries
    having a presence pointing to this guest.

    Note that the :attr:`master_key` is automatically added to
    :attr:`hidden_columns`.


    """

    details_of_master_template = _("%(details)s of %(master)s")
    """Used to build the title of a request on this table when it is a
    slave table (i.e. :attr:`master` is not None). The default value
    is defined as follows::

        details_of_master_template = _("%(details)s of %(master)s")

    """

    parameters = None
    "See :attr:`lino.core.utils.Parametrizable.parameters`."

    _layout_class = layouts.ParamsLayout
    _state_to_disabled_actions = None

    ignore_required_states = False
    """
    Whether to ignore the required states of workflow actions.

    Set this to `True` on a workflow if you want to disable workflow
    control based on the state of the object.

    Note that you must set this to True before importing any library workflows
    because permission handlers are defined when a workflow is imported. """

    sort_index = 60
    """The :attr:`sort_index <lino.core.actions.Action.sort_index>` to be
    used when this table is being used by a :class:`ShowSlaveTable
    <lino.core.actions.ShowSlaveTable>`.

    """

    icon_name = None
    """The :attr:`lino.core.actions.Action.icon_name` to be used for a
    :class:`lino.core.actions.ShowSlaveTable` action on this actor.

    """

    simple_parameters = None
    """A tuple of names of filter parameters which are handled
    automatically.

    Application developers should not set this attribute directly,
    they should rather define a :meth:`get_simple_parameters` on the
    model.

    """

    hidden_elements = frozenset()
    """A set of names of layout elements which are hidden by default.

    The default is an empty set except for
    :class:`lino.core.dbtables.Table` where this will be populated from
    :attr:`hidden_elements <lino.core.model.Model.hidden_elements>`
    of the :class:`lino.core.model.Model`.

    Note that these names are not being verified to be names of
    existing fields. This fact is being used by UNION tables like
    :class:`lino_xl.lib.vat.IntracomInvoices`

    """

    detail_html_template = 'bootstrap3/detail.html'
    """The template to be used for rendering a row of this actor as a
    detail html page.

    """
    list_html_template = 'bootstrap3/table.html'
    """The template to be used for rendering a collection of rows of this
    actor as a table html page.

    """
    welcome_message_when_count = None
    get_welcome_messages = None
    get_row_classes = None
    window_size = None
    """Set this to a tuple of `(height, width)` to have this actor
    display in a modal non-maximized window.

    - `height` must be either an integer expressing a number of rows
      or the string "auto".  If it is auto, then the window should not
      contain any v-flexible component.

    - `width` must be either an integer expressing a number of rows
      or a string of style "90%".

      Note that a relative width will be converted to a number of
      pixels when the window is rendered for the first time. That is,
      if you close the window, resize your browser window and reopen
      the same window, you will get the old size.

    """

    default_list_action_name = 'grid'
    default_elem_action_name = 'detail'

    # update_required = set()
    # delete_required = set()

    editable = None
    """Set this explicitly to `True` or `False` to make the whole table
    editable or not.  Otherwise Lino will guess what you want during
    startup and set it to `False` if the actor is a Table and has a
    `get_data_rows` method (which usually means that it is a virtual
    table), otherwise to `True`.

    Non-editable actors won't even call :meth:`get_view_permission`
    for actions whose :attr:`readonly
    <lino.core.actions.Action.readonly>` is `False`.

    The
    :class:`changes.Changes <lino.modlib.changes.Changes>`
    table is an example where this is being used: nobody should
    ever edit something in the table of Changes.  The user
    interface uses this to generate optimized JS code for this
    case.

    """

    auto_apply_params = True
    """Whether the parameter values of the parameter panel should be
    applied automatically when some value has been changed.

    """

    insert_layout_width = 60
    """
    When specifying an :attr:`insert_layout` using a simple a multline
    string, then Lino will instantiate a FormPanel with this width.
    """

    hide_window_title = False
    """
    This is set to `True` e.h. in home pages
    (e.g. :class:`lino_welfare.modlib.pcsw.models.Home`).

    """

    allow_create = True
    """
    If this is False, the table won't have any insert_action.
    """

    hide_headers = False
    """Set this to True in order to hide the column headers.

    This is ignored when the table is rendered in an ExtJS grid.
    """

    hide_top_toolbar = False
    """
    Whether a Detail Window should have navigation buttons, a "New"
    and a "Delete" buttons.  In ExtJS UI also influences the title of
    a Detail Window to specify only the current element without
    prefixing the Tables's title.

    If used in a grid view in React will remove the top toolbar
    and selection tools.

    This option is `True` in
    :class:`lino.models.SiteConfigs`,
    :class:`lino_welfare.pcsw.models.Home`,
    :class:`lino.modlib.users.desktop.MySettings`,
    :class:`lino_xl.cal.CalenderView`.

    """

    simple_slavegrid_header = False
    """
    If True the slave grid in a detail will be simplified
    """

    # paginator_rowsPerPageOptions = None
    # """Array of integer values to display inside rows per page dropdown in the paginator."""

    paginator_template = None
    """
    Paginator elements can be customized using the template property using the predefined keys, default value is
    "FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown".
    Here are the available elements that can be placed inside a paginator.

    FirstPageLink
    PrevPageLink
    PageLinks
    NextPageLink
    LastPageLink
    RowsPerPageDropdown
    CurrentPageReport
    """

    _label = None
    _editable = None
    _known_values = {}

    title = None
    """
    The text to appear e.g. as window title when the actor's default
    action has been called.  If this is not set, Lino will use the
    :attr:`label` as title.
    """

    button_text = None
    """The text to appear on buttons of a ShowSlaveTable action for this
    actor.

    """

    label = None

    default_action = None
    actor_id = None

    detail_layout = None
    '''
    Define the layout to use for the detail window.  Actors with
    :attr:`detail_layout` will get a `show_detail` action.

    When you define a :attr:`detail_layout`, you will probably also
    want to define a :attr:`insert_layout`.

    The :attr:`detail_layout` is normally an instance of
    :class:`DetailLayout <lino.core.layouts.DetailLayout>` or a
    subclass thereof.  For example::

        class FooDetail(dd.DetailLayout):
            ...

        class Foos(dd.Table):
            ...
            detail_layout = FooDetail()

    It is possible and recommended to specify :attr:`detail_layout` as
    a string, in which case it will be resolved at startup as follows:

    If the string contains at least one newline (or no newline and
    also no dot) then it is taken as the :attr:`main` of a
    :class:`DetailLayout <lino.core.layouts.DetailLayout>`.
    For example::

        class Foos(dd.Table):
            ...
            detail_layout = """
            id name
            description
            """

    If the string contains a dot ('.') and *does not contain* any
    newlines, then Lino takes this as the name of the class to be
    instantiated and used.

    For example::

        class Courses(dd.Table):
            ...
            detail_layout = 'courses.CourseDetail'

    This feature makes it possible to override the detail layout in an
    extended plugin. Before this you had to define a new class and to
    assign an instance of that class to every actor which uses it.
    But e.g. in :mod:`lino_xl.lib.courses` we have a lot of subclasses
    of the :class:`Courses` actor.
    '''

    insert_layout = None
    """
    Define the form layout to use for the insert window.

    If there's a :attr:`detail_layout` but no :attr:`insert_layout`,
    the table won't have any (+) button to create a new row via a
    dialog window, but users can still create rows by writing into the
    phantom row. Example of this is
    :class:`lino_xl.lib.courses.Topics` which has a detail layout
    with slave tables, but the model itself has only two fields (id
    and name) and it makes no sense to have an insert window.
    """

    card_layout = None
    """
    Define a layout for a card view of the table."""

    detail_template = None    # deprecated: use insert_layout instead
    insert_template = None    # deprecated: use detail_layout instead

    help_text = None
    """
    A help text that shortly explains what the default action of this
    actor does.  In a graphical user interface this will be rendered
    as a **tooltip** text.

    If this is not given by the code, Lino will potentially set it at
    startup when loading the :xfile:`help_texts.py` files.
    """

    detail_action = None
    update_action = None
    insert_action = None
    # create_action = None
    delete_action = None
    _handle_class = None  # For internal use.
    get_handle_name = None

    abstract = True
    """
    Set this to `True` to prevent Lino from generating useless
    JavaScript if this is just an abstract base class to be inherited
    by other actors.

    Note that this class attribute is not inherited to subclasses.

    """
    sum_text_column = 0
    """The index of the column which should hold the text to display on
    the totals row (returned by :meth:`get_sum_text`).

    """

    preview_limit = None
    """For non-table actors this is always `None`, otherwise see
    :attr:`lino.core.tables.AbstractTable.preview_limit`.

    """

    handle_uploaded_files = None
    """
    Handler for uploaded files.
    Same remarks as for :attr:`lino.core.actors.Actor.disabled_fields`.
    """

    def __init__(self, *args, **kw):
        raise Exception("Actors should never get instantiated")

    @classmethod
    def apply_cell_format(self, ar, row, col, recno, td):
        """
        Actor-level hook for overriding the formating when rendering
        this table as plain html.

        For example :class:`ml.cal.Events` overrides this.
        """
        pass

    @classmethod
    def actor_url(self):
        return '/' + self.app_label + '/' + self.__name__

    @classmethod
    def is_installed(self):
        return settings.SITE.is_installed(self.app_label)

    @classmethod
    def get_widget_options(self, name, **options):
        return options

    @classmethod
    def get_chooser_for_field(cls, fieldname):
        d = getattr(cls, '_choosers_dict', {})
        return d.get(fieldname, None)

    # @classmethod
    # def inject_field(cls, name, fld):
    #     # called from auth.add_user_group()
    #     setattr(cls, name, fld)
    #     cls.register_class_attribute(name, fld)

    @classmethod
    def get_pk_field(self):
        """Return the Django field used to represent the primary key
        when filling `selected_pks`.

        """
        return None

    @classmethod
    def get_actions_hotkeys(cls):
        """
        Return or yield a list of hotkeys to be linked to named actions.

        [{'key': key, 'ctrl': Bool, 'shift': Bool, 'ba': action_name}]

        """

    @classmethod
    def get_row_by_pk(self, ar, pk):
        """Return the data row identified by the given primary key.

        """
        return None

    @classmethod
    def get_master_instance(self, ar, model, pk):
        """Return the `master_instance` corresponding to the specified primary
        key.

        You need to override this on slave actors whose
        :attr:`master` is not a database model,
        e.g. the :class:`ProblemsByChecker
        <lino.modlib.checkdata.ProblemsByChecker>` table.

        `ar` is the action request on this actor. `model` is the
        :attr:`master`, except if :attr:`master` is `ContentType` (in
        which case `model` is the *requested* master).

        """
        if issubclass(model, models.Model):
            try:
                return model.get_user_queryset(ar.get_user()).get(pk=pk)
                # why not simply return model.objects.get(pk=pk) ?
            except ValueError:
                return None
            except model.DoesNotExist:
                return None
        msg = "{0} must override get_master_instance"
        msg = msg.format(self)
        raise Exception(msg)
        # from lino.core import choicelists
        # if issubclass(master, choicelists.Choice):
        #     if master.choicelist is None:
        #         kw['master_instance'] = None
        #     else:
        #         mi = master.choicelist.get_by_values(pk)
        #         kw['master_instance'] = mi
        # else:
        #     logger.info("Invalid master %s", master)

    @classmethod
    def get_disabled_fields(cls, obj, ar):
        """
        Return the cached set of disabled fields for this `obj` and `ar`.

        """
        df = getattr(obj, '_disabled_fields', None)
        if df is None:
            df = cls.make_disabled_fields(obj, ar)
            setattr(obj, '_disabled_fields', df)
        return df

    @classmethod
    def make_disabled_fields(cls, obj, ar):
        """
        Return a set of disabled fields for the specified object and
        request.

        See :doc:`/dev/disabled_fields`.
        """

        s = set()
        state = cls.get_row_state(obj)
        if state is not None:
            s |= cls._state_to_disabled_actions.get(state.name, set())
        return s

    @classmethod
    def get_request_handle(self, ar):
        """
        Return the dynamic (per-request) handle for this actor for the
        renderer used by specified action request.
        """
        # logger.info("18072017, self.get_handle_name:|%s| #1955"%(self.get_handle_name),)
        if self.get_handle_name is None:
            return self._get_handle(ar, _handle_attr_name)
        return self._get_handle(ar, self.get_handle_name(ar))

    @classmethod
    def get_navinfo(cls, ar, obj):
        """
        Return navigation info for the given obj in the given ar.

        The default implementation assumes that you navigate on the
        :attr:`data_iterator`.

        :class:`lino_xl.lib.cal.CalendarView` overrides this.

        """
        return navinfo(ar.data_iterator, obj)

    @classmethod
    def is_valid_row(self, row):
        return False

    @classmethod
    def make_params_layout_handle(cls):
        if cls.is_abstract():
            raise Exception("{} is abstract".format(cls))
        return actions.make_params_layout_handle(cls)

    @classmethod
    def is_abstract(cls):
        return cls.abstract

    @classmethod
    def has_handle(self, ui):
        return self.__dict__.get(_handle_attr_name, False)

    @classmethod
    def clear_handle(self):
        """
        When an actor has dynamic columns which depend on database
        content, then its layout handle may not persist between
        different Django test cases because a handle from a first
        test case may refer to elements which no longer exist in a
        second test case.
        """
        setattr(self, _handle_attr_name, None)

    @classmethod
    def on_analyze(self, site):
        pass

    @classmethod
    def summary_row(cls, ar, obj, **kw):
        """
        Return a HTML representation of the given  data row `obj` for usage in a
        summary panel.

        See also :meth:`lino.core.model.Model.summary_row`.

        """
        return obj.summary_row(ar, **kw)

    @classmethod
    def do_setup(self):
        pass

    @classmethod
    def get_handle(self):
        """
        Return a static handle for this actor.
        """
        #~ assert ar is None or isinstance(ui,UI), \
            #~ "%s.get_handle() : %r is not a BaseUI" % (self,ui)
        if self.get_handle_name is not None:
            raise Exception(
                "Tried to get static handle for %s (get_handle_name is %r)"
                % (self, self.get_handle_name))
        return self._get_handle(None, _handle_attr_name)

    @classmethod
    def _get_handle(self, ar, hname):
        # don't inherit from parent!
        h = self.__dict__.get(hname, None)
        # logger.info("18072017, h:|%s|, hname:|%s| #1955"%(h, hname))
        if h is None:
            h = self._handle_class(self)
            # don't store the handle instance when an exception occurs during
            # setup_handle. Because if the exception is caught by calling code,
            # the unfinished handle would remain in memory and get used by
            # subsequent calls, causing tracebacks like "AttributeError:
            # 'TableHandle' object has no attribute 'store'"
            setattr(self, hname, h)
            try:
                settings.SITE.kernel.setup_handle(h, ar)
            except Exception as e:
                # traceback.print_exc()
                logger.warning("%s setup_handle failed with %s", self, e)
                delattr(self, hname)
                # raise

        # logger.info("18072017, h:|%s|, h.store:|%s|, #1955"%(h, getattr(h,'store',None)))
        return h

    # @classmethod
    # def update_field(cls, name, **kwargs):
    #     cls._pending_field_updates.append((name, kwargs)) xxx
    #     de = getattr(cls, name)
    #     if de.model is not cls:
    #         de = copy.deepcopy(de)
    #         de.model = cls
    #         setattr(cls, name, de)
    #     for k, v in kwargs.items():
    #         setattr(de, k, v)

    @classmethod
    def class_init(cls):
        """Called internally at site startup.

        """
        # logger.info("20180201 class_init", cls)

        if hasattr(cls, 'required'):
            raise ChangedAPI(
                "{0} must convert `required` to `required_roles`".format(cls))

        master = getattr(cls, 'master', None)
        if isinstance(master, str):
        # if isinstance(master, string_types):
            cls.master = resolve_model(master)

        model = getattr(cls, 'model', None)
        if isinstance(model, str):
            model = cls.model = resolve_model(model)

        cls.collect_virtual_fields()

        # set the verbose_name of the detail_link field
        # model = cls.model
        if isinstance(model, type) and issubclass(model, models.Model):
            de = cls.detail_link
            assert de.model is not None
            # only if it hasn't been overridden by a parent actor
            if de.model is Actor:
                if de.return_type.verbose_name != model._meta.verbose_name:
                    de = copy.deepcopy(de)
                    de.model = de.return_type.model = cls
                    de.return_type.verbose_name = model._meta.verbose_name
                    de.lino_resolve_type()
                    cls.detail_link = de
                    cls.virtual_fields['detail_link'] = de
                    # cls.add_virtual_field('detail_link', de)

    @classmethod
    def init_layouts(cls):

        # 20200430 this was previously part of class_init, but is now called in
        # a second loop. Because calview.EventsParams copies parameters from Events.

        actions.install_layout(cls, 'detail_layout', layouts.DetailLayout)
        actions.install_layout(cls, 'insert_layout', layouts.InsertLayout,
            window_size=(cls.insert_layout_width, 'auto'))
        actions.install_layout(cls, 'card_layout', layouts.DetailLayout)

        if cls.abstract:
            return

        if 'parameters' in cls.__dict__:
            cls.setup_parameters(cls.parameters)
        else:
            params = {}
            if cls.parameters is not None:
                params.update(cls.parameters)
            cls.setup_parameters(params)
            if len(params):
                cls.parameters = params

        lst = []
        for n in cls.get_simple_parameters():
            if n in lst:
                logger.warning(
                    "Removed duplicate name %s returned by %s.get_simple_parameters()", n, cls)
            else:
                lst.append(n)
        cls.simple_parameters = tuple(lst)

        if cls.parameters is None and len(cls.simple_parameters) > 0 :
            cls.parameters = {}

        for name in cls.simple_parameters:
            if name not in cls.parameters:
                db_field = cls.get_data_elem(name)
                if db_field is None:
                    raise Exception("{}.get_simple_parameters() returned invalid name '{}'".format(cls, name))
                cls.parameters[name] = dbfield2params_field(db_field)
                # if "__" in name:
                #     print("20200423", cls.parameters)
        # if len(cls.parameters) == 0:
        #     cls.parameters = None # backwards compatibility

    @classmethod
    def collect_virtual_fields(cls):

        """Collect virtual fields from class attributes and register them as
        virtual fields. """
        # print("20190201 collect_virtual_fields {}".format(cls))
        for b in reversed(cls.__mro__):
            for k, v in b.__dict__.items():
            # for k in b.__dict__.keys():
            #     v = getattr(cls, k)
                if isinstance(v, fields.Constant):
                    cls.add_constant(k, v)
                elif isinstance(v, fields.VirtualField):  # 20120903b
                    cls.add_virtual_field(k, v)
                elif isinstance(v, models.Field):  # 20130910
                    # ~ print "20130910 add virtual field " ,k, cls
                    vf = fields.VirtualField(v, field_getter(k))
                    cls.add_virtual_field(k, vf)

    @classmethod
    def get_known_values(cls):
        return cls._known_values

    @classmethod
    def get_actor_editable(self):
        return self._editable

    @classmethod
    def hide_elements(self, *names):
        for name in names:
            if self.get_data_elem(name) is None:
                raise Exception("%s has no element '%s'" % self, name)
        self.hidden_elements = self.hidden_elements | set(names)

    @classmethod
    def add_view_requirements(cls, *args):
        return add_requirements(cls, *args)

    @classmethod
    def get_view_permission(self, user_type):
        """Return True if this actor as a whole is visible for users with the
        given user_type.

        """
        # return isinstance(user_type, tuple(self.required_roles))
        return True

    @classmethod
    def get_create_permission(self, ar):
        """Dynamic test per request.  This is being called only when
        :attr:`allow_create` is True.

        """
        if not settings.SITE.user_types_module:
            return True
        if ar.get_user().user_type.readonly:
            return False
        return True

    @classmethod
    def get_row_permission(cls, obj, ar, state, ba):
        """Returns True or False whether the given action request
        ActionRequest `ar` is allowed on the given row instance `row`.

        """
        if ba.action.readonly:
            return True
        if ar.get_user().user_type.readonly:
            return False
        return cls.editable

    @classmethod
    def _collect_actions(cls):
        """
        Loops through the class dict and collects all Action instances,
        calling :meth:`_attach_action`, which will set their `actor` attribute.
        Before this we create `insert_action` and `detail_action` if necessary.
        Also fill :attr:`_actions_list`.
        """

        default_action = cls.get_default_action()

        if default_action is not None:
            # cls.default_action = cls._bind_action(default_action)
            cls.default_action = cls._bind_action(
                'default_action', default_action)

        if cls.detail_layout:
            if default_action and isinstance(
                    default_action, actions.ShowDetail) and \
                    default_action.owner == cls.detail_layout:
                dtla = default_action
            else:
                if cls.detail_action and cls.detail_action.action.owner == cls.detail_layout:
                    dtla = cls.detail_action.action
                else:
                    dtla = actions.ShowDetail(cls.detail_layout)
            cls.detail_action = cls._bind_action('detail_action', dtla)
            if cls.use_detail_param_panel:
                cls.detail_action.action.use_param_panel = True
            # if str(cls).endswith("Days"):
            #     logger.info("20181230 %r detail_action is %r", cls, cls.detail_action)
            if cls.editable:
                cls.submit_detail = cls._bind_action(
                    'submit_detail', actions.SubmitDetail())

        if cls.editable:
            if cls.allow_create:
                # if cls.detail_action and not cls.hide_top_toolbar:
                if cls.insert_layout and not cls.hide_top_toolbar:
                    cls.insert_action = cls._bind_action(
                        'insert_action', cls.get_insert_action())
            if not cls.hide_top_toolbar:
                cls.delete_action = cls._bind_action(
                    'delete_action', actions.DeleteSelected())
            cls.update_action = cls._bind_action(
                'update_action', actions.SaveGridCell())
            if cls.detail_layout:
                cls.validate_form = cls._bind_action(
                    'validate_form', actions.ValidateForm())

        if is_string(cls.workflow_owner_field):
        # if isinstance(cls.workflow_owner_field, string_types):
            cls.workflow_owner_field = cls.get_data_elem(
                cls.workflow_owner_field)
        if is_string(cls.workflow_state_field):
        # if isinstance(cls.workflow_state_field, string_types):
            fld = cls.get_data_elem(cls.workflow_state_field)
            if fld is None:
                raise Exception(
                    "Failed to resolve {}.workflow_state_field {}".format(
                        cls,cls.workflow_state_field))
            cls.workflow_state_field = fld


        # note that the fld may be None e.g. cal.Component
        if cls.workflow_state_field is not None:
            for a in cls.workflow_state_field.choicelist.workflow_actions:
                setattr(cls, a.action_name, a)

        # Bind all my actions, including those inherited from parent actors.
        # Allow disabling inherited actions by setting them to None in subclass.

        for b in cls.mro():
            for k, v in b.__dict__.items():
                v = cls.__dict__.get(k, v)
                if isinstance(v, actions.Action):
                    cls._bind_action(k, v)

        cls._actions_list.sort(
            key=lambda a: (a.action.sort_index, a.action.action_name))
        # cls._actions_list = tuple(cls._actions_list)

        # build a dict which maps state.name to a set of action names
        # to be disabled on objects having that state:
        cls._state_to_disabled_actions = {}
        wsf = cls.workflow_state_field
        if wsf is not None:
            st2da = cls._state_to_disabled_actions
            for state in wsf.choicelist.get_list_items():
                st2da[state.name] = set()
            for a in wsf.choicelist.workflow_actions:
                st2da[a.target_state.name].add(a.action_name)
            if wsf.choicelist.ignore_required_states:
                # raise Exception("20181107")
                # logger.info("20181107 %s", st2da)
                # from pprint import pprint
                # pprint(st2da)
                return
            for ba in cls._actions_list:
                # st2da[ba] = 1
                if ba.action.action_name:
                    required_states = ba.action.required_states
                    if required_states:
                        # if an action has required states, then it must
                        # get disabled for all other states:
                        if is_string(required_states):
                            required_states = set(required_states.split())
                        for k in st2da.keys():
                            if k not in required_states:
                                st2da[k].add(ba.action.action_name)


    @classmethod
    def _bind_action(cls, k, a):
        # for internal use during _collect_actions()
        if not a.attach_to_actor(cls, k):
            return
        # if str(cls) == "integ.ActivityReport": # and a.__class__.__name__ == "ShowDetail":
        #     print("20190110", k, a.action_name)

        try:
            ba = BoundAction(cls, a)
        except Exception as e:
            raise Exception("Cannot bind {!r} to {!r} : {}".format(
                a, cls, e))

        names = [k]
        if a.action_name and a.action_name != k:
            names.append(a.action_name)

        for name in names:
            if name in cls._actions_dict:
                old = cls._actions_dict[name]
                cls._actions_list.remove(old)

        for name in names:
            cls._actions_dict[name] = ba
        cls._actions_list.append(ba)

        # setattr(cls, k, ba)
        return ba


    @classmethod
    def get_default_action(cls):
        pass

    @classmethod
    def get_insert_action(cls):
        return actions.ShowInsert()

    @classmethod
    def get_label(self):
        return self.label
        # return self._label  # 20200307

    @classmethod
    def get_actor_label(self):
        """Compute the label of this actor.

        """
        return self._label or self.__name__

    @classmethod
    def get_detail_title(self, ar, obj):
        """Return the string to use when building the title of a detail
        window on a given row of this actor.

        """
        return str(obj)

    @classmethod
    def get_card_title(self, ar, obj):
        return self.get_detail_title(ar, obj)

    @classmethod
    def get_main_card(self, ar,):
        return None

    @classmethod
    def get_choices_text(self, obj, request, field):
        """
        Return the text to be displayed in a combo box
        for the field `field` of this actor to represent
        the choice `obj`.
        Override this if you want a customized representation.
        For example :class:`lino_voga.models.InvoiceItems`

        """
        return obj.get_choices_text(request, self, field)

    @classmethod
    def get_title(self, ar):
        """Return the title of this actor for the given action request `ar`.

        The default implementation calls :meth:`get_title_base` and
        :meth:`get_title_tags` and returns a string of type `BASE [
        (TAG, TAG...)]`.

        Override this if your table's title should mention for example
        filter conditions.  See also :meth:`Table.get_title
        <lino.core.dbtables.Table.get_title>`.

        """
        title = self.get_title_base(ar)
        # tags = list(self.get_title_tags(ar))
        tags = [str(t) for t in self.get_title_tags(ar)]
        if len(tags):
            title += " (%s)" % (', '.join(tags))
        return title

    @classmethod
    def get_title_base(self, ar):
        """
        Return the base part of the title. This should be a translatable
        string. This is called by :meth:`get_title` to construct the
        actual title.

        It is also called by
        :meth:`lino.core.dashboard.DashboardItem.render_request`
        """
        title = self.title or self.label
        # if self.master is not None:
        if ar.master_instance is not None:
            title = self.details_of_master_template % dict(
                details=title,
                master=ar.master_instance)
        return title

    @classmethod
    def get_title_tags(self, ar):
        """
        Yield a list of translatable strings to be added to the base part
        of the title. This is called by :meth:`get_title` to construct
        the actual title.
        """
        if isinstance(self.parameters, ParameterPanel):
            for t in self.parameters.get_title_tags(ar):
                yield t
        for k in self.simple_parameters:
            v = getattr(ar.param_values, k)
            if v:
                yield str(self.parameters[k].verbose_name) + ' ' + str(v)

    @classmethod
    def setup_request(self, ar):
        """Customized versions may e.g. set `master_instance` before calling
        super().

        Used e.g. by :class:`lino_xl.lib.outbox.models.MyOutbox` or
        :class:`lino.modlib.users.ByUser`.

        Other usages are more hackerish:

        - :class:`lino_xl.lib.households.models.SiblingsByPerson`
        - :class:`lino_welfare.modlib.cal.EntriesByClient`
        - :class:`lino_welfare.pcsw.models.Home`,
        - :class:`lino.modlib.users.MySettings`.

        """
        pass

    @classmethod
    def setup_parameters(cls, params):
        """Inheritable hook for defining parameters. Called once per actor at
        site startup.  The default implementation just calls
        :meth:`setup_parameters
        <lino.core.model.Model.setup_parameters>` of the
        :attr:`model` (if a :attr:`model` is set).

        """
        if cls.model is None:
            return
        if not isinstance(cls.model, type):
            raise Exception("{}.model is {!r} (must be a class)".format(cls, cls.model))
        if issubclass(cls.model, fields.TableRow):
            cls.model.setup_parameters(params)

    @classmethod
    def get_simple_parameters(cls):
        """Inheritable hook for defining which parameters are simple.
        Expected to return a list of names of parameter fields.

        """
        if isinstance(cls.model, type) and issubclass(cls.model, fields.TableRow):
            return cls.model.get_simple_parameters()
        return []

    @classmethod
    def get_param_elem(self, name):
        # same as in Parametrizable, but here it is a class method
        if self.parameters:
            return self.parameters.get(name, None)
        return None

    @classmethod
    def check_params(cls, pv):
        # same as in Parametrizable, but here it is a class method
        if isinstance(cls.parameters, ParameterPanel):
            return cls.parameters.check_values(pv)

    @classmethod
    def get_row_state(self, obj):
        if self.workflow_state_field is not None:
            return getattr(obj, self.workflow_state_field.name)
            #~ if isinstance(state,choicelists.Choice):
                #~ state = state.value

    @fields.displayfield(_("Description"))
    def detail_link(cls, obj, ar):
        if ar is None:
            return ''
            # return str(self)
        return E.div(*forcetext([ar.obj2html(obj)]))

    # @classmethod
    # def disabled_actions(self, ar, obj):  # no longer used since 20170909
    #     """
    #     Returns a dictionary containg the names of the actions
    #     that are disabled  for the given object instance `obj`
    #     and the user who issued the given ActionRequest `ar`.

    #     Application developers should not need to override this method.

    #     Default implementation returns an empty dictionary.
    #     Overridden by :class:`dd.Table`

    #     """
    #     return {}

    @classmethod
    def override_column_headers(self, ar, **kwargs):
        """A hook to dynamically override the column headers. This has no
        effect on a GridPanel, only in printed documents or plain
        html.

        """
        return kwargs

    @classmethod
    def get_sum_text(self, ar, sums):
        """
        Return the text to display on the totals row.
        The default implementation returns "Total (N rows)".
        """
        return str(_("Total (%d rows)") % ar.get_total_count())

    @classmethod
    def get_layout_aliases(cls):
        """

        Yield a series of (ALIAS, repl) tuples that cause a name ALIAS in a
        layout based on this actor to be replaced by its replacement `repl`.

        """
        return []

    @classmethod
    def set_detail_layout(self, *args, **kw):
        """Update the :attr:`detail_layout` of this actor, or create a new
        layout if there wasn't one before.

        This is maybe deprecated. See :ticket:`526`.

        The first argument can be either a string or a
        :class:`FormLayout <lino.core.layouts.FormLayout>` instance.
        If it is a string, it will replace the currently defined
        'main' panel.  With the special case that if the current `main`
        panel is horizontal (i.e. the layout has tabs), it replaces the
        'general' tab.

        Typical usage example::

            @dd.receiver(dd.post_analyze)
            def my_details(sender, **kw):
                contacts = sender.modules.contacts
                contacts.Partners.set_detail_layout(PartnerDetail())

        """
        return self.set_form_layout(
            'detail_layout', layouts.DetailLayout, *args, **kw)

    @classmethod
    def set_insert_layout(self, *args, **kw):
        """
        Update the :attr:`insert_layout` of this actor,
        or create a new layout if there wasn't one before.

        Otherwise same usage as :meth:`set_detail_layout`.

        """
        return self.set_form_layout(
            'insert_layout', layouts.InsertLayout, *args, **kw)

    @classmethod
    def set_form_layout(self, attname, lcl, dtl=None, **kw):
        if dtl is not None:
            existing = getattr(self, attname)  # 20120914c
            if is_string(dtl):
            # if isinstance(dtl, string_types):
                if existing is None:
                    setattr(self, attname, lcl(dtl, self, **kw))
                # if existing is None or isinstance(existing, string_types):
                #     if kw:
                #         setattr(self, attname, layouts.FormLayout(
                #             dtl, self, **kw))
                #     else:
                #         setattr(self, attname, dtl)
                    return
                if '\n' in dtl and '\n' not in existing.main:
                    name = 'general'
                else:
                    name = 'main'
                if name in kw:
                    raise Exception(
                        "set_detail() got two definitions for %r." % name)
                kw[name] = dtl
            else:
                if not isinstance(dtl, lcl):
                    msg = "{} is neither a string nor a layout".format(
                        type(dtl))
                    raise Exception(msg)
                assert dtl._datasource is None
                # added for 20120914c but it wasn't the problem
                # if existing and not isinstance(existing, string_types):
                if existing and not is_string(existing):
                    if settings.SITE.strict_dependencies:
                        if not isinstance(dtl, existing.__class__):
                            raise Exception(
                                "Cannot replace existing %s %r by %r" % (
                                    attname, existing, dtl))
                    if existing._added_panels:
                        if '\n' in dtl.main:
                            raise NotImplementedError(
                                "Cannot replace existing %s with added panels %s" % (existing, existing._added_panels))
                        dtl.main += ' ' + \
                            (' '.join(list(existing._added_panels.keys())))
                        #~ logger.info('20120914 %s',dtl.main)
                        dtl._added_panels.update(existing._added_panels)
                    dtl._element_options.update(existing._element_options)
                dtl._datasource = self
                setattr(self, attname, dtl)
        if kw:
            getattr(self, attname).update(**kw)

    @classmethod
    def add_detail_panel(self, *args, **kw):
        """
        Adds a panel to the Detail of this actor.
        Arguments: see :meth:`lino.core.layouts.BaseLayout.add_panel`

        This is deprecated. Use mixins instead.

        """
        self.detail_layout.add_panel(*args, **kw)

    @classmethod
    def add_detail_tab(self, *args, **kw):
        """
        Adds a tab panel to the Detail of this actor.
        See :meth:`lino.core.layouts.BaseLayout.add_tabpanel`

        This is deprecated. Use mixins instead.

        """
        if self.detail_layout is None:
            raise Exception("{} has no detail_layout".format(self))
        self.detail_layout.add_tabpanel(*args, **kw)

    @classmethod
    def add_virtual_field(cls, name, vf):
        if False:
            # disabled because UsersWithClients defines virtual fields
            # on connection_created
            if name in cls.virtual_fields:
                raise Exception("Duplicate add_virtual_field() %s.%s" %
                                (cls, name))
        # assert vf.model is None
        # if vf.model is not None:
        #     # inherit from parent actor
        #     vf = copy.deepcopy(vf)
        # if name in cls.virtual_fields:
        #     old = cls.virtual_fields[name]
        #     if old is not vf:
        #         print("20190102 {} of {} replaces {} by {}".format(name, cls, old, vf))
        if vf.model is None:
            vf.model = cls
        elif not issubclass(cls, vf.model):
            msg = "20190201 Cannot add field {} defined in {} to {}"
            msg = msg.format(name, vf.model, cls)
            # print(msg)
            raise Exception(msg)
        vf.name = name
        # vf.attname = name
        cls.virtual_fields[name] = vf

        #~ vf.lino_resolve_type(cls,name)
        # vf.get = vf.get
        # vf.get = curry(vf.get, cls)
        # vf.get = classmethod(vf.get)
        # vf.get = curry(classmethod(vf.get), cls)
        #~ for k,v in self.virtual_fields.items():
            #~ if isinstance(v,models.ForeignKey):
                #~ v.rel.model = resolve_model(v.rel.model)

    @classmethod
    def add_constant(cls, name, vf):
        cls._constants[name] = vf
        vf.name = name

    @classmethod
    def after_site_setup(cls, site):
        self = cls
        #~ raise "20100616"
        #~ assert not self._setup_done, "%s.setup() called again" % self
        if self._setup_done:
            return True
        if self._setup_doing:
            if True:  # severe error handling
                raise Exception("%s.setup() called recursively" % self)
            else:
                logger.warning("%s.setup() called recursively" % self)
                return False
        self._setup_doing = True

        # logger.info("20181230 Actor.after_site_setup() %r", self)

        for vf in self.virtual_fields.values():
            if vf.model is self:
                vf.get = curry(vf.get, self)
                # settings.SITE.register_virtual_field(vf)

        if not self.is_abstract():
            actions.register_params(self)

            self._collect_actions()

        if not self.is_abstract():
            actions.setup_params_choosers(self)

        #~ logger.info("20130906 Gonna Actor.do_setup() on %s", self)
        self.do_setup()
        #~ self.setup_permissions()
        self._setup_doing = False
        self._setup_done = True
        #~ logger.info("20130906 Actor.after_site_setup() done: %s, default_action is %s",
            #~ self.actor_id,self.default_action)
        return True

    @classmethod
    def get_action_by_name(self, name):
        return self._actions_dict.get(name, None)
    get_url_action = get_action_by_name

    @classmethod
    def get_url_action_names(self):
        return list(self._actions_dict.keys())

    @classmethod
    def get_toolbar_actions(self, parent):
        """
        Return a list of actions for which a button should exist in the
        toolbar of the specified "parent" action.
        """
        return [ba for ba in self.get_button_actions(parent)
                if ba.action.show_in_bbar]
                # if ba.action.select_rows]

    # @classmethod
    # def get_cell_context_actions(self, cf):
    #     cca = dict()
    #     for col in self.columns:
    #         if it is a FK field::
    #             f = col.editor
    #             cca[f.name] = f.rel.to.detail_action
    #     return cca

    @classmethod
    def get_button_actions(self, parent):
        """
        Return a sorted list of actions that should be available as
        buttons in the specified `parent` (a window action).

        This is used (1) by :meth:`get_toolbar_actions` and (2) to
        reduce the list of disabled actions in `disabled_fields` to
        those which make sense.  `dbtables.make_disabled_fields`
        """
        if not parent.opens_a_window:
            # return []
            raise Exception("20180518 {} is not a windows action".format(
                parent.__class__))
        return [ba for ba in self._actions_list
                if ba.action.is_callable_from(parent)]

    @classmethod
    def get_actions(self):
        """
        Return a sorted list of all bound actions offered by this actor.
        """
        return self._actions_list

    @classmethod
    def make_chooser(cls, wrapped):
        return classmethod(wrapped)

    @classmethod
    def get_detail_layout(cls, *args):
        assert cls.detail_action is not None
        wl = cls.detail_action.get_window_layout()
        return wl.get_layout_handle(*args)

    @classmethod
    def get_list_layout(cls, *args):
        assert cls.default_action is not None
        ah = cls.get_handle()
        return ah.get_list_layout()
        # return ll.get_layout_handle(*args)

    @classmethod
    def get_detail_elems(cls, *args):
        """
        An optional first argument is the user interface plugin, a
        :class:`Plugin` instance.  If this is None, will use
        :attr:`settings.SITE.kernel.default_ui
        <lino.core.kernel.Kernel.default_ui>`.

        Returns a list of the widgets (layout elements) that make up
        the detail layout.
        """
        lh = cls.get_detail_layout(*args)
        return lh.main.elements

    @classmethod
    def get_data_elem(self, name):
        """Find data element in this actor by name.

        """
        c = self._constants.get(name, None)
        if c is not None:
            return c
        #~ return self.virtual_fields.get(name,None)

        # Note that there are models with fields named 'master', 'app_label',
        # 'model' (i.e. a name that is also used as attribute of an actor.

        vf = self.virtual_fields.get(name, None)
        if vf is not None:
            #~ logger.info("20120202 Actor.get_data_elem found vf %r",vf)
            return vf

        if self.model is not None:
            de = self.model.get_data_elem(name)
            if de is not None:
                return de

        a = getattr(self, name, None)
        if isinstance(a, actions.Action):
            return a
        # if isinstance(a, fields.VirtualField):
        #     return a
        if isinstance(a, fields.DummyField):
            return a
        # if a is not None:
        #     raise Exception("20190102 unhandled attribute {}={}".format(name, a))

        # cc = AbstractTable.get_data_elem(self,name)

        #~ logger.info("20120307 lino.core.coretools.get_data_elem %r,%r",self,name)
        s = name.split('.')
        # site = settings.SITE
        if len(s) == 1:
            m = settings.SITE.models.get(self.app_label)
            if m is None:
                raise Exception("No plugin %s" % self.app_label)
                # return None
            rpt = getattr(m, name, None)
            # if rpt is None and name != name.lower():
            #     raise Exception("20140920 No %s in %s" % (name, m))
        elif len(s) == 2:
            m = settings.SITE.models.get(s[0])
            if m is None:
                # return fields.DummyField()
                # 20130422 Yes it was a nice idea to silently
                # ignore non installed app_labels, but mistakenly
                # specifying "person.first_name" instead of
                # "person__first_name" did not raise an error...
                # raise Exception("No plugin %s is installed" % s[0])
                # See docs/specs/welfare/xcourses.rst
                return None
            rpt = getattr(m, s[1], None)
        else:
            raise Exception("Invalid data element name %r" % name)
        return rpt

    @classmethod
    def param_defaults(self, ar, **kw):
        """
        Return a dict with default values for the :attr:`parameters`.
        This will be called per request.

        Usage example. The Clients table has a parameter `coached_since`
        whose default value is empty::

          class Clients(dd.Table):
              parameters = dd.ParameterPanel(
                ...
                coached_since=models.DateField(blank=True))

        But `NewClients` is a subclass of `Clients` with the only
        difference that the default value is `amonthago`::

          class NewClients(Clients):
              @classmethod
              def param_defaults(self,ar,**kw):
                  kw = super(NewClients,self).param_defaults(ar,**kw)
                  kw.update(coached_since=amonthago())
                  return kw


        """
        for k, pf in self.parameters.items():
            # if not isinstance(pf, fields.DummyField):
            kw[k] = pf.get_default()
        return kw

    @classmethod
    def request(self, *args, **kw):
        """
        Return an action request on this actor.
        """
        kw.update(actor=self)
        return ActionRequest(*args, **kw)

    @classmethod
    def request_from(cls, ar, *args, **kwargs):
        """
        Return an action request on this actor which inherits from the
        given parent request.
        """
        sar = cls.request(*args, **kwargs)
        sar.setup_from(ar)
        return sar

    @classmethod
    def to_html(self, **kw):
        """
        """
        #~ settings.SITE.startup()
        return tostring(self.request(**kw).table2xhtml())

    @classmethod
    def get_screenshot_requests(self, language):
        """
        Return or yield a list of screenshots to generate for this actor.
        Not yet stable. Don't override this.
        Don't worry if you don't understand.
        """
        return []

    @classmethod
    def slave_as_html(cls, master, ar):
        """
        Creates and returns the method to be used when :attr:`display_mode`
        is `html`.
        """
        ar = cls.request(
            master, request=ar.request, param_values=ar.param_values if getattr(cls, "use_detail_params_value", False) else {},
            is_on_main_actor=False)
        ar.renderer = settings.SITE.kernel.default_renderer
        el = ar.table2xhtml()
        toolbar = ar.plain_toolbar_buttons()
        if len(toolbar):
            el = E.div(el, E.p(*toolbar))
        return el

    summary_sep = E.br

    @classmethod
    def get_table_summary(cls, obj, ar):
        """Return the HTML paragraph to be displayed by
        :class:`lino.core.elems.TableSummaryPanel`.  That is (1) in a
        detail form when :attr:`display_mode` is `summary` or (2)
        in a grid.

        Lino internally creates a virtualfield ``slave_summary`` on
        each table which invokes this method.

        """
        # ar = ar.spawn(self, master_instance=obj, is_on_main_actor=False)
        sar = ar.spawn_request(actor=cls, master_instance=obj, is_on_main_actor=False)
        # sar = cls.request_from(ar, master_instance=obj)
        p = qs2summary(sar, sar.data_iterator, cls.summary_sep)
        if cls.insert_action is not None:
            ir = cls.insert_action.request_from(sar)
            if ir.get_permission():
                btn = ir.ar2button()
                if len(p):
                    p.append(E.br())
                p.append(btn)
        return p

    @classmethod
    def error2str(self, e):
        return error2str(self, e)


def resolve_action(spec, action=None):
    """
    Return the `BoundAction` object corresponding to the given
    specifier `spec`. The specifier can be:

    - a model or a table
    - a bound action
    - an action instance
    - a string of the form ``myapp.MyModel`` (i.e. resolving to a model)
    - a string of the form ``myapp.MyModels`` (i.e. resolving to a table)

    If it is an action instance, Lino will use the
    :attr:`definiing_actor` of that action.

    """
    givenspec = spec

    # if isinstance(spec, string_types):
    if is_string(spec):
        site = settings.SITE
        spec = site.models.resolve(spec)
        # spec = site.actors.resolve(spec) or site.models.resolve(spec)

    if isinstance(spec, BoundAction):
        return spec

    if isinstance(spec, actions.Action):
        return spec.defining_actor.get_action_by_name(spec.action_name)

    if isinstance(spec, type) and issubclass(spec, models.Model):
        spec = spec.get_default_table()
        assert spec is not None

    if isinstance(spec, type) and issubclass(spec, Actor):
        if action:
            a = spec.get_url_action(action)
            #~ print 20121210, a
            if a is None:
                raise Exception(
                    "resolve_action(%r, %r) found None" % (spec, action))
        else:
            a = spec.default_action
            if a is None:
                raise Exception("%r default_action is None?!" % spec)
        return a

    raise Exception("Action spec %r returned invalid object %r" %
                    (givenspec, spec))
