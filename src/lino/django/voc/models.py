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

from django.db import models
from django.db.models.signals import post_syncdb

import re
voc_splitter1=re.compile("^(.*)\s+\((.*)\)\s*:\s*(.+)",re.DOTALL)
voc_splitter2=re.compile("^(.*)\s*:\s*(.+)",re.DOTALL)


# imports needed for rst_load()
from docutils import core 
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from docutils.parsers.rst import directives
from docutils import nodes 
from docutils.parsers import rst
class question(nodes.admonition): pass
class answer(nodes.admonition): pass
class vocabulary(nodes.admonition): pass
class remark(nodes.admonition): pass
class Special(BaseAdmonition):
    has_content = True
class Question(Special):
    node_class = question
class Answer(Special):
    node_class = answer
class Vocabulary(Special):
    node_class = vocabulary
class Remark(Special):
    node_class = remark
directives.register_directive("question", Question)
directives.register_directive("answer", Answer)
directives.register_directive("vocabulary", Vocabulary)
directives.register_directive("remark", Remark)


class Unit(models.Model):
    title = models.CharField(max_length=200,blank=True,null=True)
    parent = models.ForeignKey("Unit",blank=True,null=True,
                  related_name="children")
    seq = models.IntegerField(default=1)
    body = models.TextField(blank=True,null=True)
    question = models.TextField(blank=True,null=True)
    answer = models.TextField(blank=True,null=True)
    remark = models.TextField(blank=True,null=True)
    vocabulary = models.TextField(blank=True,null=True)
    
    def __unicode__(self):
        s=self.fullseq()
        if self.title:
            s += ". " + self.title
        return s
        
    def fullseq(self):
        if self.parent:
            s=self.parent.fullseq()+"."
        else:
            s=""
        s += str(self.seq)
        return s

    @models.permalink
    def get_absolute_url(self):
        return ('lino.django.voc.views.unit_detail', [str(self.id)])
        
    def prettyprint(self,level=0):
        s="  "*level+unicode(self)
        children=[u.prettyprint(level+1) for u in self.children.all()]
        if len(children):
            s += "\n" + ("\n"+"  "*level).join(children) 
        return s
        
    def save(self, force_insert=False, force_update=False):
        super(Unit, self).save(force_insert, force_update) 
        self.after_save()
                    
    def after_save(self):
        #print "after_save:", self
        self.entry_set.all().delete()
        if self.vocabulary:
            for line in self.vocabulary.splitlines():
                self.add_entry(line.strip())
    after_save.alters_data = True
                    
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
              
    # rst_load() doesn't yet work correctly 
    # for example it simply ignores tables...
    def load_rst(self,input_file,encoding="utf8"):
        f=codecs.open(input_file,"r",encoding)
        doctree = core.publish_doctree(f.read())
        self.load_tree(doctree)
        
    def load_tree(self,doctree):
        seq=0
        if not self.body:
            self.body=""
        for elem in doctree:
            if isinstance(elem,nodes.Structural):
                seq += 1
                self.save()
                child=Unit(parent=self,seq=seq)
                child.load_tree(elem)
            elif isinstance(elem,nodes.Titular):
                if self.title:
                    raise "duplicate title in %s" % (unit.title)
                self.title=elem.rawsource
                #self.load_tree(elem)
            elif isinstance(elem,nodes.admonition):
                fieldname=elem.__class__.__name__
                if getattr(self,fieldname):
                    raise "duplicate %s directive in %s" % (
                      fieldname,self.title)
                setattr(self,fieldname,elem.rawsource)
                
            elif isinstance(elem,nodes.Text):
                self.body += elem.rawsource
            elif isinstance(elem,nodes.block_quote):
                self.body += elem.rawsource
            elif isinstance(elem,nodes.system_message):
                self.body += elem.rawsource
            elif isinstance(elem,nodes.paragraph):
                self.body += elem.rawsource
                
            elif isinstance(elem,nodes.table):
                self.body += elem.rawsource
                #self.load_tree(elem)
            elif isinstance(elem,nodes.tgroup):
                #self.body += elem.rawsource
                self.load_tree(elem)
            elif isinstance(elem,nodes.thead):
                #self.body += elem.rawsource
                self.load_tree(elem)
            elif isinstance(elem,nodes.tbody):
                #self.body += elem.rawsource
                self.load_tree(elem)
            elif isinstance(elem,nodes.colspec):
                #self.body += elem.rawsource
                self.load_tree(elem)
            elif isinstance(elem,nodes.row):
                #self.body += elem.rawsource
                self.load_tree(elem)
            elif isinstance(elem,nodes.entry):
                self.body += elem.rawsource
                #self.load_tree(elem)
                
            #~ elif isinstance(elem,nodes.Element):
                #~ self.body += elem.rawsource
                #self.load_tree(elem)
            else:
                print "unhandled:", elem.__class__
        self.save()
        if self.id == 13:
            print self.body
                    
        
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
