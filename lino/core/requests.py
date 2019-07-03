# -*- coding: UTF-8 -*-
# Copyright 2009-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
See introduction in :doc:`/dev/ar`.
"""
from builtins import str
import six

import logging
logger = logging.getLogger(__name__)

from copy import copy
from xml.sax.saxutils import escape
# from urlparse import urlsplit
# from six.moves.urllib.parse import urlencode
# try:
#     from html import escape
# except ImportError:
#     from cgi import escape

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language
from django.utils import translation
from django.utils import timezone
from django.core import exceptions

from lino.core import constants
from lino.utils import AttrDict
from etgen.html import E, tostring, iselement
from lino.core.auth.utils import AnonymousUser

from .boundaction import BoundAction
from .signals import on_ui_created, pre_ui_save
from .diff import ChangeWatcher
from .utils import getrqdata
from .utils import obj2unicode
from .utils import obj2str
from .exceptions import ChangedAPI

CATCHED_AJAX_EXCEPTIONS = (Warning, exceptions.ValidationError)


class ValidActionResponses(object):
    """
    These are the allowed keyword arguments for :meth:`ar.set_response
    <BaseRequest.set_response>`, and the action responses supported by
    :js:func:`Lino.handle_action_result` (defined in
    :xfile:`linolib.js`).

    This class is never instantiated, but used as a placeholder for
    these names and their documentation.
    """

    message = None
    """
    A translatable message text to be shown to the user.
    """

    alert = None
    """
    True to specify that the message is rather important and should
    alert and should be presented in a dialog box to be confirmed by
    the user.
    """
    alert_eval_js = None
    """
    Javascript code to be evaluated after the confirmation of the alert dialog.
    """

    success = None

    errors = None
    html = None
    rows = None
    no_data_text = None
    title = None
    """The dynamic title to give to the window or component which shows this response.
    """

    count = None
    """The number of rows in a list response."""

    navinfo = None
    data_record = None
    """
    Certain requests are expected to return detailed information about
    a single data record. That's done in :attr:`data_record` which
    must itself be a dict with the following keys:

    - id : the primary key of this record_deleted
    - title : the title of the detail window
    - data : a dict with one key for every data element
    - navinfo : an object with information for the navigator
    - disable_delete : either null (if that record may be deleted, or
      otherwise a message explaining why.

    """

    record_id = None
    """
    When an action returns a `record_id`, it asks the user interface to
    jump to the given record.
    """

    refresh = None
    refresh_all = None
    close_window = None
    record_deleted = None
    xcallback = None
    
    goto_url = None
    """
    Leave current page and go to the given URL.
    """
    
    open_url = None
    """
    Open the given URL in a new browser window.
    """
    
    open_webdav_url = None
    info_message = None
    warning_message = None
    "deprecated"

    eval_js = None
    active_tab = None

    detail_handler_name = None
    """
    The name of the detail handler to be used.  Application code should
    not need to use this.  It is automatically set by
    :meth:`ActorRequest.goto_instance`.
    """

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

def bool2text(x):
    if x:
        return _("Yes")
    return _("No")
    
class BaseRequest(object):
    """
    Base class of all action requests.
    """
    user = None
    subst_user = None

    renderer = None
    """
    The renderer to use when processing this request.
    """

    actor = None
    action_param_values = None
    param_values = None
    bound_action = None
    known_values = {}
    is_on_main_actor = True
    master_instance = None
    """
    The database object which acts as master. This is `None` for master
    requests.
    """

    request = None
    """
    The incoming Django HttpRequest object which caused this action
    request.
    """

    selected_rows = []
    content_type = 'application/json'
    requesting_panel = None

    def __init__(self, request=None, parent=None,
                 is_on_main_actor=True, **kw):
        self.request = request
        self.response = dict()
        if request is not None:
            rqdata = getrqdata(request)
            kw = self.parse_req(request, rqdata, **kw)
        if parent is not None:
            self._confirm_answer = parent._confirm_answer
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
            # if not parent.is_on_main_actor or parent.actor != kw.get('actor', None):
            if not parent.is_on_main_actor:
                is_on_main_actor = False
            elif parent.actor is not None and parent.actor is not self.actor:
                is_on_main_actor = False
            # is_on_main_actor = False
        self.is_on_main_actor = is_on_main_actor
            
        self.setup(**kw)

    def setup(self,
              user=None,
              subst_user=None,
              current_project=None,
              selected_pks=None,
              selected_rows=None,
              master_instance=None,
              limit=None,
              requesting_panel=None,
              renderer=None):
        self.requesting_panel = requesting_panel
        self.master_instance = master_instance
        if user is None:
            self.user = AnonymousUser()
        else:
            self.user = user
        self.current_project = current_project
        if renderer is None:
            renderer = settings.SITE.kernel.text_renderer
        self.renderer = renderer
        self.subst_user = subst_user
        if selected_rows is not None:
            self.selected_rows = selected_rows
            assert selected_pks is None
        if selected_pks is not None:
            self.set_selected_pks(*selected_pks)

    def parse_req(self, request, rqdata, **kw):
        """
        Parse the given incoming HttpRequest and set up this action
        request from it.
        """
        if settings.SITE.user_model:
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

        if not 'selected_pks' in kw:
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
        """
        Copy certain values (renderer, user, subst_user & requesting_panel)
        from this request to the other.

        Deprecated. You should rather instantiate a request and
        specify parent instead. Or use :meth:`spawn_request` on
        parent.
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
        """
        Create a new request of same class which inherits from this one.
        """
        kw.update(parent=self)
        return self.__class__(**kw)

    def spawn(self, spec=None, **kw):
        """
        Deprecated. Use spawn_request() if possible.

        Create a new action request using default values from this one and
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
        else:
            kw.update(parent=self)
            ba = resolve_action(spec)
            spec = ba.request(**kw)
            # from lino.core.menus import create_item
            # mi = create_item(spec)
            # spec = mi.bound_action.request(**kw)
        return spec

    def get_printable_context(self, **kw):
        """
        Adds a series of names to the context used when rendering printable
        documents.
        """
        # from django.conf import settings
        from django.utils.translation import ugettext
        from django.utils.translation import pgettext
        from lino.api import dd, rt
        from lino.utils import iif
        from lino.utils.restify import restify
        from django.db import models

        # needed e.g. for polls tutorial
        for n in ('Count', 'Sum', 'Max', 'Min', 'Avg', 'F'):
            kw[n] = getattr(models, n)

        if False:  # 20150803 why was this?  It disturbed e.g. for the bs3
                   # language selector.
            sar = copy(self)
            sar.renderer = settings.SITE.kernel.html_renderer
            kw['ar'] = sar
        else:
            kw['ar'] = self

        kw['_'] = ugettext
        kw.update(
            E=E, tostring=tostring,
            dd=dd,
            rt=rt,
            decfmt=dd.decfmt,
            fds=dd.fds,
            fdm=dd.fdm,
            fdl=dd.fdl,
            fdf=dd.fdf,
            fdmy=dd.fdmy,
            iif=iif,
            bool2text=bool2text,
            bool2js=lambda b: "true" if b else "false",
            unicode=str,  # backwards-compatibility. In new template
                          # you should prefer `str`.
            pgettext=pgettext,
            now=timezone.now(),
            getattr=getattr,
            restify=restify,
            requested_language=get_language())

        def parse(s):
            # Jinja doesn't like a name 'self' in the context which
            # might exist there in a backwards-compatible appypod
            # template:
            kw.pop('self', None)
            return dd.plugins.jinja.renderer.jinja_env.from_string(
                s).render(**kw)
        kw.update(parse=parse)
        return kw

    def set_selected_pks(self, *selected_pks):
        """
        Given a tuple of primary keys, set :attr:`selected_rows` to a list
        of corresponding database objects.
        """
        #~ print 20131003, selected_pks
        self.selected_rows = []
        for pk in selected_pks:
            if pk:
                obj = self.get_row_by_pk(pk)
                if obj is not None:
                    self.selected_rows.append(obj)
        # self.selected_rows = filter(lambda x: x, self.selected_rows)
        # note: ticket #523 was because the GET contained an empty pk ("&sr=")

    def get_permission(self):
        """
        Whether this request has permission to run.  `obj` can be None if
        the action is a list action (whose `select_rows` is `False`).
        """
        if self.bound_action.action.select_rows:
            # raise Exception("20160814 {}".format(self.bound_action))
            if len(self.selected_rows) == 1:
                obj = self.selected_rows[0]
                state = self.bound_action.actor.get_row_state(obj)
                return self.bound_action.get_row_permission(self, obj, state)
        return self.bound_action.get_bound_action_permission(
            self, None, None)
        
    def set_response(self, **kw):
        """
        Set (some part of) the response to be sent when the action request
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
        for k in kw.keys():
            if not hasattr(ValidActionResponses, k):
                raise Exception("Unknown key %r in action response." % k)
        self.response.update(kw)
            
    def error(self, e=None, message=None, **kw):
        """
        Shortcut to :meth:`set_response` used to set an error response.

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
        """
        Tell the client to consider the action as successful. This is the
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
        """
        Set an answer for following confirm in a non-interactive renderer.
        """
        self._confirm_answer = ans

    def confirm(self, ok_func, *msgs):
        """
        Execute the specified callable `ok_func` after the user has
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

    def parse_memo(self, txt, **context):
        context.update(ar=self)
        return settings.SITE.kernel.memo_parser.parse(txt, **context)

    def obj2memo(self, *args, **kwargs):
        """
        Calls the site's parser's :meth:`obj2memo
        <lino.utils.memo.Parser.obj2memo>` method.
        """
        # kwargs.update(ar=self)
        return settings.SITE.kernel.memo_parser.obj2memo(*args, **kwargs)

    # def parse_memo(self, html):
    #     return self.renderer.parse_memo(html, ar=self)

    def set_callback(self, *args, **kw):
        return settings.SITE.kernel.set_callback(self, *args, **kw)

    def add_callback(self, *args, **kw):
        return settings.SITE.kernel.add_callback(self, *args, **kw)

    def goto_instance(self, *args, **kwargs):
        return self.renderer.goto_instance(self, *args, **kwargs)

    def goto_pk(self, pk, *args, **kwargs):
        """Navigate to the record with the specified primary key.

        This is similar to :meth:`goto_instance` but works only in a detail
        view.  It has the advantage of not doing permission checks and no
        database lookup just for rendering a link. """

        r = self.renderer
        if r.extjs_version:
            url = r.js2url("Lino.goto_record_id(%s)" % pk)
        else:
            url = r.get_detail_url(self.actor, pk)
        return r.href(url, *args, **kwargs)
        # ba = self.actor.detail_action
        # js = self.renderer.action_call(self, ba, dict(record_id=pk))
        # kwargs.update(eval_js=js)
        # self.set_response(**kwargs)

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

    def get_total_count(self):
        """
        TableRequest overrides this to return the number of rows.

        For other requests we assume that there is one row.  This is used e.g.
        when courses.StatusReport is shown in the the dashboard. A Report
        returns always 1 because otherwise the dashboard believes it is empty.

        """
        return 1
    
    def get_data_value(self, obj, name):
        """
        Return the value of the virtual field `name` for this action
        request on the given object `obj`.
        """
        fld = obj.get_data_elem(name)
        return fld.value_from_object(obj, self)

    def get_user(self):
        """
        Return the :class:`User <lino.modlib.users.models.User>` instance
        of the user who issued the request.  If the authenticated user
        is acting as somebody else, return that user's instance.
        """
        return self.subst_user or self.user

    def run(self, ia, *args, **kw):
        """
        Run the given instance action `ia` in a child request of this
        request.
        
        Additional arguments are forwarded to the action.
        Returns the response of the child request.
        Does not modify response of parent request.
        """
        return ia.run_from_session(self, *args, **kw)

    def story2html(self, story, *args, **kwargs):
        """
        Convert a story into a stream of HTML elements.
        """
        # return self.renderer.show_story(self, story, *args, **kwargs)
        return settings.SITE.kernel.html_renderer.show_story(
            self, story, *args, **kwargs)

    def story2rst(self, story, *args, **kwargs):
        return self.renderer.show_story(self, story, *args, **kwargs)

    def show(self, spec=None, master_instance=None, column_names=None,
             header_level=None, language=None, nosummary=False,
             stripped=True, show_links=False, header_links=False,
             **kwargs):
        """
        Show the specified table or action using the current renderer.  

        The first argument specifies the table or actor to show. It is
        forwarded to :meth:`spawn`.

        If the table is a slave table, then a `master_instance` must
        be specified as second argument.

        Optional keyword arguments are:

        :column_names: overrides default list of columns

        :show_links: show links and other html formatting.  Used
                     .e.g. in :ref:`avanti.specs.roles` where we want
                     to show whether cells are clickable or not.

        :nosummary: if it is a table with :attr:`display_mode
                    <lino.core.tables.AbstractTable.display_mode>`
                    set to ``'summary'``, force rendering it as a
                    table.

        :header_level: show also the table header (using specified
                       level)

        :header_links: make headers clickable so that user can
                       interactively change the sorting order.

        :language: overrides the default language used for headers and
                   translatable data

        Any other keyword arguments are forwarded to :meth:`spawn`.

        Note that this function either returns a string or prints to
        stdout and returns None, depending on the current renderer.

        Usage in a :doc:`tested document </dev/doctests>`:

        >>> from lino.api import rt
        >>> rt.login('robin').show('users.UsersOverview', limit=5)

        Usage in a Jinja template::

          {{ar.show('users.UsersOverview')}}
        """
        from lino.utils.report import Report
        #from lino.core.actors import Actor

        if master_instance is not None:
            kwargs.update(master_instance=master_instance)

        if spec is None:
            ar = self
        elif isinstance(spec, BaseRequest):
            assert not kwargs
            ar = spec
        else:
            #assert isinstance(spec, type) and issubclass(spec, Actor)
            ar = self.spawn(spec, **kwargs)
            # return self.renderer.show_story(spec, **kwargs)

        def doit():
            # print 20160530, ar.renderer
            if issubclass(ar.actor, Report):
                story = ar.actor.get_story(None, ar)
                return ar.renderer.show_story(
                    self, story, header_level=header_level,
                    header_links=header_links, stripped=stripped)
            return ar.renderer.show_table(
                ar, column_names=column_names, header_level=header_level,
                header_links=header_links,
                nosummary=nosummary, stripped=stripped,
                show_links=show_links)

        if language:
            with translation.override(language):
                return doit()
        return doit()

    def show_story(self, *args, **kwargs):
        """
        Shortcut to the renderer's :meth:`show_story
        <lino.core.renderer.HtmlRenderer.show_story>` method.
        """
        return self.renderer.show_story(self, *args, **kwargs)
    
    def show_dashboard(self):
        """Show the dashboard of the user who made this request.

        Utility method  for doctests."""
        return self.show_story(
            self.get_user().get_preferences().dashboard_items)

    def show_menu(self, language=None, **kwargs):
        """Show the main menu for the requesting user using the requested
        renderer.

        This is used in tested docs.

        :language: explicitly select another language than that
                   specified in the requesting user's :attr:`language
                   <lino.modlib.users.models.User.language>` field.

        """
        user = self.get_user()
        if language is None:
            language = user.language
        with translation.override(language):
            mnu = settings.SITE.get_site_menu(user.user_type)
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

    def obj2html(self, obj, *args, **kwargs):
        """
        Return a HTML element which represents a pointer to the given
        database object. Depending on the renderer this will be more
        or less clickable.
        """
        if obj is None:
            return ''
        return self.renderer.obj2html(self, obj, *args, **kwargs)

    def obj2str(self, *args, **kwargs):
        """Return a string with a pointer to the given object.
        """
        return self.renderer.obj2str(self, *args, **kwargs)

    def html_text(self, *args, **kwargs):
        """
        """
        return self.renderer.html_text(*args, **kwargs)

    def href_button(self, *args, **kwargs):
        return self.renderer.href_button(*args, **kwargs)

    def href_to_request(self, *args, **kwargs):
        return self.renderer.href_to_request(self, *args, **kwargs)

    def menu_item_button(self, *args, **kwargs):
        """Forwards to :meth:`lino.core.renderer.`"""
        return self.renderer.menu_item_button(self, *args, **kwargs)

    def show_menu_path(self, spec, language=None):
        """
        Print the menu path of the given actor or action.

        This is the replacement for :func:`show_menu_path
        <lino.api.doctest.show_menu_path>`.  It has the advantage that
        it automatically sets the language of the user and that it
        works for any user type.
        """
        from lino.sphinxcontrib.actordoc import menuselection_text
        u = self.get_user()
        mi = u.user_type.find_menu_item(spec)
        if mi is None:
            raise Exception("Invalid spec {0}".format(spec))
        if language is None:
            language = u.language
        with translation.override(language):
            print(menuselection_text(mi))

    def open_in_own_window_button(self, *args, **kwargs):
        return self.renderer.open_in_own_window_button(self, *args, **kwargs)

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

    def plain_toolbar_buttons(self, **btnattrs):
        #btnattrs = {'class': "plain-toolbar"}
        cls = self.actor
        buttons = []
        if cls is not None:
            for ba in cls.get_toolbar_actions(self.bound_action.action):
                if not ba.action.select_rows:
                    if ba.action.show_in_plain:
                        ir = ba.request_from(self)
                        if ir.get_permission():
                            buttons.append(ir.ar2button(**btnattrs))
        # print("20181106", cls, self.bound_action, buttons)
        return buttons
        # if len(buttons) == 0:
        #     return None
        # return E.p(*buttons, **btnattrs)

    def ar2button(self, *args, **kwargs):
        """Return an HTML element with a button for running this action
         request. Does not spawn another request. Does not check
         permissions.

        """
        return self.renderer.ar2button(self, *args, **kwargs)

    def instance_action_button(self, ai, *args, **kw):
        """Return an HTML element with a button which would run the given
        :class:`InstanceAction <lino.core.requests.InstanceAction>`
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

    def as_button(self, *args, **kw):
        """Return a button which when activated executes (a copy of)
        this request.

        """
        return self.renderer.action_button(
            None, self, self.bound_action, *args, **kw)

    def elem2rec1(ar, rh, elem, fields=None, **rec):
        rec.update(data=rh.store.row2dict(ar, elem, fields))
        return rec

    def elem2rec_insert(self, ah, elem):
        """
        Returns a dict of this record, designed for usage by an InsertWindow.
        """
        lh = ah.actor.insert_layout.get_layout_handle(
            settings.SITE.kernel.default_ui)
        fields = [df._lino_atomizer for df in lh._store_fields]
        if ah.store._disabled_fields_storefield is not None:
            fields.append(ah.store._disabled_fields_storefield)
        rec = self.elem2rec1(ah, elem, fields=fields)
        rec.update(title=self.get_action_title())
        rec.update(phantom=True)
        return rec

    def elem2rec_detailed(ar, elem, with_navinfo=True, **rec):
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
        rec = ar.elem2rec1(rh, elem, None, **rec)
        if ar.actor.hide_top_toolbar or ar.bound_action.action.hide_top_toolbar:
            rec.update(title=ar.get_detail_title(elem))
        else:
            rec.update(title=ar.get_breadcrumbs(elem))
            # rec.update(title=ar.get_title() + u" » " +
            #            ar.get_detail_title(elem))
        rec.update(id=elem.pk)
        # rec.update(id=ar.actor.get_pk_field().value_from_object(elem))
        if ar.actor.editable:
            rec.update(disable_delete=rh.actor.disable_delete(elem, ar))
        if rh.actor.show_detail_navigator and with_navinfo:
            rec.update(navinfo=rh.actor.get_navinfo(ar, elem))
        if ar.actor.parameters:
            rec.update(param_values=ar.actor.params_layout.params_store.pv2dict(ar, ar.param_values))

        return rec

    def get_breadcrumbs(self, elem=None):
        list_title = self.get_title()
        # TODO: make it clickable so that we can return from detail to list view
        if elem is None:
            return list_title
        else:
            # print("20190703", self.actor, self.actor.default_action)
            sar = self.spawn_request(actor=self.actor)
            list_title = tostring(
                sar.href_to_request(sar, list_title, icon_name=None))
            return list_title + u" » " + self.get_detail_title(elem)

    def form2obj_and_save(ar, data, elem, is_new):
        """
        Parses the data from HttpRequest to the model instance and saves
        it.

        This is deprecated, but still used by Restful (which is used
        only by Extensible).
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
                watcher.send_update(ar)
                ar.success(_("%s has been updated.") % obj2unicode(elem))
        else:
            ar.success(_("%s : nothing to save.") % obj2unicode(elem))

        elem.after_ui_save(ar, watcher)

    def get_help_url(self, docname=None, text=None, **kw):
        """
        Generate a link to the help section of the documentation (whose
        base is defined by :attr:`lino.core.site.Site.help_url`)

        Usage example::

            help = ar.get_help_url("foo", target='_blank')
            msg = _("You have a problem with foo."
                    "Please consult %(help)s "
                    "or ask your system administrator.")
            msg %= dict(help=tostring(help))
            kw.update(message=msg, alert=True)
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
        # phantom row disturbs when there is an insert button in
        # the toolbar
        if self.actor.no_phantom_row:
            return
        # if self.actor.insert_layout is not None \
        #    and not self.actor.stay_in_grid \
        #    and not self.actor.force_phantom_row:
        #     return
        if self.create_kw is None or not self.actor.editable \
           or not self.actor.allow_create:
            return
        if not self.actor.get_create_permission(self):
            return
        yield PhantomRow(self, **kw)

    def create_instance(self, **kw):
        """
        Create a row (a model instance if this is a database table) using
        the specified keyword arguments.
        """
        if self.create_kw:
            kw.update(self.create_kw)
        if self.known_values:
            kw.update(self.known_values)
        obj = self.actor.create_instance(self, **kw)
        return obj

    def create_instance_from_request(self, **kwargs):
        elem = self.create_instance( **kwargs)
        if self.actor.handle_uploaded_files is not None:
            self.actor.handle_uploaded_files(elem, self.request)

        if self.request is not None:
            self.ah.store.form2obj(self, self.request.POST or self.rqdata, elem, True)
        elem.full_clean()
        return elem

    def get_status(self, **kw):
        """Return a `dict` with the "status", i.e. a json representation of
        this request.

        """
        if self.actor.parameters:
            kw.update(
                param_values=self.actor.params_layout.params_store.pv2dict(
                    self, self.param_values))

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

    def summary_row(self, obj, **kwargs):
        return self.actor.summary_row(self, obj, **kwargs)

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

    def get_request_url(self, *args, **kw):
        return self.renderer.get_request_url(self, *args, **kw)

    def absolute_uri(self, *args, **kw):
        ar = self.spawn(*args, **kw)
        location = ar.get_request_url()
        return self.request.build_absolute_uri(location)

    def build_webdav_uri(self, location):
        if self.request is None:
            return location
        url = self.request.build_absolute_uri(location)
        if settings.SITE.webdav_protocol:
            url = settings.SITE.webdav_protocol + "://" + url
            # url = urlsplit(url)
            # url.scheme = settings.SITE.webdav_protocol
            # url = url.unsplit()
        print("20180410 {}", url)
        return url
        
    def pk2url(self, pk):
        return self.renderer.get_detail_url(self.actor, pk)
    
    def run(self, *args, **kw):
        """
        Runs this action request.
        """
        return self.bound_action.action.run_from_code(self, *args, **kw)


class ActionRequest(ActorRequest):
    """
    Holds information about an individual web request and provides
    methods like

    - :meth:`get_user <lino.core.actions.BaseRequest.get_user>`
    - :meth:`confirm <lino.core.actions.BaseRequest.confirm>`
    - :meth:`spawn <lino.core.actions.BaseRequest.spawn>`
    
    An `ActionRequest` is also a :class:`BaseRequest` and inherits its
    methods.

    An ActionRequest is instantiated from different shortcut methods:

    - :meth:`lino.core.actors.Actor.request`
    - :meth:`lino.core.actions.Action.request`
        

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
        # print("20170116 ActionRequest.__init__()", actor, kw)
        assert unused_renderer is None
        assert unused_request is None
        self.actor = actor
        self.rqdata = rqdata
        self.bound_action = action or actor.default_action
        BaseRequest.__init__(self, **kw)
        self.ah = actor.get_request_handle(self)

    def __str__(self):
        return "{0} {1}".format(self.__class__.__name__, self.bound_action)

    def __repr__(self):
        return "{0} {1}".format(self.__class__.__name__, self.bound_action)

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
            # self.actor.check_params(self.param_values)
            
        action = self.bound_action.action
        if action.parameters is not None:
            if len(self.selected_rows) == 1:
                apv = action.action_param_defaults(
                    self, self.selected_rows[0])
            else:
                apv = action.action_param_defaults(self, None)
                # msg = "20170116 selected_rows is {} for {!r}".format(
                #     self.selected_rows, action)
                # raise Exception(msg)
            if request is not None:
                apv.update(
                    action.params_layout.params_store.parse_params(request))
            self.action_param_values = AttrDict(**apv)
            # action.check_params(action_param_values)
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
        


class InstanceAction(object):
    """
    Volatile object which wraps a given action to be run on a given
    model instance.

    .. attribute:: bound_action

        The bound action that will run.

    .. attribute:: instance 

        The database object on which the action will run.

    .. attribute:: owner


    """

    def __init__(self, action, actor, instance, owner):
        #~ print "Bar"
        #~ self.action = action
        self.bound_action = actor.get_action_by_name(action.action_name)
        if self.bound_action is None:
            raise Exception("%s has not action %r" % (actor, action))
            # Happened 20131020 from lino_xl.lib.beid.eid_info() :
            # When `use_eid_jslib` was False, then
            # `Action.attach_to_actor` returned False.
        self.instance = instance
        self.owner = owner

    def __str__(self):
        return "{0} on {1}".format(self.bound_action, obj2str(self.instance))

    def run_from_code(self, ar, *args, **kw):
        """
        Probably to be deprecated.
        Run this action on this instance in the given session, updating
        the response of the session.  Returns the return value of the
        action.
        """
        # raise Exception("20170129 is this still used?")
        ar.selected_rows = [self.instance]
        return self.bound_action.action.run_from_code(ar, *args, **kw)

    def run_from_ui(self, ar, **kw):
        """
        Run this action on this instance in the given session, updating
        the response of the session.  Returns nothing.
        """
        # raise Exception("20170129 is this still used?")
        # kw.update(selected_rows=[self.instance])
        ar.selected_rows = [self.instance]
        self.bound_action.action.run_from_ui(ar)

    def request_from(self, ses, **kwargs):
        """
        Create an action request on this instance action without running
        the action.
        """
        kwargs.update(selected_rows=[self.instance])
        kwargs.update(parent=ses)
        ar = self.bound_action.request(**kwargs)
        return ar

    def run_from_session(self, ses, **kwargs):
        """
        Run this instance action in a child request of given session.  

        Additional arguments are forwarded to the action.
        Returns the response of the child request.
        Doesn't modify response of parent request.  
        """
        ar = self.request_from(ses, **kwargs)
        self.bound_action.action.run_from_code(ar)
        return ar.response

    def __call__(self, *args, **kwargs):
        """
        Run this instance action in an anonymous base request.  

        Additional arguments are forwarded to the action.
        Returns the response of the base request.
        """
        if len(args) and isinstance(args[0], BaseRequest):
            raise ChangedAPI("20181004")
        ar = self.bound_action.request()
        self.run_from_code(ar, *args, **kwargs)
        return ar.response

    def as_button_elem(self, ar, label=None, **kwargs):
        return settings.SITE.kernel.row_action_button(
            self.instance, ar, self.bound_action, label, **kwargs)

    def as_button(self, *args, **kwargs):
        """Return a HTML chunk with a "button" which, when clicked, will
        execute this action on this instance.  This is being used in
        the :ref:`lino.tutorial.polls`.

        """
        return tostring(self.as_button_elem(*args, **kwargs))

    def get_row_permission(self, ar):
        state = self.bound_action.actor.get_row_state(self.instance)
        # logger.info("20150202 ia.get_row_permission() %s using %s",
        #             self, state)
        return self.bound_action.get_row_permission(ar, self.instance, state)



