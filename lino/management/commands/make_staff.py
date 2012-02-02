# -*- coding: UTF-8 -*-
## Copyright 2009-2012 Luc Saffre
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
Print a list of users and optionally set the `is_superuser` 
attribute for some of them.
"""

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from lino.core.coretools import app_labels

from lino.utils import *

#~ from django.contrib.auth import models as auth
from lino.modlib.users import models as users

class Column:
    def __init__(self,name,width,meth,type=None):
        self.name = name
        self.width = width
        self.meth = meth
        self.type = type
        
class Table:
    col_sep = '|'
    def __init__(self,*columns):
        self.columns = columns

    def render(self,iter):
        s = self.col_sep + self.col_sep.join([
            unicode(col.name).ljust(col.width) 
            for col in self.columns]) + self.col_sep + '\n'
        for row in iter:
            s += self.col_sep + self.col_sep.join([
                unicode(col.meth(row)).ljust(col.width) for col in self.columns]) + self.col_sep +'\n'
        return s
              
def b2s(b):
    if b:
        return "X"
    return " "


class Command(BaseCommand):
    args = '<user1>, ...'
    help = 'Sets is_superuser attribute for specified users'

    def handle(self, *args, **options):
        for name in args:
            u = users.User.objects.get(username__exact=name)
        #~ for u in users.User.objects.all():
            #~ if u.username.lower() in args:
            if u.is_superuser:
                print u, 'was already superuser'
            else:
                u.is_superuser = True
                u.save()
                print u, "is now superuser"
            #~ else:
                #~ print i, u, "not changed"
                
        #~ from lino.modlib.system.models import Users
        #~ Users.request().as_text()
        
        #~ print '\t'.join(('i','name'.ljust(10),'staff','active'))
        #~ for i,u in enumerate(users.User.objects.all()):
            #~ print '\t'.join((str(i), unicode(u).ljust(10), b2s(u.is_superuser), b2s(u.is_active)))
            
        t = Table(
          Column('i',2,lambda (i,u) : i),
          Column('name',10,lambda (i,u) : u),
          Column('superuser',9,lambda (i,u) : b2s(u.is_superuser)),
          Column('active',6,lambda (i,u) : b2s(u.is_active)),
          )
        
        print t.render(enumerate(users.User.objects.all()))

