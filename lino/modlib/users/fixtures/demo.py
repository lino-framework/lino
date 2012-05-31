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

from lino.utils.choicelists import UserLevel

def objects():
    #~ now = datetime.datetime.now() 
    def create_user(*args,**kw):
        user = Instantiator('users.User',
          #~ 'username email first_name last_name is_staff is_superuser',
          'username email first_name last_name'
          ).build
          #~ is_active=True,last_login=now,date_joined=now).build
        u = user(*args,**kw)
        #~ u.set_password('1234')
        return u
    #~ yield create_user('user','user@example.com','John','Jones',level=UserLevel.user)
    #~ yield create_user('staff','staff@example.com','Pete','Peters',UserLevel.manager)
    #~ yield create_user('user2','user2@example.com','Pete','Peters',profile="user")
    kw = dict()
    for f in settings.LINO.user_profile_fields:
        kw[f] = UserLevel.expert
    #~ root = User.objects.get(username="root")
    #~ root.newcomers_level = UserLevel.expert
    #~ root.save()
    #~ yield create_user('root','root@example.com','Root','User',level=UserLevel.expert) 
    yield create_user('root','root@example.com','Root','User',**kw) 
    yield create_user('luc','luc@example.com','Luc','Saffre',profile="root") 
    #~ yield  create_user('user','user@example.com','John','Jones',False,False)
    #~ yield create_user('staff','staff@example.com','Pete','Peters',True,False)
    #~ yield create_user('root','root@example.com','Dick','Dickens',True,True)