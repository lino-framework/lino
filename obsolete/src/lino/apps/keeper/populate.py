#coding: latin1
## Copyright 2005-2006 Luc Saffre 

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

import sys
import os
opj = os.path.join
import codecs
import re

from lino.adamo.ddl import *
from lino.console.task import Progresser
#from lino.tools.msword import MsWordDocument
#from lupy.index.documentwriter import standardTokenizer
import keeper_tables as tables
from lino.tools.guessenc.guesser import EncodingGuesser

def standardTokenizer(string):
    """Yield a stream of downcased words from a string."""
    # copied from lupy.index.documentwriter
    r = re.compile("\\w+", re.U)
    tokenstream = re.finditer(r, string)
    for m in tokenstream:
        yield m.group().lower() 


class VolumeVisitor(Progresser):
    
    def __init__(self,vol):
        Progresser.__init__(self)
        self.volume = vol
        dbc=self.volume.getContext()
        self.ftypes = dbc.query(tables.FileType)
        self.files = dbc.query(tables.File)
        self.dirs = dbc.query(tables.Directory)

    def run(self):
        #self.task=task
        if len(self.volume.directories()) > 0:
            self.freshen(unicode(self.volume.path))
        else:
            self.load(unicode(self.volume.path))

##     def getLabel(self):
##         return "Loading "+str(self.volume)

##     def prune_dir(self,dirname):
##         return dirname in ('.svn',)

##     def status(self,msg,*args):
##         self.session.status(msg,*args)
##         self.breathe()

            
    def freshen(self,fullname,shortname=None,dir=None):
        self.status(fullname)
        if self.volume.ignoreByName(shortname): return
        if os.path.isfile(fullname):
            row = self.files.peek(dir,shortname)
            if row is None:
                row = self.files.appendRow(name=shortname,dir=dir)
            row.readTimeStamp(self,fullname)
        elif os.path.isdir(fullname):
            row = self.dirs.findone(volume=self.volume,
                                    parent=dir,name=shortname)
            if row is None:
                row = self.dirs.appendRow(name=shortname,
                                          parent=dir,
                                          volume=self.volume)
                
            #self.visit_dir(row,fullname)
            for fn in os.listdir(fullname):
                self.freshen(os.path.join(fullname,fn), fn, row)
        else:
            self.session.error("%s : no such file or directory",
                               fullname)

    def load(self,fullname,shortname=None,dir=None):
        self.status(fullname)
        if self.volume.ignoreByName(shortname): return
        if os.path.isfile(fullname):
            row = self.files.appendRow(name=shortname,dir=dir)
            row.readTimeStamp(self,fullname)
        elif os.path.isdir(fullname):
            row = self.dirs.appendRow(name=shortname,
                                      parent=dir,
                                      volume=self.volume)
            assert row.parent == dir
            for fn in os.listdir(fullname):
                self.load(os.path.join(fullname,fn), fn, row)
        else:
            self.session.error("%s : no such file or directory",fullname)


class FileVisitor: # (Task):
    # used?
    def __init__(self,vol):
        #Task.__init__(self)
        self.volume = vol
        self.encodingGuesser = EncodingGuesser()

    def looper(self,task):
        self.task=task
        sess = self.volume.getContext()
        #from lino.apps.keeper import tables 
        self.ftypes = sess.query(tables.FileType)
        self.files = sess.query(tables.File)
        self.dirs = sess.query(tables.Directory)
        self.words = sess.query(tables.Word)
        self.occurences = sess.query(tables.Occurence)
        self.volume.directories().deleteAll()
        #for row in self.dirs.query(volume=self.volume):
        #    row.delete()
        self.visit(self.volume.path,"")

##     def getLabel(self):
##         return "Loading "+self.volume.getLabel()

    def visit_file(self,fileRow,name):
        base,ext = os.path.splitext(name)
        #
        if ext.lower() == ".txt":
            self.status(name)
            s = open(name).read()
            coding = self.encodingGuesser.guess(name,s)
            self.status("%s: %s", name,coding)
            #print name,":",coding
            if coding:
                tokens = standardTokenizer(s.decode(coding))
            else:
                tokens = standardTokenizer(s)
            
            #coding = guesscoding(name)
            #f = codecs.open(name,encoding=coding)
            #tokens = standardTokenizer(f.read())
            #tokens = open(name).read().split()
            self.loadWords(fileRow,tokens)
##             count = 0
##             for ln in open(name).readlines():
##                 for w in ln.split():
##                     count += 1
##             self.verbose("%s contains %d words.", name, count)
        elif ext == ".doc":
            self.status("Ignoring MS-Word %s.", name)
            #msdoc = MsWordDocument(name)
            #fileRow.title = msdoc.title
            #self.loadWords(fileRow,msdoc.content.split())
        else:
            self.status("Ignoring unknown file %s.", name)
                    
    def loadWords(self,fileRow,tokens):
        #self.status("%s : %d words",fileRow.name,len(tokens))
        #print fileRow.path(), ".occurences.deleteAll()"
        fileRow.occurences.deleteAll()
        #self.occurences.query(file=deleteRows(file=fileRow)
        pos = 0
        for token in tokens:
            pos += 1
            self.status(fileRow.path()+": "+token)
            word = self.words.peek(token)
            if word is None:
                word = self.words.appendRow(id=token)
            #elif word.ignore:
            #    continue
            fileRow.occurences.appendRow(word=word, pos=pos)

    

encodingGuesser = EncodingGuesser()

def get_reader(fullname):
    base,ext = os.path.splitext(fullname)
    try:
        return readers[ext.lower()]
    except KeyError,e:
        return non_reader

    
def read_content(sess,fileInstance,fullname):
    r=get_reader(fullname)
    return r(sess,fileInstance,fullname)
    
    
def non_reader(sess,fileInstance,fullname):
    sess.status("Not reading %s",fullname)
    
def doc_reader(sess,fileInstance,fullname):
    sess.status("Not yet reading %s",fullname)
    
def txt_reader(sess,fileInstance,fullname):
    
    s = open(fullname).read()
    coding = encodingGuesser.guess(fullname,s)
    sess.status("%s: %s", fullname,coding)
    if coding:
        s=s.decode(coding)
    return s


def pdf_reader(sess,fileInstance,fullname):
    s=os.popen(r"s:\xpdf\pdftotext %s -" % fullname).read()
    return s.decode(sys.getfilesystemencoding())

readers = {
    '.pdf' : pdf_reader,
    '.txt' : txt_reader,
    '.doc' : doc_reader,
    }


        
