# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

from lino import ad

"""
"""

from os.path import join, dirname, exists

class App(ad.App):

    media_base_url = "http://ext.ensible.com/deploy/1.0.2/"
    media_name = 'extensible'

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
