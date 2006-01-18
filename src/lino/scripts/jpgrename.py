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

import os
from PIL import Image, ImageWin
from PIL.TiffImagePlugin import DATE_TIME

from lino.console.application import Application, UsageError


class MyException(Exception):
    pass

def dt2filename(s):
    a = s.split()
    if len(a) != 2: return None
    d=a[0].split(':')
    if len(d) != 3: return None
    t=a[1].split(':')
    if len(t) != 3: return None
    return '_'.join(d)+'-'+'_'.join(t)+'.jpg'

def avinewname(root,name):
    pass

def jpgnewname(root,name):
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
    nfn=dt2filename(exif[DATE_TIME])
    if nfn is None:
        raise MyException(
            '%s: could not parse DATE_TIME "%s"' \
            % (filename, exif[DATE_TIME]))
    return nfn    




class JpgRename(Application):

    name="Lino/jpgrename"

    copyright="""\
Copyright (c) 2002-2005 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    
    usage="usage: lino jpgrename [options] [DIR]"
    description="""\
where DIR (default .) is a directory with .jpg files to rename.
"""
    converters = {
        '.jpg' : jpgnewname,
        '.avi' : jpgnewname,
        }
    
    def setupOptionParser(self,parser):
        Application.setupOptionParser(self,parser)

        parser.add_option(
            "-s", "--simulate",
            help="simulate only, don't do it",
            action="store_true",
            dest="simulate",
            default=False)

    def run(self,sess):
         
        if len(self.args) == 0:
            dirs=['.']
        else:
            dirs=self.args

        for dirname in dirs:
            self.walk(sess,dirname)
            
    def walk(self,sess,dirname):
        for root, dirs, files in os.walk(dirname):
            okay=True
            filenames = {}
            for name in files:
                base,ext = os.path.splitext(name)
                cv = self.converters.get(ext.lower(),None)
                if cv is not None:
                    try:
                        nfn=cv(root,name)
                    except MyException,e:
                        sess.warning(str(e))
                    else:
                        if nfn is None: pass
                        elif nfn == name: pass
                        elif filenames.has_key(nfn):
                            okay=False
                            sess.warning(
                                '%s/%s: duplicate time %s', \
                                root,name,nfn)
                        else:
                            filenames[nfn] = name
            if not okay: return 
            if not sess.confirm(
                "Rename %d files in directory %s ?" % \
                (len(filenames),root)):
                return
            
            for nfn,ofn in filenames.items():
                o=os.path.join(root,ofn)
                n=os.path.join(root,nfn)
                if self.options.simulate:
                    sess.notice("Would rename %s to %s", o,n)
                else:
                    sess.notice("Rename %s to %s", o,n)
                    os.rename(o,n)
                                   

# lino.runscript expects a name consoleApplicationClass
consoleApplicationClass = JpgRename

if __name__ == '__main__':
    consoleApplicationClass().main() 
    
