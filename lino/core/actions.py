# -*- coding: UTF-8 -*-
# Copyright 2009-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""This defines the :class:`Action` class and the :func:`action`
decorator, together with some of the predefined actions.

See also:

- :ref:`dev.actions`.
- :doc:`/tutorials/actions/index`


"""

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.utils.encoding import force_unicode
from django.conf import settings
from django import http
from django.db import models

from lino.utils.xmlgen import html as xghtml
E = xghtml.E

from lino.core import constants
from lino.core.utils import obj2unicode
from lino.core.utils import resolve_model
from lino.core.utils import navinfo
from lino.core import layouts
from lino.core import fields
from lino.core import keyboard
from lino.core.signals import on_ui_created, pre_ui_delete, pre_ui_save
from lino.core.utils import ChangeWatcher
from lino.core.permissions import Permittable
from lino.core.utils import Parametrizable, InstanceAction
# from lino.modlib.users.choicelists import SiteUser
from lino.utils.choosers import Chooser

PLAIN_PAGE_LENGTH = 15


def check_for_chooser(holder, field):
    # holder is either a Model, an Actor or an Action.
    if isinstance(field, fields.DummyField):
        return
    methname = field.name + "_choices"
    m = getattr(holder, methname, None)
    if m is not None:
        ch = Chooser(holder, field, m)
        d = holder.__dict__.get('_choosers_dict', None)
        if d is None:
            d = dict()
            setattr(holder, '_choosers_dict', d)
        if ch in d:
            raise Exception("Redefinition of chooser %s" % field)
        d[field.name] = ch
    # if field.name == 'city':
    #     logger.info("20140822 chooser for %s.%s", holder, field.name)


def discover_choosers():
    logger.debug("Discovering choosers for model fields...")
    #~ logger.debug("Instantiate model reports...")
    for model in models.get_models():
        #~ n = 0
        for field in model._meta.fields + model._meta.virtual_fields:
            check_for_chooser(model, field)
        #~ logger.debug("Discovered %d choosers in model %s.",n,model)


def install_layout(cls, k, layout_class, **options):
    """
    - `k` is one of 'detail_layout', 'insert_layout', 'params_layout'
    - `layout_class`

    """
    dl = cls.__dict__.get(k, None)
    if dl is None:  # and not cls._class_init_done:
        dl = getattr(cls, k)
    if dl is None:
        return
    if isinstance(dl, basestring):
        setattr(cls, k, layout_class(dl, cls, **options))
    elif isinstance(dl, layouts.Panel):
        options.update(dl.options)
        setattr(cls, k, layout_class(dl.desc, cls, **options))
    elif dl._datasource is None:
        dl.set_datasource(cls)
        setattr(cls, k, dl)
    elif not issubclass(cls, dl._datasource):
        raise Exception(
            "Cannot reuse %s of %r for %r" %
            (k, dl._datasource, cls))


def register_params(cls):
    """Note that `cls` is either an actor or an action. And remember that
    actors are class objects while actions are instances.

    """
    if cls.parameters:
        for k, v in cls.parameters.items():
            v.set_attributes_from_name(k)
            v.table = cls

        if cls.params_layout is None:
            cls.params_layout = cls._layout_class.join_str.join(
                cls.parameters.keys())
        install_layout(cls, 'params_layout', cls._layout_class)

    elif cls.params_layout is not None:
        raise Exception("params_layout but no parameters ?!")


def setup_params_choosers(self):
    if self.parameters:
        for k, fld in self.parameters.items():
            if isinstance(fld, models.ForeignKey):
                fld.rel.to = resolve_model(fld.rel.to)
                from lino.core.kernel import set_default_verbose_name
                set_default_verbose_name(fld)
                #~ if fld.verbose_name is None:
                    #~ fld.verbose_name = fld.rel.to._meta.verbose_name

            check_for_chooser(self, fld)


def make_params_layout_handle(self, ui):
    return self.params_layout.get_layout_handle(
        settings.SITE.kernel.default_ui)


class Action(Parametrizable, Permittable):
    """
    Abstract base class for all actions.
    """

    #~ __metaclass__ = ActionMetaClass
    _layout_class = layouts.ActionParamsLayout

    label = None
    """
    The text to appear on the button.
    """
    debug_permissions = False
    save_action_name = None
    disable_primary_key = True
    """Whether primary key fields should be disabled when using this
    action. This is `True` for all actions except :class:`InsertRow`.

    """

    icon_name = None
    """The class name of an icon to be used for this action when rendered
    as toolbar button.

    Allowed icon names are defined in
    :data:`lino.core.constants.ICON_NAMES`.

    """

    hidden_elements = frozenset()
    combo_group = None
    """
    The name of another action to which to "attach" this action.
    Both actions will then be rendered as a single combobutton.

    """

    parameters = None
    "See :attr:`Parametrizable.parameters`."

    use_param_panel = False
    """Used internally. This is True for window actions whose window use
    the parameter panel: grid and emptytable (but not showdetail)

    """

    no_params_window = False
    """Set this to `True` if your action has :attr:`parameters` but you
    do *not* want it to open a window where the user can edit these
    parameters before calling the action.

    Setting this attribute to `True` means that the calling code must
    explicitly set all parameter values.  Usage example is the
    :attr:`lino.modlib.polls.models.AnswersByResponse.answer_buttons`
    virtual field.

    """

    sort_index = 90
    """
    Determins the sort order in which the actions will be presented to
    the user.

    List actions are negative and come first.

    Predefined `sort_index` values are:

    ===== =================================
    value action
    ===== =================================
    -1    :class:`as_pdf <lino.utils.appy_pod.PrintTableAction>`
    10    :class:`InsertRow`, :class:`SubmitDetail`
    11    :attr:`duplicate <lino.mixins.duplicable.Duplicable.duplicate>`
    20    :class:`detail <ShowDetailAction>`
    30    :class:`delete <DeleteSelected>`
    31    :class:`merge <lino.core.merge.MergeAction>`
    50    :class:`Print <lino.mixins.printable.BasePrintAction>`
    51    :class:`Clear Cache <lino.mixins.printable.ClearCacheAction>`
    60    :class:`ShowSlaveTable`
    90    default for all custom row actions
    ===== =================================

    """

    help_text = None
    """A help text that shortly explains what this action does.
    :mod:`lino.modlib.extjs` shows this as tooltip text.

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
    """Used by :mod:`lino.modlib.extensible` and
    :mod:`lino.modlib.awesome_uploader`.

    Example::

        class CalendarAction(dd.Action):
            extjs_main_panel = "Lino.CalendarApp().get_main_panel()"
            ...

    """

    js_handler = None
    """
    This is usually `None`. Otherwise it is the name of a Javascript
    callable to be called without arguments. That callable must have
    been defined in a :attr:`lino.core.plugin.Plugin.site_js_snippets` of the plugin.

    """

    action_name = None
    """Internally used to store the name of this action within the
    defining Actor's namespace.

    """
    defining_actor = None
    """Internally used to store the :class:`lino.core.actors.Actor` who
    defined this action.

    """

    key = None
    """
    The hotkey to associate to this action in a user interface.
    """

    default_format = 'html'
    """
    Used internally.
    """

    readonly = True
    """
    Whether this action possibly modifies data *in the given object*.
    
    This means that :class:`InsertRow` is a `readonly` action.
    Actions like :class:`InsertRow` and :class:`Duplicable
    <lino.mixins.duplicable.Duplicate>` which do not modify the given
    object but *do* modify the database, must override their
    `get_action_permission`::
    
      def get_action_permission(self, ar, obj, state):
          if user.profile.readonly:
              return False
          return super(Duplicate, self).get_action_permission(ar, obj, state)

    """

    opens_a_window = False
    """
    Used internally to say whether this action opens a window.
    """

    hide_top_toolbar = False
    """Used internally if :attr:`opens_a_window` to say whether the
    window has a top toolbar.

    """

    hide_navigator = False
    """Used internally if :attr:`opens_a_window` to say whether the
    window has a navigator.

    """

    show_in_bbar = True
    """Whether this action should be displayed as a button in the toolbar
    and the context menu.

    For example the :class:`CheckinVisitor
    <lino.modlib.reception.models.CheckinVisitor>`,
    :class:`ReceiveVisitor
    <lino.modlib.reception.models.ReceiveVisitor>` and
    :class:`CheckoutVisitor
    <lino.modlib.reception.models.CheckoutVisitor>` actions have this
    attribute explicitly set to `False` because otherwise they would be
    visible in the toolbar.

    """

    show_in_workflow = False
    """Used internally.  Whether this action should be displayed as the
    :attr:`workflow_buttons <lino.core.model.Model.workflow_buttons>`
    column. If this is True, then Lino will automatically set
    :attr:`custom_handler` to True.

    """

    custom_handler = False
    """
    Whether this action is implemented as Javascript function call.
    This is necessary if you want your action to be callable using an
    "action link" (html button).

    """

    select_rows = True
    """True if this action needs an object to act on.

    True if this action should be called on a single row (ignoring
    multiple row selection).  Set this to False if this action is a
    list action, not a row action.
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

    hide_virtual_fields = False

    required_states = None

    def __init__(self, label=None, **kw):
        """The first argument is the optional `label`, other arguments should
        be specified as keywords and can be any of the existing class
        attributes.

        """
        if label is not None:
            self.label = label

        # if self.parameters is not None and self.select_rows:
        #     self.show_in_bbar = False
        #     # see ticket #105

        for k, v in kw.items():
            if not hasattr(self, k):
                raise Exception("Invalid action keyword %s" % k)
            setattr(self, k, v)

        if self.show_in_workflow:
            self.custom_handler = True

        if self.icon_name:
            if not self.icon_name in constants.ICON_NAMES:
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

    def is_callable_from(self, caller):
        return isinstance(caller, (GridEdit, ShowDetailAction))
        #~ if self.select_rows:
            #~ return isinstance(caller,(GridEdit,ShowDetailAction))
        #~ return isinstance(caller,GridEdit)

    def is_window_action(self):
        """Return `True` if this is a "window action" (i.e. which opens a GUI
        window on the client before executin).

        """
        return self.opens_a_window or (
            self.parameters and not self.no_params_window)

    def get_status(self, ar, **kw):
        if self.parameters is not None:
            defaults = kw.get('field_values', {})
            pv = self.params_layout.params_store.pv2dict(
                ar.action_param_values, **defaults)
            kw.update(field_values=pv)
        return kw

    def get_chooser_for_field(self, fieldname):
        d = getattr(self, '_choosers_dict', {})
        return d.get(fieldname, None)

    def get_choices_text(self, obj, request, field):
        return obj.get_choices_text(request, self, field)

    def as_bootstrap_html(self, ar):
        return "Oops, no as_bootstrap_html method for %s" % self

    def make_params_layout_handle(self, ui):
        return make_params_layout_handle(self, ui)

    def get_data_elem(self, name):
        # same as in Actor but here it is an instance method
        return None

    def get_param_elem(self, name):
        # same as in Actor but here it is an instance method
        if self.parameters:
            return self.parameters.get(name, None)
        return None

    def get_widget_options(self, name, **options):
        # same as in Actor but here it is an instance method
        return options

    def get_button_label(self, actor):
        if actor is None or actor.default_action is None:
            return self.label
        if self is actor.default_action.action:
            return actor.label
        else:
            return self.label
            # since 20140923 return u"%s %s" % (self.label, actor.label)

    def full_name(self, actor):
        if self.action_name is None:
            raise Exception("Tried to full_name() on %r" % self)
            #~ return repr(self)
        if self.parameters and not self.no_params_window:
            return self.defining_actor.actor_id + '.' + self.action_name
        return str(actor) + '.' + self.action_name

    def get_action_title(self, ar):
        return ar.get_title()

    def __repr__(self):
        if self.label is None:
            return "<%s %s>" % (self.__class__.__name__, self.action_name)
        return "<%s %s (%r)>" % (
            self.__class__.__name__, self.action_name, unicode(self.label))

    def unused__str__(self):
        raise Exception("20121003 Must use full_name(actor)")
        if self.defining_actor is None:
            return repr(self)
        if self.action_name is None:
            return repr(self)
        return str(self.defining_actor) + ':' + self.action_name

    #~ def set_permissions(self,*args,**kw)
        #~ self.permission = perms.factory(*args,**kw)

    def attach_to_workflow(self, wf, name):
        assert self.action_name is None
        self.action_name = name
        self.defining_actor = wf
        setup_params_choosers(self)

    def attach_to_actor(self, actor, name):
        """Called once per Actor per Action on startup before a BoundAction
        instance is being created.  If this returns False, then the
        action won't be attached to the given actor.

        """
        if not actor.editable and not self.readonly:
            return False
        #~ if self.name is not None:
            #~ raise Exception("%s tried to attach named action %s" % (actor,self))
        #~ if actor == self.defining_actor:
            #~ raise Exception('20121003 %s %s' % (actor,name))
        if self.defining_actor is not None:
            # already defined in another actor
            return True
        if self.action_name is not None:
            raise Exception("tried to attach named action %s.%s" %
                            (actor, self.action_name))
        self.action_name = name
        self.defining_actor = actor
        if self.label is None:
            self.label = name
        setup_params_choosers(self)
        # setup_params_choosers(self.__class__)
        return True

    def __unicode__(self):
        return force_unicode(self.label)

    def get_action_permission(self, ar, obj, state):
        """Return (True or False) whether the given :class:`ActionRequest
        <lino.core.requests.BaseRequest>` `ar` should get permission
        to execute on the given Model instance `obj` (which is in the
        given `state`).

        Derived Action classes may override this to add vetos.
        E.g. the MoveUp action of a Sequenced is not available on the
        first row of given `ar`.

        """
        return True

    def get_view_permission(self, profile):
        """
        Return True if this action is visible for users of given profile.

        """
        return True

    def run_from_ui(self, ar, **kw):
        """Execute the action.  `ar` is an :class:`ActionRequest
        <lino.core.requests.BaseRequest>` object representing the
        context in which the action is running.
        """
        raise NotImplementedError(
            "%s has no run_from_ui() method" % self.__class__)

    def run_from_code(self, ar, *args, **kw):
        self.run_from_ui(ar, *args, **kw)

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
        in a toolbar (:srcref:`docs/tickets/105`)

        """

        for k, pf in self.parameters.items():
            kw[k] = pf.get_default()
        return kw

    def setup_action_request(self, actor, ar):
        pass


