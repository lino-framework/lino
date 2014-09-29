# -*- coding: UTF-8 -*-
## Copyright 2013-2014 Luc Saffre
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
See :mod:`ml.extensible`.

"""

from lino import ad

from os.path import join, dirname, exists


class Plugin(ad.Plugin):

    verbose_name = "Ext.ensible adapter"

    calendar_start_hour = 8  # setting
    calendar_end_hour = 18  # setting

    site_js_snippets = ['snippets/extensible.js']
    media_base_url = "http://ext.ensible.com/deploy/1.0.2/"
    media_name = 'extensible'

    def get_used_libs(self, html=None):
        if html:
            onclick = "alert('Extensible Calendar version is ' \
            + Ext.ensible.version);"
            tip = "Click to see Extensible Calendar version"
            text = "(version)"
            version = html.a(text, href='#', onclick=onclick, title=tip)
            yield (self.verbose_name, version,
                   "http://ext.ensible.com/products/calendar/")

    def get_css_includes(self, site):
        yield self.build_media_url('resources/css/extensible-all.css')

    def get_js_includes(self, settings, language):
        if settings.DEBUG:
            yield self.build_media_url('extensible-all-debug.js')
        else:
            yield self.build_media_url('extensible-all.js')
        if language != 'en':
            yield self.build_media_url(
                'src', 'locale',
                'extensible-lang-' + language + '.js')
