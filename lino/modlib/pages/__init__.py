# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.api.ad import Plugin, _


class Plugin(Plugin):

    ui_label = _("Pages")

    verbose_name = _("Pages")

    url_prefix = 'p'

    media_name = 'pages'

    def on_ui_init(self, kernel):
        """This is called when the kernel is being instantiated.
        """
        from lino.modlib.bootstrap3.renderer import Renderer
        self.renderer = Renderer(self)

    def get_patterns(self, ui, prefix=''):
        from django.conf.urls import patterns
        from . import views

        if prefix:
            assert prefix.endswith('/')
        rx = '^' + prefix

        urls = patterns(
            '',
            (rx + r'/?$', self.get_index_view()),
            (rx + r'(?P<ref>\w*)$', views.PagesIndex.as_view()),
        )

        # if self.url_prefix:
        #     return patterns(
        #         '', ('^' + self.url_prefix + "/", include(urls)))
        return urls

    def get_index_view(self):
        from . import views
        return views.PagesIndex.as_view()

    def setup_main_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('pages.Pages')
