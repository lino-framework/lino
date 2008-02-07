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

from django.db import models

class Person(models.Model):
    class Admin:
        pass
    firstname = models.CharField(maxlength=100)
    lastname = models.CharField(maxlength=100)
    #born = models.DateTimeField(blank=True)
    
    def __unicode__(self):
        return self.firstname+' '+self.lastname

class Song(models.Model):
    class Admin:
        pass
    author = models.ForeignKey(
        Person,
        related_name="author",
        null=True)
    
    composer = models.ForeignKey(
        Person,
        related_name="composer",
        blank=True)
    title = models.CharField(maxlength=200)
    #pub_date = models.DateField('date published',blank=True)
    published = models.IntegerField('year published',blank=True)
    text=models.TextField(blank=True)
    #votes = models.IntegerField()
 
    def __unicode__(self):
        return self.title

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
    title = models.CharField(maxlength=200)
    intro = models.TextField(blank=True)
    publisher = models.TextField(blank=True)
    
