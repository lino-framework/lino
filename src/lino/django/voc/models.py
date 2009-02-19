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

class Unit(models.Model):
    title = models.CharField(max_length=200,blank=True,null=True)
    name = models.CharField(max_length=20)
    
    def __unicode__(self):
        return u"%s -- %s" % (self.name,self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('lino.django.voc.views.unit_detail', [str(self.id)])
        
class Entry(models.Model):
    unit = models.ForeignKey("Unit")
    question = models.CharField(max_length=200)
    #question_type = models.CharField(max_length=5,blank=True,null=True)
    answer = models.CharField(max_length=200)
    pos = models.CharField(max_length=20,blank=True,null=True)
 
    def __unicode__(self):
        s=self.question
        #if len(self.question_type) > 0:
        #    s += " (" + self.question_type + ")"
        s += " : " + self.answer
        return s
        
    @models.permalink
    def get_absolute_url(self):
        return ('lino.django.voc.views.entry_page', [self.unit.id, self.id])
