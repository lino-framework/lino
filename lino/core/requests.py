# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)
"""
An action request is when a given user asks to run a given action of a
given actor.

Action requests are implemented by
:class:`lino.core.requests.BaseRequest` and its subclasses.

In application code, the traditional name for instances of action
requests  is :class:`ar`.

As a rough approximation you can say that every Django web request
gets wrapped into an action request.  The ActionRequest just holds
extended information about the "context" (like the "renderer"
being used) and provides the application with methods to
communicate with the user.
But there are exceptions, the :attr:`ar.request` can be None.

"""

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from django import http
from django.core import exceptions

from lino.core.dbutils import obj2unicode

from lino.utils import AttrDict
from lino.utils import isiterable

from lino.core import constants as ext_requests

from lino.core.dbutils import resolve_app
from lino.core.dbutils import navinfo
from lino.core.boundaction import BoundAction

from lino.utils.xmlgen.html import E

from lino.core.signals import on_ui_created
from lino.core.utils import ChangeWatcher


CATCHED_AJAX_EXCEPTIONS = (Warning, exceptions.ValidationError)

ACTION_RESPONSES = frozenset((
    'message', 'success', 'alert',
    'errors',
    'html',
    'rows',
    'data_record',
    # 'actor_url',
    'detail_handler_name',
    'record_id',
    # 'goto_record_id',
    'refresh', 'refresh_all',
    'close_window',
    'record_deleted',
    'xcallback',
    'open_url', 'open_davlink_url',
    'info_message',
    'warning_message',  # deprecated
    'eval_js'))
"""
Action responses supported by `Lino.action_handler`
(defined in :xfile:`linolib.js`).
"""


class VirtualRow(object):

    def __init__(self, **kw):
        self.update(**kw)

    def update(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)

    def get_row_permission(self, ar, state, ba):
        if ba.action.readonly:
            return True
        return False


class PhantomRow(VirtualRow):

    def __init__(self, request, **kw):
        self._ar = request
        VirtualRow.__init__(self, **kw)

    def __unicode__(self):
        return unicode(self._ar.get_action_title())


