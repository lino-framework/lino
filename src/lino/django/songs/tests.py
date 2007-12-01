## Copyright 2007 Luc Saffre.
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

import unittest
from lino.django.songs.models import Song, Person

class TestCase(unittest.TestCase):
    
    def setUp(self):
        self.john=Person(firstname="John",lastname="Lennon")
        self.john.songs_composed.create(title="Imagine",published=1968)
        self.john.songs_composed.create(title="Another song",published=1967)
        self.john.songs_composed.create(title="A last song",published=1980)
        
        self.song1 = Song.objects.create(title="Foo",
                                         text="foo, foo, foo.")

    def test01(self):
        self.assertEquals(unicode(self.song1), u'Foo')
 
