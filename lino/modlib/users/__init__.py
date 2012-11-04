## Copyright 2011-2012 Luc Saffre
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
:mod:`django.contrib.auth` module.

This module is much more simple and does not require
:mod:`django.contrib.sessions` to be installed.
See :doc:`/tickets/31` for discussion.

To use it, you must define the following things in your :class:`lino.Lino`::

    user_model = 'users.User'
    
    def get_installed_apps(self):
        for a in super(Lino,self).get_installed_apps():
            yield a
        yield 'lino.modlib.users'
        # continue with your own modules


"""

