# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""This started as a copy of :mod:`lino.modlib.plain` and moved to the
version 3 of `Bootstrap <http://twitter.github.com/bootstrap>`_ CSS
toolkit.

"""

from lino.ad import Plugin
from django.utils.translation import ugettext_lazy as _


class Plugin(Plugin):

    ui_label = _("Bootstrap")

    # site_js_snippets = ['snippets/plain.js']

    url_prefix = 'bs3'

    media_name = 'bootstrap'
    media_root = None
    media_base_url = "http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/"

    def on_ui_init(self, ui):
        from .renderer import Renderer
        self.renderer = Renderer(self)
        # ui.bs3_renderer = self.renderer

    def get_used_libs(self, html=False):
        if html is not None:
            yield ("Bootstrap", '3.x', "http://getbootstrap.com")
            # yield ("jQuery", '?', "http://...")

    def get_index_view(self):
        from . import views
        return views.Index.as_view()

    def get_patterns(self, kernel):
        from django.conf.urls import patterns
        from . import views
        urls = patterns(
            '',
            (r'^/?$', views.Index.as_view()),
            (r'^(?P<app_label>\w+)/(?P<actor>\w+)$',
             views.List.as_view()),
            (r'^(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$',
             views.Element.as_view()),
        )
        return urls
