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
The :mod:`lino.apps.plain` app adds the "plain" user interface.
"""

from lino.ad import Plugin


class Plugin(Plugin):

    url_prefix = 'b'

    # site_js_snippets = ['snippets/plain.js']

    media_base_url = "http://twitter.github.com/bootstrap/assets/"
    media_name = 'bootstrap'
    media_root = None

    def on_ui_init(self, ui):
        from .plain_renderer import PlainRenderer
        self.renderer = PlainRenderer(self)
        ui.plain_renderer = self.renderer

    def build_bootstrap_url(self, *args, **kw):
        #return self.build_media_url('bootstrap', *args, **kw)
        return self.build_media_url(*args, **kw)

    def get_used_libs(self, html=False):
        if html is not None:
            # Lino needs v 2.3.1 but we don't check that
            yield ("Bootstrap", '2.3.1?', "https://github.com/twbs/bootstrap")
            # yield ("jQuery", '?', "http://...")

    def get_index_view(self):
        from . import views
        return views.PlainIndex.as_view()

    def get_patterns(self, ui):
        from django.conf.urls import patterns, include, url
        from . import views
        rx = '^'
        urls = patterns(
            '',
            (rx + r'$', views.PlainIndex.as_view()),
            (rx + r'(?P<app_label>\w+)/(?P<actor>\w+)$',
             views.PlainList.as_view()),
            (rx + r'(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$',
             views.PlainElement.as_view()),
        )

        if ui.site.plain_prefix:
            return patterns(
                '', url('^' + self.url_prefix + "/", include(urls)))
        return urls


