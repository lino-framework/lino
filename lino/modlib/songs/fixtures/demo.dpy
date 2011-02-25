#coding: utf8
## Copyright 2009 Luc Saffre

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

import os, codecs
import yaml


from lino.apps.songs.models import *
from lino.apps.countries import models as countries
from lino.utils.instantiator import Instantiator, ManyToManyConverter


RELAX = not True

def load_yaml(model,filename):
    pfn = os.path.join(os.path.dirname(__file__),filename)
    #print "Loading input file %s ..." % filename
    fd = codecs.open(pfn,"r",'utf-8')
    try:
        for yamldict in yaml.load_all(fd):
            if yamldict is not None:
                for k in yamldict.keys():
                    if k.startswith(";"):
                        del yamldict[k]
                o = model(**yamldict)
                o.save()
                #yield o
    except Exception,e:
        if RELAX:
            print "RELAX!", pfn+":"+str(e)
        else:
            raise 
    fd.close()
    



class AuthorList(ManyToManyConverter):
    splitsep = ","
    def lookup(self,value):
        return Author.objects.get_by_name(value)

converter_classes=dict(
  composed_by=AuthorList,
  text_by=AuthorList,
  arranged_by=AuthorList,
  translated_by=AuthorList,
  written_by=AuthorList,
  )

song = Instantiator(Song,converter_classes=converter_classes).build

singer = Instantiator(Singer,"nickname first_name last_name").build
composer = Instantiator(Author,"first_name last_name born died").build
author = Instantiator(Author,"first_name last_name born died").build
translator = Instantiator(Author,"first_name last_name born died").build
place = Instantiator(Place,"name").build

rehearsal = Instantiator(Rehearsal,"date singers:nickname",
  choir=1).build
auftritt = Instantiator(Performance,
  "date place singers:nickname remark",choir=1).build
#video = Instantiator(Note,text="video recording").build
choir = Instantiator(Choir,"name place singers:nickname").build

