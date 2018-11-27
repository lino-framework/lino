# -*- coding: UTF-8 -*-
# Copyright 2009-2016 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Adds the default Lino user interface based on ExtJS.

It is being automatically included by every Lino application unless
you disable it (e.g. by overriding your :meth:`get_apps_modifiers
<lino.core.site.Site.get_apps_modifiers>` or your
:meth:`get_installed_apps <lino.core.site.Site.get_installed_apps>`
method).

When your Lino application uses the ExtJS user interface, then you may
need a `commercial license from Sencha
<https://www.sencha.com/store/extjs/>`__. Summary without warranty of
correctness: you need a commercial license if (1) your application is
not available under the GPL **and** (2) your site is used by other
people than the empoyees of the company who is the copyright holder of
your application.


.. autosummary::
   :toctree:

   views
   ext_renderer

"""

from __future__ import unicode_literals
from __future__ import print_function

from lino.api.ad import Plugin
from django.utils.translation import ugettext_lazy as _

# raise Exception("20160528")


class Plugin(Plugin):
    """Extends :class:`lino.core.plugin.Plugin`.

    """

    needs_plugins = ['lino.modlib.bootstrap3']

    enter_submits_form = False
    """Whether the :kbd:`ENTER` key (or :kbd:`CTRL+ENTER` when in a
    textarea field) should submit the form.

    The default is `False`. For sites that were in production before
    October 2015, we recommend to explain to the users that a simple
    :kbd:`ENTER` no longer submits a form, and that :kbd:`Ctrl-S` is
    the preferred keyboard shortcut for submitting a
    form. Alternatively for backwards compatibility you can set it to
    `True` using something like this::

        def setup_plugins(self):
            super(Site, self).setup_plugins()
            if self.is_installed('extjs'):
                self.plugins.extjs.configure(enter_submits_form=False)


    When you set this to `True` :xfile:`linoweb.js` adds a special
    mapping for :kbd:`ENTER`. The problem then is that the
    :kbd:`ENTER` key won't work in a plain textarea field because we
    didn't find a way to restore the default behaviour.

    """
    ui_label = _("Admin")

    use_statusbar = False
    """
    Whether to use a status bar to display certain messages to the user.
    Default is `False` since currently this is not really useful.
    """

    url_prefix = "ext"

    media_name = 'ext-3.3.1'

    # media_base_url = "http://extjs-public.googlecode.com/" + \
    #                  "svn/tags/extjs-3.3.1/release/"
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

    autorefresh_seconds = 0
    # autorefresh_seconds = 60
    """Number of seconds to wait between two refreshes when autorefresh is
    activated. Default is 60. Set this to 0 in order to deactivate
    the autorefresh button.

    """

    media_root = None
    """
    Path to the ExtJS root directory.  Only used when
    :attr:`media_base_url` is None, and when the `media` directory has
    no symbolic link named `extjs` pointing to the ExtJS root
    directory.
    """

    ui_handle_attr_name = 'extjs_handle'

    def on_ui_init(self, kernel):
        # logger.info("20140227 extjs.Plugin.on_ui_init() a")
        from .ext_renderer import ExtRenderer
        self.renderer = ExtRenderer(self)
        kernel.extjs_renderer = self.renderer

        # added 20160329
        for fl in self.renderer.param_panels:
            fl.get_layout_handle(self)

        # logger.info("20140227 extjs.Plugin.on_ui_init() b")

    def get_row_edit_lines(self, e, panel):
        from lino.core.elems import (
            GridElement, HtmlBoxElement, FieldElement, form_field_name)
        from lino.core import constants
        master_field = panel.layout_handle.layout._datasource.master_field
        if isinstance(e, GridElement):
            yield "%s.on_master_changed();" % e.as_ext()
        elif isinstance(e, HtmlBoxElement):
            yield "%s.refresh();" % e.as_ext()
        elif isinstance(e, FieldElement):
            if not panel.layout_handle.layout.editable:
                return
            holder = panel.layout_handle.layout.get_chooser_holder()
            chooser = holder.get_chooser_for_field(e.field.name)
            if not chooser:
                return
            for f in chooser.context_fields:
                if master_field and master_field.name == f.name:
                    yield "var bp = this.get_base_params();"
                    yield "%s.setContextValue('%s',bp['%s']);" % (
                        e.as_ext(), constants.URL_PARAM_MASTER_PK,
                        constants.URL_PARAM_MASTER_PK)
                    yield "%s.setContextValue('%s',bp['%s']);" % (
                        e.as_ext(), constants.URL_PARAM_MASTER_TYPE,
                        constants.URL_PARAM_MASTER_TYPE)
                else:
                    yield (
                        "%s.setContextValue('%s', record ? record."
                        "data['%s'] : undefined);" % (
                            e.as_ext(), f.name, form_field_name(f)))

    def get_css_includes(self, site):
        yield self.build_lib_url('resources/css/ext-all.css')

    def get_js_includes(self, settings, language):
        return []

    def get_head_lines(self, site, request):
        yield "<style>"
        from lino.core.constants import ICON_NAMES
        tpl = ".x-tbar-{0}{{ background-image: url({1}) !important; }}"
        for n in ICON_NAMES:
            url = site.build_static_url('images', 'mjames', n + '.png')
            yield tpl.format(n, url)
            
        yield """
.x-tbar-done{ background-image: url(/static/images/mjames/accept.png) !important; }
.x-tbar-parameters{ background-image: url(/static/images/mjames/database_gear.png) !important; }
"""
        yield "</style>"

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

    def get_patterns(self):

        from django.conf import settings
        from django.conf.urls import url  # patterns
        from . import views

        self.renderer.build_site_cache()

        rx = '^'

        urlpatterns = [
            # url(rx + '/?$', views.AdminIndex.as_view()),
            url(rx + '$', views.AdminIndex.as_view()),
            url(rx + r'api/main_html$', views.MainHtml.as_view()),
            # url(rx + r'auth$', views.Authenticate.as_view()),
            url(rx + r'grid_config/(?P<app_label>\w+)/(?P<actor>\w+)$',
                views.GridConfig.as_view()),
            url(rx + r'api/(?P<app_label>\w+)/(?P<actor>\w+)$',
                views.ApiList.as_view()),
            url(rx + r'api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$',
                views.ApiElement.as_view()),
            url(rx + r'restful/(?P<app_label>\w+)/(?P<actor>\w+)$',
                views.Restful.as_view()),
            url(rx + r'restful/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$',
                views.Restful.as_view()),
            url(rx + r'choices/(?P<app_label>\w+)/(?P<rptname>\w+)$',
                views.Choices.as_view()),
            url(rx + r'choices/(?P<app_label>\w+)/(?P<rptname>\w+)/'
                '(?P<fldname>\w+)$',
                views.Choices.as_view()),
            url(rx + r'apchoices/(?P<app_label>\w+)/(?P<actor>\w+)/'
                '(?P<an>\w+)/(?P<field>\w+)$',
                views.ActionParamChoices.as_view()),
            # the thread_id can be a negative number:
            url(rx + r'callbacks/(?P<thread_id>[\-0-9a-zA-Z]+)/'
                '(?P<button_id>\w+)$',
                views.Callbacks.as_view())
        ]
        if settings.SITE.use_eid_applet:
            urlpatterns.append(
                url(rx + r'eid-applet-service$',
                    views.EidAppletService.as_view()))
        if settings.SITE.use_jasmine:
            urlpatterns.append(
                url(rx + r'run-jasmine$', views.RunJasmine.as_view()))
        return urlpatterns
        
