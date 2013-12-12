# -*- coding: UTF-8 -*-
# Copyright 2009-2013 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""

"""

import logging
logger = logging.getLogger(__name__)

from django import http
from django.db import models
from django.db import IntegrityError
from django.conf import settings
from django.views.generic import View
#~ from django.utils import simplejson as json
from django.core import exceptions
from django.utils.translation import ugettext as _
from django.utils.translation import get_language

from lino.utils.xmlgen.html import E
from lino.utils.jsgen import py2js

from lino.core import auth
from lino.core import actors
from lino.core import constants
from lino.core import web
from lino.core.requests import BaseRequest


MAX_ROW_COUNT = 300

PLAIN_MENUS = dict()


def json_response_kw(**kw):
    return json_response(kw)


def json_response(x, content_type='application/json'):
    s = py2js(x)
    """
    Theroretically we should send content_type='application/json'
    (http://stackoverflow.com/questions/477816/the-right-json-content-type),
    but "File uploads are not performed using Ajax submission, 
    that is they are not performed using XMLHttpRequests. (...) 
    If the server is using JSON to send the return object, then 
    the Content-Type header must be set to "text/html" in order 
    to tell the browser to insert the text unchanged into the 
    document body." 
    (http://docs.sencha.com/ext-js/3-4/#!/api/Ext.form.BasicForm)
    See 20120209.
    """
    return http.HttpResponse(s, content_type=content_type)
    #~ return HttpResponse(s, content_type='text/html')
    #~ return HttpResponse(s, content_type='application/json')
    #~ return HttpResponse(s, content_type='text/json')


def requested_actor(app_label, actor):
    """
    Utility function which returns the requested actor,
    either directly or (if specified name is a model) that
    model's default table.
    """
    x = getattr(settings.SITE.modules, app_label, None)
    if x is None:
        #~ raise http.Http404("There's no app_label %r here" % app_label)
        raise Exception("There's no app_label %r here" % app_label)
    cl = getattr(x, actor)
    if not isinstance(cl, type):
        raise http.Http404("%s.%s is not a class" % (app_label, actor))
    if issubclass(cl, models.Model):
        return cl.get_default_table()
    if not issubclass(cl, actors.Actor):
        #~ raise http.Http404("%r is not an actor" % cl)
        raise http.Http404("%r is not an actor" % cl)
    return cl


def action_request(app_label, actor, request, rqdata, is_list, **kw):
    rpt = requested_actor(app_label, actor)
    action_name = rqdata.get(constants.URL_PARAM_ACTION_NAME, None)
    #~ if action_name is None:
        #~ logger.info("20130731 action_name is None")
    if not action_name:
        if is_list:
            action_name = rpt.default_list_action_name
        else:
            action_name = rpt.default_elem_action_name
    a = rpt.get_url_action(action_name)
    if a is None:
        raise http.Http404("%s has no url action %r (possible values are %s)" % (
            rpt, action_name, rpt.get_url_action_names()))
    user = request.subst_user or request.user
    if False:  # 20130829
        if not a.get_view_permission(user.profile):
            raise exceptions.PermissionDenied(
                _("As %s you have no permission to run this action.") % user.profile)
            #~ return http.HttpResponseForbidden(_("As %s you have no permission to run this action.") % user.profile)
    ar = rpt.request(request=request, action=a, **kw)
    return ar


def plain_response(ui, request, tplname, context):
    "Deserves a docstring"
    u = request.subst_user or request.user
    lang = get_language()
    k = (u.profile, lang)
    menu = PLAIN_MENUS.get(k, None)
    if menu is None:
        menu = settings.SITE.get_site_menu(ui, u.profile)
        #~ url = settings.SITE.plain_prefix + '/'
        url = settings.SITE.build_plain_url()
        menu.add_url_button(url, label=_("Home"))
        menu = menu.as_html(ui, request)
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
            main=ar.as_html(),
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
            main=ar.as_html(pk),
        )
        #~ template = web.jinja_env.get_template('detail.html')
        context.update(ar=ar)

        return plain_response(ui, request, 'detail.html', context)


class PlainIndex(View):

    """
    Similar to AdminIndex
    """

    def get(self, request, *args, **kw):
        ui = settings.SITE.ui
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
            ar = BaseRequest(user=user, request=request)
        else:
            if not a.get_view_permission(user.profile):
                raise exceptions.PermissionDenied(
                    "Action not allowed for %s" % user)
            kw.update(renderer=ui.plain_renderer)
            ar = a.request(request=request, **kw)
            #~ ar.renderer = ui.plain_renderer
            context.update(title=ar.get_title())
            # TODO: let ar generate main
            # context.update(main=ui.plain_renderer.action_call(request,a,{}))
        context.update(ar=ar)
        return plain_response(ui, request, 'plain_index.html', context)
