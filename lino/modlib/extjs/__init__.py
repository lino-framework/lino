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

"""This is the :mod:`lino.modlib.extjs` app for Lino.  It is being
automatically included by every Lino application unless you specify
``extjs`` in :setting:`hidden_apps` (or override your
:setting:`get_installed_apps` method).

When your Lino application uses the ExtJS user interface, then you may
need a commercial license from Sencha if your site is (1) your
application is not available under the GPL **and** (2) used by other
people than the empoyees of the company who wrote the application. See
:doc:`/about/proprietary` for details.

"""

from lino.ad import Plugin
from django.utils.translation import ugettext_lazy as _


class Plugin(Plugin):

    ui_label = _("Admin")

    url_prefix = "admin"

    media_name = 'extjs'

    media_base_url = "http://extjs-public.googlecode.com/" + \
                     "svn/tags/extjs-3.3.1/release/"

    media_root = None
    """Path to the ExtJS root directory.  Only used when
    :attr:`media_base_url` is None, and when the `media` directory has
    no symbolic link named `extjs` pointing to the ExtJS root
    directory.

    """


    """The URL from where to include the ExtJS library files.
    
    The default value points to the `extjs-public
    <http://code.google.com/p/extjs-public/>`_ repository and thus
    requires the clients to have an internet connection.  This
    relieves newcomers from the burden of having to specify a download
    location in their :xfile:`settings.py`.
    
    On a production site you'll probably want to download and serve
    these files yourself by setting this to `None` and setting
    :attr:`extjs_root` (or a symbolic link "extjs" in your
    :xfile:`media` directory) to point to the local directory where
    ExtJS 3.3.1 is installed).

    """

    def on_ui_init(self, ui):
        from .ext_renderer import ExtRenderer
        self.renderer = ExtRenderer(self)
        ui.extjs_renderer = self.renderer
        # ui.extjs_renderer = ui.default_renderer = self.renderer

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

        #~ print "20121110 get_urls"
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
