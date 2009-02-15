## Copyright 2006-2009 Luc Saffre

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
import tempfile
from ConfigParser import SafeConfigParser, DEFAULTSECT

lino_home = os.path.abspath(
    os.path.join( os.path.dirname(__file__),"..",".."))

class Section:
    def __init__(self,parser,name,**kw):
        self.name=name
        self.parser=parser
        parser.add_section(self.name)
        for k,v in kw.items():
            parser.set(self.name,k,v)
    def get(self,name):
        return self.parser.get(self.name,name)

config = SafeConfigParser()

paths = Section(config,'paths',
                lino_home=lino_home,
                tempdir=tempfile.gettempdir(),
                rtlib_path=os.path.join(lino_home, "rtlib"),
                tests_path=os.path.join(lino_home, "tests"),
                docs_path=os.path.join(lino_home, "docs"),
                src_path=os.path.join(lino_home, "src"),
                webhome=r"u:\htdocs\timwebs\lino",
                )

win32=Section(config,'win32',
              postscript_printer="Lexmark Optra PS")

#~ prnprint=Section(config,'prnprint',
              #~ fontWeights=None,
              #~ fontSize=12,
              #~ fontName="Courier New"
              #~ )

## gendoc = Section(config,'gendoc',
##                 basepath=paths.get('tempdir'))

#config.add_section('forms')
#config.set('forms','wishlist','wx tix cherrypy console')

#config.readfp(open('defaults.cfg'))
config.read( [
    os.path.join(lino_home,'lino.cfg'),
    os.path.expanduser('~/lino.cfg'),
    'lino.cfg'
    ])

get=config.get

def tempdirfilename(name):
    fn=os.path.join(paths.get('tempdir'),name)
    #print "tempdirfilename", fn
    return fn

