# -*- coding: UTF-8 -*-
# Copyright 2009-2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Defines :class:`HtmlRenderer` and :class:`TextRenderer`.
"""

from __future__ import unicode_literals
from __future__ import print_function
# import six
# str = six.text_type
from builtins import str
from past.builtins import basestring
from builtins import object

import logging
logger = logging.getLogger(__name__)

from cgi import escape
from atelier import rstgen

from django.conf import settings
from django.utils.encoding import force_text

from django.utils.translation import ugettext as _
from django.utils.translation import get_language

from lino.utils.html2rst import RstTable
from lino.utils import isiterable
from lino.utils.xmlgen.html import E
from lino.core import constants
from lino.core.menus import Menu, MenuItem
# from lino.utils.xmlgen.html import _html2rst as html2rst
# from lino.utils.xmlgen.html import html2rst
from lino.modlib.extjs.elems import create_layout_panel, create_layout_element

from .plugin import Plugin
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
    u = ar.get_user()
    lang = get_language()
    #~ print 2013115, [li.django_code for li in settings.SITE.languages], settings.SITE.get_default_language(), lang, u.language
    if u and u.language and lang != u.language:
        kw.setdefault(constants.URL_PARAM_USER_LANGUAGE, lang)
    #~ elif lang != settings.SITE.DEFAULT_LANGUAGE.django_code:
    elif lang != settings.SITE.get_default_language():
        kw.setdefault(constants.URL_PARAM_USER_LANGUAGE, lang)


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
    See :doc:`/dev/rendering`.
    """

    can_auth = False
    is_interactive = False
    # not_implemented_js = "alert('Not implemented')"
    not_implemented_js = None

    tableattrs = dict(cellspacing="3px", bgcolor="#ffffff", width="100%")
    cellattrs = dict(align="left", valign="top", bgcolor="#eeeeee")

    def __init__(self, plugin):
        if not isinstance(plugin, Plugin):
            raise Exception("{} is not a Plugin".format(plugin))
        self.plugin = plugin

    def ar2js(self, ar, obj, **status):
        """Return the Javascript code which would run this `ar` on the
        client.

        """
        return self.not_implemented_js


