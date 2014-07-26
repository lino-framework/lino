# -*- coding: UTF-8 -*-
## Copyright 2014 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
## You should have received a copy of the GNU Lesser General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
Adds usage of the `AwesomeUploader
<http://jsjoy.com/blog/ext-js-extension-awesome-uploader>`_ by Andrew
Rymarczyk, hosted at
<https://code.google.com/p/awesomeuploader/source/checkout>.

Example configuration in a :xfile:`settings.py` file or
a :ref:`djangosite_local` module::

    ad.configure_plugin(
        'awesomeuploader',
        maxFileSizeBytes=3145728
)


.. setting:: awesomeuploader.maxFileSizeBytes

Maximum file size in bytes



"""

from lino import ad


class Plugin(ad.Plugin):

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
