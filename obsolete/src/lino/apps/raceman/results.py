## Copyright 2004-2005 Luc Saffre 

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
import sys


from lino.ui import console
from lino.oogen import Document
from lino import adamo

from schema import makeSchema

from lino.schemas.sprl.races import Races, RaceTypes, Categories, \
     Participants, Persons, Clubs

from lino.tools import dbfreader

opj = os.path.join


def main2(dbfpath,dbpath):

    schema = makeSchema(dbfpath)
    
    sess = schema.quickStartup( filename=opj(dbpath,"raceman.db"))

    sess.progress("Generating reports...")
    if True:
    
        doc = Document("1")
    
        doc.h(1,"Raceman Generating OpenOffice documents")

        main3(doc,sess)
        outFile = opj(dbpath,"raceman_report.sxc")
        doc.save(outFile,showOutput=True)
    else:
        main3(console,sess)


def main3(doc,sess):
    
    race = sess.peek(Races,53)
    
    assert race is not None

    race.writeReport(doc)
    




    

def main(argv):

    parser = console.getOptionParser(
        usage="usage: %prog [options] DBFPATH",
        description="""\
where DBFPATh is the directory containing TIM files""")
    
    parser.add_option("-t", "--tempdir",
                      help="""\
directory for raceman files""",
                      action="store",
                      type="string",
                      dest="tempDir",
                      default=r'c:\temp')
    
    (options, args) = parser.parse_args(argv)

    if len(args) == 1:
        dbfpath = args[0]
    else:
        dbfpath = r"c:\temp\timrun"
        
    main2(dbfpath,options.tempDir)
    




if __name__ == '__main__':
    console.copyleft(name="Lino/Raceman", years='2002-2005')
    main(sys.argv[1:])




