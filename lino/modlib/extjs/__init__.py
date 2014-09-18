# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"See :mod:`ml.extjs`."

from __future__ import unicode_literals
from __future__ import print_function

from lino.ad import Plugin
from django.utils.translation import ugettext_lazy as _


class Plugin(Plugin):

    ui_label = _("Admin")

    use_statusbar = False

    url_prefix = "admin"

    media_name = 'extjs'

    media_base_url = "http://extjs-public.googlecode.com/" + \
                     "svn/tags/extjs-3.3.1/release/"

    media_root = None

    def on_ui_init(self, kernel):
        # logger.info("20140227 extjs.Plugin.on_ui_init() a")
        # raise Exception(20140227)
        from .ext_renderer import ExtRenderer
        self.renderer = ExtRenderer(self)
        kernel.extjs_renderer = self.renderer
        # ui.extjs_renderer = ui.default_renderer = self.renderer
        # logger.info("20140227 extjs.Plugin.on_ui_init() b")

    def get_css_includes(self, site):
        yield self.build_media_url('resources/css/ext-all.css')

    def get_js_includes(self, settings, language):
        return []

    def get_head_lines(cls, site, request):
        return []

    def get_used_libs(self, html=False):
        if html is not None:
            # version = '<script type="text/javascript">\
            #    document.write(Ext.version);</script>'
            onclick = "alert('ExtJS client version is ' + Ext.version);"
            tip = "Click to see ExtJS client version"
            text = "(version)"
            version = html.a(text, href='#', onclick=onclick, title=tip)
            yield ("ExtJS", version, "http://www.sencha.com")

            yield ("Silk Icons", '1.3',
                   "http://www.famfamfam.com/lab/icons/silk/")

    def get_index_view(self):
        from . import views
        return views.AdminIndex.as_view()

    def get_patterns(self, ui):
        # from django.conf.urls import patterns, include
        urls = self.get_ext_urls(ui)
        # if self.url_prefix:
        #     return patterns(
        #         '', ('^' + self.url_prefix+"/", include(urls)))
        return urls

    def get_ext_urls(self, ui):

        from django.conf.urls import patterns
        from . import views
        from lino.utils import codetime

        ui.code_mtime = codetime()

        #~ print("20121110 get_urls")
        ui.extjs_renderer.build_site_cache()

        rx = '^'
        urlpatterns = patterns(
            '',
            (rx + '/?$', views.AdminIndex.as_view()),
            (rx + r'api/main_html$',
             views.MainHtml.as_view()),
            (rx + r'auth$', views.Authenticate.as_view()),
            (rx + r'grid_config/(?P<app_label>\w+)/(?P<actor>\w+)$',
             views.GridConfig.as_view()),
            (rx + r'api/(?P<app_label>\w+)/(?P<actor>\w+)$',
             views.ApiList.as_view()),
            (rx + r'api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$',
             views.ApiElement.as_view()),
            (rx + r'restful/(?P<app_label>\w+)/(?P<actor>\w+)$',
             views.Restful.as_view()),
            (rx + r'restful/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$',
             views.Restful.as_view()),
            (rx + r'choices/(?P<app_label>\w+)/(?P<rptname>\w+)$',
             views.Choices.as_view()),
            (rx + r'choices/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<fldname>\w+)$',
             views.Choices.as_view()),
            (rx + r'apchoices/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<an>\w+)/(?P<field>\w+)$',
             views.ActionParamChoices.as_view()),
            # the thread_id can be a negative number:
            (rx + r'callbacks/(?P<thread_id>[\-0-9a-zA-Z]+)/(?P<button_id>\w+)$',
             views.Callbacks.as_view()),
        )
        if ui.site.use_eid_applet:
            urlpatterns += patterns('',
                                    (rx + r'eid-applet-service$',
                                     views.EidAppletService.as_view()),
                                    )
        if ui.site.use_jasmine:
            urlpatterns += patterns('',
                                    (rx + r'run-jasmine$',
                                     views.RunJasmine.as_view()),
                                    )
        if ui.site.user_model and self.site.use_tinymce:
            urlpatterns += patterns(
                '',
                (rx + r'templates/(?P<app_label>\w+)/'
                 + r'(?P<actor>\w+)/(?P<pk>\w+)/(?P<fldname>\w+)$',
                 views.Templates.as_view()),
                (rx + r'templates/(?P<app_label>\w+)/'
                 + r'(?P<actor>\w+)/(?P<pk>\w+)/(?P<fldname>\w+)/'
                 + r'(?P<tplname>\w+)$',
                 views.Templates.as_view()),
            )

        return urlpatterns
