## Copyright 2007-2009 Luc Saffre.
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

from lino.modlib.tools import resolve_model

Song = resolve_model('songs.Song')
Author = resolve_model('songs.Author')
Language = resolve_model('countries.Language')

class TestCase(unittest.TestCase):
    
    def setUp(self):
        en = Language(pk='en')
        self.john=Author(first_name="John",last_name="Lennon")
        self.john.save()
        self.song1=Song(title="Give Peace a Chance",
          composed_year=1971,language=en)
        self.song1.save()
        self.song1.composed_by.add(self.john)
        self.john.songs_composed.create(title="Imagine",
          composed_year=1971,language=en)

    def test01(self):
        self.assertEquals(unicode(self.song1), 'Give Peace a Chance (1)')
        self.assertEquals(self.john.songs_composed.count(), 2)
        self.assertEquals(Song.objects.count(), 2)
 