class TableAction(Action):

    def get_action_title(self, ar):
        return ar.get_title()


class RedirectAction(Action):

    def get_target_url(self, elem):
        raise NotImplementedError


def buttons2pager(buttons, title=None):
    items = []
    if title:
        items.append(E.li(E.span(title)))
    for symbol, label, url in buttons:
        if url is None:
            items.append(E.li(E.span(symbol), class_="disabled"))
        else:
            items.append(E.li(E.a(symbol, href=url)))
    # Bootstrap version 2.x
    # return E.div(E.ul(*items), class_='pagination')
    return E.ul(*items, class_='pagination pagination-sm')


class GridEdit(TableAction):
    """Open a window with a grid editor on this table as main item.

    """
    use_param_panel = True
    show_in_workflow = False
    opens_a_window = True
    action_name = 'grid'

    def is_callable_from(self, caller):
        return False

    def attach_to_actor(self, actor, name):
        #~ self.label = actor.button_label or actor.label
        self.label = actor.label
        return super(GridEdit, self).attach_to_actor(actor, name)

    def get_window_layout(self, actor):
        #~ return self.actor.list_layout
        return None

    def get_window_size(self, actor):
        return actor.window_size

    def as_bootstrap_html(self, ar, as_main=True):
        # used by lino.modlib.plain and lino.modlib.bootstrap3
        t = xghtml.Table()
        t.attrib.update(class_="table table-striped table-hover")
        if ar.limit is None:
            ar.limit = PLAIN_PAGE_LENGTH
        pglen = ar.limit
        if ar.offset is None:
            page = 1
        else:
            """
            (assuming pglen is 5)
            offset page
            0      1
            5      2
            """
            page = int(ar.offset / pglen) + 1

        ar.dump2html(t, ar.sliced_data_iterator)
        if not as_main:
            url = ar.get_request_url()  # open in own window
            return E.div(E.a(ar.get_title(), href=url), t.as_element())

        buttons = []
        kw = dict()
        kw = {}
        if pglen != PLAIN_PAGE_LENGTH:
            kw[constants.URL_PARAM_LIMIT] = pglen

        if page > 1:
            kw[constants.URL_PARAM_START] = pglen * (page - 2)
            prev_url = ar.get_request_url(**kw)
            kw[constants.URL_PARAM_START] = 0
            first_url = ar.get_request_url(**kw)
        else:
            prev_url = None
            first_url = None
        buttons.append(('<<', _("First page"), first_url))
        buttons.append(('<', _("Previous page"), prev_url))

        next_start = pglen * page
        if next_start < ar.get_total_count():
            kw[constants.URL_PARAM_START] = next_start
            next_url = ar.get_request_url(**kw)
            last_page = int((ar.get_total_count() - 1) / pglen)
            kw[constants.URL_PARAM_START] = pglen * last_page
            last_url = ar.get_request_url(**kw)
        else:
            next_url = None
            last_url = None
        buttons.append(('>', _("Next page"), next_url))
        buttons.append(('>>', _("Last page"), last_url))

        return E.div(buttons2pager(buttons), t.as_element())


