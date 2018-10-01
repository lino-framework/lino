# -*- coding: UTF-8 -*-
# Copyright 2013-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Defines the :class:`MediaFile` class.
"""
from builtins import str
from builtins import object

from os.path import join

from django.conf import settings
from lino.core.utils import is_devserver

# davlink = settings.SITE.plugins.get('davlink', None)
# has_davlink = davlink is not None and settings.SITE.use_java
has_davlink = False


class MediaFile(object):
    """
    Represents a file on the server below :setting:`MEDIA_ROOT` with
    two properties :attr:`name` and :attr:`url`.
   
    It also takes into consideration the settings
    :attr:`webdav_root <lino.core.site.Site.webdav_root>`
    :attr:`webdav_protocol <lino.core.site.Site.webdav_protocol>`
    and
    :attr:`webdav_url <lino.core.site.Site.webdav_url>`
    """

    def __init__(self, editable, *parts):
        self.editable = editable
        self.parts = parts

    @property
    def name(self):
        "return the filename on the server"
        if self.editable and (has_davlink or settings.SITE.webdav_protocol):
            return join(settings.SITE.webdav_root, *self.parts)
        return join(settings.MEDIA_ROOT, *self.parts)

    def get_url(self, request):
        "return the url that points to file on the server"
        if self.editable and request is not None:
            if is_devserver():
                url = "file://" + join(
                    settings.SITE.webdav_root, *self.parts)
            else:
                url = settings.SITE.webdav_url + "/".join(self.parts)
                url = request.build_absolute_uri(url)
            if settings.SITE.webdav_protocol:
                url = settings.SITE.webdav_protocol + "://" + url
            return url
            
        return settings.SITE.build_media_url(*self.parts)


class TmpMediaFile(MediaFile):

    def __init__(self, ar, fmt):
        ip = ar.request.META.get('REMOTE_ADDR', 'unknown_ip')
        super(TmpMediaFile, self).__init__(
            False, 'cache', 'appy' + fmt, ip, str(ar.actor) + '.' + fmt)


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
