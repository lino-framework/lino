# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds usage of the TinyMCE editor
instead of Ext.form.HtmlEditor
for RichTextFields.
See also :attr:`tinymce_root`.
See `/blog/2011/0523`.
(formerly `use_tinymce`).

"""

from lino.api import ad


def javascript(url):
    return '<script type="text/javascript" src="{0}"></script>'.format(url)


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    needs_plugins = ['lino.modlib.office']  # because of TextFieldTemplate

    site_js_snippets = ['tinymce/tinymce.js']

    url_prefix = 'tiny'

    media_name = 'tinymce'

    media_root = None
    """Path to the tinymce root directory.  Only to be used on a
    development server if the `media` directory has no symbolic link
    to the TinyMCE root directory, and only if :attr:`use_tinymce` is
    True.

    """

    media_base_url = "http://www.tinymce.com/js/tinymce/jscripts/tiny_mce/"

    def get_used_libs(self, html=False):
        if html is not None:
            yield ("TinyMCE", '?', "http://www.tinymce.com/")

    def get_js_includes(self, settings, language):
        yield self.build_media_url('tiny_mce.js')
        yield settings.SITE.build_media_url(
            "lino", "tinymce", "Ext.ux.TinyMCE.js")

    def get_head_lines(self, site, request):
        # yield javascript(site.build_media_url("tinymce", "tiny_mce.js"))
        # yield javascript(site.build_media_url(
        #     "lino", "tinymce", "Ext.ux.TinyMCE.js"))
        yield """
<script language="javascript" type="text/javascript">
    tinymce.init({
            theme : "advanced"
            // , mode : "textareas"
    });
</script>"""

    def get_patterns(self, kernel):
        from django.conf.urls import patterns
        from . import views

        urlpatterns = patterns(
            '',
            (r'^templates/(?P<app_label>\w+)/'
             + r'(?P<actor>\w+)/(?P<pk>\w+)/(?P<fldname>\w+)$',
             views.Templates.as_view()),
            (r'^templates/(?P<app_label>\w+)/'
             + r'(?P<actor>\w+)/(?P<pk>\w+)/(?P<fldname>\w+)/'
             + r'(?P<tplname>\w+)$',
             views.Templates.as_view()))

        return urlpatterns

    def get_row_edit_lines(self, e, panel):
        from lino.modlib.extjs.elems import TextFieldElement
        if isinstance(e, TextFieldElement):
            if e.format == 'html':
                yield "%s.refresh();" % e.as_ext()

    def setup_config_menu(self, site, profile, m):
        if site.user_model is not None:
            mg = site.plugins.office
            m = m.add_menu(mg.app_label, mg.verbose_name)
            m.add_action('tinymce.MyTextFieldTemplates')

    def setup_explorer_menu(self, site, profile, m):
        if site.user_model is not None:
            mg = site.plugins.office
            m = m.add_menu(mg.app_label, mg.verbose_name)
            m.add_action('tinymce.TextFieldTemplates')