class ShowDetailAction(Action):
    """
    Open the :term:`detail Window` on a row of this table.
    """
    icon_name = 'application_form'
    #~ icon_file = 'application_form.png'
    opens_a_window = True
    show_in_workflow = False
    save_action_name = 'submit_detail'

    sort_index = 20
    #~ callable_from = (GridEdit,)

    def is_callable_from(self, caller):
        return isinstance(caller, GridEdit)

    #~ show_in_detail = False
    #~ needs_selection = True
    action_name = 'detail'
    label = _("Detail")
    help_text = _("Open a detail window on this record")

    def get_window_layout(self, actor):
        return actor.detail_layout

    def get_window_size(self, actor):
        wl = self.get_window_layout(actor)
        return wl.window_size

    #~ def get_elem_title(self,elem):
        #~ return _("%s (Detail)")  % unicode(elem)

    def as_bootstrap_html(self, ar, pk):
        rpt = ar.actor

        navigator = None
        if pk and pk != '-99999' and pk != '-99998':
            elem = ar.get_row_by_pk(pk)
            if elem is None:
                raise http.Http404("%s has no row with primary key %r" %
                                   (rpt, pk))
                #~ raise Exception("20120327 %s.get_row_by_pk(%r)" % (rpt,pk))
            if ar.actor.show_detail_navigator:

                ni = navinfo(ar.data_iterator, elem)
                if ni:
                    buttons = []
                    #~ buttons.append( ('*',_("Home"), '/' ))

                    buttons.append(
                        ('<<', _("First page"), ar.pk2url(ni['first'])))
                    buttons.append(
                        ('<', _("Previous page"), ar.pk2url(ni['prev'])))
                    buttons.append(
                        ('>', _("Next page"), ar.pk2url(ni['next'])))
                    buttons.append(
                        ('>>', _("Last page"), ar.pk2url(ni['last'])))

                    navigator = buttons2pager(buttons)
                else:
                    navigator = E.p("No navinfo")
        else:
            elem = None

        wl = ar.bound_action.get_window_layout()
        #~ print 20120901, wl.main
        lh = wl.get_layout_handle(settings.SITE.kernel.default_ui)

        #~ items = list(render_detail(ar,elem,lh.main))
        items = list(lh.main.as_plain_html(ar, elem))
        if navigator:
            items.insert(0, navigator)
        #~ print E.tostring(E.div())
        #~ if len(items) == 0: return ""
        main = E.form(*items)
        #~ print 20120901, lh.main.__html__(ar)
        
        # The `method="html"` argument isn't available in Python 2.6,
        # only 2.7.  It is useful to avoid side effects in case of
        # empty elements: the default method (xml) writes an empty
        # E.div() as "<div/>" while in HTML5 it must be "<div></div>"
        # (and the ending / is ignored).
        
        #~ return E.tostring(main, method="html")
        #~ return E.tostring(main)
        return main


