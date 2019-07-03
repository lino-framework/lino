# -*- coding: UTF-8 -*-
# Copyright 2009-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
Defines :class:`HtmlRenderer` and :class:`TextRenderer`.
"""

from __future__ import print_function
from __future__ import unicode_literals

import logging
from builtins import object
# str = six.text_type
from builtins import str

import six

logger = logging.getLogger(__name__)

from cgi import escape
from atelier import rstgen

from django.conf import settings
from django.db import models
# from django.utils.encoding import force_text
from django.utils.text import format_lazy


from django.utils.translation import ugettext as _
from django.utils.translation import get_language

from etgen.html2rst import RstTable
from lino.utils import isiterable
from lino.utils.jsgen import py2js, js_code
from etgen.html import E, tostring, iselement, forcetext, to_rst
from lino.core import constants
from lino.core.fields import TableRow

from lino.core.menus import Menu, MenuItem
# from etgen.html import _html2rst as html2rst
# from etgen.html import html2rst

from .dashboard import DashboardItem
from .views import json_response

# from . import elems

if False:
    from lino.utils.jscompressor import JSCompressor
    jscompress = JSCompressor().compress
else:
    def jscompress(s):
        return s


def add_user_language(kw, ar):
    if len(settings.SITE.languages) == 1:
        return
    lang = get_language()

    # We set 'ul' only when it is not the default language. But

    # print('20170113 add_user_language', lang, ar.request.LANGUAGE_CODE)

    if False:
        # set it aways because it seems that it is rather difficult to
        # verify which will be the default language.
        kw.setdefault(constants.URL_PARAM_USER_LANGUAGE, lang)
        return
    u = ar.get_user()
    # print("20170113 add_user_language", u, lang)
    #~ print 2013115, [li.django_code for li in settings.SITE.languages], settings.SITE.get_default_language(), lang, u.language
    if u and u.language and lang != u.language:
        kw.setdefault(constants.URL_PARAM_USER_LANGUAGE, lang)
    #~ elif lang != settings.SITE.DEFAULT_LANGUAGE.django_code:
    elif lang != settings.SITE.get_default_language():
        kw.setdefault(constants.URL_PARAM_USER_LANGUAGE, lang)

    # print("20170113 add_user_language", ar, kw, lang, u.language, settings.SITE.get_default_language())


    #~ if len(settings.SITE.languages) > 1:
      #~
        #~ ul = rqdata.get(constants.URL_PARAM_USER_LANGUAGE,None)
        #~ if ul:
            #~ translation.activate(ul)
            #~ request.LANGUAGE_CODE = translation.get_language()


class NOT_GIVEN(object):
    pass


class Renderer(object):
    """
    Base class for all Lino renderers.

    See :doc:`/dev/rendering`.
    """

    can_auth = False
    is_interactive = False
    # not_implemented_js = "alert('Not implemented')"
    not_implemented_js = None
    extjs_version = None

    def __init__(self, plugin=None):
        # if not isinstance(plugin, Plugin):
        #     raise Exception("{} is not a Plugin".format(plugin))
        self.plugin = plugin

    def ar2js(self, ar, obj, **status):
        """
        Return the Javascript code that would run this `ar` on the client.
        """
        return self.not_implemented_js

    # def get_detail_action(self, ar, obj):
        # a = obj.get_detail_action(ar)

        # if a is not None:
        #     if ar is None or a.get_bound_action_permission(ar, obj, None):
        #         return a

    def get_detail_url(self, actor, pk, *args, **kw):
        # return str(actor)+"/"+str(pk)
        return "Detail"  # many doctests depend on this


    def render_action_response(self, ar):
        """Builds a JSON response from response information stored in given
        ActionRequest.

        """
        return json_response(ar.response, ar.content_type)

    # def render_action_response(self, ar):
    #     """In a plain HTML UI this will return a full HTML index page, in
    #     ExtJS it will return JSON code.

    #     """
    #     raise NotImplementedError()


