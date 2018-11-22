# -*- coding: UTF-8 -*-
## Copyright 2014-2015 Rumma & Ko Ltd

"""
Adds usage of the `AwesomeUploader
<http://jsjoy.com/blog/ext-js-extension-awesome-uploader>`_ by Andrew
Rymarczyk, hosted at
<https://code.google.com/p/awesomeuploader/source/checkout>.

Example configuration in a :xfile:`settings.py` file or
a :xfile:`lino_local.py` file::

    ad.configure_plugin(
        'awesomeuploader',
        maxFileSizeBytes=3145728
    )


.. setting:: awesomeuploader.maxFileSizeBytes

Maximum file size in bytes



"""

from lino import ad


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = "Awesome Uploader"

    uploader_root = '/awesomeuploader/'

    site_js_snippets = ['awesomeuploader/snippet.js']
    # media_base_url = "http://ext.ensible.com/deploy/1.0.2/"
    media_name = 'awesomeuploader'

    def get_used_libs(self, html=None):
        if html:
            onclick = "alert('Cannot yet detect version ');"
            tip = "Click to see Awesomeuploader version"
            text = "(version)"
            version = html.a(text, href='#', onclick=onclick, title=tip)
            yield (self.verbose_name, version,
                   "http://jsjoy.com/blog/ext-js-extension-awesome-uploader")

    def get_css_includes(self, site):
        yield self.build_media_url('AwesomeUploader.css')

    def get_js_includes(self, settings, language):
        yield self.build_media_url('Ext.ux.form.FileUploadField.js')
        yield self.build_media_url('Ext.ux.XHRUpload.js')
        yield self.build_media_url('swfupload.js')
        yield self.build_media_url('swfupload.swfobjectjs')
        yield self.build_media_url('AwesomeUploader.js')

    def setup_main_menu(config, site, user_type, m):
        mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('awesomeuploader.UploaderPanel')


