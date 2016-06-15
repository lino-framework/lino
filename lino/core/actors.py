# -*- coding: UTF-8 -*-
# Copyright 2009-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""This defines :class:`Actor` and related classes.

See :doc:`/dev/actors`.


"""
from past.builtins import cmp
from builtins import str
# import six
# str = six.text_type
from past.builtins import basestring

import logging
from future.utils import with_metaclass
logger = logging.getLogger(__name__)

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
from lino.utils import curry, AttrDict
from lino.utils.xmlgen.html import E

from .roles import SiteUser

actor_classes = []
actors_dict = None
actors_list = None

ACTOR_SEP = '.'


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
    if not settings.SITE.is_installed(a.app_label):
        # happens when sphinx autodoc imports a non installed module
        # logger.info("20150416 register_actor skipped %s", a)
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
        #~ if cls.is_abstract():
            #~ actions.register_params(cls)
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
        cls.actions = AttrDict()
        cls._actions_list = []  # 20121129

        # inherit virtual fields defined on parent Actors
        for b in bases:
            bd = getattr(b, 'virtual_fields', None)
            if bd:
                cls.virtual_fields.update(bd)

        if True:  # (20130817) tried to move this to a later moment
            for k, v in list(classDict.items()):
                cls.register_class_attribute(k, v)

        #~ if classname == 'Tasks':
            #~ logger.info("20130817 no longer added actor vfs")

        #~ cls.params = []
        #~ for k,v in classDict.items():
            #~ if isinstance(v,models.Field):
                #~ v.set_attributes_from_name(k)
                #~ v.table = cls
                #~ cls.params.append(v)
        #~ cls.install_params_on_actor()
        if classname not in (
                'Table', 'AbstractTable', 'VirtualTable',
                'Action', 'Actor', 'Frame',
                'ChoiceList', 'Workflow',
                'EmptyTable', 'Dialog'):
            if actor_classes is None:
                #~ logger.debug("%s definition was after discover",cls)
                pass
            elif not cls.__name__.startswith('unused_'):
                # ~ cls.class_init() # 20120115
                actor_classes.append(cls)
            #~ logger.debug("ActorMetaClass.__new__(%s)", cls)
        return cls

    def __str__(cls):
        return cls.actor_id

    @property
    def label(cls):
        return cls.get_actor_label()

    @property
    def known_values(cls):
        return cls.get_known_values()

    @property
    def editable(cls):
        return cls.get_actor_editable()


class Actor(with_metaclass(ActorMetaClass, type('NewBase', (actions.Parametrizable, Permittable), {}))):
    """The base class for all actors.  Subclassed by :class:`AbstractTable
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

    The following class methods are `None` in the default
    implementation. Subclass can define them.

    .. classmethod:: get_handle_name(self, ar)

        Most actors use the same UI handle for each request.  But
        e.g. :class:`lino_welfare.modlib.debts.models.PrintEntriesByBudget`
        overrides this to implement dynamic columns depending on it's
        master_instance.


    .. classmethod:: get_row_classes(self, ar)

        If a method of this name is defined on an actor, then it must
        be a class method which takes an :class:`ar
        <lino.core.requests.BaseRequest>` as single argument and
        returns either None or a string "red", "green" or "blue"
        (todo: add more colors and styles). Example::

            @classmethod
            def get_row_classes(cls,obj,ar):
                if obj.client_state == pcsw.ClientStates.newcomer:
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

    """

    required_roles = set([SiteUser])
    """See :attr:`lino.core.permissions.Permittable.required_roles`"""

    model = None
    """
    Set this on
    """

    actions = None
    """An :class:`AttrDict <atelier.utils.AttrDict>` containing the
    actions available on this actor.

    """

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
    """The name of a ForeignKey field of this table's :attr:`model` that
    points to it's :attr:`master`.  The :attr:`master_key` is
    automatically added to :attr:`hidden_columns`.

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
    """A set of names of filter parameters which are handled automatically.

    Application developers should normally not set this attribute but
    define a :meth:`get_simple_parameters` on the model.
    If you set this attribute yourself, then
    :meth:`get_simple_parameters` will not be called.

    """

    hidden_elements = frozenset()
    """A set of names of layoutelements which are hidden by default.

    The default is an empty set except for
    :class:`lino.core.dbtables.Table` where this will be populated from
    :attr:`hidden_elements <lino.core.model.Model.hidden_elements>`
    of the :class:`lino.core.model.Model`.
    """

    detail_html_template = 'bootstrap3/detail.html'
    """The template to be used for rendering a row of this actor as a
    detail html page.

    """
    list_html_template = 'bootstrap3/table.html'
    """The template to be used for rendering a collection of rows of this
    actor as a table html page.

    """

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
    :class:`changes.Changes<lino.modlib.changes.models.Changes>`
    table is an example where this is being used: nobody should
    ever edit something in the table of Changes.  The user
    interface uses this to generate optimized JS code for this
    case.

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
    If this is False, then then Actor won't have no insert_action.
    """

    hide_top_toolbar = False
    """
    Whether a Detail Window should have navigation buttons, a "New"
    and a "Delete" buttons.  In ExtJS UI also influences the title of
    a Detail Window to specify only the current element without
    prefixing the Tables's title.
    
    This option is True in
    :class:`lino.models.SiteConfigs`,
    :class:`lino_welfare.pcsw.models.Home`,
    :class:`lino.modlib.users.models.Mysettings`.

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
    """Define the form layout to use for the detail window.  Actors with
    :attr:`detail_layout` will automatocally get a `show_detail`
    action.

    When you define a :attr:`detail_layout`, you will probably also
    want to define a :attr:`insert_layout`.

    """

    insert_layout = None
    """Define the form layout to use for the insert window.  If there's a
    :attr:`detail_layout` but no :attr:`insert_layout`, Lino will use
    :attr:`detail_layout` for the insert window.

    """

    detail_template = None    # deprecated: use insert_layout instead
    insert_template = None    # deprecated: use detail_layout instead
    help_text = None
    detail_action = None
    update_action = None
    insert_action = None
    # create_action = None
    delete_action = None
    _handle_class = None  # For internal use.
    get_handle_name = None

    abstract = False
    """
    Set this to `True` to prevent Lino from generating useless
    JavaScript if this is just an abstract base class to be inherited
    by other actors.

    """
    sum_text_column = 0
    """The index of the column which should hold the text to display on
    the totals row (returned by :meth:`get_sum_text`).

    """

    sum_text_column = 0
    """The index of the column which should hold the text to display on
    the totals row (returned by :meth:`get_sum_text`).

    """

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
    def get_widget_options(self, name, **options):
        return options

    @classmethod
    def get_chooser_for_field(cls, fieldname):
        d = getattr(cls, '_choosers_dict', {})
        return d.get(fieldname, None)

    @classmethod
    def register_class_attribute(cls, k, v):
        if isinstance(v, fields.Constant):
            cls.add_constant(k, v)
        elif isinstance(v, fields.VirtualField):  # 20120903b
            cls.add_virtual_field(k, v)
        elif isinstance(v, models.Field):  # 20130910
            #~ print "20130910 add virtual field " ,k, cls
            vf = fields.VirtualField(v, field_getter(k))
            cls.add_virtual_field(k, vf)

    @classmethod
    def inject_field(cls, name, fld):
        # called from auth.add_user_group()
        setattr(cls, name, fld)
        cls.register_class_attribute(name, fld)

    @classmethod
    def get_pk_field(self):
        """Return the Django field object used to represent the primary key
        when filling `selected_pks`.

        """
        return None

    @classmethod
    def get_row_by_pk(self, ar, pk):
        """Return the data row identified by the given primary key.

        """
        return None

    @classmethod
    def get_master_instance(self, ar, model, pk):
        """Return the `master_instance` corresponding to the specified primary
        key.

        You need to override this only on slave actors whose
        :attr:`master` is something else than a database model,
        e.g. the :class:`ProblemsByChecker
        <lino.modlib.plausibility.models.ProblemsByChecker>` table.

        `ar` is the action request on this actor. `model` is the
        :attr:`master`, except if :attr:`master` is `ContentType` (in
        which case `model` is the *requested* master).

        """
        if issubclass(model, models.Model):
            try:
                return model.objects.get(pk=pk)
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
    def disabled_fields(cls, obj, ar):
        """
        Return a set of field names that should not be editable
        for the specified `obj` and `request`.

        If defined in the Actor, this must be a class method that accepts
        two arguments `obj` and `ar` (an `ActionRequest`)::

          @classmethod
          def disabled_fields(cls, obj, ar):
              ...
              return set()

        If not defined in the Table, Lino will look whether the Table's
        model has a `disabled_fields` method and install a wrapper to this
        model method.  When defined on the model, is must be an *instance*
        method::

          def disabled_fields(self, ar):
              ...
              return set()

        See also :srcref:`docs/tickets/2`.


        """
        return set()

    @classmethod
    def get_request_handle(self, ar):
        """Return the dynamic (per-request) handle for this actor for the
        renderer used by specified action request.  Don't override.

        """
        if self.get_handle_name is None:
            return self._get_handle(ar, _handle_attr_name)
        return self._get_handle(ar, self.get_handle_name(ar))

    @classmethod
    def is_valid_row(self, row):
        return False

    @classmethod
    def make_params_layout_handle(self, ui):
        return actions.make_params_layout_handle(self, ui)

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
        return obj.summary_row(ar, **kw)

    @classmethod
    def do_setup(self):
        pass

    @classmethod
    def get_handle(self):
        """Return a static handle for this actor for the given renderer."""
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
        if h is None:
            h = self._handle_class(self)
            setattr(self, hname, h)
            settings.SITE.kernel.setup_handle(h, ar)
        return h

    @classmethod
    def class_init(cls):
        """Called internally at site startup. Don't override.

        """
        # if str(cls) == 'courses.Pupils':
        #     print("20160329 class_init")
        if hasattr(cls, 'required'):
            raise ChangedAPI(
                "{0} must convert `required` to `required_roles`".format(cls))
        master = getattr(cls, 'master', None)
        if isinstance(master, basestring):
            cls.master = resolve_model(master)

        actions.install_layout(cls, 'detail_layout', layouts.DetailLayout)
        actions.install_layout(
            cls, 'insert_layout', layouts.InsertLayout,
            window_size=(cls.insert_layout_width, 'auto'))

        if cls.parameters is None:
            params = cls.get_parameter_fields()
            if len(params):
                cls.parameters = params
        else:
            cls.parameters = cls.get_parameter_fields(**cls.parameters)

        cls.simple_parameters = cls.get_simple_parameters()
        # if cls.simple_parameters is None:
        #     cls.simple_parameters = cls.get_simple_parameters()
        # else:
        #     raise ChangedAPI("20150829 {0}".format(cls))

    @classmethod
    def get_known_values(self):
        return self._known_values

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
    def get_view_permission(self, profile):
        """Return True if this actor as a whole is visible for users with the
        given profile.

        """
        # return isinstance(profile, tuple(self.required_roles))
        return True

    @classmethod
    def get_create_permission(self, ar):
        """Dynamic test per request.  This is being called only when
        :attr:`allow_create` is True.

        """
        if ar.get_user().profile.readonly:
            return False
        return True

    @classmethod
    def get_row_permission(cls, obj, ar, state, ba):
        """Returns True or False whether the given action request
        ActionRequest `ar` is allowed on the given row instance `row`.

        """
        if ba.action.readonly:
            return True
        if ar.get_user().profile.readonly:
            return False
        return cls.editable

    @classmethod
    def _collect_actions(cls):
        """
        Loops through the class dict and collects all Action instances,
        calling `_attach_action` which will set their `actor` attribute.
        Before this we create `insert_action` and `detail_action` if necessary.
        Also fill _actions_list.
        """

        default_action = cls.get_default_action()

        if default_action is not None:
            cls.default_action = cls.bind_action(default_action)

        if cls.detail_layout:
            if default_action and isinstance(
                    default_action, actions.ShowDetailAction):
                cls.detail_action = cls.bind_action(default_action)
            else:
                cls.detail_action = cls.bind_action(actions.ShowDetailAction())
            if cls.editable:
                cls.submit_detail = cls.bind_action(actions.SubmitDetail())

        if cls.editable:
            if cls.allow_create:
                # cls.create_action = cls.bind_action(actions.SubmitInsert())
                if cls.detail_action and not cls.hide_top_toolbar:
                    cls.insert_action = cls.bind_action(actions.InsertRow())
            if not cls.hide_top_toolbar:
                cls.delete_action = cls.bind_action(actions.DeleteSelected())
            cls.update_action = cls.bind_action(actions.SaveRow())
            if cls.detail_layout:
                cls.validate_form = cls.bind_action(actions.ValidateForm())

        if isinstance(cls.workflow_owner_field, basestring):
            cls.workflow_owner_field = cls.get_data_elem(
                cls.workflow_owner_field)

        #~ if isinstance(cls.workflow_state_field,basestring):
            #~ fld = cls.get_data_elem(cls.workflow_state_field)
            # ~ if fld is not None: # e.g. cal.Component
                #~ cls.workflow_state_field = fld
                #~ for name,a in cls.get_state_actions():
                    #~ print 20120709, cls,name,a
                    #~ setattr(cls,name,a)

        if isinstance(cls.workflow_state_field, basestring):
            cls.workflow_state_field = cls.get_data_elem(
                cls.workflow_state_field)
            #~ note that fld may be None e.g. cal.Component
        if cls.workflow_state_field is not None:
            for a in cls.workflow_state_field.choicelist.workflow_actions:
                setattr(cls, a.action_name, a)

        # bind all my actions, including those inherited from parent actors:
        for b in cls.mro():
            for k, v in list(b.__dict__.items()):
                # Allow disabling inherited actions by setting them to
                # None in subclass.
                v = cls.__dict__.get(k, v)
                if isinstance(v, actions.Action):
                    if not k in cls.actions:
                        if v.attach_to_actor(cls, k):
                            cls.bind_action(v)

        def f(a, b):
            return cmp(a.action.sort_index, b.action.sort_index)
        # cls._actions_list.sort(f)
        from functools import cmp_to_key
        cls._actions_list.sort(key=cmp_to_key(f))
        cls._actions_list = tuple(cls._actions_list)

    @classmethod
    def bind_action(self, a):
        ba = BoundAction(self, a)
        if a.action_name is not None:
            self.actions.define(a.action_name, ba)
        self._actions_list.append(ba)
        return ba

    @classmethod
    def get_default_action(cls):
        pass

    @classmethod
    def get_label(self):
        return self.label

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

        Override this if your Table's title should mention for example
        filter conditions.  See also :meth:`Table.get_title
        <lino.core.dbtables.Table.get_title>`.

        """
        # NOTE: similar code in dbtables
        title = self.get_title_base(ar)
        tags = list(self.get_title_tags(ar))
        if len(tags):
            title += " (%s)" % (', '.join(tags))
        return title

    @classmethod
    def get_title_base(self, ar):
        """Return the base part of the title. This should be a translatable
        string. This is called by :meth:`get_title` to construct the
        actual title.

        """
        title = self.title or self.label
        if self.master is not None:
            title = self.details_of_master_template % dict(
                details=title,
                master=ar.master_instance)
        return title

    @classmethod
    def get_title_tags(self, ar):
        """Yield a list of translatable strings to be added to the base part
        of the title. This is called by :meth:`get_title` to construct
        the actual title.

        """
        for k in self.simple_parameters:
            v = getattr(ar.param_values, k)
            if v:
                yield str(self.parameters[k].verbose_name) \
                    + ' ' + str(v)

    @classmethod
    def setup_request(self, ar):
        """Customized versions may e.g. set `master_instance` before calling
        super().

        Used e.g. by :class:`lino_xl.lib.outbox.models.MyOutbox` or
        :class:`lino.modlib.users.mixins.ByUser`.

        Other usages are more hackerish:

        - :class:`lino_xl.lib.households.models.SiblingsByPerson`
        - :class:`lino_welfare.modlib.cal.models.EventsByClient`
        - :class:`lino_welfare.pcsw.models.Home`,
        - :class:`lino.modlib.users.models.MySettings`.

        """
        pass

    @classmethod
    def get_parameter_fields(cls, **fields):
        """Inheritable hook for defining parameters. Called once per actor at
        site startup.  The default implementation just calls
        :meth:`get_parameter_fields
        <lino.core.model.Model.get_parameter_fields>` of the
        :attr:`model` (if a :attr:`model` is set).

        """
        if cls.model is None:
            return fields
        return cls.model.get_parameter_fields(**fields)

    @classmethod
    def get_simple_parameters(cls):
        """Inheritable hook for defining which parameters are simple.
        Expected to return a set of names of parameter fields.

        """
        if cls.model is None:
            return set([])
        return cls.model.get_simple_parameters()

    @classmethod
    def get_param_elem(self, name):
        # same as in Parametrizable, but here it is a class method

        if self.parameters:
            return self.parameters.get(name, None)
        return None

    @classmethod
    def get_row_state(self, obj):
        if self.workflow_state_field is not None:
            return getattr(obj, self.workflow_state_field.name)
            #~ if isinstance(state,choicelists.Choice):
                #~ state = state.value

    @classmethod
    def disabled_actions(self, ar, obj):
        """
        Returns a dictionary containg the names of the actions
        that are disabled  for the given object instance `obj`
        and the user who issued the given ActionRequest `ar`.

        Application developers should not need to override this method.

        Default implementation returns an empty dictionary.
        Overridden by :class:`dd.Table`

        """
        return {}

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
        return self.set_form_layout('detail_layout', *args, **kw)

    @classmethod
    def set_insert_layout(self, *args, **kw):
        """
        Update the :attr:`insert_layout` of this actor,
        or create a new layout if there wasn't one before.

        Otherwise same usage as :meth:`set_detail_layout`.

        """
        return self.set_form_layout('insert_layout', *args, **kw)

    @classmethod
    def set_form_layout(self, attname, dtl=None, **kw):
        if dtl is not None:
            existing = getattr(self, attname)  # 20120914c
            if isinstance(dtl, basestring):
                if existing is None:
                    setattr(self, attname, layouts.FormLayout(
                        dtl, self, **kw))
                # if existing is None or isinstance(existing, basestring):
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
                assert isinstance(dtl, layouts.FormLayout)
                assert dtl._datasource is None
                # added for 20120914c but it wasn't the problem
                if existing and not isinstance(existing, basestring):
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
        self.detail_layout.add_tabpanel(*args, **kw)

    @classmethod
    def add_virtual_field(cls, name, vf):
        # disabled because UsersWithClients defines virtual fields on
        # connection_created
        if False:
            if name in cls.virtual_fields:
                raise Exception("Duplicate add_virtual_field() %s.%s" %
                                (cls, name))
        cls.virtual_fields[name] = vf
        #~ vf.lino_resolve_type(cls,name)
        vf.name = name
        vf.get = curry(vf.get, cls)
        #~ for k,v in self.virtual_fields.items():
            #~ if isinstance(v,models.ForeignKey):
                #~ v.rel.model = resolve_model(v.rel.model)

    @classmethod
    def add_constant(cls, name, vf):
        cls._constants[name] = vf
        vf.name = name

    @classmethod
    def after_site_setup(self, site):
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
        #~ logger.info("20130219 Actor.after_site_setup() %s", self)
        self._setup_doing = True

        if not self.is_abstract():
            actions.register_params(self)

        self._collect_actions()

        #~ Parametrizable.after_site_setup(self)
        #~ super(Actor,self).after_site_setup(site)
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
        return self.actions.get(name, None)
    get_url_action = get_action_by_name

    @classmethod
    def get_url_action_names(self):
        return list(self.actions.keys())

    @classmethod
    def get_toolbar_actions(self, cf):
        return [ba for ba in self.get_actions(cf)
                if ba.action.show_in_bbar]
                # if ba.action.select_rows]
        
    @classmethod
    def get_actions(self, callable_from=None):
        if callable_from is None:
            return self._actions_list
        return [ba for ba in self._actions_list
                if ba.action.is_callable_from(callable_from)]

    @classmethod
    def make_chooser(cls, wrapped):
        return classmethod(wrapped)
    
    @classmethod
    def get_data_elem(self, name):
        """Find data element in this actor by name.

        """
        c = self._constants.get(name, None)
        if c is not None:
            return c
        #~ return self.virtual_fields.get(name,None)
        vf = self.virtual_fields.get(name, None)
        if vf is not None:
            #~ logger.info("20120202 Actor.get_data_elem found vf %r",vf)
            return vf

        a = getattr(self, name, None)
        if isinstance(a, actions.Action):
            return a
        if isinstance(a, fields.DummyField):
            return a

        #~ logger.info("20120307 lino.core.coretools.get_data_elem %r,%r",self,name)
        s = name.split('.')
        if len(s) == 1:
            #~ app_label = model._meta.app_label
            m = settings.SITE.modules[self.app_label]
            if m is None:
                raise Exception("No module %s" % self.app_label)
                return None
            rpt = getattr(m, name, None)
            # if rpt is None and name != name.lower():
            #     raise Exception("20140920 No %s in %s" % (name, m))
        elif len(s) == 2:
            m = settings.SITE.modules.get(s[0], None)
            if m is None:
                # return fields.DummyField()
                # 20130422 Yes it was a nice idea to silently
                # ignore non installed app_labels, but mistakenly
                # specifying "person.first_name" instead of
                # "person__first_name" did not raise an error...
                # raise Exception("No module %s" % s[0])
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
        for k, pf in list(self.parameters.items()):
            # if not isinstance(pf, fields.DummyField):
            kw[k] = pf.get_default()
        return kw

    @classmethod
    def request(self, *args, **kw):
        """Return an :class:`ActionRequest <lino.core.requests.ActionRequest>`
        on this actor.

        """
        kw.update(actor=self)
        return ActionRequest(*args, **kw)

    @classmethod
    def request_from(self, ar, *args, **kw):
        sar = self.request(*args, **kw)
        sar.setup_from(ar)
        return sar

    @classmethod
    def to_html(self, **kw):
        """
        """
        #~ settings.SITE.startup()
        return E.tostring(self.request(**kw).table2xhtml())

    @classmethod
    def get_screenshot_requests(self, language):
        """
        Return or yield a list of screenshots to generate for this actor.
        Not yet stable. Don't override this.
        Don't worry if you don't understand.
        """
        return []

    @classmethod
    def slave_as_html_meth(self):
        """Creates and returns the method to be used when
        :attr:`slave_grid_format` is `html`.

        """
        def meth(master, ar):
            #~ ar = self.request(ui,request=ar.request,
                #~ master_instance=master,param_values={})
            ar = self.request(master, request=ar.request, param_values={})
            ar.renderer = settings.SITE.kernel.default_renderer
            #~ s = ui.table2xhtml(ar).tostring()
            return ar.table2xhtml()
            #~ s = etree.tostring(ui.table2xhtml(ar))
            #~ return s
        return meth

    summary_sep = E.br

    @classmethod
    def get_slave_summary(self, obj, ar):
        """Return the HTML paragraph to be displayed by
        :class:`lino.core.elems.TableSummaryPanel`.  That is (1) in a
        detail form when :attr:`slave_grid_format` is `summary` or (2)
        in a grid.

        Lino internally creates a virtualfield ``slave_summary`` on
        each table which invokes this method.

        """
        ar = ar.spawn(self, master_instance=obj)
        return qs2summary(ar, ar.data_iterator, self.summary_sep)

    @classmethod
    def error2str(self, e):
        return error2str(self, e)


def resolve_action(spec, action=None):
    """Return the `BoundAction` object corresponding to the given
    specifier `spec`. The specifier can be:

    - a model or a table
    - a string of the form ``myapp.MyModel`` (i.e. resolving to a model)
    - a string of the form ``myapp.MyModels`` (i.e. resolving to a table)

    """
    givenspec = spec

    if isinstance(spec, basestring):
        spec = settings.SITE.modules.resolve(spec)
        #~ if a is None:
            #~ raise Exception("Could not resolve action specifier %r" % spec)

    if isinstance(spec, BoundAction):
        return spec

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

    