class HtmlRenderer(Renderer):
    """
    A Lino renderer for producing HTML content.
    """
    tableattrs = dict(cellspacing="3px", bgcolor="#ffffff", width="100%")
    # cellattrs = dict(align="left", valign="top", bgcolor="#eeeeee")
    cellattrs = {'class': 'text-cell'}
    """The default attributes to be applied to every table cell.
    """

    def reload_js(self):
        """
        Returns a js string to go inside of a href in the dashboard for reloading the dashboard.
        """
        return ""

    row_classes_map = {}

    def js2url(self, js):
        """There is no Javascript here."""
        return js

    def href(self, url, text):
        return E.a(text, href=url)

    def show_table(self, *args, **kwargs):
        return ''.join([
            tostring(e) for e in self.table2story(*args, **kwargs)])

    def html_text(self, html):
        """Render a chunk of HTML text.

        This does nothing, it just returns the given chunk of
        HTML. Except on ExtJS, where it wraps the chunk into an
        additional ``<div class="htmlText"></div>`` tag.

        """
        return html

    def table2story(self, ar, nosummary=False, stripped=True,
                    show_links=False, header_level=None,
                    **kwargs):
        """
        Returns a HTML element representing the given action request as a
        table. See :meth:`ar.show
        <lino.core.request.BaseRequest.show>`.

        Silently ignores the parameters `stripped` and `header_links`
        since for HTML these options have no meaning.
        """
        # if ar.actor.master is not None and not nosummary:
        if not nosummary:
            if ar.actor.display_mode == 'summary':
                yield ar.actor.get_table_summary(ar.master_instance, ar)
                return

        if header_level is not None:
            k = "h" + str(header_level)
            h = getattr(E, k)(six.text_type(ar.get_title()))
            yield h

        yield ar.table2xhtml(**kwargs)

        # if show_toolbar:
        #     toolbar = ar.plain_toolbar_buttons()
        #     if len(toolbar):
        #         yield E.p(*toolbar)


    def request_handler(self, ar, *args, **kw):
        """
        Return a string with Javascript code that would run the given
        action request `ar`.
        """
        return self.not_implemented_js

    def instance_handler(self, ar, obj, ba):
        """
        Return a string of Javascript code which would open a detail window
        on the given database object.
        """
        if ba is None:
            ba = obj.get_detail_action(ar)
        # print(20180831, ar.actor)
        # ba = obj.__class__.get_default_table().detail_action
        # print(20180831, ba.get_view_permission(ar.get_user().user_type))
        if ba is not None:
            return self.action_call(ar, ba, dict(record_id=obj.pk))

    def href_to(self, ar, obj, text=None):
        h = self.obj2url(ar, obj)
        if h is None:
            # return escape(force_text(obj))
            return escape(str(obj))
        uri = self.js2url(h)
        # return self.href(uri, text or force_text(obj))
        return self.href(uri, text or str(obj))

    def href_to_request(self, ar, tar, text=None, **kw):
        """

        Return a string with an URL which would run the given target request
        `tar`."""

        # TODO: remove the `ar` as it is not needed.

        uri = self.js2url(self.request_handler(tar))
        return self.href_button_action(
            tar.bound_action, uri, text or tar.get_title(), **kw)

    def href_button_action(
            self, ba, url, text=None, title=None, icon_name=NOT_GIVEN, **kw):
        """

        Return an etree element of a ``<a href>`` tag which when clicked would
        execute the given bound action `ba`.

        """
        # changed 20130905 for "Must read eID card button"
        # but that caused icons to not appear in workflow_buttons.
        if icon_name is NOT_GIVEN:
            icon_name = ba.action.icon_name
        if 'style' not in kw:
            if icon_name is None:
                kw.update(style="text-decoration:none")
                # Experimental. Added 20150430
            else:
                kw.update(style="vertical-align:-30%;")
        return self.href_button(url, text, title, icon_name=icon_name, **kw)

    def href_button(self, url, text, title=None, icon_name=None, **kw):
        """Return an etree element of a ``<a href>`` tag to the given URL
        `url`.

        `url` is what goes into the `href` part. If `url` is `None`,
        then we return just a ``<b>`` tag.

        `text` is what goes between the ``<a>`` and the ``</a>``. This
        can be either a string or a tuple (or list) of strings (or
        etree elements).

        """
        # logger.info('20121002 href_button %s', unicode(text))
        if title:
            # Remember that Python 2.6 doesn't like if title is a Promise
            kw.update(title=str(title))
            #~ return xghtml.E.a(text,href=url,title=title)
        if not isinstance(text, (tuple, list)):
            text = (text,)
        text = forcetext(text)
        if url is None:
            return E.b(*text)

        kw.update(href=url)
        if icon_name is not None:
            src = settings.SITE.build_static_url(
                'images', 'mjames', icon_name + '.png')
            img = E.img(src=src, alt=icon_name)
            return E.a(img, **kw)
        else:
            return E.a(*text, **kw)

    def action_call(self, ar, ba, status):
        """Returns the action name. This is not a valid link, but it's
        important to differentiate between clickable and non-clickable
        :meth:`obj2html` calls.

        """
        return str(ba.action)

    def open_in_own_window_button(self, ar):
        """
        Return a button which opens the given table request in its own window.

        """
        return self.window_action_button(
            ar, ar.actor.default_action,
            label="⏏",  # 23CF
            style="text-decoration:none;",
            title=_("Show this table in own window"))

    def window_action_button(
            self, ar, ba,
            status={}, label=None, title=None, **kw):
        """
        Render the given bound action `ba` as an action button.

        Returns a HTML tree element.

        """
        label = label or ba.get_button_label()
        url = self.js2url(self.action_call(ar, ba, status))
        #~ logger.info('20121002 window_action_button %s %r',a,unicode(label))
        return self.href_button_action(ba, url, str(label),
                                       title or ba.action.help_text, **kw)

    def quick_add_buttons(self, ar):
        """Returns a HTML chunk that displays "quick add buttons" for the
        given :class:`action request
        <lino.core.dbtables.TableRequest>`: a button :guilabel:`[New]`
        followed possibly (if the request has rows) by a
        :guilabel:`[Show last]` and a :guilabel:`[Show all]` button.

        See also :srcref:`docs/tickets/56`.

        """
        buttons = []
        # btn = ar.insert_button(_("New"))
        # if btn is not None:
        sar = ar.actor.insert_action.request_from(ar)
        if sar.get_permission():
            btn = sar.ar2button(None, _("New"))
            buttons.append(btn)
            buttons.append(' ')
        n = ar.get_total_count()
        #~ print 20120702, [o for o in ar]
        if n > 0:
            obj = ar.data_iterator[n - 1]
            st = ar.get_status()
            st.update(record_id=obj.pk)
            #~ a = ar.actor.get_url_action('detail_action')
            a = ar.actor.detail_action
            buttons.append(self.window_action_button(
                ar.request, a, st, _("Show Last"),
                icon_name='application_form',
                title=_("Show the last record in a detail window")))
            buttons.append(' ')
            #~ s += ' ' + self.window_action_button(
                #~ ar.ah.actor.detail_action,after_show,_("Show Last"))
            #~ s += ' ' + self.href_to_request(ar,"[%s]" % unicode(_("Show All")))
            buttons.append(self.href_to_request(
                None, ar,
                _("Show All"),
                icon_name='application_view_list',
                title=_("Show all records in a table window")))
        #~ return '<p>%s</p>' % s
        return E.p(*buttons)

    def get_home_url(self, *args, **kw):
        return settings.SITE.kernel.default_ui.build_plain_url(*args, **kw)

    def obj2url(self, ar, obj):
        ba = obj.get_detail_action(ar)
        if ba is not None:
            return self.get_detail_url(ba.actor, obj.pk)

    def obj2html(self, ar, obj, text=None, **kwargs):
        """Return a html representation of a pointer to the given database
        object.

        Examples see :ref:`obj2href`.

        """
        if text is None:
            # text = (force_text(obj),)
            text = (str(obj),)
        elif isinstance(text, six.string_types) or iselement(text):
            text = (text,)
        url = self.obj2url(ar, obj)
        if url is None:
            return E.em(*text)
        return self.href_button(url, text, **kwargs)

    def obj2str(self, *args, **kwargs):
        return tostring(self.obj2html(*args, **kwargs))

    def quick_upload_buttons(self, rr):
        return '[?!]'

    def ar2button(self, ar, obj=None, label=None, title=None, **kwargs):
        ba = ar.bound_action
        label = label or ba.get_button_label()
        status = ar.get_status()
        js = self.ar2js(ar, obj, **status)
        uri = self.js2url(js)
        return self.href_button_action(
            ba, uri, label, title or ba.action.help_text, **kwargs)

    def menu_item_button(self, ar, mi, label=None, icon_name=None, **kwargs):
        """Render the given menu item `mi` as an action button.

        Returns a HTML tree element.
        Currently supports only window actions.

        """
        label = label or mi.label or mi.bound_action.get_button_label()
        if mi.instance is not None:
            kwargs.update(status=dict(record_id=mi.instance.pk))
        return self.window_action_button(
            ar, mi.bound_action, label=label,
            icon_name=icon_name, **kwargs)

    def action_button(self, obj, ar, ba, label=None, **kw):
        label = label or ba.get_button_label()
        return "[%s]" % label

    def action_call_on_instance(self, obj, ar, ba, request_kwargs={}, **st):
        """Return a string with Javascript code that would run the given
        action `ba` on the given model instance `obj`. The second
        parameter (`ar`) is the calling action request.

        """
        return self.not_implemented_js

    def row_action_button(
            self, obj, ar, ba, label=None, title=None, request_kwargs={},
            **kw):
        """
        Return a HTML fragment that displays a button-like link
        which runs the bound action `ba` when clicked.
        """
        label = label or ba.get_button_label()
        request_kwargs.update(selected_rows=[obj])
        js = self.action_call_on_instance(obj, ar, ba, request_kwargs)
        uri = self.js2url(js)
        return self.href_button_action(
            ba, uri, label, title or ba.action.help_text, **kw)

    def row_action_button_ar(
            self, obj, ar, label=None, title=None, request_kwargs={},
            **kw):
        """
        Return a HTML fragment that displays a button-like link
        which runs the action request `ar` when clicked.
        """
        ba = ar.bound_action
        label = label or ba.get_button_label()
        js = self.action_call_on_instance(obj, ar, ba)
        uri = self.js2url(js)
        return self.href_button_action(
            ba, uri, label, title or ba.action.help_text, **kw)

    def show_story(self, ar, story, stripped=True, **kwargs):
        """
        Render the given story as an HTML element. Ignore `stripped`
        because it makes no sense in HTML.

        A story is an iterable of things that can be rendered.

        """
        from lino.core.actors import Actor
        from lino.core.tables import TableRequest
        from lino.core.requests import ActionRequest
        elems = []
        try:
            for item in forcetext(story):
                # print("20180907 {}".format(item))
                if iselement(item):
                    elems.append(item)
                elif isinstance(item, type) and issubclass(item, Actor):
                    ar = item.default_action.request(parent=ar)
                    elems.extend(self.table2story(ar, **kwargs))
                elif isinstance(item, TableRequest):
                    assert item.renderer is not None
                    elems.extend(self.table2story(item, **kwargs))
                elif isinstance(item, ActionRequest):
                    # example : courses.StatusReport in dashboard
                    assert item.renderer is not None
                    elems.append(self.show_story(ar, item.actor.get_story(None, ar), **kwargs))
                elif isinstance(item, DashboardItem):
                    elems.append(E.div(
                        self.show_story(ar, item.render(ar), **kwargs),
                        CLASS="dashboard-item " + item.actor.actor_id.replace(".","-") if getattr(item, "actor", False) else ""
                    ))
                elif isiterable(item):
                    elems.append(self.show_story(ar, item, **kwargs))
                    # for i in self.show_story(item, *args, **kwargs):
                    #     yield i
                else:
                    raise Exception("Cannot handle %r" % item)
        except Warning as e:
            elems.append(str(e))
        # print("20180907 show_story in {} : {}".format(ar.renderer, elems))
        return E.div(*elems) if elems else ""

    def show_menu(self, ar, mnu, level=1):
        """
        Render the given menu as an HTML element.
        Used for writing test cases.
        """
        if not isinstance(mnu, Menu):
            assert isinstance(mnu, MenuItem)
            if mnu.bound_action:
                sar = mnu.bound_action.actor.request(
                    action=mnu.bound_action,
                    user=ar.user, subst_user=ar.subst_user,
                    requesting_panel=ar.requesting_panel,
                    renderer=self, **mnu.params)
                # print("20170113", sar)
                url = sar.get_request_url()
            else:
                url = mnu.href
            assert mnu.label is not None
            if url is None:
                return E.p()  # spacer
            return E.li(E.a(str(mnu.label), href=url, tabindex="-1"))

        items = [self.show_menu(ar, mi, level + 1) for mi in mnu.items]
        #~ print 20120901, items
        if level == 1:
            return E.ul(*items, **{'class':'nav navbar-nav'})
        if mnu.label is None:
            raise Exception("%s has no label" % mnu)
        if level == 2:
            cl = 'dropdown'
            menu_title = E.a(
                str(mnu.label), E.b(' ', **{'class': "caret"}), href="#",
                data_toggle="dropdown", **{'class':'dropdown-toggle'})
        elif level == 3:
            menu_title = E.a(str(mnu.label), href="#")
            cl = 'dropdown-submenu'
        else:
            raise Exception("Menu with more than three levels")
        return E.li(
            menu_title,
            E.ul(*items, **{'class':'dropdown-menu'}),
            **{'class':cl})

    def goto_instance(self, ar, obj, **kw):
        pass

    def add_help_text(self, kw, help_text, title, datasource, fieldname):
        pass