class HtmlRenderer(Renderer):
    row_classes_map = {}

    def js2url(self, js):
        if not js:
            return None
        js = escape(js)
        # js = js.replace('"', '&quot;')
        return 'javascript:' + js

    def href(self, url, text):
        return E.a(text, href=url)

    def show_table(self, *args, **kwargs):
        return E.tostring(self.table2story(*args, **kwargs))

    def table2story(self, ar, nosummary=False, stripped=True, **kw):
        """Returns a HTML element representing the given action request as a
        table. See :meth:`ar.show <lino.core.request.BaseRequest.show>`.

        This silently ignores the parameter `stripped` since for HTML
        this has no meaning.

        """
        if ar.actor.master is not None and not nosummary:
            if ar.actor.slave_grid_format == 'summary':
                return ar.actor.get_slave_summary(ar.master_instance, ar)
        return ar.table2xhtml(**kw)

    def action_call(self, request, bound_action, status):
        return None

    def action_call_on_instance(self, obj, ar, ba, request_kwargs={}, **st):
        """Return a string with Javascript code that would run the given
        action `ba` on the given model instance `obj`. The second
        parameter (`ar`) is the calling action request.

        """
        return self.not_implemented_js

    def request_handler(self, ar, *args, **kw):
        """Return a string with Javascript code that would run the given
        action request `ar`.

        """
        return self.not_implemented_js
        
    def href_to_request(self, sar, tar, text=None, **kw):
        """Return a string with an URL which would run the given target
request `tar`."""
        uri = self.js2url(self.request_handler(tar))
        return self.href_button_action(
            tar.bound_action, uri, text or tar.get_title(), **kw)

    def href_button_action(
            self, ba, url, text=None, title=None, icon_name=NOT_GIVEN, **kw):
        """
        changed 20130905 for "Must read eID card button"
        but that caused icons to not appear in workflow_buttons.
        """
        if icon_name is NOT_GIVEN:
            icon_name = ba.action.icon_name
        if 'style' not in kw:
            if icon_name is None:
                kw.update(style="text-decoration:none")
                # Experimental. Added 20150430
            else:
                kw.update(style="vertical-align:-30%;")
        return self.href_button(url, text, title, icon_name=icon_name, **kw)

    def href_button(
            self, url, text, title=None, target=None, icon_name=None, **kw):
        """
        Returns an etree object of a "button-like" ``<a href>`` tag.
        """
        # logger.info('20121002 href_button %s', unicode(text))
        if target:
            kw.update(target=target)
        if title:
            # Remember that Python 2.6 doesn't like if title is a Promise
            kw.update(title=str(title))
            #~ return xghtml.E.a(text,href=url,title=title)
        if not isinstance(text, (tuple, list)):
            text = (text,)
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
                #~ after_show = ar.get_status()
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

    def pk2url(self, ar, pk, **kw):
        return None

    def get_home_url(self, *args, **kw):
        return settings.SITE.kernel.default_ui.build_plain_url(*args, **kw)

    def instance_handler(self, ar, obj):
        "Overridden by :mod:`lino.modlib.extjs.ext_renderer`"
        return None

    def obj2html(self, ar, obj, text=None, **kwargs):
        """Return a html representation of a pointer to the given database
        object."""
        if text is None:
            text = (force_text(obj),)
        elif isinstance(text, basestring) or E.iselement(text):
            text = (text,)
        url = self.instance_handler(ar, obj)
        if url is None:
            return E.em(*text)
        return E.a(*text, href=url, **kwargs)

    def quick_upload_buttons(self, rr):
        return '[?!]'

    def create_layout_element(self, *args, **kw):
        return create_layout_element(*args, **kw)

    def create_layout_panel(self, *args, **kw):
        return create_layout_panel(*args, **kw)

    # def insert_button(self, ar, text, known_values={}, **options):
    #     return '[?!]'

    def ar2button(self, ar, obj=None, label=None, title=None, **kw):
        ba = ar.bound_action
        # label = label or ba.action.label
        label = label or ba.get_button_label()
        status = ar.get_status()
        js = self.ar2js(ar, obj, **status)
        uri = self.js2url(js)
        return self.href_button_action(
            ba, uri, label, title or ba.action.help_text, **kw)

    def row_action_button(
            self, obj, ar, ba, label=None, title=None, request_kwargs={},
            **kw):
        """
        Return a HTML fragment that displays a button-like link
        which runs the bound action `ba` when clicked.
        """
        label = label or ba.get_button_label()
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

    def window_action_button(
            self, request, ba,
            after_show={}, label=None, title=None, **kw):
        """
        Return a HTML chunk for a button that will execute this action.
        """
        label = label or ba.get_button_label()
        url = self.js2url(self.action_call(request, ba, after_show))
        #~ logger.info('20121002 window_action_button %s %r',a,unicode(label))
        return self.href_button_action(ba, url, str(label),
                                       title or ba.action.help_text, **kw)

    def action_button(self, obj, ar, ba, label=None, **kw):
        label = label or ba.get_button_label()
        return "[%s]" % label

    def show_story(self, ar, story, stripped=True, **kwargs):
        """Render the given story as an HTML element. Ignore `stripped`
        because it makes no sense in HTML.

        """
        from lino.core.actors import Actor
        from lino.core.tables import TableRequest
        elems = []
        for item in story:
            if E.iselement(item):
                elems.append(item)
            elif isinstance(item, type) and issubclass(item, Actor):
                ar = item.default_action.request(parent=ar)
                elems.append(self.table2story(ar, **kwargs))
            elif isinstance(item, TableRequest):
                assert item.renderer is not None
                elems.append(self.table2story(item, **kwargs))
            elif isiterable(item):
                elems.append(self.show_story(ar, item, **kwargs))
                # for i in self.show_story(item, *args, **kwargs):
                #     yield i
            else:
                raise Exception("Cannot handle %r" % item)
        return E.div(*elems)

    def obj2str(self, ar, obj, text=None, **kwargs):
        return E.tostring(self.obj2html(ar, obj, text, **kwargs))

    def show_menu(self, ar, mnu, level=1):
        """
        Render the given menu as an HTML element.
        Used for writing test cases.
        """
        if not isinstance(mnu, Menu):
            assert isinstance(mnu, MenuItem)
            if mnu.bound_action:
                sr = mnu.bound_action.actor.request(
                    action=mnu.bound_action,
                    user=ar.user, subst_user=ar.subst_user,
                    requesting_panel=ar.requesting_panel,
                    renderer=self, **mnu.params)

                url = sr.get_request_url()
            else:
                url = mnu.href
            assert mnu.label is not None
            if url is None:
                return E.p()  # spacer
            return E.li(E.a(mnu.label, href=url, tabindex="-1"))

        items = [self.show_menu(ar, mi, level + 1) for mi in mnu.items]
        #~ print 20120901, items
        if level == 1:
            return E.ul(*items, class_='nav navbar-nav')
        if mnu.label is None:
            raise Exception("%s has no label" % mnu)
        if level == 2:
            cl = 'dropdown'
            menu_title = E.a(
                str(mnu.label), E.b(' ', class_="caret"), href="#",
                class_='dropdown-toggle', data_toggle="dropdown")
        elif level == 3:
            menu_title = E.a(str(mnu.label), href="#")
            cl = 'dropdown-submenu'
        else:
            raise Exception("Menu with more than three levels")
        return E.li(
            menu_title,
            E.ul(*items, class_='dropdown-menu'),
            class_=cl)


