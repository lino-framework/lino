# -*- coding: UTF-8 -*-
# Copyright 2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

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
    publisher_page_template = "publisher/page.pub.html"
    publisher_item_template = "publisher/item.pub.html"

    preview_publication = PreviewPublication()

    # @dd.action(select_rows=False)
    # def preview_publication(self, ar):
    #     sr_selected = not isclass(self)
    #     if sr_selected:
    #         ar.success(open_url=self.publisher_url())
    #     else:
    #         ar.success(open_url=self.publisher_url(self, not sr_selected))

    def publisher_url(self):
        return "/{}/{}".format(self.publisher_location, self.pk)

    # def publisher_url(self, list=False):
    #     if list:
    #         return "/{}/".format(self.publisher_location)
    #     return "/{}/{}".format(self.publisher_location, self.pk)

    def render_from(self, tplname, ar):
        env = settings.SITE.plugins.jinja.renderer.jinja_env
        context = ar.get_printable_context(obj=self)
        template = env.get_template(tplname)
        # print("20210112 publish {} {} using {}".format(cls, obj, template))
        # context = dict(obj=self, request=request, language=get_language())
        return template.render(**context)

    def get_publisher_response(self, ar):
        html = self.render_from(self.publisher_page_template, ar)
        return http.HttpResponse(html, content_type='text/html;charset="utf-8"')

    @classmethod
    def render_dashboard_items(cls, ar):
        for obj in cls.get_dashboard_objects(ar):
            yield obj.render_from(obj.publisher_item_template, ar)

    @classmethod
    def get_dashboard_objects(cls, ar):
        return []
