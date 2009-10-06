## Copyright 2007-2008 Luc Saffre.
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
from datetime import datetime

class Node(models.Model):

    class Admin:
        fields = (
            (None, dict(fields=('title','name','parent', 'abstract','body'))),
            ("Dates & times", dict(fields=('published','modified','created'))),
            ("Other", dict(fields=('hidden',),classes='collapse')),
            )
        
            #("Parent", dict(fields=('parent','seq'),classes='collapse')),

        list_display=('title','parent', 'abstract','name','published','hidden')
        
        list_filter=['published']
        search_fields=['title','abstract']
        date_hierarchy='published'
    
    title = models.CharField(max_length=200)
    abstract = models.TextField(blank=True)
    body = models.TextField(blank=True)
    name = models.CharField(max_length=30,blank=True)
    
    published = models.DateTimeField('published',default=datetime.now)
    created = models.DateTimeField('created',default=datetime.now)
    modified = models.DateTimeField('last modified',auto_now=True)
    
    parent = models.ForeignKey('self',null=True,blank=True,related_name='child_set')
    # children of a same parent will be ordered by this:
    seq = models.SmallIntegerField("sequence in parent",null=True,blank=True)

    hidden = models.BooleanField(default=False)
    
    #image = FilePathField(path="/home/mraamat/public_images",recursive=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["published"]

#class Resource(models.Model):
#    
#    id = models.CharField(max_length=100)
#    uri = models.CharField(max_length=200)
