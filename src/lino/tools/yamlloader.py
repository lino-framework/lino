# -*- coding: ISO-8859-1 -*-
## Copyright 2007-2008 Luc Saffre

## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
   
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
   
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

    
import sys
import os
import fnmatch
import codecs

import yaml

from lino.console.application import Application, OperationFailed



#DEBUG=False
DEBUG=True
RELAX=False
#RELAX=True


class YamlLoader(Application):
    
    input_encoding="ISO-8859-1"
    
    def setupOptionParser(self,parser):
        Application.setupOptionParser(self,parser)
    
        parser.add_option("-i", "--input", help="""\
        filter input files""",
                     action="store",
                     type="string",
                     dest="inputFiles",
                     default=None)
    

    def add_from_file(self,filename,pfn,yamldict):
        root,ext=os.path.splitext(filename)
        if ext == ".sng":
            adder=self.addsong
        elif ext in [ ".txt" ]:
            if root == "persons":
                adder=self.addperson
            else:
                adder=self.addtext
        else:
            raise OperationFailed("%s : unknown file extension" % filename)
        yamldict['filename']=filename
        yamldict['mtime']=os.path.getmtime(pfn)
        adder(**yamldict)
        
        
    def loadfile(self,filename,input_encoding=None,**kw):
        if self.options.inputFiles is not None:
            if not fnmatch.fnmatch(filename, self.options.inputFiles):
                self.verbose("Skipping file %s",filename)
                return
        if input_encoding is None:
            input_encoding=self.input_encoding
        for path in self.input_dirs:
            pfn=os.path.join(path,filename)
            if os.path.exists(pfn):
                self.notice("Loading input file %s ...",pfn)
                fd = codecs.open(pfn,"r",input_encoding)
                try:
                    for yamldict in yaml.load_all(fd):
                        if type(yamldict) == type({}):
                            for k in yamldict.keys():
                                if k.startswith(";"):
                                    del yamldict[k]
                            yamldict.update(kw)
                        self.add_from_file(filename,pfn,yamldict)
                except Exception,e:
                    if DEBUG:
                        raise
                    elif RELAX:
                        print "RELAX!", pfn+":"+str(e)
                    else:
                        raise OperationFailed(pfn+":"+str(e))
                fd.close()
                return
        raise OperationFailed(
            "%s : file not found in input_dirs (%s)" % (filename,
                                                        self.input_dirs))

        
