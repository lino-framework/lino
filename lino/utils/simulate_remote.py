# -*- coding: UTF-8 -*-
## Copyright 2010-2011 Luc Saffre
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
Simulate HTTP authentication  when working with the development server 
(`manage.py runserver`). This middleware simply reads the :envvar:`REMOTE_USER` 
environment variable (of the process running the development server) 
and inserts this to every request's `META['REMOTE_USER']`.

To use this, insert it to your MIDDLEWARE_CLASSES somewhere before 
'django.contrib.auth.middleware.RemoteUserMiddleware'::

    from lino.demos.std.settings import *
    MIDDLEWARE_CLASSES = (
        'lino.utils.simulate_remote.SimulateRemoteUserMiddleware',
    ) + MIDDLEWARE_CLASSES 
        
Be careful to not inadvertently include this to your :setting:`MIDDLEWARE_CLASSES` 
on a production server since it will override the HTTP authentication.

See also http://docs.djangoproject.com/en/dev/howto/auth-remote-user/


"""

import os


class SimulateRemoteUserMiddleware(object):
    def process_request(self, request):
        #~ x = os.environ.get('REMOTE_USER')
        x = os.environ.get('REMOTE_USER','root')
        request.META['REMOTE_USER'] = x
        #~ if x:
            #~ request.META['REMOTE_USER'] = x
            #~ print "WARNING: Treating all requests as coming from authenticated user %s" % x