class ShowEmptyTable(ShowDetailAction):
    use_param_panel = True
    action_name = 'show'
    default_format = 'html'
    #~ hide_top_toolbar = True
    hide_navigator = True
    icon_name = None

    def is_callable_from(self, caller):
        return isinstance(caller, GridEdit)

    def attach_to_actor(self, actor, name):
        self.label = actor.label
        return super(ShowEmptyTable, self).attach_to_actor(actor, name)

    def as_bootstrap_html(self, ar):
        return super(ShowEmptyTable, self).as_bootstrap_html(ar, '-99998')


class InsertRow(TableAction):
    """Open the Insert window filled with a row of blank or default
    values.  The new row will be actually created only when this
    window gets submitted.

    """
    save_action_name = 'submit_insert'

    disable_primary_key = False

    label = _("New")
    icon_name = 'add'  # if action rendered as toolbar button
    show_in_workflow = False
    opens_a_window = True
    hide_navigator = True
    sort_index = 10
    hide_top_toolbar = True
    help_text = _("Insert a new record")
    # ~ readonly = False # see blog/2012/0726
    # required_roles = set([SiteUser])
    action_name = 'insert'
    key = keyboard.INSERT  # (ctrl=True)
    hide_virtual_fields = True

    def get_action_title(self, ar):
        return _("Insert into %s") % force_unicode(ar.get_title())

    def get_window_layout(self, actor):
        return actor.insert_layout or actor.detail_layout

    def get_window_size(self, actor):
        wl = self.get_window_layout(actor)
        return wl.window_size

    def get_action_permission(self, ar, obj, state):
        # see blog/2012/0726
        if settings.SITE.user_model and ar.get_user().profile.readonly:
            return False
        return super(InsertRow, self).get_action_permission(ar, obj, state)

    def get_status(self, ar, **kw):
        kw = super(InsertRow, self).get_status(ar, **kw)
        if 'record_id' in kw:
            return kw
        if 'data_record' in kw:
            return kw
        # raise Exception("20150218 %s" % self)
        elem = ar.create_instance()
        # existing = getattr(ar, '_elem', None)
        # if existing is not None:
        #     raise Exception("20150218 %s %s", elem, existing)
        #     if existing == elem:
        #         return kw
        # ar._elem = elem
        rec = ar.elem2rec_insert(ar.ah, elem)
        kw.update(data_record=rec)
        return kw


