# -*- coding: iso-8859-1 -*-

## Copyright 2005-2009 Luc Saffre 

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

import os
import time
import datetime
from PIL import Image, ImageWin
from PIL.TiffImagePlugin import DATE_TIME

from lino.console.application import Application, UsageError

class MyException(Exception):
    pass

def avitime(root,name):
    pass

def wavtime(root,name,seq):
    # this is wrong.
    # i want to know how the creation date is stored in .wav files
    filename=os.path.join(root, name)
    sti=os.stat(filename)
    return time.localtime(sti.st_ctime)
    #return time.strftime("%Y_%m_%d-%H_%M_%S.wav",ct)
    

class JpgRename(Application):

    name="Lino/jpgrename"

    copyright="""\
Copyright (c) 2002-2009 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    
    usage="usage: lino jpgrename [options] [DIR]"
    description="""\
where DIR (default .) is a directory with .jpg files to rename.
"""
    def setupOptionParser(self,parser):
        Application.setupOptionParser(self,parser)

        parser.add_option(
            "-s", "--simulate",
            help="simulate only, don't do it",
            action="store_true",
            dest="simulate",
            default=False)

        parser.add_option(
            "-d", "--timediff",
            help="correct EXIF time by adding TIMEDIFF minutes",
            action="store", type="int",
            dest="timediff",
            default=0)
        
        parser.add_option(
            "--suffix",
            help="add SUFFIX to each filename",
            action="store", type="string",
            dest="suffix",
            default="")

    def run(self):
         
        self.converters = {
            '.jpg' : self.jpgtime,
            '.avi' : avitime,
            '.wav' : wavtime,
            }

        if len(self.args) == 0:
            dirs=['.']
        else:
            dirs=self.args

        for dirname in dirs:
            self.walk(dirname)
            
    def walk(self,dirname):
        for root, dirs, files in os.walk(dirname):
            filedates = []
            for name in files:
                base,ext = os.path.splitext(name)
                cv = self.converters.get(ext.lower(),None)
                if cv is not None:
                    try:
                        dt=cv(root,name)
                    except MyException,e:
                        self.warning(str(e))
                    else:
                        if dt is None: pass
                        else:
                            filedates.append((dt,base,ext))
            if len(filedates) == 0:
                self.notice("Nothing to do.")
                return
                
            filedates.sort(lambda a,b : cmp(a[0],b[0]))
            
            if not self.confirm(
                "Rename %d files in directory %s ?" % \
                (len(filedates),root)):
                return
            seq=0
            for dt,oldname,ext in filedates:
                seq += 1
                newname=self.dt2filename(dt,seq)
                if self.options.suffix:
                    newname+=self.options.suffix
                o=os.path.join(root,oldname)+ext
                n=os.path.join(root,newname)+ext
                if self.options.simulate:
                    self.notice("Would rename %s to %s", o,n)
                else:
                    self.notice("Rename %s to %s", o,n)
                    try:
                        os.rename(o,n)
                    except WindowsError,e:
                        self.warning(str(e))
                                   
    def dt2filename(self,dt,seq):
        dt += datetime.timedelta(0,0,0,0,self.options.timediff)
        #print '_'.join(d)+'-'+'_'.join(t)+'.jpg', "->", dt.strftime("%Y_%m_%d-%H_%M_%S.jpg")
        #return '_'.join(d)+'-'+'_'.join(t)+'.jpg'
        if True: # my new naming schema
            return dt.strftime("%Y%m%d") + "-%03d" % seq
        else:
            return dt.strftime("%Y_%m_%d-%H_%M_%S")

    def jpgtime(self,root,name):
        filename=os.path.join(root, name)
        try:
            img = Image.open(filename)
        except IOError,e:
            raise MyException(filename + ":" + str(e))
        exif=img._getexif()
        if exif is None:
            raise MyException(filename+ ': no EXIF information found')
        if not exif.has_key(DATE_TIME):
            raise MyException(filename+ ':'+ str(exif.keys()))
        a = exif[DATE_TIME].split()
        if len(a) != 2: 
            raise MyException(filename+ ': invalid DATE_TIME format')
        d=a[0].split(':')
        if len(d) != 3: 
            raise MyException(filename+ ': invalid DATE format')
        t=a[1].split(':')
        if len(t) != 3: 
            raise MyException(filename+ ': invalid TIME format')
        args=[int(x) for x in d] + [int(x) for x in t]
        return datetime.datetime(*args)
        
    def unused(self):
        nfn=self.dt2filename(exif[DATE_TIME])
        if nfn is None:
            raise MyException(
                '%s: could not parse DATE_TIME "%s"' \
                % (filename, exif[DATE_TIME]))
        nfn+= self.options.suffix
        return nfn + ".jpg"

   
def main(*args,**kw):
    JpgRename().main(*args,**kw)
