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
        
    def before_save(self):
        if self.nickname is None:
            self.nickname = self.first_name+' '+self.last_name

class Song(models.Model):
    title = models.CharField(max_length=200)
    published = models.IntegerField('year published',blank=True,null=True)
    text = models.TextField(blank=True,null=True)
    #votes = models.IntegerField()
 
    composers = models.ManyToManyField(
        Person,
        related_name="songs_composed")
    textauthor = models.ManyToManyField(
        Person,
        related_name="texts_written")
        
    def __unicode__(self):
        return self.title + " (%d)" % self.id
        
class Rehearsal(models.Model):        
    date = models.DateField('date',blank=True,null=True)
    singers = models.ManyToManyField(Person)
    songs = models.ManyToManyField(Song)
    remark = models.TextField(blank=True,null=True)

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
    

class Songbook(models.Model):
    class Admin:
        pass
    title = models.CharField(max_length=200)
    intro = models.TextField(blank=True,null=True)
    publisher = models.TextField(blank=True,null=True)
    

# reports

from lino.django.utils import reports
from lino.django.utils.layouts import PageLayout 
    
class Rehearsals(reports.Report):
    model = Rehearsal
    #page_layout_class = RehearsalPageLayout
    columnNames = "date remark songs:40 singers:40"
                  

    #~ def inlines(self):
        #~ return dict(songs=SongsByRehearsal())


class Singers(reports.Report):
    model = Person
    #page_layout_class = RehearsalPageLayout
    columnNames = "id first_name last_name"

class Songs(reports.Report):
    model = Song
    #page_layout_class = RehearsalPageLayout
    columnNames = "id title composers"
