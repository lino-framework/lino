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

import os
import codecs
from models import Unit, Entry
from django.core import serializers
from django.test import TestCase


class TestCase(TestCase):
    #fixtures=[ 'pkk.yaml' ]
    def setUp(self):
        pass
        
    #~ def test01(self):
        #~ unit=Unit.objects.get(id=3)
        #~ unit.save()
        #~ entries=unit.entry_set.all()
        #~ s="\n".join([e.word1 for e in entries])
        #~ print s
        #~ self.assertEquals(s, unit.vocabulary)
        
    #~ def test02(self):
        #~ entries=Entry.objects.all()
        #~ self.assertEquals(len(entries),192)
        #~ entries=Entry.objects.filter(word1__startswith="p")
        #~ self.assertEquals(len(entries),20)
        #~ s="\n".join([e.word1 for e in entries])
        #~ print s
        #~ #print "test00",entries
        #~ self.assertEquals(s,"""\
#~ père
        #~ """)

    def test03(self):
        pkk=Unit()
        dirname=os.path.dirname(__file__)
        pkk.load_rst(os.path.join(dirname,"data","pkk","pkk.rst"))
        self.assertEqual(len(Unit.objects.all()),8)
        self.assertEqual(len(pkk.children.all()),7)
        u1=pkk.children.all()[0]
        u2=pkk.children.all()[1]
        u3=pkk.children.all()[2]
        self.assertEqual(u1.parent,pkk)
        self.assertEqual(u2.parent,pkk)
        self.assertEqual(u3.parent,pkk)
        
        u4=pkk.children.all()[2]
        self.assertEqual(u4.title,"Esimesed laused")
        
        entries=Entry.objects.all()
        self.assertEquals(len(entries),24)
        entries=Entry.objects.filter(word1__startswith="p")
        self.assertEquals(len(entries),2)
        if False:
            s="\n".join([e.word1 for e in entries])
            print s
            #print "test00",entries
            self.assertEquals(s,u"""\
père
            """)
        
        if False:
          s="\n".join([u.title for u in pkk.unit_set.all()])
          print s
          self.assertEqual(s,"""\
          """)
          
        format='json'
        serializers.get_serializer(format)
        objects = []
        for model in (Unit,Entry):
            objects.extend(model._default_manager.all())
        outfile=os.path.join(dirname,"fixtures","pkk.json")
        f=codecs.open(outfile,"w","utf8")
        f.write(serializers.serialize(format, objects))
        

        
     
        
## Run these tests using "python manage.py test".
## see http://docs.djangoproject.com/en/dev/topics/testing/#topics-testing
