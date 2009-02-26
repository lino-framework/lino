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
from django import forms
from lino.django import xdjango


class TestCase(TestCase):
    def test01(self):
        
        u1 = Unit(title="First Chapter")
        u1.save()
        self.assertEqual(u1.seq,1)
        u = Unit(title="First Section",parent=u1)
        u.save()
        self.assertEqual(u.seq,1)
        u = Unit(title="Second Section",parent=u1)
        u.save()
        self.assertEqual(u.seq,2)
        
        self.assertEqual(u.pk,3)
        try:
            print "set parent to self"
            u.parent=u
            u.save()
            print "save() : done"
        except xdjango.ValidationError,e:
            #s="\n".join([e.as_text() for m in e.messages])
            s=str(e) # .messages.as_text()
            self.assertEqual(s,"Parent cannot be self")
        else:
            self.fail("Expected forms.ValidationError")
            

class PkkTestCase(TestCase):
    fixtures=[ 'pkk.yaml' ]
    def setUp(self):
        for u in Unit.objects.all():
            u.save()
        
    def test01(self):
        unit=Unit.objects.get(pk=5)
        # unit.save()
        entries=unit.entry_set.all()
        s="\n".join([e.word1 for e in entries])
        #print s
        self.assertEquals(s.split(), u"""
        grand, grande
        gentil, gentille
        petit, petite
        méchant, méchante
        sale, sale
        propre, propre
        est-ce que
        oui
        non """.split())
        
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
        # total number of rows in each table:
        units=Unit.objects.all()
        self.assertEqual(len(units),6)
        self.assertEqual(len(Entry.objects.all()),9)
        
        pkk=unit=Unit.objects.get(pk=1)
        self.assertEqual(len(pkk.children.all()),1)
        
        s=pkk.prettyprint()
        #print s
        self.assertEqual(s,u"""\
1. Prantsuse keele kurs algajatele
  1.1. Esimene tund
    1.1.1. Sissejuhatus
      1.1.2. Olema
      1.1.3. Esimesed laused
      1.1.4. Mees või naine?""")
        
        
        #~ u1=pkk.children.all()[0]
        #~ u2=pkk.children.all()[1]
        #~ u3=pkk.children.all()[2]
        #~ self.assertEqual(u1.parent,pkk)
        #~ self.assertEqual(u2.parent,pkk)
        #~ self.assertEqual(u3.parent,pkk)
        
        #~ u4=pkk.children.all()[2]
        #~ self.assertEqual(u4.title,"Esimesed laused")
        
        entries=Entry.objects.filter(word1__startswith="p")
        self.assertEquals(len(entries),2)
        s="\n".join([e.word1 for e in entries])
        #print s
        self.assertEquals(s.split(),u"""
petit, petite
propre, propre
        """.split())
        
          
        #~ format='json'
        #~ serializers.get_serializer(format)
        #~ objects = []
        #~ for model in (Unit,Entry):
            #~ objects.extend(model._default_manager.all())
        #~ outfile=os.path.join(dirname,"fixtures","pkk.json")
        #~ f=codecs.open(outfile,"w","utf8")
        #~ f.write(serializers.serialize(format, objects))
        
        
        
        

        
     
        
## Run these tests using "python manage.py test".
## see http://docs.djangoproject.com/en/dev/topics/testing/#topics-testing
