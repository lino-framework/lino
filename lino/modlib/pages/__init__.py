# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.api.ad import Plugin, _


class Plugin(Plugin):

    ui_label = _("Pages")
    verbose_name = _("Pages")

    ui_handle_attr_name = 'pages_handle'
    url_prefix = 'p'

    # media_name = 'pages'

    def on_ui_init(self, ui):
        from .renderer import Renderer
        self.renderer = Renderer(self)
        # from lino.modlib.bootstrap3.renderer import Renderer
        # self.renderer = Renderer(self)

    def get_patterns(self):
        from django.conf.urls import url
        from . import views

        return [
            # url(r'^/?$', self.get_index_view()),
            url(r'^$', self.get_index_view()),
            url(r'^(?P<ref>\w*)$', views.PagesIndex.as_view())]

    def get_index_view(self):
        from . import views
        return views.PagesIndex.as_view()

    def setup_main_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('pages.Pages')
