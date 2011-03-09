## Copyright 2011 Luc Saffre
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

"""
Middleware to be used on sites with :doc:`/topics/http_auth`.
"""

from lino.modlib.auth.models import User
from lino.utils import dblogger

class RemoteUserMiddleware(object):
    """
    
    This does the same as
    :class:`django.contrib.auth.middleware.RemoteUserMiddleware`, 
    but in a simplified manner without using Sessions.
    
    The header used is configurable and defaults to ``REMOTE_USER``.  Subclass
    this class and change the ``header`` attribute if you need to use a
    different header.
    

    """

    # Name of request header to grab username from.  This will be the key as
    # used in the request.META dictionary, i.e. the normalization of headers to
    # all uppercase and the addition of "HTTP_" prefix apply.
    header = "REMOTE_USER"

    def process_request(self, request):
        try:
            username = request.META[self.header]
        except KeyError:
            request.user = None
            # If specified header doesn't exist, set `user` to None
            return
        try:
            request.user = User.objects.get(username=username)
        except User.DoesNotExist,e:
            u = User(username=username)
            u.full_clean()
            u.save()
            dblogger.info("Creating new user %s from request %s",u,request)
            request.user = u

