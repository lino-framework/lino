# -*- coding: UTF-8 -*-
# Copyright 2020-2021 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.api.ad import Plugin

from lino.core.dashboard import DashboardItem

class PublisherDashboardItem(DashboardItem):

    def __init__(self, model, **kwargs):
        self.model = model
        super(PublisherDashboardItem, self).__init__(str(model), **kwargs)

    def render(self, ar, **kwargs):
        return self.model.render_dashboard_items(ar, **kwargs)

class Plugin(Plugin):

    needs_plugins = ["lino.modlib.jinja"]

    # ui_handle_attr_name = "publisher"

    def get_patterns(self):
        from django.conf.urls import url
        from lino.core.utils import models_by_base
        from . import views
        from .mixins import Publishable

        for m in models_by_base(Publishable):
            if m.publisher_location is not None:
                yield url('^{}/(?P<pk>.+)$'.format(m.publisher_location),
                    views.Element.as_view(publisher_model=m))
                yield url('^{}/$'.format(m.publisher_location),
                    views.Element.as_view(publisher_model=m))
        # yield url('^$',views.Index.as_view())
        # yield url('^login$',views.Login.as_view())

    def get_dashboard_items(self, user):
        # print("20210112 get_dashboard_items")
        from lino.core.utils import models_by_base
        from .mixins import Publishable
        for m in models_by_base(Publishable):
            # print("20210112 ", m, m.publisher_location)
            yield PublisherDashboardItem(m)