class TextRenderer(HtmlRenderer):
    """The renderer used when rendering to .rst files and console output.

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
        print(self.table2story(*args, **kwargs))

    def table2story(self, ar, column_names=None, header_level=None,
                    nosummary=False, stripped=True, **kwargs):
        """Render the given table request as reStructuredText to stdout.
        See :meth:`ar.show <lino.core.request.BaseRequest.show>`.
        """

        if ar.actor.master is not None and not nosummary:
            if ar.actor.slave_grid_format == 'summary':
                s = E.to_rst(
                    ar.actor.get_slave_summary(ar.master_instance, ar),
                    stripped=stripped)
                if stripped:
                    s = s.strip()
                return s

        fields, headers, widths = ar.get_field_info(column_names)

        sums = [fld.zero for fld in fields]
        rows = []
        recno = 0
        for row in ar.sliced_data_iterator:
            recno += 1
            rows.append([x for x in ar.row2text(fields, row, sums)])
        if len(rows) == 0:
            s = str(ar.no_data_text)
            if not stripped:
                s = "\n" + s + "\n"
            return s

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
        s = t.to_rst(rows)
        if header_level is not None:
            h = rstgen.header(header_level, ar.get_title())
            if stripped:
                h = h.strip()
            s = h + "\n" + s
            # s = E.tostring(E.h2(ar.get_title())) + s
        return s

    def show_story(self, ar, story, stripped=True, **kwargs):
        """Render the given story as reStructuredText to stdout."""
        from lino.core.actors import Actor
        from lino.core.requests import ActionRequest

        for item in story:
            if E.iselement(item):
                print(E.to_rst(item, stripped))
            elif isinstance(item, type) and issubclass(item, Actor):
                ar = item.default_action.request(parent=ar)
                self.show_table(ar, stripped=stripped, **kwargs)
            elif isinstance(item, ActionRequest):
                self.show_table(item, stripped=stripped, **kwargs)
                # print(item.table2rst(*args, **kwargs))
            elif isiterable(item):
                self.show_story(ar, item, stripped, **kwargs)
                # for i in self.show_story(ar, item, *args, **kwargs):
                #     print(i)
            else:
                raise Exception("Cannot handle %r" % item)

    def obj2str(self, ar, obj, text=None, **kwargs):
        """Used by :meth:`lino.core.requests.BaseRequest.obj2str`.
        """
        if text is None:
            text = force_text(obj)
        # return "**{0}**".format(text)
        return settings.SITE.obj2text_template.format(text)