def objects():

    #~ language = Instantiator(countries.Language,"id name").build
    #~ yield language('la','Latin')
    #~ yield language('he','Hebrew')
    
    yield place('Tallinn',country="ee")
    yield place('Vigala',country="ee") # 2
    yield place('Paldiski',country="ee") # 3
    yield place(u'Pärnu',country="ee") # 4
    
    yield singer("ls","Luc","Saffre")
    yield singer("er","Erich","Roots")
    yield singer("pr","Pille-Riin","Roots")
    yield singer("kj","Kristiina",u"Jõgi")
    yield singer("as","Aili","Soonberg")
    yield singer("rj","Ruth","Johanson")
    yield singer("lr","Ly","Rumma")
    yield singer("bs","Bruno","Saffre")
    
    yield choir("Vigala Maarja koguduse ansambel",2,
      "as kj lr ls er pr rj")
    
    #~ for o in load_yaml(author,'demo_authors.yaml'): yield o
    #~ for o in load_yaml(song,'demo_songs.yaml'): yield o
    load_yaml(author,'demo_authors.yaml')
    load_yaml(song,'demo_songs.yaml')
    
    collection = Instantiator(Collection,
      "title place:name").build
    yield collection("Luci Kammerkoori noodid",songs="""
    33 26
    """)
    yield collection("cpdl.org",songs="""
    9 16 32 
    """)
    yield collection(
      'Vaimulike laule kooridele ja ansamblitele 3',
      'Tallinn',year=2007,
      author=Author.objects.get_by_name(u'Silvi Mänd'),songs="22")
    yield collection(u"Päevaviisid",songs="""
    37
    """)
    
    a = auftritt("2007-09-09",2,"pr er as rj kj ls",
      "Esimene avalik esinemine kohvilaual")
    a.add_songs(1,2)
    a = auftritt("2007-10-21",3,"pr er as rj kj ls",
      "Esimemine Paldiskis")
    a.add_songs(3,4,5,6)
    
    a = auftritt("2008-01-06",2,"pr er as rj kj ls",
      "Esinemine Vigala kirikus")
    a.add_songs(8,9,11)
    
    e = auftritt("2008-04-13",2,"pr er as rj kj ls",
      u"Esinemine Vigala kiriku käärkambris")    
    e.add_song(34)
    e.add_song(27).add_link(text="Video",
     url="http://www.youtube.com/watch?v=Eb-J1G-xjoM&feature=channel_page")
    e.add_song(35).add_link(text="Video",
     url="http://www.youtube.com/watch?v=BwiOyYtf3DI&feature=channel_page")
    e.add_song(13).add_link(text="Video",
     url="http://www.youtube.com/watch?v=Unsyh-fjJaM&feature=channel_page")
    
    a = auftritt("2008-05-11",2,"pr er as rj kj ls",
      "Esinemine Vigala kirikus")    
    a = auftritt("2008-05-25",2,"as kj ls",
      u"Väike esinemine Vigala kirikus")    
    a.add_songs(6,35)
    
    e = auftritt("2008-06-21",2,"as kj ls bs","Iirise ristsed")
    e.add_songs(1)
    
    e = auftritt("2008-09-07",2,"pr er as rj kj ls",
      u"Esinemine Vigala kirikus (669. kiriku aastapäev)")
    e.add_song(18).add_link(text="Video",
     url="http://www.youtube.com/watch?v=bqCsSVWF9AA&feature=channel_page")
    e.add_song(19).add_link(text="Video",
     url="http://www.youtube.com/watch?v=dTDoNCbkZYM&feature=channel_page")
    
     
    e = auftritt("2008-12-24",2,"pr er as rj kj ls",u"Esinemine Vigala kirikus")
    e.add_songs(8,21)
    
    e = auftritt("2008-12-31",2,"pr er as rj kj ls",u"Esinemine Vigala kirikus")    
    e.add_songs(6,10,20)
    
    e = auftritt("2009-04-12",2,"er as kj lr ls",u"Esinemine Vigala kirikus")
    e.add_songs(22,25)
    
    e = rehearsal("2009-04-26","as kj lr ls")
    e.add_songs(35,32,26,28)
    e = rehearsal("2009-05-03","as kj lr ls")
    e.add_songs(35,32,28,33)
    e = rehearsal("2009-05-17","as kj lr ls pr er")
    e.add_songs(35,26,32,28)
    e = rehearsal("2009-05-24","kj lr ls pr er rj")
    e.add_songs(35,32,33,26,28)
    e = auftritt("2009-06-07",2,"as kj lr ls er pr",
      u"Jüri saatmine")
    e.add_song(6)
      
    e = rehearsal("2009-06-07","as kj lr ls pr er",
      remark="Esimene proovipäev")
    e.add_song(14).add_link(text="Video",
      url="http://www.youtube.com/watch?v=7_8r5WevmDI")
    e.add_songs(26,32,33,22,28,20,25)
      
    e = auftritt("2009-06-09",4,"as kj lr ls er pr rj",
      u"Esinemine Pärnu Eliisabeti kirikus")
    e.add_song(14)
    e.add_song(20,remark="salmid 2-5").add_link(text="Video",
      url="http://www.youtube.com/watch?v=O02OHxv0oSg") 
      # Õhtul vaiksel tunnil    
    e.add_song(28).add_link(text="Video",
      url="http://www.youtube.com/watch?v=DVbXWWRwWHA") 
      # ma annan oma südame
    e.add_song(22).add_link(text="Video",
      url="http://www.youtube.com/watch?v=D0Qb9zgMkwI") # Sõber kas tunned
    e.add_song(26).add_link(text="Video",
      url="http://www.youtube.com/watch?v=3rRpV8baHEg") # Peace    
    e.add_song(6).add_link(text="Video",
      url="http://www.youtube.com/watch?v=aDC6kURdhLw") # vanaiiri
 