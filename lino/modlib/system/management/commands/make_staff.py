# -*- coding: UTF-8 -*-
## Copyright 2009-2010 Luc Saffre
## This file is part of the TimTools project.
## TimTools is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## TimTools is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with TimTools; if not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from lino.core.coretools import app_labels

from lino.utils import *

from django.contrib.auth import models as auth

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
        s = self.col_sep + self.col_sep.join([unicode(col.name).ljust(col.width) for col in self.columns]) + self.col_sep + '\n'
        for row in iter:
            s += self.col_sep + self.col_sep.join([unicode(col.meth(row)).ljust(col.width) for col in self.columns]) + self.col_sep +'\n'
        return s
              
def b2s(b):
    if b:
        return "X"
    return " "


class Command(BaseCommand):
    args = '<user1>, ...'
    help = 'Sets is_staff attribut for specified users'

    def handle(self, *args, **options):
        for name in args:
            u = auth.User.objects.get(username__exact=name)
        #~ for u in auth.User.objects.all():
            #~ if u.username.lower() in args:
            if u.is_staff:
                print u, 'was already staff'
            else
                u.is_staff = True
                u.save()
                print u, "is now staff"
            #~ else:
                #~ print i, u, "not changed"
                
        #~ from lino.modlib.system.models import Users
        #~ Users.request().as_text()
        
        #~ print '\t'.join(('i','name'.ljust(10),'staff','active'))
        #~ for i,u in enumerate(auth.User.objects.all()):
            #~ print '\t'.join((str(i), unicode(u).ljust(10), b2s(u.is_staff), b2s(u.is_active)))
            
        t = Table(
          Column('i',2,lambda (i,u) : i),
          Column('name',10,lambda (i,u) : u),
          Column('staff',6,lambda (i,u) : b2s(u.is_staff)),
          Column('active',6,lambda (i,u) : b2s(u.is_active)),
          )
        
        print t.render(enumerate(auth.User.objects.all()))

