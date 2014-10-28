# -*- coding: UTF-8 -*-
# Copyright 2012-2013 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.ad import Plugin
from django.utils.translation import ugettext_lazy as _


class Plugin(Plugin):

    ui_label = _("Pages")

    verbose_name = _("Pages")

    url_prefix = 'p'

    media_name = 'pages'

    def __init__(self, *args, **kw):
        super(Plugin, self).__init__(*args, **kw)
        from lino.modlib.bootstrap3.renderer import Renderer
        self.renderer = Renderer(self)

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

