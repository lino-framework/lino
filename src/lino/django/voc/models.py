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
from django.db.models.signals import post_syncdb

import re

word1_splitter=re.compile("^(.*)\s+\((.*)\)",re.DOTALL)


class Unit(models.Model):
    title = models.CharField(max_length=200,blank=True,null=True)
    iname = models.CharField(max_length=20,blank=True,null=True)
    parent = models.ForeignKey("Unit",blank=True,null=True)
    instruction = models.TextField(blank=True,null=True)
    question = models.TextField(blank=True,null=True)
    answer = models.TextField(blank=True,null=True)
    remark = models.TextField(blank=True,null=True)
    vocabulary = models.TextField(blank=True,null=True)
    
    def __unicode__(self):
        return unicode(self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('lino.django.voc.views.unit_detail', [str(self.id)])
        
    def after_save(self):
        print "after_save:", self
        self.entry_set.all().delete()
        if self.vocabulary:
            for word1 in self.vocabulary.splitlines():
                word1=word1.strip()
                #print repr(word1)
                for e in Entry.objects.filter(word1=word1):
                    e.units.add(self)
                    e.save()
    after_save.alters_data = True
                    
                    
    def save(self, force_insert=False, force_update=False):
        super(Unit, self).save(force_insert, force_update) 
        self.after_save()
                    
        
class Entry(models.Model):
    word1 = models.CharField(max_length=200)
    word1_suffix = models.CharField(max_length=200,blank=True,null=True)
    word2 = models.CharField(max_length=200)
    word2_suffix = models.CharField(max_length=200,blank=True,null=True)
    units = models.ManyToManyField(Unit)
    #pos = models.CharField(max_length=20,blank=True,null=True)
 
    def __unicode__(self):
        s=self.word1
        if self.word1_suffix:
            s += " (" + self.word1_suffix + ")"
        s += " = " + self.word2
        return s
        
    @models.permalink
    def get_absolute_url(self):
        return ('lino.django.voc.views.entry_page', [self.unit.id, self.id])
        
    def before_save(self):
        print "before_save"
        mo=word1_splitter.match(self.word1)
        if mo:
            self.word1=mo.group(1).strip()
            self.word1_suffix=mo.group(2).strip()
            print repr(self.word1),repr(self.word1_suffix)
    before_save.alters_data = True

    def save(self, force_insert=False, force_update=False):
        self.before_save()
        super(Entry, self).save(force_insert, force_update) 

def my_callback(sender,**kw):
  print "my_callback",sender
  
post_syncdb.connect(my_callback)