class TextRenderer(HtmlRenderer):
    """
    Lino renderer which renders tables as reStructuredText to stdout.
    Used for doctests and console output.
    See also :class:`TestRenderer`.
    """

    user = None

    def __init__(self, *args, **kw):
        HtmlRenderer.__init__(self,  *args, **kw)
        self.user = None

    def get_request_url(self, ar, *args, **kw):
        return None

    def menu2rst(self, ar, mnu, level=1):
        """Used by :meth:`show_menu`."""

        if not isinstance(mnu, Menu):
            return str(mnu.label)

        has_submenus = False
        for i in mnu.items:
            if isinstance(i, Menu):
                has_submenus = True
        items = [self.menu2rst(ar, mi, level + 1) for mi in mnu.items]
        if has_submenus:
            s = rstgen.ul(items).strip() + '\n'
            if mnu.label is not None:
                s = str(mnu.label) + ' :\n\n' + s
        else:
            s = ', '.join(items)
            if mnu.label is not None:
                s = str(mnu.label) + ' : ' + s
        return s

    def show_menu(self, ar, mnu, stripped=True, level=1):
        """
        Render the given menu as a reStructuredText
        formatted bullet list.
        Called from :meth:`lino.core.requests.BaseRequest.show_menu`.

        :stripped: remove lots of blanklines which are necessary for
                   reStructuredText but disturbing in a doctest
                   snippet.

        """
        s = self.menu2rst(ar, mnu, level)
        if stripped:
            for ln in s.splitlines():
                if ln.strip():
                    print(ln)
        else:
            print(s)

    def show_table(self, *args, **kwargs):
        for ln in self.table2story(*args, **kwargs):
            print(ln)

    def table2story(self, ar, column_names=None, header_level=None,
                    header_links=None, nosummary=False, stripped=True,
                    show_links=False, **kwargs):
        """
        Render the given table request as reStructuredText to stdout.  See
        :meth:`ar.show <lino.core.request.BaseRequest.show>`.
        """

        if ar.actor.master is not None and not nosummary:
            if ar.actor.display_mode == 'summary':
                s = to_rst(
                    ar.actor.get_table_summary(ar.master_instance, ar),
                    stripped=stripped)
                if stripped:
                    s = s.strip()
                yield s
                return

        fields, headers, widths = ar.get_field_info(column_names)

        sums = [fld.zero for fld in fields]
        rows = []
        recno = 0
        for row in ar.sliced_data_iterator:
            recno += 1
            if show_links:
                rows.append([
                    to_rst(x) for x in ar.row2html(
                        recno, fields, row, sums)])
            else:
                rows.append([x for x in ar.row2text(fields, row, sums)])

        if header_level is not None:
            h = rstgen.header(header_level, ar.get_title())
            if stripped:
                h = h.strip()
            yield h
            # s = h + "\n" + s
            # s = tostring(E.h2(ar.get_title())) + s

        if len(rows) == 0:
            s = str(ar.no_data_text)
            if not stripped:
                s = "\n" + s + "\n"
            yield s
            return

        if not ar.actor.hide_sums:
            has_sum = False
            for i in sums:
                if i:
                    #~ print '20120914 zero?', repr(i)
                    has_sum = True
                    break
            if has_sum:
                rows.append([x for x in ar.sums2html(fields, sums)])

        t = RstTable(headers, **kwargs)
        yield t.to_rst(rows)

    def show_story(self, ar, story, stripped=True, **kwargs):
        """Render the given story as reStructuredText to stdout."""
        from lino.core.actors import Actor
        from lino.core.tables import TableRequest
        from lino.core.requests import ActionRequest

        try:
            for item in forcetext(story):
                if iselement(item):
                    print(to_rst(item, stripped))
                elif isinstance(item, type) and issubclass(item, Actor):
                    ar = item.default_action.request(parent=ar)
                    self.show_table(ar, stripped=stripped, **kwargs)
                elif isinstance(item, DashboardItem):
                    self.show_story(
                        ar, item.render(ar), stripped, **kwargs)
                elif isinstance(item, TableRequest):
                    self.show_table(item, stripped=stripped, **kwargs)
                    # print(item.table2rst(*args, **kwargs))
                elif isinstance(item, ActionRequest):
                    # example : courses.StatusReport in dashboard
                    assert item.renderer is not None
                    self.show_story(ar, item.actor.get_story(None, ar), **kwargs)
                elif isiterable(item):
                    self.show_story(ar, item, stripped, **kwargs)
                    # for i in self.show_story(ar, item, *args, **kwargs):
                    #     print(i)
                else:
                    raise Exception("Cannot handle %r" % item)
        except Warning as e:
            print(e)

    def obj2str(self, ar, obj, text=None, **kwargs):
        """Used by :meth:`lino.core.requests.BaseRequest.obj2str`.
        """
        if text is None:
            # text = force_text(obj)
            text = str(obj)
        # return "**{0}**".format(text)
        return settings.SITE.obj2text_template.format(text)

