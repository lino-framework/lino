# -*- coding: UTF-8 -*-
# Copyright 2009-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Views for `lino.modlib.bootstrap3`.

"""
from __future__ import division
from past.utils import old_div

import logging
logger = logging.getLogger(__name__)

from django import http
from django.conf import settings
from django.views.generic import View
from django.core import exceptions
from django.utils.translation import ugettext as _
from django.utils.translation import get_language


from lino.api import dd
from lino.core import constants
from lino.core import auth
from lino.core.requests import BaseRequest
from lino.core.tablerequest import TableRequest
from lino.core.views import action_request
from lino.core.utils import navinfo
from lino.utils.xmlgen.html import E
from lino.utils.xmlgen import html as xghtml

PLAIN_PAGE_LENGTH = 15

MENUS = dict()


def http_response(ar, tplname, context):
    "Deserves a docstring"
    u = ar.get_user()
    lang = get_language()
    k = (u.profile, lang)
    menu = MENUS.get(k, None)
    if menu is None:
        menu = settings.SITE.get_site_menu(None, u.profile)
        bs3 = settings.SITE.plugins.bootstrap3
        if False:  # 20150803 home button now in base.html
            assert bs3.renderer is not None
            url = bs3.build_plain_url()
            menu.add_url_button(url, label=_("Home"))
        e = bs3.renderer.show_menu(ar, menu)
        menu = E.tostring(e)
        MENUS[k] = menu
    context.update(menu=menu)
    context = ar.get_printable_context(**context)
    context['ar'] = ar
    context['memo'] = ar.parse_memo  # MEMO_PARSER.parse
    env = settings.SITE.plugins.jinja.renderer.jinja_env
    template = env.get_template(tplname)

    response = http.HttpResponse(
        template.render(**context),
        content_type='text/html;charset="utf-8"')

    return response


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


def table2html(ar, as_main=True):
    """Represent the given table request as an HTML table.

    `ar` is the request to be rendered, an instance of
    :class:`lino.core.tablerequest.TableRequest`.

    The returned HTML enclosed in a ``<div>`` tag and generated using
    :mod:`lino.utils.xmlgen.html`.

    If `as_main` is True, include additional elements such as a paging
    toolbar. (This argument is currently being ignored.)

    """
    as_main = True
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
        page = int(old_div(ar.offset, pglen)) + 1

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
        last_page = int(old_div((ar.get_total_count() - 1), pglen))
        kw[constants.URL_PARAM_START] = pglen * last_page
        last_url = ar.get_request_url(**kw)
    else:
        next_url = None
        last_url = None
    buttons.append(('>', _("Next page"), next_url))
    buttons.append(('>>', _("Last page"), last_url))

    return E.div(buttons2pager(buttons), t.as_element())
        

def layout2html(ar, elem):

    wl = ar.bound_action.get_window_layout()
    #~ print 20120901, wl.main
    lh = wl.get_layout_handle(settings.SITE.kernel.default_ui)

    items = list(lh.main.as_plain_html(ar, elem))
    # if navigator:
    #     items.insert(0, navigator)
    #~ print E.tostring(E.div())
    #~ if len(items) == 0: return ""
    return E.form(*items)
    #~ print 20120901, lh.main.__html__(ar)


class List(View):
    """Render a list of records.

    """
    def get(self, request, app_label=None, actor=None):
        ar = action_request(app_label, actor, request, request.GET, True)
        ar.renderer = dd.plugins.bootstrap3.renderer

        context = dict(
            title=ar.get_title(),
            heading=ar.get_title(),
        )

        if isinstance(ar, TableRequest):
            context.update(main=table2html(ar))
        else:
            context.update(main=layout2html(ar, None))

        context.update(ar=ar)
        return http_response(ar, ar.actor.list_html_template, context)


class Element(View):
    """Render a single record.

    """
    def get(self, request, app_label=None, actor=None, pk=None):
        ar = action_request(app_label, actor, request, request.GET, False)
        ar.renderer = dd.plugins.bootstrap3.renderer

        navigator = None
        if pk and pk != '-99999' and pk != '-99998':
            elem = ar.get_row_by_pk(pk)
            if elem is None:
                raise http.Http404("%s has no row with primary key %r" %
                                   (ar.actor, pk))
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

        main = layout2html(ar, elem)
       
        # The `method="html"` argument isn't available in Python 2.6,
        # only 2.7.  It is useful to avoid side effects in case of
        # empty elements: the default method (xml) writes an empty
        # E.div() as "<div/>" while in HTML5 it must be "<div></div>"
        # (and the ending / is ignored).
        
        #~ return E.tostring(main, method="html")
        #~ return E.tostring(main)
        # return main

        context = dict(
            title=ar.get_action_title(),
            obj=elem,
            form=main,
            navigator=navigator,
        )
        #~ template = web.jinja_env.get_template('detail.html')
        context.update(ar=ar)
        return http_response(ar, ar.actor.detail_html_template, context)


class Index(View):
    """
    Render the main page.
    """
    def get(self, request, *args, **kw):
        ui = dd.plugins.bootstrap3
        assert ui.renderer is not None
        context = dict(
            title=settings.SITE.title,
            main=settings.SITE.get_main_html(request, extjs=ui),
        )
        if settings.SITE.user_model is None:
            user = auth.AnonymousUser.instance()
        else:
            user = request.subst_user or request.user
        ar = BaseRequest(
            user=user, request=request,
            renderer=ui.renderer)
        # context.update(ar=ar)
        return http_response(ar, 'bootstrap3/index.html', context)
