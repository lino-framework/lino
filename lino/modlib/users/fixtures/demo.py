# -*- coding: UTF-8 -*-
## Copyright 2010-2012 Luc Saffre
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

import datetime
from django.conf import settings
#~ from lino.tools import resolve_model
from lino.utils.instantiator import Instantiator
#from lino import reports
#contacts = reports.get_app('contacts')

from lino.utils.perms import UserProfiles

def objects():
    def create_user(*args,**kw):
        user = Instantiator('users.User',
          'username email first_name last_name'
          ).build
        u = user(*args,**kw)
        #~ u.set_password('1234')
        return u
    #~ kw = dict()
    #~ for f in settings.LINO.user_profile_fields:
        #~ kw[f] = UserLevel.expert
    yield create_user('root','root@example.com','Root','User',profile=UserProfiles.admin) 
    yield create_user('luc','luc@example.com','Luc','Saffre',profile=UserProfiles.admin) 
