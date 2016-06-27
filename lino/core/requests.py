# -*- coding: UTF-8 -*-
# Copyright 2009-2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""
See introduction in :doc:`/dev/ar`.

.. autosummary::

"""
from builtins import str
from builtins import object
import six

import logging
logger = logging.getLogger(__name__)

from copy import copy
from cgi import escape

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language
from django.utils import translation
from django.utils import timezone
from django.core import exceptions

from lino.core.utils import obj2unicode
from lino.core import constants
from lino.core.utils import navinfo
from lino.core.boundaction import BoundAction
from lino.core.signals import on_ui_created, pre_ui_save
from lino.core.utils import ChangeWatcher
from lino.core.utils import getrqdata
from lino.utils import AttrDict
from lino.utils.xmlgen.html import E


CATCHED_AJAX_EXCEPTIONS = (Warning, exceptions.ValidationError)


class ValidActionResponses(object):
    """These are the allowed keyword arguments for :meth:`ar.set_response
    <BaseRequest.set_response>`, and the action responses supported by
    :js:func:`Lino.handle_action_result` (defined in :xfile:`linolib.js`).

    This class is never instantiated, but used as a placeholder for
    these names and their documentation.

    """

    message = None
    """a string with a message to be shown to the user.
    """

    alert = None
    """ True to specify that the message is rather important
    and should alert and should be presented in a dialog box to be
    confirmed by the user.
    """

    success = None

    errors = None
    html = None
    rows = None

    data_record = None
    """Certain requests are expected to return the detailed information
    about a single data record. That's done in :attr:`data_record`
    which must itself be a dict with the following keys:

    - id : the primary key of this record_deleted
    - title : the title of the detail window
    - data : a dict with one key for every data element
    - navinfo : an object with information for the navigator
    - disable_delete : either null (if that record may be deleted, or
      otherwise a message explaining why.

    """

    record_id = None
    """When an action returns a `record_id`, it asks the user interface to
    jump to the given record.

    """

    refresh = None
    refresh_all = None
    close_window = None
    record_deleted = None
    xcallback = None
    open_url = None
    open_davlink_url = None
    info_message = None
    warning_message = None
    "deprecated"

    eval_js = None
    active_tab = None

    detail_handler_name = None
    """The name of the detail handler to be used.  Application code should
    not need to use this.  It is automatically set by
    :meth:`ActorRequest.goto_instance`.

    """


# ACTION_RESPONSES = frozenset((
#     'message', 'success', 'alert',
#     'errors',
#     'html',
#     'rows',
#     'data_record',
#     'detail_handler_name',
#     'record_id',
#     'refresh', 'refresh_all',
#     'close_window',
#     'record_deleted',
#     'xcallback',
#     'open_url',
#     'open_davlink_url',
#     'info_message',
#     'warning_message',  # deprecated
#     'eval_js',
#     'active_tab'))


class VirtualRow(object):

    def __init__(self, **kw):
        self.update(**kw)

    def update(self, **kw):
        for k, v in list(kw.items()):
            setattr(self, k, v)

    def get_row_permission(self, ar, state, ba):
        if ba.action.readonly:
            return True
        return False


from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class PhantomRow(VirtualRow):

    def __init__(self, request, **kw):
        self._ar = request
        VirtualRow.__init__(self, **kw)

    def __str__(self):
        return six.text_type(self._ar.get_action_title())


inheritable_attrs = frozenset(
    'user subst_user renderer requesting_panel master_instance'.split())


class BaseRequest(object):
    """Base class of all action requests.

    """
    user = None
    subst_user = None

    renderer = None
    """The renderer to use when processing this request."""

    actor = None
    action_param_values = None
    param_values = None
    bound_action = None
    known_values = {}
    master_instance = None
    """The database object which acts as master. This is `None` for master
    requests.

    """

    request = None
    """The incoming Django HttpRequest object which caused this action
    request.

    """

    selected_rows = []
    content_type = 'application/json'
    requesting_panel = None

    def __init__(self, request=None, parent=None, **kw):
        self.request = request
        self.response = dict()
        if request is not None:
            rqdata = getrqdata(request)
            kw = self.parse_req(request, rqdata, **kw)
        if parent is not None:
            for k in inheritable_attrs:
                if k in kw:
                    if kw[k] is None:
                        raise Exception("%s : %s=None" % (kw, k))
                else:
                    kw[k] = getattr(parent, k)
            kv = kw.setdefault('known_values', {})
            kv.update(parent.known_values)
            # kw.setdefault('user', parent.user)
            # kw.setdefault('subst_user', parent.subst_user)
            # kw.setdefault('renderer', parent.renderer)
            # kw.setdefault('requesting_panel', parent.requesting_panel)
            
        self.setup(**kw)

    def setup(self,
              user=None,
              subst_user=None,
              current_project=None,
              selected_pks=None,
              master_instance=None,
              limit=None,
              requesting_panel=None,
              renderer=None):
        """If a `limit` is specified, this is ignored silently.
        """
        self.requesting_panel = requesting_panel
        self.master_instance = master_instance
        if user is None:
            from lino.modlib.users.utils import AnonymousUser
            self.user = AnonymousUser.instance()
        else:
            self.user = user
        self.current_project = current_project
        if renderer is None:
            renderer = settings.SITE.kernel.text_renderer
        self.renderer = renderer
        self.subst_user = subst_user

        if selected_pks is not None:
            self.set_selected_pks(*selected_pks)

    def parse_req(self, request, rqdata, **kw):
        """Parse the given incoming HttpRequest and set up this action
request from it.

        """
        kw.update(user=request.user)
        kw.update(subst_user=request.subst_user)
        kw.update(requesting_panel=request.requesting_panel)
        kw.update(current_project=rqdata.get(
            constants.URL_PARAM_PROJECT, None))

        # If the incoming request specifies an active tab, then the
        # response must forward this information. Otherwise Lino would
        # forget the current tab when a user saves a detail form for
        # the first time.  The `active_tab` is not (yet) used directly
        # by Python code, so we don't store it as attribute on `self`,
        # just in the response.
        tab = rqdata.get(constants.URL_PARAM_TAB, None)
        if tab is not None:
            tab = int(tab)
            # logger.info("20150130 b %s", tab)
            self.set_response(active_tab=tab)

        selected = rqdata.getlist(constants.URL_PARAM_SELECTED)
        kw.update(selected_pks=selected)

        #~ if settings.SITE.user_model:
            #~ username = rqdata.get(constants.URL_PARAM_SUBST_USER,None)
            #~ if username:
                #~ try:
                    #~ kw.update(subst_user=settings.SITE.user_model.objects.get(username=username))
                #~ except settings.SITE.user_model.DoesNotExist, e:
                    #~ pass
        # logger.info("20140503 ActionRequest.parse_req() %s", kw)
        return kw

    def setup_from(self, other):
        """Copy certain values (renderer, user, subst_user &
        requesting_panel) from this request to the other.

        """
        if not self.must_execute():
            return
            # raise Exception("Request %r was already executed" % other)
        self.renderer = other.renderer
        # self.cellattrs = other.cellattrs
        # self.tableattrs = other.tableattrs
        self.user = other.user
        self.subst_user = other.subst_user
        self._confirm_answer = other._confirm_answer
        # self.master_instance = other.master_instance  # added 20150218
        self.requesting_panel = other.requesting_panel

    def spawn_request(self, **kw):
        """Create a new of same class which inherits from this one.

        """
        kw.update(parent=self)
        return self.__class__(**kw)

    def spawn(self, spec=None, **kw):
        """Create a new action request using default values from this one and
        the action specified by `spec`.

        The first argument, `spec` can be:

        - a string with the name of a model, actor or action
        - a :class:`BoundAction` instance
        - another action request (deprecated use)

        """
        from lino.core.actors import resolve_action
        if isinstance(spec, ActionRequest):  # deprecated use
            # raise Exception("20160627 Deprecated")
            for k, v in list(kw.items()):
                assert hasattr(spec, k)
                setattr(spec, k, v)
            spec.setup_from(self)
        elif isinstance(spec, BoundAction):
            kw.update(parent=self)
            spec = spec.request(**kw)
            # spec.setup_from(self)
        else:
            kw.update(parent=self)
            ba = resolve_action(spec)
            spec = ba.request(**kw)
            # from lino.core.menus import create_item
            # mi = create_item(spec)
            # spec = mi.bound_action.request(**kw)
        return spec

    def get_printable_context(self, **kw):
        """Adds a series of names to the context used when rendering printable
        documents. See :doc:`/user/templates_api`.

        """
        # from django.conf import settings
        from django.utils.translation import ugettext
        from django.utils.translation import pgettext
        from lino.api import dd, rt
        from lino.utils import iif
        from lino.utils.restify import restify


        if False:  # 20150803 why was this?  It disturbed e.g. for the bs3
                   # language selector.
            sar = copy(self)
            sar.renderer = settings.SITE.kernel.html_renderer
            kw['ar'] = sar
        else:
            kw['ar'] = self

        kw['_'] = ugettext
        kw.update(
            E=E,
            dd=dd,
            rt=rt,
            decfmt=dd.decfmt,
            fds=dd.fds,
            fdm=dd.fdm,
            fdl=dd.fdl,
            fdf=dd.fdf,
            fdmy=dd.fdmy,
            iif=iif,
            unicode=str,  # backwards-compatibility. In new template
                          # you should prefer `str`.
            pgettext=pgettext,
            now=timezone.now(),
            getattr=getattr,
            restify=restify,
            requested_language=get_language())

        def parse(s):
            # return settings.SITE.jinja_env.from_string(s).render(**kw)
            return dd.plugins.jinja.renderer.jinja_env.from_string(
                s).render(**kw)
        kw.update(parse=parse)
        return kw

    def set_selected_pks(self, *selected_pks):
        """Given a tuple of primary keys, set :attr:`selected_rows` to a list
        of corresponding database objects.

        """
        #~ print 20131003, selected_pks
        self.selected_rows = [
            self.get_row_by_pk(pk) for pk in selected_pks if pk]
        # note: ticket #523 was because the GET contained an empty pk ("&sr=")

    def get_permission(self):
        """Whether this request has permission to run on the given database
        object. `obj` can be None if the action is a list action
        (whose `select_rows` is `False`).

        """
        if self.bound_action.action.select_rows:
            if len(self.selected_rows) == 0:
                return False
            obj = self.selected_rows[0]
            state = self.bound_action.actor.get_row_state(obj)
            return self.bound_action.get_row_permission(self, obj, state)
        return self.bound_action.get_bound_action_permission(
            self, None, None)
        
    def set_response(self, **kw):
        """Set (some part of) the response to be sent when the action request
        finishes.  Allowed keywords are documented in
        :class:`ValidActionResponses`.

        This does not yet respond anything, it is stored until the action
        has finished. The response might be overwritten by subsequent
        calls to :meth:`set_response`.

        :js:func:`Lino.handle_action_result` will get these instructions
        as *keywords* and thus will not know the order in which they have
        been issued. This is a design decision.  We *want* that, when
        writing custom actions, the order of these instructions does not
        matter.

        """
        for k in list(kw.keys()):
            if not hasattr(ValidActionResponses, k):
                raise Exception("Unknown key %r in action response." % k)
        self.response.update(kw)
            
    def error(self, e=None, message=None, **kw):
        """Shortcut to :meth:`set_response` used to set an error response.

        The first argument should be either an exception object or a
        text with a message.

        If a message is not explicitly given, Lino escapes any
        characters with a special meaning in HTML. For example::

            NotImplementedError: <dl> inside <text:p>
    
        will be converted to::
    
            NotImplementedError: &lt;dl&gt; inside &lt;text:p&gt;

        """
        kw.update(success=False)
        kw.update(alert=_("Error"))  # added 20140304
        if isinstance(e, Exception):
            if False:  # useful when debugging, but otherwise rather disturbing
                logger.exception(e)
            if hasattr(e, 'message_dict'):
                kw.update(errors=e.message_dict)
        if message is None:
            try:
                message = six.text_type(e)
            except UnicodeDecodeError as e:
                message = repr(e)
            message = escape(message)
        kw.update(message=message)
        self.set_response(**kw)

    def success(self, message=None, alert=None, **kw):
        """Tell the client to consider the action as successful. This is the
        same as :meth:`set_response` with `success=True`.

        First argument should be a textual message.

        """
        kw.update(success=True)
        if alert is not None:
            if alert is True:
                alert = _("Success")
            kw.update(alert=alert)
        if message is not None:
            if 'message' in self.response and alert is None:
                # ignore alert-less messages when there is already a
                # message set. For example
                # finan.FinancialVoucherItem.parter_changed with more
                # than 1 suggestion.
                pass
            else:
                kw.update(message=message)
        self.set_response(**kw)

    def append_message(self, level, msg, *args, **kw):
        if args:
            msg = msg % args
        if kw:
            msg = msg % kw
        k = level + '_message'
        old = self.response.get(k, None)
        if old is None:
            self.response[k] = msg
        else:
            self.response[k] = old + '\n' + msg
        # return self.success(*args,**kw)

    def debug(self, msg, *args, **kw):
        if settings.SITE.verbose_client_info_message:
            self.append_message('info', msg, *args, **kw)

    def info(self, msg, *args, **kw):
        # deprecated?
        self.append_message('info', msg, *args, **kw)

    def warning(self, msg, *args, **kw):
        # deprecated?
        self.append_message('warning', msg, *args, **kw)

    _confirm_answer = True

    def set_confirm_answer(self, ans):
        """Set a "No" answer for following confirm in a non-interactive
        renderer.

        """
        self._confirm_answer = ans

    def confirm(self, ok_func, *msgs):
        """Execute the specified callable `ok_func` after the user has
        confirmed the specified message.
        
        The confirmation message may be specified as a series of
        positional arguments which will be concatenated to a single
        prompt.

        The callable will be called with a single positional argument
        which will be the action request that confirmed the
        message. In a web context this will be another object than
        this one.

        In a non-interactive environment the `ok_func` function is
        called directly (i.e. we don't ask any confirmation and act as
        confirmation had been given).

        """
        cb = self.add_callback(*msgs)

        def noop(ar):
            return ar.success(_("Aborted"))
        cb.add_choice('yes', ok_func, _("Yes"))
        cb.add_choice('no', noop, _("No"))
        self.set_callback(cb)

        if not self.renderer.is_interactive:
            if self._confirm_answer:
                ok_func(self)

    def parse_memo(self, html, **context):
        context.update(ar=self)
        return settings.SITE.kernel.memo_parser.parse(html, **context)

    # def parse_memo(self, html):
    #     return self.renderer.parse_memo(html, ar=self)

    def render_jinja(self, template, **context):
        sar = copy(self)
        # sar.renderer = settings.SITE.kernel.html_renderer
        sar.renderer = settings.SITE.plugins.jinja.renderer
        context.update(ar=sar)
        # self.renderer = settings.SITE.plugins.bootstrap3.renderer
        return template.render(**context)

    def set_callback(self, *args, **kw):
        return settings.SITE.kernel.set_callback(self, *args, **kw)

    def add_callback(self, *args, **kw):
        return settings.SITE.kernel.add_callback(self, *args, **kw)

    def goto_instance(self, obj, **kw):
        """
        Ask the client to display a :term:`detail window` on the given
        record. The client might ignore this if Lino does not know a
        detail window.

        This is a utility wrapper around :meth:`set_response` which sets
        either `data_record` or a `record_id`.

        Usually `data_record`, except if it is a `file upload
        <https://docs.djangoproject.com/en/dev/topics/http/file-uploads/>`_
        where some mysterious decoding problems (:blogref:`20120209`)
        force us to return a `record_id` which has the same visible
        result but using an additional GET.

        If the calling window is a detail on the same table, then it
        should simply get updated to the given record. Otherwise open a
        new detail window.

        """
        js = self.instance_handler(obj)
        kw.update(eval_js=js)
        self.set_response(**kw)

    def close_window(self, **kw):
        """Ask client to close the current window. This is the same as
        :meth:`BaseRequest.set_response` with `close_window=True`.

        """
        kw.update(close_window=True)
        self.set_response(**kw)

    def set_content_type(self, ct):
        # logger.info("20140430 set_content_type(%r)", ct)
        self.content_type = ct

    def must_execute(self):
        return True

    def get_data_value(self, obj, name):
        """Return the value of the virtual field `name` for this action
        request on the given object `obj`.

        """
        fld = obj.get_data_elem(name)
        return fld.value_from_object(obj, self)

    def get_user(self):
        """Return the :class:`User <lino.modlib.users.models.User>` instance
        of the user who issued the request.  If the authenticated user
        is acting as somebody else, return that user's instance.

        """
        return self.subst_user or self.user

    def add_system_note(self, owner, subject, body, silent):
        """Calls the Site's :meth:`emit_system_note
        <lino.core.site.Site.emit_system_note>` method.

        """
        settings.SITE.emit_system_note(
            self.request, owner, subject, body, silent)

    def run(self, thing, *args, **kw):
        """The first parameter `thing` may be an :class:`InstanceAction
        <lino.core.utils.InstanceAction>` or a Model instance.

        """
        return thing.run_from_session(self, *args, **kw)

    def story2html(self, story, *args, **kwargs):
        """Convert a story into a stream of HTML elements.

        """
        # return self.renderer.show_story(self, story, *args, **kwargs)
        return settings.SITE.kernel.html_renderer.show_story(
            self, story, *args, **kwargs)

    def story2rst(self, story, *args, **kwargs):
        return self.renderer.show_story(self, story, *args, **kwargs)

    def show(self, spec, master_instance=None, column_names=None,
             header_level=None, language=None, nosummary=False,
             stripped=True, **kwargs):
        """Show the specified table or action using the current renderer.  If
        the table is a :term:`slave table`, then a `master_instance` must
        be specified as second argument.

        The first argument specifies the table or actor to show. It is
        forwarded to :meth:`spawn`.

        Optional keyword arguments are:

        :column_names: overrides default list of columns

        :nosummary: if it is a table with :attr:`slave_grid_format
                    <lino.core.tables.AbstractTable.slave_grid_format>`
                    set to ``'summary'``, force rendering it as a
                    table.

        :header_level: show also the header (using specified level)

        :language: overrides the default language used for headers and
                   translatable data

        Any other keyword arguments are forwarded to :meth:`spawn`.

        Note that this function either returns a string or prints to
        stdout and returns None, depending on the current renderer.

        Usage in a :doc:`tested document </dev/tested_docs>`:

        >>> from lino.api import rt
        >>> rt.login('robin').show('users.UsersOverview', limit=5)

        Usage in a Jinja template::

          {{ar.show('users.UsersOverview')}}

        """
        from lino.utils.report import Report

        if master_instance is not None:
            kwargs.update(master_instance=master_instance)

        ar = self.spawn(spec, **kwargs)

        def doit():
            # print 20160530, ar.renderer
            if issubclass(ar.actor, Report):
                story = ar.actor.get_story(None, ar)
                return ar.renderer.show_story(
                    self, story, header_level=header_level, stripped=stripped)
            return ar.renderer.show_table(
                ar, column_names=column_names, header_level=header_level,
                nosummary=nosummary, stripped=stripped)

        if language:
            with translation.override(language):
                return doit()
        return doit()

    def show_menu(self, language=None, **kwargs):
        """Show the main menu for the requesting user using the requested
        renderer.

        This is uses in tested docs.

        :language: explicitly select another language than that
                   specified in the requesting user's :attr:`language
                   <lino.modlib.users.models.User.language>` field.

        """
        user = self.get_user()
        if language is None:
            language = user.language
        with translation.override(language):
            mnu = settings.SITE.get_site_menu(None, user.profile)
            self.renderer.show_menu(self, mnu, **kwargs)

    def get_home_url(self, *args, **kw):
        """Return URL to the "home page" as defined by the renderer, without
        switching language to default language.

        """
        if translation.get_language() != settings.SITE.DEFAULT_LANGUAGE:
            kw[constants.URL_PARAM_USER_LANGUAGE] = translation.get_language()
        return self.renderer.get_home_url(*args, **kw)

    def get_request_url(self, *args, **kw):
        """When called on a BaseRequest, this just redirects to home.

        """
        return self.renderer.get_home_url(*args, **kw)

    def summary_row(self, obj, **kwargs):
        return obj.summary_row(self, **kwargs)

    def instance_handler(self, *args, **kwargs):
        return self.renderer.instance_handler(self, *args, **kwargs)

    def pk2url(self, *args, **kwargs):
        return self.renderer.pk2url(self, *args, **kwargs)

    def obj2html(self, *args, **kwargs):
        """Return a HTML element which represents a pointer to the given
        database object. Depending on the renderer this will be more
        or less clickable.

        """
        return self.renderer.obj2html(self, *args, **kwargs)

    def obj2str(self, *args, **kwargs):
        """Return a string with a pointer to the given object.
        """
        return self.renderer.obj2str(self, *args, **kwargs)

    def href_button(self, *args, **kwargs):
        return self.renderer.href_button(*args, **kwargs)

    def href_to_request(self, *args, **kwargs):
        return self.renderer.href_to_request(self, *args, **kwargs)

    def window_action_button(self, *args, **kwargs):
        # settings.SITE.logger.info(
        #     "20160529 window_action_button %s %s", args, self.renderer)
        return self.renderer.window_action_button(self, *args, **kwargs)

    def row_action_button(self, obj, ba, *args, **kwargs):
        return self.renderer.row_action_button(
            obj, None, ba, *args, **kwargs)

    def row_action_button_ar(self, obj, *args, **kw):
        """Return an HTML element with a button for running this action
         request on the given database object. Does not spawn another
         request.

        """
        return self.renderer.row_action_button_ar(obj, self, *args, **kw)

    def ar2button(self, *args, **kw):
        """Return an HTML element with a button for running this action
         request. Does not spawn another request. Does not check
         permissions.

        """
        return self.renderer.ar2button(self, *args, **kw)

    def instance_action_button(self, ai, *args, **kw):
        """Return an HTML element with a button which would run the given
        :class:`InstanceAction <lino.core.utils.InstanceAction>`
        ``ai`` on the client.

        """
        # logger.info("20141106 %s", ai.instance)
        return self.renderer.row_action_button(
            ai.instance, self, ai.bound_action, *args, **kw)

    def action_button(self, ba, obj, *args, **kwargs):
        """Returns the HTML of an action link which will run the specified
        action.

        ``kwargs`` may contain additional html attributes like `style`.

        """
        return self.renderer.action_button(obj, self, ba, *args, **kwargs)

    def get_detail_title(self, elem):
        return self.actor.get_detail_title(self, elem)

    def put_button(self, obj, text, data, **kw):
        """
        Render a button which when clicked will send a PUT
        for the given row with the specified data.
        
        Usage example::
        
            @dd.displayfield(_("My answer"))
            def answer_buttons(self,obj,ar):
                l = []
                if self.choice is None:
                    kw = dict(title=_("Select this value"))
                    for c in self.question.get_choiceset().choices.all():
                        l.append(
                            ar.put_button(self,
                            unicode(c), dict(choice=c),**kw))
                else:
                    l.append(E.b(unicode(self.choice)))
                    l.append(ar.put_button(
                        self, _("Undo"), dict(choice=None),
                        title=_("Undo your vote")))
                return E.span(*join_elems(l))

        
        """
        return self.renderer.put_button(self, obj, text, data, **kw)

    def as_button(self, *args, **kw):
        """Return a button which when activated executes (a copy of)
        this request.

        """
        return self.renderer.action_button(
            None, self, self.bound_action, *args, **kw)

    def elem2rec1(ar, rh, elem, **rec):
        rec.update(data=rh.store.row2dict(ar, elem))
        return rec

    def elem2rec_insert(self, ah, elem):
        """
        Returns a dict of this record, designed for usage by an InsertWindow.
        """
        rec = self.elem2rec1(ah, elem)
        rec.update(title=self.get_action_title())
        rec.update(phantom=True)
        return rec

    def elem2rec_detailed(ar, elem, **rec):
        """Adds additional information for this record, used only by detail
        views.

        The "navigation information" is a set of pointers to the next,
        previous, first and last record relative to this record in
        this report.  (This information can be relatively expensive
        for records that are towards the end of the queryset.  See
        `/blog/2010/0716`, `/blog/2010/0721`, `/blog/2010/1116`,
        `/blog/2010/1207`.)

        recno 0 means "the requested element exists but is not
        contained in the requested queryset".  This can happen after
        changing the quick filter (search_change) of a detail view.

        """
        rh = ar.ah
        rec = ar.elem2rec1(rh, elem, **rec)
        if ar.actor.hide_top_toolbar:
            rec.update(title=ar.get_detail_title(elem))
        else:
            #~ print(ar.get_title())
            #~ print(dd.obj2str(elem))
            #~ print(repr(unicode(elem)))
            if True:  # before 20131017
                rec.update(title=ar.get_title() + u" » " +
                           ar.get_detail_title(elem))
            else:  # todo
                rec.update(title=E.tostring(ar.href_to_request(ar))
                           + u" » " + ar.get_detail_title(elem))
        rec.update(id=elem.pk)
        if ar.actor.editable:
            rec.update(disable_delete=rh.actor.disable_delete(elem, ar))
        if rh.actor.show_detail_navigator:
            rec.update(navinfo=navinfo(ar.data_iterator, elem))
        return rec

    def form2obj_and_save(ar, data, elem, is_new):
        """Parses the data from HttpRequest to the model instance and saves it

        This is used by `ApiList.post` and `ApiElement.put`, and by
        `Restful.post` and `Restful.put`.

        20140505 : no longer used by ApiList and ApiElement, but still
        by Restful.*

        """
        if is_new:
            watcher = None
        else:
            watcher = ChangeWatcher(elem)
        ar.ah.store.form2obj(ar, data, elem, is_new)
        elem.full_clean()

        if is_new or watcher.is_dirty():
            pre_ui_save.send(sender=elem.__class__, instance=elem, ar=ar)
            elem.before_ui_save(ar)

            kw2save = {}
            if is_new:
                kw2save.update(force_insert=True)
            else:
                kw2save.update(force_update=True)

            elem.save(**kw2save)

            if is_new:
                on_ui_created.send(elem, request=ar.request)
                ar.success(_("%s has been created.") % obj2unicode(elem))
            else:
                watcher.send_update(ar.request)
                ar.success(_("%s has been updated.") % obj2unicode(elem))
        else:
            ar.success(_("%s : nothing to save.") % obj2unicode(elem))

        elem.after_ui_save(ar, watcher)

    def get_help_url(self, docname=None, text=None, **kw):
        """Generate a link to the help section of the documentation (whose
        base is defined by :attr:`lino.core.site.Site.help_url`)

        Usage example::

            help = ar.get_help_url("foo", target='_blank')
            msg = _("You have a problem with foo."
                    "Please consult %(help)s "
                    "or ask your system administrator.")
            msg %= dict(help=E.tostring(help))
            kw.update(message=msg, alert=True)

        The :ref:`lino.tutorial.pisa` tutorial shows a resulting message
        generated by the print action.

        """
        if text is None:
            text = six.text_type(_("the documentation"))
        url = settings.SITE.help_url
        if docname is not None:
            url = "%s/help/%s.html" % (url, docname)
        return E.a(text, href=url, **kw)


class ActorRequest(BaseRequest):
    """Base for :class:`ActionRequest`, but also used directly by
    :meth:`lino.core.kernel.Kernel.run_callback`.

    """
    no_data_text = _("No data to display")

    def create_phantom_rows(self, **kw):
        if self.create_kw is None or not self.actor.editable \
           or not self.actor.allow_create:
            return
        if not self.actor.get_create_permission(self):
            return
        yield PhantomRow(self, **kw)

    def create_instance(self, **kw):
        """Create a row (a model instance if this is a database table) using
        the specified keyword arguments.

        """
        if self.create_kw:
            kw.update(self.create_kw)
        if self.known_values:
            kw.update(self.known_values)
        obj = self.actor.create_instance(self, **kw)
        return obj

    def create_instance_from_request(self):
        elem = self.create_instance()
        if self.actor.handle_uploaded_files is not None:
            self.actor.handle_uploaded_files(elem, self.request)

        if self.request is not None:
            self.ah.store.form2obj(self, self.request.POST, elem, True)
        elem.full_clean()
        return elem

    def get_status(self, **kw):
        """Return a `dict` with the "status", i.e. a json representation of
        this request.

        """
        if self.actor.parameters:
            kw.update(
                param_values=self.actor.params_layout.params_store.pv2dict(
                    self.param_values))

        kw = self.bound_action.action.get_status(self, **kw)

        bp = kw.setdefault('base_params', {})

        if self.current_project is not None:
            bp[constants.URL_PARAM_PROJECT] = self.current_project

        if self.subst_user is not None:
            bp[constants.URL_PARAM_SUBST_USER] = self.subst_user.id
        return kw

    # def spawn(self, actor, **kw):
    #     """Same as :meth:`BaseRequest.spawn`, except that the first positional
    #     argument is an `actor`.

    #     """
    #     if actor is None:
    #         actor = self.actor
    #     return super(ActorRequest, self).spawn(actor, **kw)

    def summary_row(self, *args, **kw):
        return self.actor.summary_row(self, *args, **kw)

    def get_sum_text(self, sums):
        return self.actor.get_sum_text(self, sums)

    def get_row_by_pk(self, pk):
        return self.actor.get_row_by_pk(self, pk)

    def get_action_title(self):
        return self.bound_action.action.get_action_title(self)

    def get_title(self):
        return self.actor.get_title(self)

    def render_to_dict(self):
        return self.bound_action.action.render_to_dict(self)

    def goto_instance(self, obj, **kw):
        """Ask the client to open a detail window on this object.  The effect
        is like :meth:`BaseRequest.goto_instance`, but if the detail
        layout of the current actor can be used for the object to be
        displayed, we don't want to open a new detail window.

        This calls :meth:`obj.get_detail_action
        <lino.core.model.Model.get_detail_action>`.

        """
        # e.g. find_by_beid is called from viewport, so there is no
        # requesting_panel.
        # if self.actor.model is None \
        #    or not isinstance(obj, self.actor.model) \
        #    or self.actor.detail_action is None:
        #     return super(ActorRequest, self).goto_instance(obj, **kw)
        da = obj.get_detail_action(self)
        if da is None:
            return
        if da.actor != self.actor:
            return super(ActorRequest, self).goto_instance(obj, **kw)
        # da = self.actor.detail_action
        self.set_response(detail_handler_name=da.full_name())
        if self.actor.handle_uploaded_files is not None:
            self.set_response(record_id=obj.pk)
        else:
            self.set_response(data_record=self.elem2rec_detailed(obj))

    def get_request_url(self, *args, **kw):
        return self.renderer.get_request_url(self, *args, **kw)

    def absolute_uri(self, *args, **kw):
        ar = self.spawn(*args, **kw)
        #~ location = ar.renderer.get_request_url(ar)
        location = ar.get_request_url()
        return self.request.build_absolute_uri(location)

    def run(self, *args, **kw):
        """
        Runs this action request.
        """
        return self.bound_action.action.run_from_code(self, *args, **kw)


class ActionRequest(ActorRequest):
    """Holds information about an indivitual web request and provides
    methods like

    - :meth:`get_user <lino.core.actions.BaseRequest.get_user>`
    - :meth:`confirm <lino.core.actions.BaseRequest.confirm>`
    - :meth:`spawn <lino.core.actions.BaseRequest.spawn>`
    
    An `ActionRequest` is also a :class:`BaseRequest` and inherits its
    methods.

    """
    create_kw = None
    renderer = None

    offset = None
    limit = None
    order_by = None

    def __init__(self, actor=None,
                 unused_request=None, action=None, unused_renderer=None,
                 rqdata=None,
                 **kw):
        """
        An ActionRequest is instantiated from different shortcut methods:
        
        - :meth:`lino.core.actors.Actor.request`
        - :meth:`lino.core.actions.Action.request`
        
        """
        assert unused_renderer is None
        assert unused_request is None
        self.actor = actor
        self.rqdata = rqdata
        self.bound_action = action or actor.default_action
        BaseRequest.__init__(self, **kw)
        self.ah = actor.get_request_handle(self)

    def setup(self,
              known_values=None,
              param_values=None,
              action_param_values={},
              **kw):
        BaseRequest.setup(self, **kw)
        #~ 20120111
        #~ self.known_values = known_values or self.report.known_values
        #~ if self.report.known_values:
        #~ d = dict(self.report.known_values)
        kv = dict()
        for k, v in list(self.actor.known_values.items()):
            kv.setdefault(k, v)
        if known_values:
            kv.update(known_values)
        self.known_values = kv

        request = self.request

        if self.actor.parameters is not None:
            pv = self.actor.param_defaults(self)

            for k in list(pv.keys()):
                if k not in self.actor.parameters:
                    raise Exception(
                        "%s.param_defaults() returned invalid keyword %r" %
                        (self.actor, k))

            # New since 20120913.  E.g. newcomers.Newcomers is a
            # simple pcsw.Clients with
            # known_values=dict(client_state=newcomer) and since there
            # is a parameter `client_state`, we override that
            # parameter's default value.

            for k, v in list(self.known_values.items()):
                if k in pv:
                    pv[k] = v

            # New since 20120914.  MyClientsByGroup has a `group` as
            # master, this must also appear as `group` parameter
            # value.  Lino now understands tables where the master_key
            # is also a parameter.

            if self.actor.master_key is not None:
                if self.actor.master_key in pv:
                    pv[self.actor.master_key] = self.master_instance
            if param_values is None:
                if request is not None:
                    # call get_layout_handle to make sure that
                    # params_store has been created:
                    self.actor.params_layout.get_layout_handle(
                        self.renderer.plugin)
                    ps = self.actor.params_layout.params_store
                    # print('20160329 requests.py', ps, self.actor.parameters)
                    if ps is not None:
                        pv.update(ps.parse_params(request))
                    else:
                        raise Exception(
                            "20160329 params_layout {0} has no params_store "
                            "in {1!r}".format(
                                self.actor.params_layout, self.actor))
            else:
                for k in list(param_values.keys()):
                    if k not in pv:
                        raise Exception(
                            "Invalid key '%s' in param_values of %s "
                            "request (possible keys are %s)" % (
                                k, self.actor, list(pv.keys())))
                pv.update(param_values)
            # print("20160329 ok", pv)
            self.param_values = AttrDict(**pv)
        action = self.bound_action.action
        if action.parameters is not None:
            apv = action.action_param_defaults(self, None)
            if request is not None:
                apv.update(
                    action.params_layout.params_store.parse_params(request))
            self.action_param_values = AttrDict(**apv)
            self.set_action_param_values(**action_param_values)
        self.bound_action.setup_action_request(self)

    def set_action_param_values(self, **action_param_values):
        apv = self.action_param_values
        for k in list(action_param_values.keys()):
            if k not in apv:
                raise Exception(
                    "Invalid key '%s' in action_param_values "
                    "of %s request (possible keys are %s)" %
                    (k, self.actor, list(apv.keys())))
        apv.update(action_param_values)

    def get_data_iterator(self):
        raise NotImplementedError

    def get_base_filename(self):
        return six.text_type(self.actor)
        #~ s = self.get_title()
        #~ return s.encode('us-ascii','replace')

