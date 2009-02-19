# -*- coding: utf-8 -*-

## Copyright 2008-2009 Luc Saffre.
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

from models import Unit, Entry
from django.test import TestCase


class TestCase(TestCase):
    fixtures=[ 'pkk.yaml' ]
    def setUp(self):
        pass
        
    def test01(self):
        mitmus=Unit.objects.get(id=3)
        mitmus.update_entries()
        s=mitmus.entry_set.all()
        print s
        self.assertEquals(s, "")
        
    def test00(self):
        print Entry.objects.all()

     
        
## Run these tests using "python manage.py test".
## see http://docs.djangoproject.com/en/dev/topics/testing/#topics-testing
