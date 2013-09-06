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

import os

from django.conf import settings

class MediaFile(object):
    """
    Represents a file on the server with two properties `name` and `url`,
    using
    :setting:`MEDIA_ROOT`
    :attr:`use_davlink <lino.site.Site.use_davlink>`
    :attr:`webdav_root <lino.site.Site.webdav_root>`
    :attr:`webdav_url <lino.site.Site.webdav_url>`
    """
    def __init__(self,editable,*parts):
        self.editable = editable
        self.parts = parts
        
    @property
    def name(self):
        "return the filename on the server"
        if self.editable and settings.SITE.use_davlink:
            return os.path.join(settings.SITE.webdav_root,*self.parts)
        return os.path.join(settings.MEDIA_ROOT,*self.parts)
        
    @property
    def url(self):
        "return the url that points to file on the server"
        if self.editable and settings.SITE.use_davlink:
            return settings.SITE.webdav_url + "/".join(self.parts)
        return settings.SITE.build_media_url(*self.parts)

class TmpMediaFile(MediaFile):
    def __init__(self,ar,fmt):
        ip = ar.request.META.get('REMOTE_ADDR','unknown_ip')
        super(TmpMediaFile,self).__init__(False,'cache', 'appy'+fmt, ip, str(ar.actor) + '.' + fmt)


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

