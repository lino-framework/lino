#coding: utf8

## Copyright 2010 Luc Saffre
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

"""
Simulate HTTP authentication  when working with the development server 
(`manage.py runserver`). This middleware simply reads the REMOTE_USER 
environment variable (of the process running the development server) 
and inserts this to `request.META['REMOTE_USER']`.

To use this, insert it to your MIDDLEWARE_CLASSES somewhere before 
'django.contrib.auth.middleware.RemoteUserMiddleware'

    if sys.platform == 'win32':
        MIDDLEWARE_CLASSES = (
            'lino.utils.simulate_remote.SimulateRemoteUserMiddleware',
        ) + MIDDLEWARE_CLASSES 
        

"""


class SimulateRemoteUserMiddleware(object):
    def process_request(self, request):
        request.META['REMOTE_USER'] = os.environ.get('REMOTE_USER')

