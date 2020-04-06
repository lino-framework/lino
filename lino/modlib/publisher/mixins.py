# -*- coding: UTF-8 -*-
# Copyright 2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.api import dd, rt, _

from django import http
from django.conf import settings
from django.utils.translation import get_language
from lino.modlib.printing.mixins import Printable
from lino.modlib.printing.choicelists import BuildMethods


class Publishable(Printable):
    class Meta:
        abstract = True
        app_label = 'publisher'

    publisher_location = None
    publisher_template = "publisher/default.pub.html"

    def publisher_url(self):
        return "/{}/{}".format(self.publisher_location, self.pk)

    def get_publisher_response(self, ar):
        env = settings.SITE.plugins.jinja.renderer.jinja_env
        template = env.get_template(self.publisher_template)
        context = ar.get_printable_context(obj=self)
        # context = dict(obj=self, request=request, language=get_language())
        response = http.HttpResponse(
            template.render(**context),
            content_type='text/html;charset="utf-8"')
        return response

    @classmethod
    def get_dashboard_objects(cls, user):
        return []
