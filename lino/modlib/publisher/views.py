# -*- coding: UTF-8 -*-
# Copyright 2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from django.conf import settings
from django import http
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

from lino.core import auth
from lino.core.requests import BaseRequest

from django.shortcuts import redirect


class Element(View):

    publisher_model = None

    def get(self, request, pk=None):
        ar = BaseRequest(request=request, renderer=settings.SITE.kernel.default_renderer, permalink_uris=True)
        obj = self.publisher_model.objects.get(id=pk) if pk is not None else None
        return self.publisher_model.get_publisher_response(ar, obj)


class Index(View):
    """
    Render the main page.
    """
    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kw):
        # raise Exception("20171122 {} {}".format(
        #     get_language(), settings.MIDDLEWARE_CLASSES))
        ar = BaseRequest(request=request, renderer=settings.SITE.kernel.default_renderer, permalink_uris=True)
        env = settings.SITE.plugins.jinja.renderer.jinja_env
        template = env.get_template("publisher/index.pub.html")
        context = ar.get_printable_context(obj=self)
        response = http.HttpResponse(
            template.render(**context),
            content_type='text/html;charset="utf-8"')
        return response

class Login(View):
    """
    Render the main page.
    """
    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kw):
        # raise Exception("20171122 {} {}".format(
        #     get_language(), settings.MIDDLEWARE_CLASSES))
        ar = BaseRequest(request=request, renderer=settings.SITE.kernel.default_renderer, permalink_uris=True)
        env = settings.SITE.plugins.jinja.renderer.jinja_env
        template = env.get_template("publisher/login.html")
        context = ar.get_printable_context(obj=self)
        response = http.HttpResponse(
            template.render(**context),
            content_type='text/html;charset="utf-8"')
        return response

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kw):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(
            request, username=username, password=password)
        auth.login(request, user, backend=u'lino.core.auth.backends.ModelBackend')

        return redirect("/")
