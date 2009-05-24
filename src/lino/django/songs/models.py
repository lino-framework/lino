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

from django.db import models

from lino.django.utils.models import Language

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    #born = models.DateTimeField(blank=True,null=True)
    born = models.IntegerField(blank=True,null=True)
    died = models.IntegerField(blank=True,null=True)
    nickname = models.CharField(max_length=200,blank=True,null=True)
    
    def __unicode__(self):
        s = self.first_name+' '+self.last_name
        if self.born and self.died:
            s += " (%d-%d)" % (self.born,self.died)
        return s
        
    def save(self, *args, **kwargs):
        if self.nickname is None:
            self.nickname = self.make_nickname()
        super(Person,self).save(*args,**kwargs)
        
    def make_nickname(self):
        if self.first_name:
            return self.first_name + " " + self.last_name
        return self.last_name

class Author(Person):
    pass

class Singer(Person):
    voice = models.CharField(max_length=10,blank=True,null=True)
    def __unicode__(self):
        s = self.first_name
        if self.voice is not None:
            s += " (%s)" % self.voice
        return s
    

class Song(models.Model):
    title = models.CharField(max_length=200)
    published = models.IntegerField('year published',
      blank=True,null=True)
    text = models.TextField(blank=True,null=True)
    language = models.ForeignKey(Language)
    #votes = models.IntegerField()
 
    composer = models.ManyToManyField(
        Author,
        related_name="songs_composed")
    textauthor = models.ManyToManyField(
        Author,
        related_name="texts_written")
    arranged_by = models.ManyToManyField(
        Author,
        related_name="songs_arranged")
        
    def __unicode__(self):
        return self.title + " (%d)" % self.id
        
class Rehearsal(models.Model):        
    date = models.DateField('date',blank=True,null=True)
    singers = models.ManyToManyField(Singer)
    songs = models.ManyToManyField(Song)
    remark = models.TextField(blank=True,null=True)

    def __unicode__(self):
        s = str(self.date)
        if self.remark:
            s += " (%s)" % self.remark
        return s
        
#~ class Work(models.Model):
    #~ class Admin:
        #~ pass
    #~ composer = models.ForeignKey(
        #~ Person,
        #~ related_name="songs_composed")
    #~ textauthor = models.ForeignKey(
        #~ Person,
        #~ related_name="texts_written")
    #~ song = models.ForeignKey(
        #~ Song,
        #~ related_name="composed_by")
    #~ remark = models.TextField(blank=True,null=True)
    
    
class Translation(models.Model):
    class Admin:
        pass
    translator = models.ForeignKey(
        Person,
        related_name="translator",
        null=True)
    original = models.ForeignKey(
        Song,
        related_name="original",
        null=True)
    target = models.ForeignKey(
        Song,
        related_name="target",
        null=True)
    

class Place(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey('utils.Country',blank=True,null=True)
    
    def __unicode__(self):
        return self.name
    
class Collection(models.Model):
    title = models.CharField(max_length=200)
    intro = models.TextField(blank=True,null=True)
    #publisher = models.TextField(blank=True,null=True)
    year = models.IntegerField(blank=True,null=True)
    author = models.ForeignKey(Author,blank=True,null=True)
    place = models.ForeignKey(Place,blank=True,null=True)
    songs = models.ManyToManyField(Song)
    
    def __unicode__(self):
        return self.title
    

# reports

from lino.django.utils import reports, perms
from lino.django.utils.layouts import PageLayout 
    
class Rehearsals(reports.Report):
    model = Rehearsal
    #page_layout_class = RehearsalPageLayout
    columnNames = "date remark songs:40 singers:40"

class Collections(reports.Report):
    model = Collection
    columnNames = "title place year author id"

class Places(reports.Report):
    model = Place
    columnNames = "name country id"


class Singers(reports.Report):
    model = Singer
    #page_layout_class = RehearsalPageLayout
    columnNames = "id first_name last_name voice"
    order_by = "last_name"

class Authors(reports.Report):
    model = Author
    #queryset = Author.objects.filter(singer__exact=None)
    #page_layout_class = RehearsalPageLayout
    columnNames = "id first_name last_name born died"
    order_by = "last_name"

    
#~ class RehearsalsBySong(reports.Report):
    #~ model = Song
    #~ master = Rehearsal
    
class SongPageLayout(PageLayout):
    main = """
    id title language
    composer textauthor arranged_by
    rehearsal_set
    """

class Songs(reports.Report):
    model = Song
    page_layout_class = SongPageLayout
    columnNames = "id title language composer textauthor arranged_by"

    #~ def inlines(self):
        #~ return dict(rehearsals=RehearsalsBySong())

def lino_setup(lino):
    m = lino.add_menu("songs","~Songs",can_view=perms.is_authenticated)
    m.add_action(Rehearsals())
    m.add_action(Singers())
    m.add_action(Authors())
    m.add_action(Songs())
    m.add_action(Collections())
    m.add_action(Places())
