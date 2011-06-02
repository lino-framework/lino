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
from django.utils.translation import ugettext as _
from lino.utils.instantiator import Instantiator, i2d
from lino.tools import resolve_model

#~ from django.contrib.auth import models as auth
from lino.modlib.users import models as auth

def objects():
  
    u = auth.User.objects.get(pk=1)
    
    notetype = Instantiator('notes.NoteType').build
    tel = notetype(name="phone report",build_method='appyodt',template='notes.Note.Telefonnotiz.odt')
    yield tel
    yield notetype(name="todo")
    
    
    #~ Person = resolve_model('contacts.Person')
    #~ Company = resolve_model('contacts.Company')
    
    #~ print Person.objects.all()
    
    #~ luc = Person.objects.get(name__exact='Saffre Luc')
    #~ rko = Company.objects.get(name__exact=u'Rumma & Ko OÜ')
    
    #~ note = Instantiator('notes.Note',type=tel).build
    #~ n = note(user=u,date=i2d(20091208),subject=u"note for company %s" % rko,body="""Lorem ipsum...""",owner=rko)
    #~ yield n    
    
    #~ n = note(user=u,date=i2d(20091208),subject=u"note for person %s" % luc,body="""Lorem ipsum...""",owner=luc)
    #~ yield n 
