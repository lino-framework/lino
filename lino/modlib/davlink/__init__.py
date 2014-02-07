# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
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

"""Add this to your :setting:`get_installed_apps` if your Site should
feature actions that ask the client to launch webdav office documents.

When this app is installed, then you must also add the `.jar` files
required by :ref:`davlink` into your media directory, in a
subdirectory named "davlink".

"""

from lino import ad


class Plugin(ad.Plugin):  # was: use_davlink

    # site_js_snippets = ['plugins/eidreader.js']
    media_name = 'davlink'

    def get_head_lines(self, site, request):
        if not site.use_java:
            return
        p = self.build_media_url('DavLink.jar')
        # p = self.build_media_url('davlink.jnlp')
        p = request.build_absolute_uri(p)
        yield '<applet name="DavLink" code="davlink.DavLink.class"'
        yield '        archive="%s"' % p
        yield '        width="0" height="0">'
        # yield '<param name="separate_jvm" value="true">' # 20130913
        # yield '<param name="permissions" value="all-permissions">'
        # yield '<param name="jnlp_href" value="%s">' % p
        yield '</applet>'


