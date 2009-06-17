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

from django.utils.safestring import mark_safe

from lino.django.apps.countries import models as countries # import Country, Language
from lino.django.utils.render import HREF

class Place(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(countries.Country)
    
    def __unicode__(self):
        return self.name
        

class PersonManager(models.Manager):
    def get_by_name(self,s):
        #print "get_by_name(%r)" % s
        try:
            return self.get(nickname__exact=s)
        except self.model.DoesNotExist,e:
            pass
        a = s.split()
        #~ if len(a) == 1: 
            #~ return self.get(nickname__exact=s)
        last_name = a.pop()
        for p in self.filter(last_name__exact=last_name):
            i = 0
            ok = True
            for fn in p.first_name.split():
                if a[i].endswith("."):
                    if not fn.startswith(a[i][:-1]):
                        ok = False
                elif i < len(a):
                    if a[i] != fn:
                        ok = False
                i += 1
            if ok:
                return p
        raise self.model.DoesNotExist("get_by_name(%r) failed" % s)
        
        
    
class Person(models.Model):
    objects = PersonManager()
    first_name = models.CharField(max_length=100,blank=True)
    last_name = models.CharField(max_length=100,blank=True)
    #born = models.DateTimeField(blank=True,null=True)
    born = models.IntegerField(blank=True,null=True)
    died = models.IntegerField(blank=True,null=True)
    nickname = models.CharField(max_length=200,blank=True)
    name_prefix = models.CharField(max_length=10,blank=True)
    
    def __unicode__(self):
        #s = self.first_name + ' ' + self.last_name
        s = self.get_full_name()
        if self.born and self.died:
            s += " (%d-%d)" % (self.born,self.died)
        return s
        
    #~ def save(self, *args, **kwargs):
        #~ if len(self.nickname) == 0:
            #~ self.nickname = self.make_nickname()
        #~ super(Person,self).save(*args,**kwargs)
        
    def get_full_name(self):
        if len(self.nickname) > 0:
            return self.nickname
        l = [s for s in (self.first_name,
            self.name_prefix,
            self.last_name) if len(s)]
        return " ".join(l)
        #~ if self.first_name:
            #~ return self.first_name + " " + self.last_name
        #~ return self.last_name
    full_name = property(get_full_name)
        

class Author(Person):
    objects = PersonManager()

class Singer(Person):
    voice = models.CharField(max_length=10,blank=True,null=True)
    def __unicode__(self):
        s = self.first_name
        if self.voice is not None:
            s += " (%s)" % self.voice
        return s
    
class Choir(models.Model):
    name = models.CharField(max_length=200)
    place = models.ForeignKey(Place)
    singers = models.ManyToManyField(Singer)
    
    def __unicode__(self):
        return self.name
        

class Song(models.Model):
    title = models.CharField(max_length=200)
    #year_published = models.IntegerField(blank=True,null=True)
    text = models.TextField(blank=True)
    language = models.ForeignKey(countries.Language)
    origin = models.CharField(max_length=200)
    remarks = models.TextField(blank=True)
 
    composed_year = models.IntegerField(blank=True,null=True)
    text_year = models.IntegerField(blank=True,null=True)
    composed_by = models.ManyToManyField(
        Author,
        related_name="songs_composed")
    written_by = models.ManyToManyField(
        Author,
        related_name="songs_written")
    text_by = models.ManyToManyField(
        Author,
        related_name="texts_written")
    arranged_by = models.ManyToManyField(
        Author,
        related_name="songs_arranged")
    translated_by = models.ManyToManyField(
        Author,
        related_name="songs_translated")
    voices = models.CharField(max_length=200)
    bible_ref = models.CharField(max_length=200)
    based_on = models.ForeignKey("Song",blank=True,null=True)
    copyright = models.CharField(max_length=200)
        
    def __unicode__(self):
        return self.title + " (%d)" % self.id
        
class Event(models.Model):
    date = models.DateField('date',blank=True,null=True)
    choir = models.ForeignKey(Choir)
    singers = models.ManyToManyField(Singer)
    #songs = models.ManyToManyField(Song,through="SongEvent")
    remark = models.TextField(blank=True)
    
    def add_song(self,song,**kw):
        if not kw.has_key('seq'):
            kw['seq'] = self.songevent_set.count() + 1
        if not isinstance(song,Song):
            song = Song.objects.get(pk=song)
        se = SongEvent(event=self,song=song,**kw)
        se.save()
        return se

    def add_songs(self,*songs,**kw):
        for song in songs:
            self.add_song(song,**kw)
            
    def __unicode__(self):
        s = str(self.date)
        if self.remark:
            s += " (%s)" % self.remark
        return s
        
class Rehearsal(Event):
    pass
    
class Performance(Event):
    place = models.ForeignKey(Place)
    
class SongEvent(models.Model):
    event = models.ForeignKey(Event) #,related_name="songs")
    seq = models.IntegerField(default=0)
    song = models.ForeignKey(Song,related_name="events")
    remark = models.TextField(blank=True)
    
    def add_link(self,**kw):
        n = self.link_set.create(**kw)
        #n = Link(songevent=self,**kw)
        n.save()
        return n
        
class Link(models.Model):
    url = models.URLField()
    text = models.CharField(max_length=200)
    #date = models.DateField('date',blank=True,null=True)
    songevent = models.ForeignKey(SongEvent)
    #song = models.ForeignKey(Song)
    #event = models.ForeignKey(Event,blank=True,null=True)

    def __unicode__(self):
        if self.text:
            return self.text
        return models.Model.__unicode__(self)
        #if self.text:
        #    return HREF(self.url,self.text)
        #return HREF(self.url,self.url)
        
    def get_instance_url(self):
        # see sites.LinoSite.get_instance_url()
        if self.url:
            return self.url
        

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


class SongPageLayout(PageLayout):
    main = """
    id title language voices
    origin based_on bible_ref
    composed_by text_by written_by
    arranged_by
    translated_by
    events
    """
    def inlines(self):
        return dict(events=EventsBySong())

class PerformancePageLayout(PageLayout):
    main = """
    id date place remark 
    choir
    songs
    singers
    """
    def inlines(self):
        return dict(songs=SongsByEvent())
    
class Rehearsals(reports.Report):
    #page_layouts = (EventPageLayout,)
    model = Rehearsal
    #page_layout_class = RehearsalPageLayout
    columnNames = "date remark songs:20 singers:10"
    order_by = "date"

class Performances(reports.Report):
    model = Performance
    columnNames = "date place remark songs:20 singers:10"
    order_by = "date"
    page_layouts = (PerformancePageLayout,)
    

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
    columnNames = "id get_full_name born died first_name last_name"
    order_by = "last_name"

    
class EventsBySong(reports.Report):
    model = SongEvent
    master = Song
    columnNames = "event remark link_set"
    
class SongsByEvent(reports.Report):
    model = SongEvent
    master = Event
    columnNames = "seq song link_set remark"

class Songs(reports.Report):
    model = Song
    page_layouts = (SongPageLayout,)
    columnNames = "id title language voices composed_by text_by written_by"

class SongEvents(reports.Report):
    model = SongEvent

class SongsByEvent(reports.Report):
    model = SongEvent
    master = Event
    columnNames = "seq song remark link_set"


class Links(reports.Report):
    model = Link

class Choirs(reports.Report):
    model = Choir


def lino_setup(lino):
    m = lino.add_menu("songs","~Songs",can_view=perms.is_authenticated)
    m.add_action(Rehearsals())
    m.add_action(Performances())
    m.add_action(Singers())
    m.add_action(Authors())
    m.add_action(Songs())
    m.add_action(Collections())
    m.add_action(Places())
    m.add_action(Links())
    m.add_action(SongEvents())
