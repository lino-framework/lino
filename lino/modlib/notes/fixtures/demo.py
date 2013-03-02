#coding: utf-8
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
TODO: this fixture fails if settings.SITE.project_model is 
empty or points to a model that has no `name` field.
"""

import decimal

from django.conf import settings
from django.utils.translation import ugettext as _
from lino.utils.instantiator import Instantiator
from lino.core.modeltools import resolve_model
from lino.utils import i2d, Cycler


#~ from django.contrib.auth import models as auth
from lino.modlib.users import models as auth

def objects():
    #~ User = settings.SITE.user_model()
    User = resolve_model(settings.SITE.user_model)
    Project = resolve_model(settings.SITE.project_model)
    Note = resolve_model('notes.Note')
    NoteType = resolve_model('notes.NoteType')
    
    USERS = Cycler(User.objects.all())
    qs = Project.objects.all()
    if qs.count() > 10:
        qs = qs[:10]
    PROJECTS = Cycler(qs)
    #~ PROJECTS = Cycler(Project.objects.filter(name__startswith="A"))
    #~ PROJECTS = Cycler(Project.objects.all())
    #~ COMPANIES = Cycler(Company.objects.all())
    NTYPES = Cycler(NoteType.objects.all())
    
    #~ u = User.objects.get(username='root')
    
    notetype = Instantiator('notes.NoteType').build
    tel = notetype(name="phone report",build_method='appyodt')
    yield tel
    yield notetype(name="todo")
    
    for i in range(100):
        yield Note(user=USERS.pop(),
            date=settings.SITE.demo_date(days=i),
            subject="Important note %d" % i,
            #~ company=COMPANIES.pop(),
            project=PROJECTS.pop(),
            type=NTYPES.pop())
        
    
    
