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

import re

lang1_splitter=re.compile("^(.*)\w\((.*)\)",re.DOTALL)


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
        
    def update_entries(self):
        print "update_entries: ", self.entry_set.all()
        self.entry_set.all().delete()
        if self.vocabulary:
            for lang1 in self.vocabulary.splitlines():
                print lang1
                for e in Entry.objects.filter(lang1=lang1):
                    e.units.add(self)
    update_entries.alters_data = True
                    
                    
    def save(self, force_insert=False, force_update=False):
        super(Unit, self).save(force_insert, force_update) 
        update_entries()
                    
        
class Entry(models.Model):
    lang1 = models.CharField(max_length=200)
    lang1_suffix = models.CharField(max_length=5,blank=True,null=True)
    lang2 = models.CharField(max_length=200)
    units = models.ManyToManyField(Unit)
    #pos = models.CharField(max_length=20,blank=True,null=True)
 
    def __unicode__(self):
        s=self.lang1
        if self.lang1_suffix:
            s += " (" + self.lang1_suffix + ")"
        s += " = " + self.lang2
        return s
        
    @models.permalink
    def get_absolute_url(self):
        return ('lino.django.voc.views.entry_page', [self.unit.id, self.id])
        
    def before_save(self):
        mo=lang1_splitter.match(self.lang1)
        if mo:
            self.lang1=mo.group(1).strip()
            self.lang1_suffix=mo.group(2).strip()
    before_save.alters_data = True

    def save(self, force_insert=False, force_update=False):
        self.before_save()
        super(Entry, self).save(force_insert, force_update) 
