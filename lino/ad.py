# Copyright 2013 Luc Saffre
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

"""
Example::

    from lino import ad
    
    class Plugin(ad.Plugin):
        extends = 'lino.modlib.cal'
        depends = ['lino.modlib.contacts']
    
"""
from os.path import exists
from urllib import urlencode

from djangosite import Plugin as BasePlugin


class Plugin(BasePlugin):

    "Lino extension to `djangosite.Plugin`"

    ui_label = None

    media_base_url = None
    """
    Remote URL base for media files.
    """

    media_root = None
    """Local path where third-party media files are installed.

    Only used if this app has :attr:`media_base_url` empty and
    :attr:`media_name` non-empty, *and* if the :xfile:`media`
    directory has no entry named :attr:`media_name`.

    """

    media_name = None
    """Either `None` (default) or a non-empty string with the name of the
    subdirectory of your :xfile:`media` directory which is expected to
    contain media files for this app.

    `None` means that there this app has no media files of her own.
    Best practice is to set this to the `app_label`.  Will be ignored
    if :setting:`media_base_url` is nonempty.

    """

    url_prefix = None
    """
    The url prefix under which this app should ask to
    install its url patterns.
    """

    site_js_snippets = []
    """
    List of js snippets to be injected into the `lino_*.js` file.
    """

    def before_analyze(self, site):
        """This is called when the kernel is being instantiated.
        """
        pass

    def on_ui_init(cls, kernel):
        """This is called when the kernel is being instantiated.
        """
        pass

    def get_patterns(self, ui):
        """Return a list of url patterns to be added to the Site's patterns.

        """
        return []

    def get_css_includes(self, site):
        return []

    def get_js_includes(self, settings, language):
        return []

    def get_head_lines(cls, site, request):
        return []

    def build_media_url(self, *parts, **kw):
        if self.media_base_url:
            url = self.media_base_url + '/'.join(parts)
            if len(kw):
                url += "?" + urlencode(kw)
            return url
        return self.buildurl('media', self.media_name, *parts, **kw)

    def build_plain_url(self, *args, **kw):
        if self.url_prefix:
            return self.buildurl(self.url_prefix, *args, **kw)
        return self.buildurl(*args, **kw)

    def buildurl(self, *args, **kw):
        url = self.site.site_prefix + ("/".join(args))
        if len(kw):
            url += "?" + urlencode(kw)
        return url

    def setup_media_links(self, ui, urlpatterns):
        if self.media_name is None:
            return

        if self.media_base_url:
            return

        source = self.media_root
        if not source:
            # raise Exception("%s.media_root is not set." % self)
            return

        if not exists(source):
            raise Exception(
                "Directory %s (specified in %s.media_root) does not exist" %
                (source, self))
        ui.setup_media_link(
            urlpatterns,
            self.media_name, source=source)


