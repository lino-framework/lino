# -*- coding: UTF-8 -*-
# Copyright 2009-2013 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""

"""

import logging
logger = logging.getLogger(__name__)

from django import http
from django.conf import settings
from django.views.generic import View
#~ from django.utils import simplejson as json
from django.core import exceptions
from django.utils.translation import ugettext as _
from django.utils.translation import get_language

from lino.utils.xmlgen.html import E

from lino.core import auth
from lino.core import web
from lino.core.requests import BaseRequest
from lino.ui.views import action_request


PLAIN_MENUS = dict()


def plain_response(ui, request, tplname, context):
    "Deserves a docstring"
    u = request.subst_user or request.user
    lang = get_language()
    k = (u.profile, lang)
    menu = PLAIN_MENUS.get(k, None)
    if menu is None:
        menu = settings.SITE.get_site_menu(ui, u.profile)
        #~ url = settings.SITE.plain_prefix + '/'
        plain = settings.SITE.plugins.plain
        assert plain.renderer is not None
        url = plain.build_plain_url()
        menu.add_url_button(url, label=_("Home"))
        menu = menu.as_bootstrap_html(plain.renderer, request)
        menu = E.tostring(menu)
        PLAIN_MENUS[k] = menu
    context.update(menu=menu, E=E)
    web.extend_context(context)
    template = settings.SITE.jinja_env.get_template(tplname)

    response = http.HttpResponse(
        template.render(**context),
        content_type='text/html;charset="utf-8"')

    return response


class PlainList(View):

    def get(self, request, app_label=None, actor=None):
        ar = action_request(app_label, actor, request, request.GET, True)
        ar.renderer = settings.SITE.ui.plain_renderer
        context = dict(
            title=ar.get_title(),
            heading=ar.get_title(),
            #~ tbar = buttons,
            main=ar.as_bootstrap_html(),
        )
        context.update(ar=ar)
        return plain_response(settings.SITE.ui, request, 'table.html', context)


class PlainElement(View):

    """
    Render a single record from :class:`lino.ui.PlainRenderer`.
    """

    def get(self, request, app_label=None, actor=None, pk=None):
        ui = settings.SITE.ui
        ar = action_request(app_label, actor, request, request.GET, False)
        ar.renderer = ui.plain_renderer

        context = dict(
            title=ar.get_action_title(),
            #~ menu = E.tostring(menu),
            #~ tbar = buttons,
            main=ar.as_bootstrap_html(pk),
        )
        #~ template = web.jinja_env.get_template('detail.html')
        context.update(ar=ar)

        return plain_response(ui, request, 'detail.html', context)


class PlainIndex(View):

    """
    Similar to AdminIndex
    """

    def get(self, request, *args, **kw):
        # ui = settings.SITE.ui
        ui = settings.SITE.plugins.plain
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
                    "Action not allowed for %s" % user.profile)
            # kw.update(renderer=ui.plain_renderer)
            kw.update(renderer=ui.renderer)
            ar = a.request(request=request, **kw)
            context.update(title=ar.get_title())
            # TODO: let ar generate main
            # context.update(main=ui.plain_renderer.action_call(request,a,{}))
        context.update(ar=ar)
        return plain_response(ui, request, 'plain_index.html', context)
