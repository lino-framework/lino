# -*- coding: UTF-8 -*-
# Copyright 2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
A user interface for Lino applications that uses `OpenUI5
<http://openui5.org>`__.

Started in January 2018 as an alternative to :mod:`lino.modlib.extjs`.
Not finished.

.. autosummary::
   :toctree:

    views
    renderer
    models
"""

from lino.api.ad import Plugin


class Plugin(Plugin):
    # ui_label = _("Bootstrap")
    ui_handle_attr_name = 'openui5_handle'

    # site_js_snippets = ['snippets/plain.js']

    needs_plugins = ['lino.modlib.jinja']

    url_prefix = 'ui5'

    media_name = 'openui5'

    # media_root = None
    # media_base_url = "http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/"

    def on_ui_init(self, kernel):
        from .renderer import Renderer
        self.renderer = Renderer(self)
        # ui.bs3_renderer = self.renderer
        kernel.extjs_renderer = self.renderer

    def get_patterns(self):
        from django.conf.urls import url
        from . import views

        rx = '^'

        urls = [
            url(rx + r'$', views.App.as_view()),

            url(rx + r'auth$', views.Authenticate.as_view()),

            url(rx + r'api/main_html$', views.MainHtml.as_view()),

            # To be fased out
            url(rx + r'restful/(?P<app_label>\w+)/(?P<actor>\w+)$',
                views.ApiList.as_view()),
            url(rx + r'restful/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$',
                views.ApiElement.as_view()),
            # From extjs
            url(rx + r'api/(?P<app_label>\w+)/(?P<actor>\w+)$',
                views.ApiList.as_view()),
            url(rx + r'api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$',
                views.ApiElement.as_view()),
            url(rx + r'choices/(?P<app_label>\w+)/(?P<rptname>\w+)$',
                views.Choices.as_view()),
            url(rx + r'choices/(?P<app_label>\w+)/(?P<rptname>\w+)/'
                     '(?P<fldname>\w+)$',
                views.Choices.as_view()),

            # For generating views
            url(rx + r'ui/(?P<name>.*)$',
                views.Connector.as_view()),
            url(rx + r'callbacks/(?P<thread_id>[\-0-9a-zA-Z]+)/'
                     '(?P<button_id>\w+)$',
                views.Callbacks.as_view()),

        ]
        return urls

    def get_used_libs(self, html=False):
        if html is not None:
            yield ("Openui5", '1.50.8', "http://openui5.org")
            # yield ("jQuery", '?', "http://...")
            yield ("CKEditor", "4.8", "https://ckeditor.com/")

    # def get_index_view(self):
    #     from . import views
    #     return views.App.as_view()
