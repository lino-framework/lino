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

import os
from lino import ad
import jinja2


class Plugin(ad.Plugin):

    media_name = 'davlink'

    def get_head_lines(self, site, request):
        if not site.use_java:
            return
        # jar = self.build_media_url('DavLink.jar')
        # jar = request.build_absolute_uri(jar)
        jnlp = site.build_media_url(*self.jnlp_file_parts())
        # jnlp = request.build_absolute_uri(jnlp)
        # yield '<applet code="davlink.DavLink"'
        yield '<applet name="DavLink" code="davlink.DavLink"'
        # yield '        archive="%s"' % jar
        yield '        width="1" height="1">'
        # yield '<param name="separate_jvm" value="true">' # 20130913
        # yield '<param name="permissions" value="all-permissions">'
        yield '<param name="jnlp_href" value="%s">' % jnlp
        yield '</applet>'

    def write_jnlp_file(self, f):
        context = dict(
            site=self.site,
        )
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(
            os.path.dirname(__file__)))
        tpl = env.get_template('template.jnlp')
        f.write(tpl.render(**context))

    def get_patterns(self, ui):
        from django.conf import settings
        fn = os.path.join(settings.MEDIA_ROOT, *self.jnlp_file_parts())
        ui.site.make_cache_file(fn, self.write_jnlp_file)
        return []

    def jnlp_file_parts(self):
        return ('cache', self.media_name + '.jnlp')
