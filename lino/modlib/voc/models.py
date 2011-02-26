## Copyright 2008-2010 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.


import codecs

from docutils.core import publish_parts

import re
voc_splitter1=re.compile("^(.*)\s+\((.*)\)\s*:\s*(.+)",re.DOTALL)
voc_splitter2=re.compile("^(.*)\s*:\s*(.+)",re.DOTALL)

from django import forms
from django.db import models
from django.utils.safestring import mark_safe 

from lino import reports
from lino.utils import perms

from lino.utils.validatingmodel import TomModel, ModelValidationError


FORMATS = (
  ( "R", "reStructuredText"),
  ( "M", "markdown"),
  ( "T", "textile"),
)
 
MAX_NESTING_LEVEL=10


class Unit(TomModel):
    
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
        

    def formatted(self):
        docutils_settings = getattr(settings,
                "RESTRUCTUREDTEXT_FILTER_SETTINGS", {})
        parts = publish_parts(source=smart_str(value), 
                 writer_name="html4css1",
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
    
    def full_clean(self):
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
        super(Unit,self).full_clean(*args,**kw)


    def validate_parent(self):
        l=[]
        p = self.parent
        if p == self:
            raise ModelValidationError("Parent cannot be self")
        #print "clean()", self.instance
        while p is not None:
            if p in l:
                raise ModelValidationError("Parent recursion")
            if len(l) > MAX_NESTING_LEVEL:
                raise ModelValidationError("Nesting level")
            l.append(p)
            p=p.parent


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
              
        
class Entry(TomModel):
    word1 = models.CharField(max_length=200)
    word1_suffix = models.CharField(max_length=200,blank=True,null=True)
    word2 = models.CharField(max_length=200)
    word2_suffix = models.CharField(max_length=200,blank=True,null=True)
    units = models.ManyToManyField(Unit)
    #pos = models.CharField(max_length=20,blank=True,null=True)
 
    def __unicode__(self):
        s = self.word1
        if self.word1_suffix:
            s += " (" + self.word1_suffix + ")"
        s += " = " + self.word2
        return s
        
        


#~ class UnitForm(forms.ModelForm):
  
    #~ class Meta:
        #~ model = Unit

    #~ def clean_parent(self):
        #~ p = self.cleaned_data.get("parent")
        #~ if p == self.instance:
            #~ raise forms.ValidationError("Parent cannot be self")
        #~ l=[]
        #~ while p is not None:
            #~ if p in l:
                #~ raise forms.ValidationError("Parent recursion")
            #~ if len(l) > MAX_NESTING_LEVEL:
                #~ raise forms.ValidationError("Nesting level")
            #~ l.append(p)
            #~ p=p.parent
        #~ return self.cleaned_data


#
# reports definition
#

class Units(reports.Report):
    model = Unit
    #model_form = UnitForm
    order_by = "id"
    column_names = "id title name parent seq format"

class UnitsPerParent(reports.Report):
    #model_form = UnitForm
    column_names = "id title name seq format parent"
    order_by = "seq"
    master = Unit
    model = Unit
    
    def __init__(self,parent,**kw):
        self.parent=parent
        reports.Report.__init__(self,**kw)
        
    #~ def get_queryset(self):
        #~ return Unit.objects.filter(parent=self.parent).order_by("seq")
    #~ queryset=property(get_queryset)

class Entries(reports.Report):
    model = Entry
    #model_form = forms.models.modelform_factory(Entry)

#
# menu setup
#
def lino_setup(lino):
    m = lino.add_menu("voc","Vocabulary",
      can_view=perms.is_authenticated)
    m.add_action(Units(),label="List of All Units",)
    m.add_action(UnitsPerParent(None),name="tree",
        label="Table of Contents")
    m.add_action(Entries(),label="List of Entries",)
