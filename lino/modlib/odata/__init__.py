# -*- coding: UTF-8 -*-
# Copyright 2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api.ad import Plugin


class Plugin(Plugin):

    ui_handle_attr_name = 'odata_handle'

    needs_plugins = ['lino.modlib.jinja']

    url_prefix = 'od'

    def get_patterns(self):
        from django.conf.urls import url
        from . import views

        rx = '^'
        urls = [
            # url(rx + r'/?$', views.Index.as_view()),
            url(rx + r'\$metadata', views.Metadata.as_view()),
            url(rx + r'$', views.Index.as_view()),
            url(rx + r'auth', views.Authenticate.as_view()),
            url(rx + r'(?P<app_label>\w+)/(?P<actor>\w+)$',
                views.List.as_view()),
            url(rx + r'(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$',
                views.Element.as_view()),
        ]
        return urls

    def get_index_view(self):
        from . import views
        return views.Index.as_view()