class TestRenderer(TextRenderer):
    """
    Like :class:`TextRenderer` but returns a string instead of
    printing to stdout.

    Experimentally used in :mod:`lino_book.projects.watch.tests`
    and :mod:`lino_book.projects.lydia.tests`.
    """
    def show_table(self, *args, **kwargs):
        return '\n'.join(self.table2story(*args, **kwargs))


class MailRenderer(HtmlRenderer):
    """
    A Lino renderer to be used when sending emails.

    Subclassed by :class:`lino.modlib.jinja.renderer.JinjaRenderer`
    """
    def get_detail_url(self, actor, pk, *args, **kw):
        # return self.plugin.build_plain_url(
        #     'api', actor.app_label, actor.__name__, str(pk), *args, **kw)
        if actor.model:
            return "{}api/{}/{}/{}".format(
                settings.SITE.mobile_server_url or settings.SITE.server_url,
                actor.model._meta.app_label, actor.model.get_default_table().__name__, pk)
        return "{}api/{}/{}/{}".format(
            settings.SITE.server_url,
            actor.app_label, actor.__name__, pk)

    def show_story(self, *args, **kwargs):
        e = super(MailRenderer, self).show_story(*args, **kwargs)
        return tostring(e)


class JsRenderer(HtmlRenderer):
    """
    A Lino renderer for HTML with JavaScript.
    Common base for
    :class:`lino_react.react.renderer.Renderer`,
    :class:`lino.modlib.extjs.ext_renderer.ExtRenderer` and
    :class:`lino_extjs6.extjs.ext_renderer.ExtRenderer`.
    """

    def reload_js(self):
        """
        Returns a js string to go inside of a href in the dashboard for reloading the dashboard.
        """
        return "Lino.viewport.refresh();"


    def goto_instance(self, ar, obj, detail_action=None, **kw):
        """Ask the client to display a detail window on the given
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

        If the detail layout of the current actor can be used for the
        object to be displayed, we don't want to open a new detail
        window.

        This calls :meth:`obj.get_detail_action
        <lino.core.model.Model.get_detail_action>`.

        """
        if ar.actor is not None:
            da = detail_action or obj.get_detail_action(ar)
            if da is None:
                return
            if da.actor == ar.actor:
                ar.set_response(detail_handler_name=da.full_name())
                if ar.actor.handle_uploaded_files is not None:
                    ar.set_response(record_id=obj.pk)
                else:
                    ar.set_response(
                        data_record=ar.elem2rec_detailed(obj))
                return
        js = self.instance_handler(ar, obj, detail_action)
        kw.update(eval_js=js)
        ar.set_response(**kw)

    def js2url(self, js):
        if not js:
            return None
        js = escape(js)
        return 'javascript:' + js

    def get_action_status(self, ar, ba, obj, **kw):
        kw.update(ar.get_status())
        if ba.action.parameters and not ba.action.keep_user_values:
            apv = ar.action_param_values
            if apv is None:
                apv = ba.action.action_param_defaults(ar, obj)
            ps = ba.action.params_layout.params_store
            kw.update(field_values=ps.pv2dict(ar, apv))
        if isinstance(obj, (models.Model, TableRow)):
            kw.update(record_id=obj.pk)

        return kw

    def ar2js(self, ar, obj, **status):
        """Implements :meth:`lino.core.renderer.HtmlRenderer.ar2js`.

        """
        rp = ar.requesting_panel
        ba = ar.bound_action

        if ba.action.is_window_action():
            # Window actions have been generated by
            # js_render_window_action(), so we just call its `run(`)
            # method:
            status.update(self.get_action_status(ar, ba, obj))
            return "Lino.%s.run(%s,%s)" % (
                ba.full_name(), py2js(rp), py2js(status))

        # It's a custom ajax action generated by
        # js_render_custom_action().

        # 20140429 `ar` is now None, see :ref:`welfare.tested.integ`
        if ba.action.select_rows:
            params = self.get_action_params(ar, ba, obj)
            return "Lino.%s(%s,%s,%s,%s)" % (
                ba.full_name(), py2js(rp),
                py2js(ar.is_on_main_actor), py2js(obj.pk), py2js(params))
        # assert obj is None
        # return "oops"
        # params = self.get_action_params(ar, ba, obj)
        # url = ar.get_request_url()

        url = self.plugin.build_plain_url(
            ar.actor.app_label, ar.actor.__name__)
        params = ar.get_status().get('base_params', None)
        pp = "function() {return %s;}" % py2js(params)
        return "Lino.list_action_handler(%s,%s,%s,%s)()" % (
            py2js(url), py2js(ba.action.action_name),
            py2js(ba.action.http_method),pp)


    def get_detail_url(self, actor, pk, *args, **kw):
        return self.plugin.build_plain_url(
            'api', actor.app_label, actor.__name__, str(pk), *args, **kw)


    def obj2url(self, ar, obj):
        return self.js2url(self.instance_handler(ar, obj, None))

    def add_help_text(self, kw, help_text, title, datasource, fieldname):
        if settings.SITE.use_quicktips:
            if settings.SITE.show_internal_field_names:
                ttt = "(%s.%s) " % (datasource, fieldname)
            else:
                ttt = ''
            if help_text:
                ttt = format_lazy(u"{}{}", ttt, help_text)
            if ttt:
                # kw.update(qtip=self.field.help_text)
                # kw.update(toolTipText=self.field.help_text)
                # kw.update(tooltip=self.field.help_text)
                kw.update(listeners=dict(render=js_code(
                    "Lino.quicktip_renderer(%s,%s)" % (
                        py2js(title),
                        py2js(ttt)))
                ))

