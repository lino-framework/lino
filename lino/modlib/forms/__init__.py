# -*- coding: UTF-8 -*-
# Copyright 2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
This started as a copy of :mod:`lino.modlib.bootstrap`.

.. autosummary::
   :toctree:

    views
    renderer
    models
"""

from lino.api.ad import Plugin


class Plugin(Plugin):

    ui_handle_attr_name = 'forms_handle'

    needs_plugins = ['lino.modlib.jinja']

    url_prefix = 'f'

    def on_ui_init(self, ui):
        from .renderer import Renderer
        self.renderer = Renderer(self)
        # ui.bs3_renderer = self.renderer

    def get_patterns(self):
        from django.conf.urls import url
        from . import views

        rx = '^'

        urls = [
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

