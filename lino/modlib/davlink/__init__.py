# -*- coding: UTF-8 -*-
# Copyright 2014-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Deprecated.  Use :attr:`lino.core.site.Site.webdav_protocol`
instead.  Adds actions for editing printable documents on a server
with :doc:`/admin/webdav`.

When this plugin is installed, you can still easily disable it by
setting :attr:`use_java <lino.core.site.Site.use_java>` to `False` in
your :xfile:`settings.py`.

.. obsolete: When this plugin is enabled, then you must also add the `.jar` files
   required by :ref:`davlink` into your media directory, in a
   subdirectory named "davlink".  TODO: move :ref:`davlink` to a `static`
   directory in the Lino repository.
"""

import os
from lino.api import ad
import jinja2


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    site_js_snippets = ['davlink/davlink.js']

    media_name = 'davlink'

    def get_body_lines(self, site, request):
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
            davlink=self,
        )
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(
            os.path.dirname(__file__)))
        tpl = env.get_template('template.jnlp')
        f.write(tpl.render(**context))

    def on_ui_init(self, kernel):
        fn = os.path.join(*self.jnlp_file_parts())
        kernel.make_cache_file(fn, self.write_jnlp_file)

    def jnlp_file_parts(self):
        return ('cache', self.media_name + '.jnlp')
    
    def setup_quicklinks(self, user, tb):
        if self.site.use_java:
            tb.add_action('davlink.Toolbar', 'reset_davlink')

