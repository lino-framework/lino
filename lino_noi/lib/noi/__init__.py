# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
#
# This file is part of Lino Noi.
#
# Lino Noi is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Noi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Noi.  If not, see
# <http://www.gnu.org/licenses/>.

"""
The main plugin for Lino Noi.

.. autosummary::
   :toctree:

    models
   fixtures.linotickets

"""

from lino.api.ad import Plugin


class Plugin(Plugin):

    ui_handle_attr_name = 'noi'

    url_prefix = 'noi'

    def on_ui_init(self, ui):
        from .renderer import Renderer
        self.renderer = Renderer(self)

    def get_patterns(self):
        from django.conf.urls import url  # , include
        from . import views

        Ticket = self.site.modules.tickets.Ticket
        urlpatterns = [
            url(r'^$',
                views.Index.as_view(),
                name='index'),
            url(r'^ticket/(?P<pk>[0-9]+)/$',
                views.Detail.as_view(model=Ticket)),
            # url('', include('lino.core.urls'))
        ]

        return urlpatterns

    def get_used_libs(self, html=False):
        if html is not None:
            yield ("Bootstrap", '3.3.4', "http://getbootstrap.com")
            # yield ("jQuery", '?', "http://...")

    def get_index_view(self):
        from . import views
        return views.Index.as_view()

