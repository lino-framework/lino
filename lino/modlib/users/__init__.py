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

Lino's :mod:`lino.modlib.users` is an alternative to Django's 
:mod:`django.contrib.auth` module when there is already 
a central user management system (e.g. an LDAP server)
running on a site and authentication granted by the web server.

See :doc:`/tickets/31` for discussion.

This module is much more simple and does not require
:mod:`django.contrib.sessions` to be installed.

Here's how to install this in your :xfile:`settings.py`::

  INSTALLED_APPS = [
    #~ 'django.contrib.sessions',
    #~ 'django.contrib.auth',
    'lino.modlib.users',
    ...
  ]

  MIDDLEWARE_CLASSES = [
      'django.middleware.common.CommonMiddleware',
      #~ 'django.contrib.sessions.middleware.SessionMiddleware',
      #~ 'django.contrib.auth.middleware.AuthenticationMiddleware',
      'lino.modlib.users.middleware.RemoteUserMiddleware',
  ]
  
  AUTHENTICATION_BACKENDS = [
    #~ 'django.contrib.auth.backends.RemoteUserBackend',
  ]
  
(In practice you don't need to worry about these settings since your 
`local_settings.py` imports them, you don't even see them.)

"""