class UpdateRowAction(Action):
    show_in_workflow = False
    readonly = False
    # required_roles = set([SiteUser])


class SaveRow(Action):
    """
    Called when user edited a cell of a non-phantom record in a grid.
    Installed as `update_action` on every :class:`Actor`.

    """
    sort_index = 10
    show_in_workflow = False
    action_name = 'grid_put'
    readonly = False
    auto_save = False

    def is_callable_from(self, caller):
        return False

    def run_from_ui(self, ar, **kw):
        # logger.info("20140423 SubmitDetail")
        elem = ar.selected_rows[0]
        # ar.form2obj_and_save(ar.rqdata, elem, False)
        self.save_existing_instance(elem, ar)

    def save_existing_instance(self, elem, ar):
        watcher = ChangeWatcher(elem)
        ar.ah.store.form2obj(ar, ar.rqdata, elem, False)
        elem.full_clean()

        if watcher.is_dirty():
            pre_ui_save.send(sender=elem.__class__, instance=elem, ar=ar)
            elem.before_ui_save(ar)
            elem.save(force_update=True)
            watcher.send_update(ar.request)
            ar.success(_("%s has been updated.") % obj2unicode(elem))
        else:
            ar.success(_("%s : nothing to save.") % obj2unicode(elem))

        elem.after_ui_save(ar, watcher)

        # TODO: in fact we need *either* `rows` (when this was called
        # from a Grid) *or* `goto_instance` (when this was called from a
        # form).  But how to find out which one is needed?
        # if ar.edit_mode == constants.EDIT_MODE_GRID:
        ar.set_response(rows=[ar.ah.store.row2list(ar, elem)])


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

    def is_callable_from(self, caller):
        return False

    def run_from_ui(self, ar, **kw):
        elem = ar.create_instance_from_request()
        ar.ah.store.form2obj(ar, ar.rqdata, elem, False)
        elem.full_clean()
        ar.success()
        # ar.set_response(rows=[ar.ah.store.row2list(ar, elem)])
        ar.goto_instance(elem)


