# -*- coding: UTF-8 -*-
# Copyright 2012-2013 Luc Saffre
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

from lino.ad import Plugin
from django.utils.translation import ugettext_lazy as _


class Plugin(Plugin):

    ui_label = _("Pages")

    verbose_name = _("Pages")

    url_prefix = 'p'

    def __init__(self, *args, **kw):
        super(Plugin, self).__init__(*args, **kw)
        from lino.modlib.plain.plain_renderer import PlainRenderer
        self.renderer = PlainRenderer(self)

    def get_patterns(self, ui):
        from django.conf.urls import patterns
        from . import views

        urls = patterns(
            '',
            (r'^/?$', self.get_index_view()),
            (r'^(?P<ref>\w*)$', views.PagesIndex.as_view()),
        )

        # if self.url_prefix:
        #     return patterns(
        #         '', ('^' + self.url_prefix + "/", include(urls)))
        return urls

    def get_index_view(self):
        from . import views
        return views.PagesIndex.as_view()