class BaseRequest(object):

    """Base class for :class:`ActionRequest` and :class:`TableRequest
    <lino.core.tables.TableRequest>`. 

    A bare `BaseRequest` instance is returned as a "session" by
    :func:`rt.login`.

    """
    # Some of the following are needed e.g. for polls tutorial
    actor = None
    action_param_values = None
    param_values = None
    bound_action = None

    request = None
    """
    The Django HttpRequest object which caused this action request.
    """

    renderer = None
    selected_rows = []
    content_type = 'application/json'

    def __init__(self, request=None, **kw):
        self.request = request
        self.response = dict()
        if request is not None:
            if request.method in ('PUT', 'DELETE'):
                rqdata = http.QueryDict(request.body)
                # note that `body` was named `raw_post_data` before Django 1.4
                #~ print 20130222, rqdata
            else:
                rqdata = request.REQUEST
            kw = self.parse_req(request, rqdata, **kw)
        #~ 20120605 self.ah = actor.get_handle(ui)
        self.setup(**kw)

    def set_response(self, **kw):
        """Set (some part of) the response to be sent when the action request
        finishes.  Allowed keywords are:

        - ``message`` -- a string with a message to be shown to the user.

        - ``alert`` -- True to specify that the message is rather important
          and should alert and should be presented in a dialog box to be
          confirmed by the user.

        - ``success``
        - ``errors``
        - ``html``
        - ``rows``
        - ``data_record``
        - ``goto_record_id``
        - ``refresh``
        - ``refresh_all``
        - ``close_window``
        - ``xcallback``
        - ``open_url``
        - ``open_davlink_url``
        - ``info_message``
        - ``warning_message``
        - ``eval_js``

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
            if not k in ACTION_RESPONSES:
                raise Exception("Unknown key %r in action response." % k)
        self.response.update(kw)
            
    def error(self, e=None, message=None, **kw):
        """
        Shortcut to :meth:`set_response` used to set an error response.
        The first argument should be either an exception object or a message.
        """
        kw.update(success=False)
        kw.update(alert=_("Error"))  # added 20140304
        #~ if e is not None:
        if isinstance(e, Exception):
            if False:  # useful when debugging, but otherwise rather disturbing
                logger.exception(e)
            if hasattr(e, 'message_dict'):
                kw.update(errors=e.message_dict)
        if message is None:
            message = unicode(e)
        kw.update(message=message)
        self.set_response(**kw)

    def success(self, message=None, alert=None, **kw):
        """Tell the client to consider the action as successful. This is the
        same as :meth:`BaseRequest.set_response` with `success=True`.

        First argument should be a textual message.

        """
        kw.update(success=True)
        if alert is not None:
            if alert is True:
                alert = _("Success")
            kw.update(alert=alert)
        if message:
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
        #~ return self.success(*args,**kw)

    def debug(self, msg, *args, **kw):
        if settings.SITE.verbose_client_info_message:
            self.append_message('info', msg, *args, **kw)

    def info(self, msg, *args, **kw):
        self.append_message('info', msg, *args, **kw)

    def warning(self, msg, *args, **kw):
        self.append_message('warning', msg, *args, **kw)

    def confirm(self, ok_func, *msgs):
        """Execute the specified callable `ok` after the user has confirmed
        the specified message.  All remaining positional arguments to
        `confirm` are concatenated to a single callback message.  This
        method then calls :meth:`callback` (see there for
        implementation notes).

        The callable may not expect any mandatory arguments
        (this is different than for the raw callback method)

        """
        cb = self.add_callback(*msgs)

        def noop(ar):
            return ar.success(_("Aborted"))
        cb.add_choice('yes', ok_func, _("Yes"))
        cb.add_choice('no', noop, _("No"))
        self.set_callback(cb)

    def render_jinja(self, template, **context):
        saved_renderer = self.renderer
        self.renderer = settings.SITE.plugins.bootstrap3.renderer
        retval = template.render(**context)
        self.renderer = saved_renderer
        return retval

    def set_callback(self, *args, **kw):
        return settings.SITE.ui.set_callback(self, *args, **kw)

    def add_callback(self, *args, **kw):
        return settings.SITE.ui.add_callback(self, *args, **kw)

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

    def setup_from(self, other):
        """Copy certain values (renderer, user, subst_user &
        requesting_panel) from this request to the other.

        """
        if not self.must_execute():
            return
            #~ raise Exception("Request %r was already executed" % other)
        self.renderer = other.renderer
        self.user = other.user
        self.subst_user = other.subst_user
        self.requesting_panel = other.requesting_panel

    def parse_req(self, request, rqdata, **kw):
        """
        Parse the given Django HttpRequest and setup from it.
        
        """
        kw.update(user=request.user)
        kw.update(subst_user=request.subst_user)
        kw.update(requesting_panel=request.requesting_panel)
        kw.update(current_project=rqdata.get(
            ext_requests.URL_PARAM_PROJECT, None))

        selected = rqdata.getlist(ext_requests.URL_PARAM_SELECTED)
        #~ kw.update(selected_rows = [self.actor.get_row_by_pk(pk) for pk in selected])
        kw.update(selected_pks=selected)

        #~ if settings.SITE.user_model:
            #~ username = rqdata.get(ext_requests.URL_PARAM_SUBST_USER,None)
            #~ if username:
                #~ try:
                    #~ kw.update(subst_user=settings.SITE.user_model.objects.get(username=username))
                #~ except settings.SITE.user_model.DoesNotExist, e:
                    #~ pass
        # logger.info("20140503 ActionRequest.parse_req() %s", kw)
        return kw

    def setup(self,
              user=None,
              subst_user=None,
              current_project=None,
              selected_pks=None,
              requesting_panel=None,
              renderer=None):
        self.requesting_panel = requesting_panel
        self.user = user
        self.current_project = current_project
        if renderer is not None:
            self.renderer = renderer
        self.subst_user = subst_user

        if selected_pks is not None:
            self.set_selected_pks(*selected_pks)

    def set_selected_pks(self, *selected_pks):
        #~ print 20131003, selected_pks
        self.selected_rows = [self.get_row_by_pk(pk) for pk in selected_pks]

    def get_user(self):
        """Return the :class:`User <ml.users.User>` instance of the user who
        issued the request.  If the authenticated user is acting as
        somebody else, return that user's instance.

        """
        return self.subst_user or self.user

    def add_system_note(self, owner, subject, body, silent):
        settings.SITE.emit_system_note(
            self.reqwuest, owner, subject, body, silent)
    def spawn(self, spec, **kw):
        """
        Create a new ActionRequest using default values from this one and
        the action specified by `spec`.

        """

        if isinstance(spec, ActionRequest):
            for k, v in kw.items():
                assert hasattr(spec, k)
                setattr(spec, k, v)
            spec.setup_from(self)
        elif isinstance(spec, BoundAction):
            spec = spec.request(**kw)
            spec.setup_from(self)
        else:
            from lino.core.menus import create_item
            mi = create_item(spec)
            kw.setdefault('user', self.user)
            kw.setdefault('subst_user', self.subst_user)
            kw.setdefault('renderer', self.renderer)
            kw.setdefault('requesting_panel', self.requesting_panel)
            spec = mi.bound_action.request(**kw)
        return spec

    def run(self, thing, *args, **kw):
        """The first parameter `thing` may be an InstanceAction or a Model
        instance.

        """
        return thing.run_from_session(self, *args, **kw)

    #~ def set_language(self,*args):
        #~ set_language(*args)

    # def show_slaves(self, master_instance, *args, **kwargs):
    #     for spec in args:
    #         self.show(spec, master_instance, **kwargs)

    def story2html(self, story, *args, **kw):
        """
        Convert a stream of story items into a stream of HTML elements.
        """
        from lino.core.actors import Actor
        from lino.core.tables import TableRequest
        for item in story:
            if E.iselement(item):
                yield item
            elif isinstance(item, type) and issubclass(item, Actor):
                yield self.show(item, *args, **kw)
            elif isinstance(item, TableRequest):
                assert item.renderer is not None
                yield self.renderer.show_request(item)
            elif isiterable(item):
                for i in self.story2html(item, *args, **kw):
                    yield i
            else:
                raise Exception("Cannot handle %r" % item)

    def show(self, spec, master_instance=None, column_names=None,
             header_level=None, language=None, **kw):
        """
        Show the specified table or action using the current renderer.  If
        the table is a :term:`slave table`, then a `master_instance` must
        be specified as second argument.

        The first argument, `spec` can be:
        - a string with the name of a model, actor or action
        - another action request
        - a bound action (i.e. a :class:`BoundAction` instance)

        Optional keyword arguments are

        - `column_names` overrides default list of columns
        - `header_level` show also the header (using specified level)
        - `language` overrides the default language used for headers and
          translatable data

        Any other keyword arguments are forwarded to :meth:`spawn`.

        Usage in a tested doc:

        >>> from lino import rt
        >>> rt.login('robin').show('users.UsersOverview', limit=5)

        Usage in a Jinja template::

          {{ar.show('users.UsersOverview')}}

        Usage in an appy.pod template::

          do text from ar.show('users.UsersOverview')

        Note that this function either returns a string or prints to
        stdout and returns None, depending on the current renderer.


        """
        # 20130905 added master_instance positional arg. but finally didn't use
        # it.
        if master_instance is not None:
            kw.update(master_instance=master_instance)

        ar = self.spawn(spec, **kw)

        def doit():
            return ar.renderer.show_request(
                ar, column_names=column_names, header_level=header_level)

        if language:
            with translation.override(language):
                return doit()
        return doit()

    def show_menu(self, remove_blanklines=True):
        """
        Used in tested docs
        """
        mnu = settings.SITE.get_site_menu(None, self.get_user().profile)
        s = mnu.as_rst(self)
        if remove_blanklines:
            for ln in s.splitlines():
                if ln.strip():
                    print ln
        else:
            print s

    def get_request_url(self, *args, **kw):
        return self.renderer.get_home_url(*args, **kw)

    def summary_row(self, obj, **kw):
        return obj.summary_row(self, **kw)

    def instance_handler(self, *args, **kw):
        return self.renderer.instance_handler(self, *args, **kw)

    def pk2url(self, *args, **kw):
        return self.renderer.pk2url(self, *args, **kw)

    def obj2html(self, *args, **kw):
        return self.renderer.obj2html(self, *args, **kw)

    def href_button(self, *args, **kw):
        return self.renderer.href_button(*args, **kw)

    def href_to_request(self, *args, **kw):
        return self.renderer.href_to_request(self, *args, **kw)

    def window_action_button(self, *args, **kw):
        return self.renderer.window_action_button(self, *args, **kw)

    def row_action_button(self, obj, a, *args, **kw):
        return self.renderer.row_action_button(
            obj, None, a, *args, **kw)

    def instance_action_button(self, ai, *args, **kw):
        """Return an HTML element with a button (or a button-like href) which,
        when clicked, will run the given instance action ``ai``.
        ``ai`` must be an instance of :class:`InstanceAction
        <lino.core.actions.InstanceAction>`.
        """
        # logger.info("20141106 %s", ai.instance)
        return self.renderer.row_action_button(
            ai.instance, self, ai.bound_action, *args, **kw)

    def action_button(self, ba, obj, *args, **kwargs):
        """
        Returns the HTML of an action link which will run the specified
        action.

        ``kwargs`` may contain additional html attributes like `style`.

        """
        return self.renderer.action_button(obj, self, ba, *args, **kwargs)

    def insert_button(self, *args, **kw):
        """
        Returns the HTML of an action link which will open the
        :term:`insert window` of this request.

        """
        return self.renderer.insert_button(self, *args, **kw)

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
                        #~ l.append(self.select_choice.as_button_elem(ar, unicode(c)))
                else:
                    l.append(E.b(unicode(self.choice)))
                    l.append(ar.put_button(
                        self, _("Undo"), dict(choice=None),
                        title=_("Undo your vote")))
                return E.p(*join_elems(l))

        
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

    def elem2rec_insert(ar, ah, elem):
        """
        Returns a dict of this record, designed for usage by an InsertWindow.
        """
        rec = ar.elem2rec1(ah, elem)
        rec.update(title=ar.get_action_title())
        rec.update(phantom=True)
        return rec

    def elem2rec_detailed(ar, elem, **rec):
        """Adds additional information for this record, used only by
    detail views.

        The "navigation information" is a set of pointers to the next,
        previous, first and last record relative to this record in
        this report.  (This information can be relatively expensive
        for records that are towards the end of the report.  See
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
        if not is_new:
            watcher = ChangeWatcher(elem)
        ar.ah.store.form2obj(ar, data, elem, is_new)
        elem.full_clean()

        if is_new or watcher.is_dirty():

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

        elem.after_ui_save(ar)

    def get_help_url(self, docname=None, text=None, **kw):
        """Generate a link to the help section of the documentation (whose
        base is defined by :attr:`lino.core.site_def.Site.help_url`)

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
            text = unicode(_("the documentation"))
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

        self.ah.store.form2obj(self, self.request.POST, elem, True)
        elem.full_clean()
        return elem

    def get_status(self, **kw):
        if self.actor.parameters:
            kw.update(
                param_values=self.actor.params_layout.params_store.pv2dict(
                    self.param_values))

        if self.bound_action.action.parameters is not None:
            defaults = kw.get('field_values', {})
            pv = self.bound_action.action.params_layout.params_store.pv2dict(
                self.action_param_values, **defaults)
            kw.update(field_values=pv)

        bp = kw.setdefault('base_params', {})

        if self.current_project is not None:
            bp[ext_requests.URL_PARAM_PROJECT] = self.current_project

        if self.subst_user is not None:
            bp[ext_requests.URL_PARAM_SUBST_USER] = self.subst_user.id
        return kw

    def spawn(self, actor, **kw):
        """Same as :meth:`BaseRequest.spawn`, except that the first positional
        argument is an `actor`.

        """
        if actor is None:
            actor = self.actor
        return super(ActorRequest, self).spawn(actor, **kw)

    def summary_row(self, *args, **kw):
        return self.actor.summary_row(self, *args, **kw)

    def get_sum_text(self):
        return self.actor.get_sum_text(self)

    def get_row_by_pk(self, pk):
        return self.actor.get_row_by_pk(self, pk)

    def as_bootstrap_html(self, *args, **kw):
        return self.bound_action.action.as_bootstrap_html(self, *args, **kw)

    def get_action_title(self):
        return self.bound_action.action.get_action_title(self)

    def get_title(self):
        return self.actor.get_title(self)

    def render_to_dict(self):
        return self.bound_action.action.render_to_dict(self)

    def goto_instance(self, obj, **kw):
        "See :meth:`BaseRequest.goto_instance`"
        # e.g. find_by_beid is called from viewport, so there is no
        # requesting_panel.
        if self.actor.model is None \
           or not isinstance(obj, self.actor.model) \
           or self.actor.detail_action is None:
           # or self.requesting_panel is None:
            return super(ActorRequest, self).goto_instance(obj, **kw)
        da = obj.get_detail_action(self)
        if da is None:
            return
        self.set_response(
            detail_handler_name=da.full_name())
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

    def to_rst(self, *args, **kw):
        """
        Returns a string representing this request in reStructuredText markup.
        """
        return self.actor.to_rst(self, *args, **kw)

    def run(self, *args, **kw):
        """
        Runs this action request.
        """
        return self.bound_action.action.run_from_code(self, *args, **kw)


class ActionRequest(ActorRequest):

    """
    Holds information about an indivitual web request and provides methods like

    - :meth:`get_user <lino.core.actions.BaseRequest.get_user>`
    - :meth:`confirm <lino.core.actions.BaseRequest.confirm>`
    - :meth:`spawn <lino.core.actions.BaseRequest.spawn>`
    
    An `ActionRequest` is also a :class:`BaseRequest` and inherits its methods.
    
    """
    create_kw = None
    renderer = None

    offset = None
    limit = None
    order_by = None

    def __init__(self, actor=None,
                 request=None, action=None, renderer=None,
                 rqdata=None,
                 param_values=None,
                 action_param_values=None,
                 **kw):
        """
        An ActionRequest is instantiated from different shortcut methods:
        
        - :meth:`lino.core.actors.Actor.request`
        - :meth:`lino.core.actions.Action.request`
        
        """
        #~ ActionRequest.__init__(self,ui,action)
        self.actor = actor
        self.rqdata = rqdata
        self.bound_action = action or actor.default_action
        action = self.bound_action.action
        BaseRequest.__init__(self, request=request, renderer=renderer, **kw)
        self.ah = actor.get_request_handle(self)
        if self.actor.parameters is not None:
            pv = self.actor.param_defaults(self)

            for k in pv.keys():
                if not k in self.actor.parameters:
                    raise Exception(
                        "%s.param_defaults() returned invalid keyword %r" %
                        (self.actor, k))

            # New since 20120913.  E.g. newcomers.Newcomers is a
            # simple pcsw.Clients with
            # known_values=dict(client_state=newcomer) and since there
            # is a parameter `client_state`, we override that
            # parameter's default value.

            for k, v in self.known_values.items():
                if k in pv:
                    pv[k] = v

            # New since 20120914.  MyClientsByGroup has a known group,
            # this must also appear as `group` parameter value.  Lino
            # now understands tables where the master_key is also a
            # parameter.

            if self.actor.master_key is not None:
                if self.actor.master_key in pv:
                    pv[self.actor.master_key] = self.master_instance

            if param_values is None:
                if request is not None:
                    ps = self.actor.params_layout.params_store
                    pv.update(ps.parse_params(request))
            else:
                for k in param_values.keys():
                    if not k in pv:
                        raise Exception(
                            "Invalid key '%s' in param_values of %s "
                            "request (possible keys are %s)" % (
                                k, actor, pv.keys()))
                pv.update(param_values)

            self.param_values = AttrDict(**pv)

        if action.parameters is not None:
            apv = action.action_param_defaults(self, None)
            if request is not None:
                apv.update(
                    action.params_layout.params_store.parse_params(request))
            #~ logger.info("20130122 action_param_defaults() returned %s",apv)
            if action_param_values is not None:
                for k in action_param_values.keys():
                    if not k in apv:
                        raise Exception(
                            "Invalid key '%s' in action_param_values "
                            "of %s request (possible keys are %s)" %
                            (k, actor, apv.keys()))
                apv.update(action_param_values)
            self.action_param_values = AttrDict(**apv)

        self.bound_action.setup_action_request(self)
        # if str(self.actor).startswith('uploads.'):
        #     logger.info("20140503 %s --> edit_mode is %s",
        #                 self, self.edit_mode)

    def setup(self,
              #~ param_values={},
              known_values=None,
              **kw):
        BaseRequest.setup(self, **kw)
        #~ 20120111
        #~ self.known_values = known_values or self.report.known_values
        #~ if self.report.known_values:
        #~ d = dict(self.report.known_values)
        kv = dict()
        for k, v in self.actor.known_values.items():
            kv.setdefault(k, v)
        if known_values:
            kv.update(known_values)
        self.known_values = kv

    def get_data_iterator(self):
        raise NotImplementedError

    def get_base_filename(self):
        return str(self.actor)
        #~ s = self.get_title()
        #~ return s.encode('us-ascii','replace')

