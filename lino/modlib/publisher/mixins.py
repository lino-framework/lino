# -*- coding: UTF-8 -*-
# Copyright 2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.api import dd, rt, _

from django import http
from django.conf import settings
from django.utils.translation import get_language
from lino.modlib.printing.mixins import Printable
from lino.modlib.printing.choicelists import BuildMethods

from inspect import isclass

class PreviewPublication(dd.Action):
    label = _("Preview")
    select_rows = False

    def run_from_ui(self, ar, **kw):
        sr_selected = not isclass(self)
        if sr_selected:
            ar.success(open_url=self.publisher_url())
        else:
            ar.success(open_url=self.publisher_url(self, not sr_selected))

    def get_view_permission(self, user_type):
        if not dd.is_installed('publisher'):
            return False
        return super(PreviewPublication, self).get_view_permission(user_type)


class Publishable(Printable):
    class Meta:
        abstract = True
        app_label = 'publisher'

    publisher_location = None
    publisher_template = "publisher/default.pub.html"
    publisher_list_template = "publisher/default_list.pub.html"

    list_template = "publisher/default_list_item.html"

    preview_publication = PreviewPublication()

    # @dd.action(select_rows=False)
    # def preview_publication(self, ar):
    #     sr_selected = not isclass(self)
    #     if sr_selected:
    #         ar.success(open_url=self.publisher_url())
    #     else:
    #         ar.success(open_url=self.publisher_url(self, not sr_selected))

    def publisher_url(self, list=False):
        if list:
            return "/{}/".format(self.publisher_location)
        return "/{}/{}".format(self.publisher_location, self.pk)

    @classmethod
    def get_publisher_response(cls, ar, obj=None):
        env = settings.SITE.plugins.jinja.renderer.jinja_env
        template = env.get_template(cls.publisher_template if obj else cls.publisher_list_template)
        context = ar.get_printable_context(obj=obj, model=cls)
        # context = dict(obj=self, request=request, language=get_language())
        response = http.HttpResponse(
            template.render(**context),
            content_type='text/html;charset="utf-8"')
        return response

    @classmethod
    def get_dashboard_objects(cls, user):
        return []
