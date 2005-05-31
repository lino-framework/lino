#coding: latin1
## Copyright 2005 Luc Saffre 

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

from lino.adamo.ddl import *
from lino.misc.jobs import Task
#from lino.tools.msword import MsWordDocument
from lino.guessenc.guesser import EncodingGuesser
from lupy.index.documentwriter import standardTokenizer


    
class VolumeVisitor(Task):
    
    def __init__(self,vol):
        Task.__init__(self)
        self.volume = vol

    def start(self):
        from lino.apps.keeper import tables 
        sess = self.volume.getSession()
        self.ftypes = sess.query(tables.FileTypes)
        self.files = sess.query(tables.Files)
        self.dirs = sess.query(tables.Directories)
        if len(self.volume.directories) > 0:
            self.freshen(self.volume.path,"")
        else:
            self.load(self.volume.path,"")

    def getLabel(self):
        return "Loading "+self.volume.getLabel()

    def freshen(self,fullname,shortname,dir=None):
        self.status(fullname)
        if os.path.isfile(fullname):
            row = self.files.peek(dir,shortname)
            if row is None:
                row = self.files.appendRow(name=shortname,dir=dir)
            self.readTimeStamp(row,fullname)
        elif os.path.isdir(fullname):
            row = self.dirs.findone(parent=dir,name=shortname)
            if row is None:
                row = self.dirs.appendRow(name=shortname,
                                          parent=dir,
                                          volume=self.volume)
                
            self.visit_dir(row,fullname)
        else:
            self.error("%s : no such file or directory",fullname)

    def load(self,fullname,shortname,dir=None):
        self.status(fullname)
        if os.path.isfile(fullname):
            if self.reloading:
                row = self.files.peek(dir,shortname)
            else:
                row=None
            if row is None:
                row = self.files.appendRow(name=shortname,dir=dir)
            #self.visit_file(row,fullname)
            self.readTimeStamp(row,fullname)
        elif os.path.isdir(fullname):
            #print "findone(",dict(parent=dir,name=shortname),")"
            if self.reloading:
                row = self.dirs.findone(parent=dir,name=shortname)
            else:
                row=None
            if row is None:
                row = self.dirs.appendRow(name=shortname,
                                          parent=dir,
                                          volume=self.volume)
                assert row.parent == dir
            self.visit_dir(row,fullname)
        else:
            self.error("%s : no such file or directory",fullname)

    def visit_dir(self,dirRow,fullname):
        #self.status("visit_dir " + fullname)
        for fn in os.listdir(fullname):
            self.visit(
                os.path.join(fullname,fn),
                fn,
                dirRow)
        
    def readTimeStamp(self,fileRow,fullname):
        try:
            st = os.stat(fullname)
            sz = st.st_size
            mt = st.st_mtime
        except OSError,e:
            self.error("os.stat('%s') failed" % fullname)
            return
        row.mtime = x

class FileVisitor(Task):
    
    def __init__(self,vol):
        Task.__init__(self)
        self.volume = vol
        self.encodingGuesser = EncodingGuesser()

    def start(self):
        sess = self.volume.getSession()
        from lino.apps.keeper import tables 
        self.ftypes = sess.query(tables.FileTypes)
        self.files = sess.query(tables.Files)
        self.dirs = sess.query(tables.Directories)
        self.words = sess.query(tables.Words)
        self.occurences = sess.query(tables.Occurences)
        self.volume.directories.deleteAll()
        #for row in self.dirs.query(volume=self.volume):
        #    row.delete()
        self.visit(self.volume.path,"")

    def getLabel(self):
        return "Loading "+self.volume.getLabel()

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

    


        
