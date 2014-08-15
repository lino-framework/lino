# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

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
