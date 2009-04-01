## Copyright 2009 Luc Saffre

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


from lino.django.tom import reports
from django.contrib.auth.models import Permission, User, Group

class Permissions(reports.Report):
    queryset=Permission.objects.order_by('content_type__app_label', 'codename')


  
class Users(reports.Report):
    queryset=User.objects.order_by("username")

class Groups(reports.Report):
    queryset=Group.objects.order_by("name")


def setup_menu(menu):
    m = menu.addMenu("system","~System")
    m.addAction(Permissions())
    m.addAction(Users())
    m.addAction(Groups())