class SubmitDetail(SaveRow):
    """The "Save" button of a :term:`detail window`.

    Called when the OK button of a Detail Window was clicked.
    Installed as `submit_detail` on every actor.

    """
    icon_name = 'disk'
    help_text = _("Save changes in this form")
    label = _("Save")
    action_name = ShowDetailAction.save_action_name

    def is_callable_from(self, caller):
        return isinstance(caller, ShowDetailAction)

    def run_from_ui(self, ar, **kw):
        # logger.info("20140423 SubmitDetail")
        elem = ar.selected_rows[0]
        # ar.form2obj_and_save(ar.rqdata, elem, False)
        self.save_existing_instance(elem, ar)
        ar.goto_instance(elem)


class CreateRow(Action):
    """Called when user edited a cell of a phantom record in a grid.
    """
    sort_index = 10
    auto_save = False
    show_in_workflow = False
    readonly = False

    def is_callable_from(self, caller):
        return False

    def run_from_ui(self, ar, **kw):
        elem = ar.create_instance_from_request()
        self.save_new_instance(ar, elem)

    def save_new_instance(self, ar, elem):
        pre_ui_save.send(sender=elem.__class__, instance=elem, ar=ar)
        elem.before_ui_save(ar)
        elem.save(force_insert=True)
        # yes, `on_ui_created` comes *after* save()
        on_ui_created.send(elem, request=ar.request)
        elem.after_ui_create(ar)
        elem.after_ui_save(ar, None)
        ar.success(_("%s has been created.") % obj2unicode(elem))

        if ar.actor.handle_uploaded_files is None:
            # The `rows` can contain complex strings which cause
            # decoding problems on the client when responding to a
            # file upload
            ar.set_response(rows=[ar.ah.store.row2list(ar, elem)])
        else:
            # Must set text/html for file uploads, otherwise the
            # browser adds a <PRE></PRE> tag around the AJAX response.
            ar.set_content_type('text/html')

        if ar.actor.stay_in_grid:
            return
            # No need to ask refresh_all since closing the window will
            # automatically refresh the underlying window.

        ar.goto_instance(elem)


