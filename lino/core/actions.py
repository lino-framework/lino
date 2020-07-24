# -*- coding: UTF-8 -*-
# Copyright 2009-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""This defines the :class:`Action` class and the :func:`action`
decorator, and some of the standard actions.  See :ref:`dev.actions`.

"""

import logging; logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as gettext
from django.utils.text import format_lazy
from django.utils.encoding import force_text
from django.conf import settings
from django.db import models

from django.apps import apps ; get_models = apps.get_models

from lino.core import constants
from lino.core import layouts
from lino.core import fields
from lino.core import keyboard
from lino.modlib.users.utils import get_user_profile
from lino.utils.choosers import check_for_chooser

from .permissions import Permittable
from .utils import obj2unicode
from .utils import resolve_model
from .utils import navinfo
from .utils import Parametrizable
from .utils import traverse_ddh_fklist
from .requests import InstanceAction

def discover_choosers():
    logger.debug("Discovering choosers for model fields...")
    # ~ logger.debug("Instantiate model reports...")
    for model in get_models():
        # ~ n = 0
        allfields = model._meta.fields
        for field in allfields:
            check_for_chooser(model, field)
        # ~ logger.debug("Discovered %d choosers in model %s.",n,model)


def install_layout(cls, k, layout_class, **options):
    """
    - `cls` is the actor (a class object)
    - `k` is one of 'detail_layout', 'insert_layout', 'params_layout', 'card_layout'
    - `layout_class`

    """
    # if str(cls) == 'courses.Pupils':
    #     print("20160329 install_layout", k, layout_class)
    dl = cls.__dict__.get(k, None)
    if dl is None:  # and not cls._class_init_done:
        dl = getattr(cls, k, None)
    if dl is None:
        return
    if isinstance(dl, str):
        if '\n' in dl or not '.' in dl:
            setattr(cls, k, layout_class(dl, cls, **options))
        else:
            layout_class = settings.SITE.models.resolve(dl)
            if layout_class is None:
                raise Exception("Unresolved {} {!r} for {}".format(k, dl, cls))
            setattr(cls, k, layout_class(None, cls, **options))
    elif isinstance(dl, layouts.Panel):
        options.update(dl.options)
        setattr(cls, k, layout_class(dl.desc, cls, **options))
    else:
        if not isinstance(dl, layout_class):
            if not isinstance(cls, type):
                # cls is an action instance
                cls = cls.__class__
            msg = "{}.{}.{} must be a string, " \
                  "a Panel or an instance of {} (not {!r})"
            raise Exception(msg.format(
                cls.__module__, cls.__name__, k, layout_class.__name__, dl))
        if dl._datasource is None:
            dl.set_datasource(cls)
            setattr(cls, k, dl)
        elif not issubclass(cls, dl._datasource):
            raise Exception(
                "Cannot reuse %s instance (%s of %r) for %r" %
                (dl.__class__, k, dl._datasource, cls))


def register_params(cls):
    """`cls` is either an actor (a class object) or an action (an
    instance).

    """
    if cls.parameters:
        for k, v in cls.parameters.items():
            v.set_attributes_from_name(k)
            v.table = cls
            # v.model = cls  # 20181023 experimentally

        if cls.params_layout is None:
            cls.params_layout = cls._layout_class.join_str.join(
                cls.parameters.keys())
        install_layout(cls, 'params_layout', cls._layout_class)

    elif cls.params_layout is not None:
        raise Exception(
            "{} has a params_layout but no parameters".format(
                cls))


def setup_params_choosers(self):
    if self.parameters:
        for k, fld in self.parameters.items():
            if isinstance(fld, models.ForeignKey):
                msg = "Invalid target %s in parameter {} of {}".format(
                    k, self)
                fld.remote_field.model = resolve_model(fld.remote_field.model, strict=msg)
                fields.set_default_verbose_name(fld)

            check_for_chooser(self, fld)


def make_params_layout_handle(self):
    # `self` is either an Action instance or an Actor class object
    return self.params_layout.get_layout_handle(
        settings.SITE.kernel.default_ui)


class Action(Parametrizable, Permittable):
    """
    Abstract base class for all actions.

    The first argument is the optional `label`, other arguments should
    be specified as keywords and can be any of the existing class
    attributes.

    """
    # ~ __metaclass__ = ActionMetaClass
    _layout_class = layouts.ActionParamsLayout

    label = None
    """
    The label of this action. A short descriptive text in user
    language. Used e.g. on menu items. Also on toolbar buttons if they
    have neither :attr:`icon_name` nor :attr:`button_text`.
    """

    button_text = None
    """
    The text to appear on buttons for this action. If this is not
    defined, the :attr:`label` is used.
    """

    button_color = None
    """
    The color to be used on icon-less buttons for this action
    (i.e. which have no :attr:`icon_name`).  See also
    :attr:`lino.core.site.Site.use_silk_icons`.

    Not yet implemented. This is currently being ignored.
    """

    debug_permissions = False
    save_action_name = None

    disable_primary_key = True
    """
    Whether primary key fields should be disabled when using this
    action. This is `True` for all actions except :class:`ShowInsert`.
    """

    keep_user_values = False
    """
    Whether the parameter window should keep its values between
    different calls. If this is True, Lino does not fill any default
    values and leaves those from a previous call.

    Deprecated because it (1) is not used on any production site, (2) has a
    least two side effect: the fields *never* get a default value, even not on
    first execution, and you cannot explicitly specify programmatic field
    values. And (3) we actually wouldn't want to specify this per action but per
    field.

    """
    icon_name = None
    """
    The class name of an icon to be used for this action when
    rendered as toolbar button.  Allowed icon names are defined in
    :data:`lino.core.constants.ICON_NAMES`.

    """
    ui5_icon_name = None
    react_icon_name = None
    hidden_elements = frozenset()

    combo_group = None
    """
    The name of another action to which to "attach" this action.
    Both actions will then be rendered as a single combobutton.

    """
    parameters = None
    use_param_panel = False
    """
    Used internally. This is True for window actions whose window use
    the parameter panel: grid and emptytable (but not showdetail)

    """
    no_params_window = False
    """
    Set this to `True` if your action has :attr:`parameters` but you
    do *not* want it to open a window where the user can edit these
    parameters before calling the action.

    Setting this attribute to `True` means that the calling code must
    explicitly set all parameter values.  Usage example are the
    :attr:`lino_xl.lib.polls.models.AnswersByResponse.answer_buttons`
    and :attr:`lino_xl.lib-tickets.Ticket.quick_assign_to`
    virtual fields.

    """
    sort_index = 90
    """
    Determines the sort order in which the actions will be presented
    to the user.

    List actions are negative and come first.

    Predefined `sort_index` values are:

    ===== =================================
    value action
    ===== =================================
    -1    :class:`as_pdf <lino_xl.lib.appypod.PrintTableAction>`
    10    :class:`ShowInsert`
    11    :attr:`duplicate <lino.mixins.duplicable.Duplicable.duplicate>`
    20    :class:`detail <ShowDetail>`
    30    :class:`delete <DeleteSelected>`
    31    :class:`merge <lino.core.merge.MergeAction>`
    50    :class:`Print <lino.mixins.printable.BasePrintAction>`
    51    :class:`Clear Cache <lino.mixins.printable.ClearCacheAction>`
    52    :attr:`lino.modlib.users.UserPlan.start_plan`
    53    :attr:`lino.modlib.users.UserPlan.update_plan`
    60    :class:`ShowSlaveTable`
    90    default for all custom row actions
    100   :class:`SubmitDetail`
    200   default for all workflow actions (:class:`ChangeStateAction <lino.core.workflows.ChangeStateAction>`)
    ===== =================================


    """
    help_text = None
    """
    A help text that shortly explains what this action does.  In a
    graphical user interface this will be rendered as a **tooltip**
    text.

    If this is not given by the code, Lino will potentially set it at
    startup when loading the :xfile:`help_texts.py` files.

    """

    submit_form_data = False
    """
    Should the running of the action include all known form values in
    the request.
    """

    auto_save = True
    """
    What to do when this action is being called while the user is on a
    dirty record.

    - `False` means: forget any changes in current record and run the
      action.

    - `True` means: save any changes in current record before running
      the action.  `None` means: ask the user.

    """

    extjs_main_panel = None
    """
    Used by :mod:`lino_xl.lib.extensible` and
    :mod:`lino.modlib.awesome_uploader`.

    Example::

        class CalendarAction(dd.Action):
            extjs_main_panel = "Lino.CalendarApp().get_main_panel()"
            ...


    """

    js_handler = None
    """
    This is usually `None`.  Otherwise it is the name of a Javascript
    callable to be called without arguments. That callable must have
    been defined in a :attr:`lino.core.plugin.Plugin.site_js_snippets`
    of the plugin.
    """

    action_name = None
    """
    Internally used to store the name of this action within the
    defining Actor's namespace.

    """

    defining_actor = None
    """
    The :class:`lino.core.actors.Actor` who uses this action for the
    first time.  This is set during :meth:`attach_to_actor`.  This is
    used internally e.g. by :mod:`lino.modlib.extjs` when generating
    JavaScript code for certain actions.
    """

    parameters = None
    """
    See :attr:`lino.core.utils.Parametrizable.parameters`.
    """

    key = None
    """
    Not used. The keyboard hotkey to associate to this action in a
    user interface.
    """

    default_format = 'html'
    """
    Used internally.
    """

    editable = True
    """

    Whether the parameter fields should be editable.
    Setting this to False seems nonsense.
    """

    readonly = True
    """
    Whether this action is readonly, i.e. does not change any data in
    the current data object.

    Setting this to `False` will (1) disable the action for
    `readonly` user types or when
    :attr:`lino.core.site.Site.readonly` is True, and (2) will
    cause it to be logged when :attr:`log_each_action_request
    <lino.core.site.Site.log_each_action_request>` is set to
    `True`.

    Note that :class:`ShowInsert` is readonly because it does not
    modify the current data object.  For example the button would
    be disabled on a registered invoice.

    Note that when a readonly action actually *does* modify the
    object, Lino won't "notice" it.

    Discussion

    Maybe we should change the name `readonly` to `modifying` or
    `writing` (and set the default value `False`).  Because for the
    application developer that looks more natural.  Or --maybe better
    but probably with even more consequences-- the default value
    should be `False`.  Because being readonly, for actions, is a kind
    of "privilege": they don't get logged, they also exists for
    readonly users...  It would be more "secure" when the developer
    must explicitly "say something" it when granting that privilege.

    Another subtlety is the fact that this attribute is used by
    :class:`lino.modlib.users.UserAuthored`.  For example the
    :class:`StartTicketSession
    <lino_xl.lib.working.StartTicketSession>` action in :ref:`noi` is
    declared "readonly" because we want Workers who are not Triagers
    to see this action even if they are not the author (reporter) of a
    ticket.  In this use case the name should rather be
    `requires_authorship`.
    """

    opens_a_window = False
    """
    Whether this action opens a window.  If this is True, the user
    interface is responsible for rendering that window.
    """

    hide_top_toolbar = False
    """
    Used internally if :attr:`opens_a_window` to say whether the
    window has a top toolbar.

    """
    hide_navigator = False
    """
    Used internally if :attr:`opens_a_window` to say whether the
    window has a navigator.

    """

    show_in_plain = False
    """
    Whether this action should be displayed as a button in the toolbar
    of a plain html view.
    """

    show_in_bbar = True
    """
    Whether this action should be displayed as a button in the toolbar
    and the context menu of a full grid.

    For example the :class:`CheckinVisitor
    <lino_xl.lib.reception.models.CheckinVisitor>`,
    :class:`ReceiveVisitor
    <lino_xl.lib.reception.models.ReceiveVisitor>` and
    :class:`CheckoutVisitor
    <lino_xl.lib.reception.models.CheckoutVisitor>` actions have this
    attribute explicitly set to `False` because otherwise they would be
    visible in the toolbar.
    """

    show_in_workflow = False
    """
    Whether this action should be displayed in the
    :attr:`workflow_buttons <lino.core.model.Model.workflow_buttons>`
    column.  If this is True, then Lino will automatically set
    :attr:`custom_handler` to True.
    """

    custom_handler = False
    """
    Whether this action is implemented as Javascript function call.
    This is necessary if you want your action to be callable using an
    "action link" (html button).
    """

    select_rows = True
    """
    True if this action needs an object to act on.

    Set this to `False` if this action is a list action, not a row
    action.
    """
    http_method = 'GET'
    """
    HTTP method to use when this action is called using an AJAX call.

    """

    preprocessor = 'null'  # None
    """
    Name of a Javascript function to be invoked on the web client when
    this action is called.
    """

    window_type = None
    """
    On actions that opens_a_window this must be a unique one-letter
    string expressing the window type.

    Allowed values are:

    - None : opens_a_window is False
    - 't' : ShowTable
    - 'd' : ShowDetail
    - 'i' : ShowInsert

    This can be used e.g. by a summary view to decide how to present the
    summary data (usage example
    :meth:`lino.modlib.uploads.AreaUploads.get_table_summary`).

    """

    callable_from = "td"
    """
    A string that specifies from which :attr:`window_type` this action
    is callable.  None means that it is only callable from code.

    Default value is 'td' which means from both table and detail
    (including ShowEmptyTable which is subclass of ShowDetail). But
    not callable from ShowInsert.
    """

    hide_virtual_fields = False
    required_states = None

    def __init__(self, label=None, **kwargs):
        if label is not None:
            self.label = label

        # if self.parameters is not None and self.select_rows:
        #     self.show_in_bbar = False
        #     # see ticket #105

        for k, v in kwargs.items():
            if not hasattr(self, k):
                raise Exception("Invalid action keyword %s" % k)
            setattr(self, k, v)

        if self.show_in_workflow:
            self.custom_handler = True

        if self.icon_name:
            if self.icon_name not in constants.ICON_NAMES:
                raise Exception(
                    "Unkonwn icon_name '{0}'".format(self.icon_name))

        register_params(self)

    def __get__(self, instance, owner):
        """
        When a model has an action "foo", then getting an attribute
        "foo" of a model instance will return an :class:`InstanceAction`.
        """
        if instance is None:
            return self
        return InstanceAction(
            self, instance.get_default_table(), instance, owner)

    def get_django_form(self):
        """returns a django form object based on the params of this action"""
        from django import forms

        mapping = {
            "PasswordField":"CharField"
        }

        class LinoForm(forms.Form):
            pass
        for name,field in self.parameters.items():
            setattr(LinoForm, name, getattr(forms, mapping.get(field.__class__.__name__,field.__class__.__name__))())
        return LinoForm

    @classmethod
    def decorate(cls, *args, **kw):
        """
        Return a decorator which turns an instance method on a model or a
        class method on an actor into an action of this class.

        The decorated method will be installed as the actions's
        :meth:`run_from_ui <Action.run_from_ui>` method.

        All arguments are forwarded to :meth:`Action.__init__`.

        """

        def decorator(fn):
            assert not 'required' in kw
            # print 20140422, fn.__name__
            kw.setdefault('custom_handler', True)
            a = cls(*args, **kw)

            def wrapped(ar):
                obj = ar.selected_rows[0] if ar.selected_rows else ar.actor.model
                return fn(obj, ar)

            a.run_from_ui = wrapped
            return a

        return decorator

    def get_required_roles(self, actor):
        return actor.required_roles

    def is_callable_from(self, caller):
        """
        Return `True` if this action makes sense as a button from within
        the specified `caller` (an action instance which must have a
        :attr:`window_type`).  Do not override this method on your
        subclass ; rather specify :attr:`callable_from`.
        """
        assert caller.window_type is not None
        if self.callable_from is None:
            return False
        return caller.window_type in self.callable_from
        # return isinstance(caller, self.callable_from)

    def is_window_action(self):
        """Return `True` if this is a "window action" (i.e. which opens a GUI
        window on the client before executin).

        """
        return self.opens_a_window or (
                self.parameters and not self.no_params_window)

    def get_status(self, ar, **kw):
        if self.parameters is not None:
            if self.keep_user_values:
                kw.update(field_values={})
            else:
                defaults = kw.get('field_values', {})
                pv = self.params_layout.params_store.pv2dict(
                    ar, ar.action_param_values, **defaults)
                kw.update(field_values=pv)
        return kw

    def get_chooser_for_field(self, fieldname):
        d = getattr(self, '_choosers_dict', {})
        return d.get(fieldname, None)

    def get_choices_text(self, obj, request, field):
        return obj.get_choices_text(request, self, field)

    def make_params_layout_handle(self):
        return make_params_layout_handle(self)

    def get_data_elem(self, name):
        # same as in Actor but here it is an instance method
        return self.defining_actor.get_data_elem(name)

    def get_param_elem(self, name):
        # same as in Actor but here it is an instance method
        if self.parameters:
            return self.parameters.get(name, None)
        return None

    def get_widget_options(self, name, **options):
        # same as in Actor but here it is an instance method
        return options

    def get_label(self):
        """
        Return the `label` of this action, or the `action_name` if the
        action has no explicit label.
        """
        return self.label or self.action_name

    def get_button_label(self, actor):
        if actor is None or actor.default_action is None:
            return self.label
        if self is actor.default_action.action:
            return actor.label
            # return actor.get_actor_label()  # 20200307
        else:
            return self.button_text or self.label
            # since 20140923 return u"%s %s" % (self.label, actor.label)

    def full_name(self, actor):
        if self.action_name is None:
            raise Exception("Tried to full_name() on %r" % self)
            # ~ return repr(self)
        if self.parameters and not self.no_params_window:
            return self.defining_actor.actor_id + '.' + self.action_name
        return str(actor) + '.' + self.action_name

    def get_action_title(self, ar):
        return ar.get_title()

    def __repr__(self):
        if self.label is None:
            name = self.action_name
        else:
            label_repr = repr(str(self.label))
            name = "{} ({})".format(self.action_name, label_repr)
        # if self.button_text:
        #     name = repr(str(self.button_text)) + " " + name
        return "<{}.{} {}>".format(
            self.__class__.__module__,
            self.__class__.__name__,
            name)

    def __str__(self):
        # return force_text(self.label)
        # return str(self.get_label())
        return str(self.get_label())

    def unused__str__(self):
        raise Exception("20121003 Must use full_name(actor)")
        if self.defining_actor is None:
            return repr(self)
        if self.action_name is None:
            return repr(self)
        return str(self.defining_actor) + ':' + self.action_name

    # ~ def set_permissions(self,*args,**kw)
    # ~ self.permission = perms.factory(*args,**kw)

    def attach_to_workflow(self, wf, name):
        if self.action_name is not None:
            assert self.action_name == name
        self.action_name = name
        self.defining_actor = wf
        setup_params_choosers(self)

    def attach_to_actor(self, owner, name):
        """
        Called once per actor and per action on startup before a
        :class:`BoundAction` instance is created.  If this returns
        False, then the action won't be attached to the given actor.

        The owner is the actor which "defines" the action, i.e. uses
        that instance for the first time.  Subclasses of the owner may
        re-use the same instance without becoming the owner.
        """
        # if not actor.editable and not self.readonly:
        #     return False
        if self.defining_actor is not None:
            # already defined by another actor
            return True
        self.defining_actor = owner
        # if self.label is None:
        #     self.label = name
        if self.action_name is not None:
            return True
            # if name == self.action_name:
            #     return True
            # raise Exception(
            #     "tried to attach named action %s.%s as %s" %
            #     (actor, self.action_name, name))
        self.action_name = name
        setup_params_choosers(self)
        # setup_params_choosers(self.__class__)
        return True

    def get_action_permission(self, ar, obj, state):
        """Return (True or False) whether the given :class:`ActionRequest
        <lino.core.requests.BaseRequest>` `ar` should get permission
        to run on the given Model instance `obj` (which is in the
        given `state`).

        Derived Action classes may override this to add vetos.
        E.g. the MoveUp action of a Sequenced is not available on the
        first row of given `ar`.

        This should be used only for light-weight tests. If this
        requires a database lookup, consider disabling the action in
        :meth:`disabled_fields
        <lino.core.model.Model.disabled_fields>` where you can disable
        multiple actions and fields at once.

        """
        return True

    def get_view_permission(self, user_type):
        """
        Return True if this action is visible for users of given user_type.

        """
        return True

    def run_from_ui(self, ar, **kwargs):
        """
        Execute the action.  `ar` is an :class:`ActionRequest
        <lino.core.requests.BaseRequest>` object representing the
        context in which the action is running.
        """
        raise NotImplementedError(
            "%s has no run_from_ui() method" % self.__class__)

    def run_from_code(self, ar=None, *args, **kwargs):
        """
        Probably to be deprecated.
        Execute the action.  The default calls :meth:`run_from_ui`.  You
        may override this to define special behaviour
        """
        self.run_from_ui(ar, *args, **kwargs)

    def run_from_session(self, ses, *args, **kw):  # 20130820
        if len(args):
            obj = args[0]
        else:
            obj = None
        ia = InstanceAction(self, self.defining_actor, obj, None)
        return ia.run_from_session(ses, **kw)

    def action_param_defaults(self, ar, obj, **kw):
        """Same as :meth:`lino.core.actors.Actor.param_defaults`, except that
        on an action it is a instance method.

        Note that this method is not called for actions which are rendered
        in a toolbar (:ticket:`1336`).

        Usage examples:
        :class:`lino.modlib.users.actions.SendWelcomeMail`

        """

        for k, pf in list(self.parameters.items()):
            # print 20151203, pf.name, repr(pf.rel.to)
            kw[k] = pf.get_default()
        return kw

    def setup_action_request(self, actor, ar):
        pass

    def get_layout_aliases(self):
        """

        Yield a series of (ALIAS, repl) tuples that cause a name ALIAS in a
        layout based on this action to be replaced by its replacement `repl`.

        """
        return []


class TableAction(Action):

    def get_action_title(self, ar):
        return ar.get_title()


# class RedirectAction(Action):

#     def get_target_url(self, elem):
#         raise NotImplementedError


class ShowTable(TableAction):
    """
    Open a window with a grid editor on this table as main widget.
    """
    use_param_panel = True
    show_in_workflow = False
    opens_a_window = True
    window_type = 't'
    action_name = 'grid'
    select_rows = False
    callable_from = None

    # def is_callable_from(self, caller):
    #     return False

    # def attach_to_actor(self, actor, name):
    #     self.label = actor.label
    #     return super(ShowTable, self).attach_to_actor(actor, name)

    def get_label(self):
        return self.label or self.defining_actor.label

    def get_window_layout(self, actor):
        # ~ return self.actor.list_layout
        return None

    def get_window_size(self, actor):
        return actor.window_size


class ShowDetail(Action):
    help_text = _("Open a detail window on this record.")
    action_name = 'detail'
    label = _("Detail")
    icon_name = 'application_form'
    ui5_icon_name = "sap-icon://detail-view"
    opens_a_window = True
    window_type = 'd'
    show_in_workflow = False
    save_action_name = 'submit_detail'
    callable_from = 't'
    sort_index = 20

    def __init__(self, dl, label=None, **kwargs):
        self.owner = dl
        super(ShowDetail, self).__init__(label, **kwargs)

    def get_required_roles(self, actor):
        if self.owner.required_roles is None:
            return actor.required_roles
        return self.owner.required_roles

    def get_window_layout(self, actor):
        return actor.detail_layout

    def get_window_size(self, actor):
        wl = self.get_window_layout(actor)
        return wl.window_size


class ShowEmptyTable(ShowDetail):
    """
    The default action for :class:`lino.utils.report.EmptyTable`.
    """
    use_param_panel = True
    action_name = 'show'
    default_format = 'html'
    # ~ hide_top_toolbar = True
    hide_navigator = True
    icon_name = None
    callable_from = 't'

    # def attach_to_actor(self, actor, name):
    #     self.label = actor.label
    #     return super(ShowEmptyTable, self).attach_to_actor(actor, name)

    def get_label(self):
        return self.label or self.defining_actor.label

    def as_bootstrap_html(self, ar):
        return super(ShowEmptyTable, self).as_bootstrap_html(ar, '-99998')


class ShowInsert(TableAction):
    """
    Open the Insert window filled with a row of blank or default
    values.  The new row will be actually created only when this
    window gets submitted.
    """
    save_action_name = 'submit_insert'
    show_in_plain = True
    disable_primary_key = False

    label = _("New")
    if True:  # settings.SITE.use_silk_icons:
        icon_name = 'add'  # if action rendered as toolbar button
    else:
        # button_text = u"❏"  # 274F Lower right drop-shadowed white square
        # button_text = u"⊞"  # 229e SQUARED PLUS
        button_text = u"⊕"  # 2295 circled plus

    ui5_icon_name = "sap-icon://add"
    help_text = _("Insert a new record")

    show_in_workflow = False
    opens_a_window = True
    window_type = 'i'
    hide_navigator = True
    sort_index = 10
    hide_top_toolbar = True
    # required_roles = set([SiteUser])
    action_name = 'insert'
    key = keyboard.INSERT  # (ctrl=True)
    hide_virtual_fields = True
    # readonly = False
    select_rows = False
    http_method = "POST"

    def attach_to_actor(self, owner, name):
        if owner.model is not None:
            self.help_text = format_lazy(
                _("Open a dialog window to insert a new {}."), owner.model._meta.verbose_name)
        return super(ShowInsert, self).attach_to_actor(owner, name)

    def get_action_title(self, ar):
        # return _("Insert into %s") % force_text(ar.get_title())
        if ar.actor.model is None:
            return _("Insert into %s") % force_text(ar.get_title())
        return format_lazy(_("New {}"), ar.actor.model._meta.verbose_name)

    def get_window_layout(self, actor):
        return actor.insert_layout or actor.detail_layout

    def get_window_size(self, actor):
        wl = self.get_window_layout(actor)
        return wl.window_size

    def get_view_permission(self, user_type):
        # the action is readonly because it doesn't write to the
        # current object, but since it does modify the adtabase we
        # want to hide it for readonly users.
        if user_type and user_type.readonly:
            return False
        return super(ShowInsert, self).get_view_permission(user_type)

    def create_instance(self, ar):
        """
        Create a temporary instance that will not be saved, used only to
        build the button.
        """
        return ar.create_instance()

    def get_status(self, ar, **kw):
        kw = super(ShowInsert, self).get_status(ar, **kw)
        if 'record_id' in kw:
            return kw
        if 'data_record' in kw:
            return kw
        # raise Exception("20150218 %s" % self)
        elem = self.create_instance(ar)
        rec = ar.elem2rec_insert(ar.ah, elem)
        kw.update(data_record=rec)
        return kw


# class UpdateRowAction(Action):
#     show_in_workflow = False
#     readonly = False
#     # required_roles = set([SiteUser])


# this is a first attempt to solve the "cannot use active fields in
# insert window" problem.  not yet ready for use. the idea is that
# active fields should not send a real "save" request (either POST or
# PUT) in the background but a "validate_form" request which creates a
# dummy instance from form content, calls it's full_clean() method to
# have other fields filled in, and then return the modified form
# content. Fails because the Record.phantom in ExtJS then still gets
# lost.

class ValidateForm(Action):
    # called by active_fields
    show_in_workflow = False
    action_name = 'validate'
    readonly = False
    auto_save = False
    callable_from = None

    def run_from_ui(self, ar, **kwargs):
        elem = ar.create_instance_from_request(**kwargs)
        ar.ah.store.form2obj(ar, ar.rqdata, elem, False)
        elem.full_clean()
        ar.success()
        # ar.set_response(rows=[ar.ah.store.row2list(ar, elem)])
        ar.goto_instance(elem)


class SaveGridCell(Action):
    """
    Called when user edited a cell of a non-phantom record in a grid.
    Installed as `update_action` on every :class:`Actor`.

    """
    sort_index = 10
    show_in_workflow = False
    action_name = 'grid_put'
    http_method = "PUT"
    readonly = False
    auto_save = False
    callable_from = None

    def run_from_ui(self, ar, **kw):
        # logger.info("20140423 SubmitDetail")
        elem = ar.selected_rows[0]
        elem.save_existing_instance(ar)
        ar.set_response(rows=[ar.ah.store.row2list(ar, elem)])

        # We also need *either* `rows` (when this was called from a
        # Grid) *or* `goto_instance` (when this was called from a
        # form).


class SubmitDetail(SaveGridCell):
    """Save changes in the detail form.

    This is rendered as the "Save" button of a :term:`detail window`.

    Installed as `submit_detail` on every actor.

    """
    sort_index = 100
    icon_name = 'disk'
    help_text = _("Save changes in this form")
    label = _("Save")
    action_name = ShowDetail.save_action_name
    submit_form_data = True
    callable_from = 'd'

    def run_from_ui(self, ar, **kw):
        # logger.info("20140423 SubmitDetail")
        for elem in ar.selected_rows:
            elem.save_existing_instance(ar)
            if not settings.SITE.is_installed("react"):
                # No point in clos
                if ar.actor.stay_in_grid:
                    ar.close_window()
                else:
                    ar.goto_instance(elem)


class CreateRow(Action):
    """
    Called when user edited a cell of a phantom record in a grid.
    """
    sort_index = 10
    auto_save = False
    show_in_workflow = False
    readonly = False
    callable_from = None
    http_method = "POST"

    # select_rows = False
    # submit_form_data = True
    def run_from_ui(self, ar, **kwargs):
        elem = ar.create_instance_from_request(**kwargs)
        self.save_new_instance(ar, elem)

    def save_new_instance(self, ar, elem):
        elem.save_new_instance(ar)
        ar.success(_("%s has been created.") % obj2unicode(elem))

        # print(19062017, "Ticket 1910")
        if ar.actor.handle_uploaded_files is None:
            # The `rows` can contain complex strings which cause
            # decoding problems on the client when responding to a
            # file upload
            ar.set_response(rows=[ar.ah.store.row2list(ar, elem)])
            ar.set_response(navinfo=navinfo(ar.data_iterator, elem))
        else:
            # Must set text/html for file uploads, otherwise the
            # browser adds a <PRE></PRE> tag around the AJAX response.
            ar.set_content_type('text/html')

        # if ar.actor.stay_in_grid and ar.requesting_panel:
        if ar.actor.stay_in_grid:
            # do not open a detail window on the new instance
            return

        ar.goto_instance(elem)

        # No need to ask refresh_all since closing the window will
        # automatically refresh the underlying window.

    def save_new_instances(self, ar, elems):
        """Currently only used for file uploads."""
        for e in elems:
            e.save_new_instance(ar)

        ar.success(
            _("%s files have been uploaded: %s") % (len(elems), "\n".join([obj2unicode(elem) for elem in elems])))

        # print(19062017, "Ticket 1910")
        if ar.actor.handle_uploaded_files is None:
            ar.set_response(rows=[ar.ah.store.row2list(ar, elem[0])])
            ar.set_response(navinfo=navinfo(ar.data_iterator, elem[0]))
        else:
            # Must set text/html for file uploads, otherwise the
            # browser adds a <PRE></PRE> tag around the AJAX response.
            ar.set_content_type('text/html')

        # if ar.actor.stay_in_grid and ar.requesting_panel:
        if ar.actor.stay_in_grid:
            # do not open a detail window on the new instance
            return

        ar.goto_instance(elem[0])

        # No need to ask refresh_all since closing the window will
        # automatically refresh the underlying window.


class SubmitInsert(CreateRow):
    """
    Create a new database row using the data specified in the insert
    window.  Called when the OK button of an Insert Window was
    clicked.  Installed as `submit_insert` on every `dd.Model
    <lino.core.model.Model>`.
    """
    label = _("Create")
    action_name = None  # 'post'
    help_text = _("Create the record and open a detail window on it")
    http_method = "POST"

    callable_from = 'i'

    def run_from_ui(self, ar, **kwargs):
        # must set requesting_panel to None, otherwise javascript
        # button actions would try to refer the requesting panel which
        # is going to be closed (this disturbs at least in ticket
        # #219)
        ar.requesting_panel = None
        if ar.actor.handle_uploaded_files is not None and len(ar.request.FILES.getlist("file")) > 1:
            # Multiple uploads possible, note plural method names.
            elems = ar.create_instances_from_request(**kwargs)
            self.save_new_instances(ar, elems)
            ar.set_response(close_window=True)
        else:
            elem = ar.create_instance_from_request(**kwargs)
            self.save_new_instance(ar, elem)
            ar.set_response(close_window=True)
        # if settings.SITE.is_installed("react"):
        #     ar.goto_instance(elem)

        # ar.set_response(
        #     eval_js=ar.renderer.obj2url(ar, elem).replace('javascript:', '', 1)
        # )


# class SubmitInsertAndStay(SubmitInsert):
#     sort_index = 11
#     switch_to_detail = False
#     action_name = 'poststay'
#     label = _("Create without detail")
#     help_text = _("Don't open a detail window on the new record")


class ExplicitRefresh(Action):  # experimental 20170929
    label = _("Go")
    show_in_bbar = False
    # js_handler = 'function(panel) {panel.refresh()}'
    js_handler = 'function(btn, evt) {console.log("20170928", this); this.refresh()}'
    # def run_from_ui(self, ar, **kw):
    #     ar.set_response(refresh_all=True)


class ShowSlaveTable(Action):
    """
    An action which opens a window showing another table (to be
    specified when instantiating the action).
    """
    TABLE2ACTION_ATTRS = ('help_text', 'icon_name', 'react_icon_name', 'label',
                          'sort_index', 'required_roles', 'button_text')
    show_in_bbar = True

    def __init__(self, slave_table, **kw):
        self.slave_table = slave_table
        self.explicit_attribs = set(kw.keys())
        super(ShowSlaveTable, self).__init__(**kw)

    @classmethod
    def get_actor_label(self):
        return self.get_label() or self.slave_table.label

    def attach_to_actor(self, actor, name):
        if isinstance(self.slave_table, str):
            T = settings.SITE.models.resolve(self.slave_table)
            if T is None:
                msg = "Invalid action {} on actor {!r}: " \
                      "no table named {}".format(
                    name, actor, self.slave_table)
                raise Exception(msg)
            self.slave_table = T
        for k in self.TABLE2ACTION_ATTRS:
            if k not in self.explicit_attribs:
                attr = getattr(self.slave_table, k, None)
                setattr(self, k, attr)
        return super(ShowSlaveTable, self).attach_to_actor(actor, name)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        sar = ar.spawn(self.slave_table, master_instance=obj)
        js = ar.renderer.request_handler(sar)
        ar.set_response(eval_js=js)


class MultipleRowAction(Action):
    """Base class for actions that update something on every selected row.
    """
    custom_handler = True

    def run_on_row(self, obj, ar):
        """This is being called on every selected row.
        """
        raise NotImplementedError()

    def run_from_ui(self, ar, **kw):
        ar.success(**kw)
        n = 0
        for obj in ar.selected_rows:
            if not ar.response.get('success'):
                ar.info("Aborting remaining rows")
                break
            ar.info("%s for %s...", str(self.label), str(obj))
            n += self.run_on_row(obj, ar)
            ar.set_response(refresh_all=True)

        msg = _("%d row(s) have been updated.") % n
        ar.info(msg)
        # ~ ar.success(msg,**kw)


class DeleteSelected(MultipleRowAction):
    """Delete the selected row(s).

    This action is automatically installed on every editable actor.

    """

    action_name = 'delete_selected'  # because...
    if True:  # settings.SITE.use_silk_icons:
        icon_name = 'delete'
    else:
        button_text = u"⊖"  # 2296 CIRCLED MINUS
        # button_text = u"⊟"  # 229F SQUARED MINUS

    ui5_icon_name = 'sap-icon://less'
    help_text = _("Delete this record")
    auto_save = False
    sort_index = 30
    readonly = False
    show_in_workflow = False
    # required_roles = set([SiteUser])
    # ~ callable_from = (ShowTable,ShowDetail)
    # ~ needs_selection = True
    label = _("Delete")
    # ~ url_action_name = 'delete'
    key = keyboard.DELETE  # (ctrl=True)

    # ~ client_side = True

    def run_from_ui(self, ar, **kw):
        objects = []
        for obj in ar.selected_rows:
            objects.append(str(obj))
            msg = ar.actor.disable_delete(obj, ar)
            if msg is not None:
                ar.error(None, msg, alert=True)
                return

        # build a list of volatile related objects that will be deleted together
        # with this one
        cascaded_objects = {}
        kernel = settings.SITE.kernel
        for obj in ar.selected_rows:
            for m, fk in traverse_ddh_fklist(obj.__class__):
                # print(20200724, fk)
                if fk.name in m.allow_cascaded_delete:
                    qs = m.objects.filter(**{fk.name:obj})
                    n = qs.count()
                    if n:
                        if m in cascaded_objects:
                            cascaded_objects[m] += n
                        else:
                            cascaded_objects[m] = n

            # print "20141208 generic related objects for %s:" % obj
            for gfk, fk_field, qs in kernel.get_generic_related(obj):
                if gfk.name in qs.model.allow_cascaded_delete:
                    n = qs.count()
                    if n:
                        cascaded_objects[qs.model] = n

        def ok(ar2):
            super(DeleteSelected, self).run_from_ui(ar, **kw)
            # refresh_all must be True e.g. for when user deletes an item of a
            # bank statement
            ar2.success(record_deleted=True, refresh_all=True)

            # hack required for extjs:
            if ar2.actor.detail_action:
                ar2.set_response(
                    detail_handler_name=ar2.actor.detail_action.full_name())

        d = dict(num=len(objects), targets=', '.join(objects))
        if len(objects) == 1:
            d.update(type=ar.actor.model._meta.verbose_name)
        else:
            d.update(type=ar.actor.model._meta.verbose_name_plural)
            if len(objects) > 10:
                objects = objects[:9] + ["..."]
        msg = gettext("You are about to delete %(num)d %(type)s\n(%(targets)s)") % d

        if len(cascaded_objects):
            lst = ["{} {}".format(n, m._meta.verbose_name if n == 1 else m._meta.verbose_name_plural)
                for m, n in cascaded_objects.items()]
            msg += "\n" + gettext("as well as all related volatile records ({})").format(
                ", ".join(lst))

        ar.confirm(ok, "{}. {}".format(msg, gettext("Are you sure?")),
                   uid="deleting %(num)d %(type)s pks=" % d + "".join([str(t.pk) for t in ar.selected_rows]))

    def run_on_row(self, obj, ar):
        obj.delete_instance(ar)
        return 1


action = Action.decorate


def get_view_permission(e):
    if isinstance(e, Permittable) and not e.get_view_permission(
            get_user_profile()):
        return False
    # e.g. pcsw.ClientDetail has a tab "Other", visible only to system
    # admins but the "Other" contains a GridElement RolesByPerson
    # which is not per se reserved for system admins.  js of normal
    # users should not try to call on_master_changed() on it
    parent = e.parent
    while parent is not None:
        if isinstance(parent, Permittable) and not parent.get_view_permission(
                get_user_profile()):
            return False  # bug 3 (bcss_summary) blog/2012/0927
        parent = parent.parent
    return True
