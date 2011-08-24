#coding: utf-8
## Copyright 2009-2010 Luc Saffre
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

import decimal

from django.conf import settings
from django.utils.translation import ugettext as _
from lino.utils.instantiator import Instantiator, i2d
from lino.tools import resolve_model


#~ from django.contrib.auth import models as auth
from lino.modlib.users import models as auth

def objects():
  
    #~ User = settings.LINO.user_model()
    User = resolve_model(settings.LINO.user_model)
    u = User.objects.get(username='root')
    
    notetype = Instantiator('notes.NoteType').build
    tel = notetype(name="phone report",build_method='appyodt',template='notes.Note.Telefonnotiz.odt')
    yield tel
    yield notetype(name="todo")
    
    