class SubmitInsert(CreateRow):
    """Called when the OK button of an Insert Window was clicked.
    Installed as `submit_insert` on every `dd.Model <lino.core.model.Model>`.
    """
    label = _("Create")
    action_name = None  # 'post'
    help_text = _("Create the record and open a detail window on it")

    def is_callable_from(self, caller):
        return isinstance(caller, InsertRow)

    def run_from_ui(self, ar, **kw):
        elem = ar.create_instance_from_request()
        self.save_new_instance(ar, elem)
        ar.set_response(close_window=True)

# class SubmitInsertAndStay(SubmitInsert):
#     sort_index = 11
#     switch_to_detail = False
#     action_name = 'poststay'
#     label = _("Create without detail")
#     help_text = _("Don't open a detail window on the new record")


class ShowSlaveTable(Action):
    """A action which opens a window showing a table.  The table must be
    specified when instantiating the action.

    """
    TABLE2ACTION_ATTRS = tuple('help_text icon_name label sort_index'.split())
    show_in_bbar = True

    def __init__(self, slave_table, **kw):
        self.slave_table = slave_table
        self.explicit_attribs = set(kw.keys())
        super(ShowSlaveTable, self).__init__(**kw)

    @classmethod
    def get_actor_label(self):
        return self._label or self.slave_table.label

    def attach_to_actor(self, actor, name):
        if isinstance(self.slave_table, basestring):
            T = settings.SITE.modules.resolve(self.slave_table)
            if T is None:
                raise Exception("No table named %s" % self.slave_table)
            self.slave_table = T
        for k in self.TABLE2ACTION_ATTRS:
            if not k in self.explicit_attribs:
                setattr(self, k, getattr(self.slave_table, k))
        return super(ShowSlaveTable, self).attach_to_actor(actor, name)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        sar = ar.spawn(self.slave_table, master_instance=obj)
        js = ar.renderer.request_handler(sar)
        ar.set_response(eval_js=js)


class NotifyingAction(Action):
    """An action with a generic dialog window of three fields "Summary",
    "Description" and a checkbox "Don't send email notification". The
    default implementation calls the request's :meth:`add_system_note
    <lino.core.requests.BaseRequest.add_system_note>` method.

    Screenshot of a notifying action:

    .. image:: /images/screenshots/reception.CheckinVisitor.png
        :scale: 50

    Dialog fields:

    .. attribute:: subject
    .. attribute:: body
    .. attribute:: silent

    """
    custom_handler = True

    parameters = dict(
        notify_subject=models.CharField(
            _("Summary"), blank=True, max_length=200),
        notify_body=fields.RichTextField(_("Description"), blank=True),
        notify_silent=models.BooleanField(
            _("Don't send email notification"), default=False),
    )

    params_layout = layouts.Panel("""
    notify_subject
    notify_body
    notify_silent
    """, window_size=(50, 15))

    def get_notify_subject(self, ar, obj):
        """
        Return the default value of the `notify_subject` field.
        """
        return None

    def get_notify_body(self, ar, obj):
        """
        Return the default value of the `notify_body` field.
        """
        return None

    def action_param_defaults(self, ar, obj, **kw):
        kw = super(NotifyingAction, self).action_param_defaults(ar, obj, **kw)
        if obj is not None:
            s = self.get_notify_subject(ar, obj)
            if s is not None:
                kw.update(notify_subject=s)
            s = self.get_notify_body(ar, obj)
            if s is not None:
                kw.update(notify_body=s)
        return kw

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        ar.set_response(message=ar.action_param_values.notify_subject)
        ar.set_response(refresh=True)
        ar.set_response(success=True)
        self.add_system_note(ar, obj)

    def add_system_note(self, ar, owner, **kw):
        #~ body = _("""%(user)s executed the following action:\n%(body)s
        #~ """) % dict(user=ar.get_user(),body=body)
        ar.add_system_note(
            owner,
            ar.action_param_values.notify_subject,
            ar.action_param_values.notify_body,
            ar.action_param_values.notify_silent, **kw)


