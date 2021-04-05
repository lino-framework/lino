# -*- coding: UTF-8 -*-
# Copyright 2015-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""See ;doc:`/specs/tinymce`.

"""

from lino.api import ad


#TINYMCE_VERSION = '3.4.8'
#TINYMCE_VERSION = '4.1.10'
TINYMCE_VERSION = '3.5.11'

"""Which version of TinyMCE to use.

With 4.1.10, windows containing a TextField don't open, and the JS
console says "TypeError: sp is undefined". That's because we did not
yet get Andrew Mayorov's
:srcref:`lino/modlib/tinymce/static/byteforce/Ext.ux.TinyMCE.js` to
work with TinyMCE 4.  It seems that either ControlManager or
WindowManager no longer are functions in tinymce4.

"""


def javascript(url):
    return '<script type="text/javascript" src="{0}"></script>'.format(url)


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    needs_plugins = ['lino.modlib.office']
    # needs_plugins = ['lino.modlib.office', 'lino.modlib.extjs']

    site_js_snippets = ['tinymce/tinymce.js']

    url_prefix = 'tinymce'

    # window_width = 600
    # window_height = 500

    document_domain = None
    """The domain name of this production site."""

    window_width = 500
    """The initial width of the window to use when editing in own
    window.

    """

    window_height = 400
    """The initial height of the window to use when editing in own
    window.

    """

    field_buttons = (
        "bold,italic,underline,|,justifyleft,justifycenter,justifyright,|,"
        "bullist,numlist,|,outdent,indent,|,undo,redo,|,removeformat,template")
    """The toolbar buttons when editing a field inside a detail form."""

    window_buttons1 = (
        "save,cancel,|,bold,italic,underline,|,justifyleft,justifycenter,"
        "justifyright,fontselect,fontsizeselect,formatselect,|,"
        "search,replace")
    """The first row of toolbar buttons when editing in own window."""
    window_buttons2 = (
        "cut,copy,paste,template,|,bullist,numlist,|,outdent,indent,|,"
        "undo,redo,|,link,unlink,anchor,image,|,code,preview,|,forecolor,"
        "backcolor")
    """The second row of toolbar buttons when editing in own window."""

    window_buttons3 = (
        "insertdate,inserttime,|,spellchecker,advhr,,removeformat,|,"
        "sub,sup,|,charmap,emotions,|,tablecontrols")
    """The third row of toolbar buttons when editing in own window."""

    media_name = 'tinymce-' + TINYMCE_VERSION
    """Lino currently includes three versions of TinyMCE, but for
    production sites we still use the eldest version 3.4.8.

    """

    media_root = None
    # media_base_url = "http://www.tinymce.com/js/tinymce/jscripts/tiny_mce/"
    # media_base_url = "http:////tinymce.cachefly.net/4.1/tinymce.min.js"

    def get_used_libs(self, html=False):
        if html is not None:
            yield ("TinyMCE", TINYMCE_VERSION, "http://www.tinymce.com/")
            yield ("Ext.ux.TinyMCE", '0.8.4', "http://www.byte-force.com")

    def get_js_includes(self, settings, language):
        if settings.SITE.kernel.default_renderer.extjs_version:
            if TINYMCE_VERSION.startswith('3'):
                yield self.build_lib_url('tiny_mce.js')
            else:
                yield self.build_lib_url('tinymce.min.js')
            yield settings.SITE.build_static_url("byteforce", "Ext.ux.TinyMCE.js")

    def get_patterns(self):
        from django.urls import re_path as url
        # from django.conf.urls import url
        from . import views

        rx = '^'

        urlpatterns = [
            url(rx + r'templates/(?P<app_label>\w+)/'
                + r'(?P<actor>\w+)/(?P<pk>\w+)/(?P<fldname>\w+)$',
                views.Templates.as_view()),
            url(rx + r'templates/(?P<app_label>\w+)/'
                + r'(?P<actor>\w+)/(?P<pk>\w+)/(?P<fldname>\w+)/'
                + r'(?P<tplname>\w+)$',
                views.Templates.as_view())]

        return urlpatterns

    def get_row_edit_lines(self, e, panel):
        from lino.core.elems import TextFieldElement
        if isinstance(e, TextFieldElement):
            if e.format == 'html':
                yield "%s.refresh();" % e.as_ext()

    def setup_config_menu(self, site, user_type, m):
        if site.user_model is not None:
            mg = site.plugins.office
            m = m.add_menu(mg.app_label, mg.verbose_name)
            m.add_action('tinymce.MyTextFieldTemplates')

    def setup_explorer_menu(self, site, user_type, m):
        if site.user_model is not None:
            mg = site.plugins.office
            m = m.add_menu(mg.app_label, mg.verbose_name)
            m.add_action('tinymce.TextFieldTemplates')
