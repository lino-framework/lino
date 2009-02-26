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

import codecs

from django import forms
from django.db import models
#from django.db.models.signals import post_syncdb
from django.utils.safestring import mark_safe 

from lino.django import xdjango


from docutils.core import publish_parts

import re
voc_splitter1=re.compile("^(.*)\s+\((.*)\)\s*:\s*(.+)",re.DOTALL)
voc_splitter2=re.compile("^(.*)\s*:\s*(.+)",re.DOTALL)


FORMATS = (
  ( "R", "reStructuredText"),
  ( "M", "markdown"),
  ( "T", "textile"),
)
 
MAX_NESTING_LEVEL=10


class Unit(xdjango.Model):
    
    name = models.CharField(max_length=20,blank=True)
    title = models.CharField(max_length=200,blank=True,null=True)
    parent = models.ForeignKey("Unit",blank=True,null=True,
                  related_name="children")
    seq = models.IntegerField(blank=True,null=True)
    body = models.TextField(blank=True,null=True)
    question = models.TextField(blank=True,null=True)
    answer = models.TextField(blank=True,null=True)
    remark = models.TextField(blank=True,null=True)
    vocabulary = models.TextField(blank=True,null=True)
    format = models.CharField(max_length=1,\
      choices=FORMATS,default="R")     
      
   
    def __unicode__(self):
        s=self.fullseq()
        if self.title:
            s += ". " + self.title
        return s
        
    def fullseq(self):
        if self.parent:
            return self.parent.fullseq()+"."+str(self.seq)
        return str(self.seq)
        
    def fullname(self):
        if self.parent:
            return self.parent.fullname() + "/" + self.name
        return self.name
        
    def parent_list(self):
        if self.parent:
            return self.parent.parent_list() + [ self.parent ]
        return []
        

    @models.permalink
    def get_absolute_url(self):
        return ('lino.django.voc.views.unit_detail', [str(self.id)])
        
    def formatted(self):
        docutils_settings = getattr(settings, "RESTRUCTUREDTEXT_FILTER_SETTINGS", {})
        parts = publish_parts(source=smart_str(value), writer_name="html4css1",
                 settings_overrides=docutils_settings)
        return mark_safe(force_unicode(parts["fragment"]))
    formatted.is_safe = True         

    def prettyprint(self,level=0):
        s="  "*level+unicode(self)
        children=[u.prettyprint(level+1) for u in self.children.all()]
        if len(children):
            s += "\n" + ("\n"+"  "*level).join(children) 
        return s
        
        
    def after_save(self):
        #print "after_save:", self
        self.entry_set.all().delete()
        if self.vocabulary:
            for line in self.vocabulary.splitlines():
                self.add_entry(line.strip())
    #after_save.alters_data = True
    
    def before_save(self):
        if self.seq is not None:
            return
        if self.parent is None:
            siblings=Unit.objects.filter(parent__isnull=True)
        else:
            siblings=Unit.objects.filter(parent=self.parent)
        seq=0
        for u in siblings:
            seq=max(seq,u.seq)
        self.seq=seq+1




    def add_entry(self,line):
        if len(line) == 0: return
        mo=voc_splitter1.match(line)
        if mo:
            d=dict(word1=mo.group(1),
                   word1_suffix=mo.group(2),
                   word2=mo.group(3))
        else:
            mo=voc_splitter2.match(line)
            if mo:
                d=dict(word1=mo.group(1),
                       word2=mo.group(2))
            else:
                raise "could not parse %r" % line
        qs=Entry.objects.filter(**d)
        if len(qs) == 0:
            e=Entry(**d)
            e.save()
        elif len(qs) == 1:
            e=qs[0]
        else:
            raise "duplicate voc entry %r" % line
        self.entry_set.add(e)
              
        
class Entry(xdjango.Model):
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
        
    #~ def before_save(self):
        #~ print "before_save"
        #~ mo=voc_splitter.match(self.word1)
        #~ if mo:
            #~ self.word1=mo.group(1).strip()
            #~ self.word1_suffix=mo.group(2).strip()
            #~ print repr(self.word1),repr(self.word1_suffix)
    #~ before_save.alters_data = True

    #~ def save(self, force_insert=False, force_update=False):
        #~ self.before_save()
        #~ super(Entry, self).save(force_insert, force_update) 
        
        

#~ def my_callback(sender,**kw):
  #~ print "my_callback",sender
  
#~ post_syncdb.connect(my_callback)




class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit

    def clean(self):
        l=[]
        p = self.cleaned_data.get("parent")
        if p == self.instance:
            #print "gonna raise", self.instance.pk
            raise forms.ValidationError("Parent cannot be self")
        #print "clean()", self.instance
        while p is not None:
            if p in l:
                raise forms.ValidationError("Parent recursion")
            if len(l) > MAX_NESTING_LEVEL:
                raise forms.ValidationError("Nesting level")
            l.append(p)
            p=p.parent
        return self.cleaned_data

Unit.model_form = UnitForm

