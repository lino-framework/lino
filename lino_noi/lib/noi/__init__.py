# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The main plugin for Lino Noi.

.. autosummary::
   :toctree:

    models
    roles

"""

from lino.api.ad import Plugin


class Plugin(Plugin):

    ui_handle_attr_name = 'noi'

    url_prefix = 'noi'

    def on_ui_init(self, ui):
        from .renderer import Renderer
        self.renderer = Renderer(self)

    def get_patterns(self):
        from django.conf.urls import url, include
        from . import views

        Ticket = self.site.modules.tickets.Ticket
        urlpatterns = [
            url(r'^$',
                views.Index.as_view(),
                name='index'),
            url(r'^ticket/(?P<pk>[0-9]+)/$',
                views.Detail.as_view(model=Ticket)),
            url('', include('lino.core.urls'))
        ]

        return urlpatterns

    def get_used_libs(self, html=False):
        if html is not None:
            yield ("Bootstrap", '3.3.4', "http://getbootstrap.com")
            # yield ("jQuery", '?', "http://...")

    def get_index_view(self):
        from . import views
        return views.Index.as_view()

