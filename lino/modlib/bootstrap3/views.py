# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""

"""

import logging
logger = logging.getLogger(__name__)

from django import http
from django.conf import settings
from django.views.generic import View
from django.core import exceptions
from django.utils.translation import ugettext as _
from django.utils.translation import get_language

from lino.utils.xmlgen.html import E

from lino import dd
from lino.core import auth
from lino.core import web
from lino.core.requests import BaseRequest
from lino.ui.views import action_request


MENUS = dict()


def http_response(request, tplname, context):
    "Deserves a docstring"
    u = request.subst_user or request.user
    lang = get_language()
    k = (u.profile, lang)
    menu = MENUS.get(k, None)
    if menu is None:
        menu = settings.SITE.get_site_menu(None, u.profile)
        bs3 = settings.SITE.plugins.bootstrap3
        assert bs3.renderer is not None
        url = bs3.build_plain_url()
        menu.add_url_button(url, label=_("Home"))
        menu = menu.as_bootstrap_html(bs3.renderer, request)
        menu = E.tostring(menu)
        MENUS[k] = menu
    context.update(menu=menu, E=E)
    web.extend_context(context)
    template = settings.SITE.jinja_env.get_template(tplname)

    response = http.HttpResponse(
        template.render(**context),
        content_type='text/html;charset="utf-8"')

    return response


class List(View):

    def get(self, request, app_label=None, actor=None):
        ar = action_request(app_label, actor, request, request.GET, True)
        # ar.renderer = settings.SITE.ui.bs3_renderer
        ar.renderer = dd.plugins.bootstrap3.renderer
        context = dict(
            title=ar.get_title(),
            heading=ar.get_title(),
            #~ tbar = buttons,
            main=ar.as_bootstrap_html(),
        )
        context.update(ar=ar)
        return http_response(request, ar.actor.list_html_template, context)


class Element(View):

    """
    Render a single record from :class:`lino.ui.PlainRenderer`.
    """

    def get(self, request, app_label=None, actor=None, pk=None):
        ar = action_request(app_label, actor, request, request.GET, False)
        ar.renderer = dd.plugins.bootstrap3.renderer

        context = dict(
            title=ar.get_action_title(),
            #~ menu = E.tostring(menu),
            #~ tbar = buttons,
            main=ar.as_bootstrap_html(pk),
        )
        #~ template = web.jinja_env.get_template('detail.html')
        context.update(ar=ar)
        return http_response(request, ar.actor.detail_html_template, context)


class Index(View):

    """
    Similar to AdminIndex
    """

    def get(self, request, *args, **kw):
        ui = dd.plugins.bootstrap3
        assert ui.renderer is not None
        context = dict(
            title=settings.SITE.title,
            main='',
        )
        if settings.SITE.user_model is not None:
            user = request.subst_user or request.user
        else:
            user = auth.AnonymousUser.instance()
        a = settings.SITE.get_main_action(user)
        if a is None:
            ar = BaseRequest(
                user=user, request=request,
                renderer=ui.renderer)
        else:
            if not a.get_view_permission(user.profile):
                raise exceptions.PermissionDenied(
                    "As %s you have no permission to run this action."
                    % user.profile)
                # The text of an Exception may not be
                # internationalized because some error handling code
                # may want to write it to a plain ascii stream.
            kw.update(renderer=ui.renderer)
            ar = a.request(request=request, **kw)
            context.update(title=ar.get_title())
            # TODO: let ar generate main
            # context.update(main=ui.bs3_renderer.action_call(request,a,{}))
        context.update(ar=ar)
        return http_response(request, 'bootstrap3/index.html', context)