class MultipleRowAction(Action):
    """Base class for actions that update something on every selected row.
    """
    custom_handler = True
    callable_from = (GridEdit, ShowDetailAction)

    def run_on_row(self, obj, ar):
        """This is being called on every selected row.
        """
        raise NotImplemented()

    def run_from_ui(self, ar, **kw):
        ar.success(**kw)
        n = 0
        for obj in ar.selected_rows:
            if not ar.response.get('success'):
                ar.info("Aborting remaining rows")
                break
            ar.info("%s for %s...", unicode(self.label), unicode(obj))
            n += self.run_on_row(obj, ar)
            ar.set_response(refresh_all=True)

        msg = _("%d row(s) have been updated.") % n
        ar.info(msg)
        #~ ar.success(msg,**kw)


class DeleteSelected(MultipleRowAction):
    """The action used to delete the selected row(s). Automatically
    installed on every editable actor.

    """

    action_name = 'delete_selected'  # because...
    icon_name = 'delete'
    help_text = _("Delete this record")
    auto_save = False
    sort_index = 30
    readonly = False
    show_in_workflow = False
    # required_roles = set([SiteUser])
    #~ callable_from = (GridEdit,ShowDetailAction)
    #~ needs_selection = True
    label = _("Delete")
    #~ url_action_name = 'delete'
    key = keyboard.DELETE  # (ctrl=True)
    #~ client_side = True

    def run_from_ui(self, ar, **kw):
        objects = []
        for obj in ar.selected_rows:
            objects.append(unicode(obj))
            msg = ar.actor.disable_delete(obj, ar)
            if msg is not None:
                ar.error(None, msg, alert=True)
                return
        
        def ok(ar2):
            super(DeleteSelected, self).run_from_ui(ar, **kw)
            ar2.success(record_deleted=True)
            if ar2.actor.detail_action:
                ar2.set_response(
                    detail_handler_name=ar2.actor.detail_action.full_name())

        d = dict(num=len(objects), targets=', '.join(objects))
        if len(objects) == 1:
            d.update(type=ar.actor.model._meta.verbose_name)
        else:
            d.update(type=ar.actor.model._meta.verbose_name_plural)
        ar.confirm(
            ok,
            string_concat(
                _("You are about to delete %(num)d %(type)s:\n"
                  "%(targets)s") % d,
                '\n',
                _("Are you sure ?")))

    def run_on_row(self, obj, ar):
        pre_ui_delete.send(sender=obj, request=ar.request)
        obj.delete()
        return 1


def action(*args, **kw):
    """Decorator to define custom actions.
    
    The decorated function will be installed as the actions's
    :meth:`run_from_ui <Action.run_from_ui>` method.

    Same signature as :meth:`Action.__init__`.
    In practice you'll possibly use:
    :attr:`label <Action.label>`,
    :attr:`help_text <Action.help_text>` and
    :attr:`required_roles <lino.core.permissions.Permittable.required_roles>`.

    """
    def decorator(fn):
        assert not 'required' in kw
        # print 20140422, fn.__name__
        kw.setdefault('custom_handler', True)
        a = Action(*args, **kw)

        def wrapped(ar):
            obj = ar.selected_rows[0]
            return fn(obj, ar)
        a.run_from_ui = wrapped
        return a
    return decorator


def get_view_permission(e):
    from lino.utils import jsgen
    if isinstance(e, Permittable) and not e.get_view_permission(
            jsgen._for_user_profile):
        return False
    # e.g. pcsw.ClientDetail has a tab "Other", visible only to system
    # admins but the "Other" contains a GridElement RolesByPerson
    # which is not per se reserved for system admins.  js of normal
    # users should not try to call on_master_changed() on it
    parent = e.parent
    while parent is not None:
        if isinstance(parent, Permittable) and not parent.get_view_permission(
                jsgen._for_user_profile):
            return False  # bug 3 (bcss_summary) blog/2012/0927
        parent = parent.parent
    return True


