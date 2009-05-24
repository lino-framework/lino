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


from lino.django.utils import reports
from django.contrib.auth.models import Permission, User, Group
from lino.django.utils import perms

class Permissions(reports.Report):
    model = Permission
    order_by = 'content_type__app_label codename'
  
class Users(reports.Report):
    model = User
    order_by = "username"

class Groups(reports.Report):
    model = Group
    order_by = "name"

    
def setup_menu(menu):
    m = menu.add_menu("system","~System")
    m.add_action(Permissions())
    m.add_action(Users())
    m.add_action(Groups())
    m.can_view = perms.is_staff
