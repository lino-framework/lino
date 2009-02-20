#coding: utf-8
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

import csv
import codecs


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

#~ UNIT_DATA = (
  #~ ("1", u"Leçon 1"),
  #~ ("2", u"Leçon 2"),
  #~ ("3", u"Leçon 3"),
  #~ ("4", u"Leçon 4"),
  #~ ("5", u"Leçon 5"),
  #~ ("6", u"Leçon 6"),
#~ )
#~ UNIT_STMT = "INSERT INTO voc_unit (name, title) VALUES %s;\n"

#~ ENTRY_DATA = (
  #~ (1, "je", "", "mina" ),
  #~ (1, "tu", "", "sina" ),
  #~ (1, "il", "", "tema" ),
  #~ (1, "pullover", "nm", "kampsun" ),
#~ )

#ENTRY_STMT = "INSERT INTO voc_entry (unit_id, question,question_type,answer) VALUES %s;\n"

ENTRY_STMT = "INSERT INTO voc_entry (%s) VALUES (%s);\n"


#~ def assql(x):
  #~ if type(x) == int:
    #~ return str(x)
  #~ if type(x) == tuple:
    #~ return "(" + ",".join([assql(y) for y in x]) + ")"
  #~ return '"' + x.encode('utf-8') + '"' 
  
#~ f=file("sql/unit.sql","w")
#~ for e in UNIT_DATA:
    #~ f.write(UNIT_STMT % assql(e))
#~ f.close()

#~ f=file("sql/entry.sql","w")
#~ for e in ENTRY_DATA:
    #~ f.write(ENTRY_STMT % assql(e))
    
def int2sql(x):
    #print repr(x)
    return str(int(x))
def str2sql(x):
    #return '"' + x.encode('utf-8') + '"' 
    return '"' + x + '"' 
  
fieldmap = dict(
  id=int2sql, 
  word1=str2sql,
  word2=str2sql,
  word1_suffix=str2sql)

r = unicode_csv_reader(codecs.open('voc.csv','r',"utf-8"))
titles = r.next()

fields=[]
i=0
for fieldname in titles:
    converter=fieldmap.get(fieldname,None)
    if converter is not None:
        fields.append( (fieldname,converter,i) )
    i+=1
    
for name,cv,i in fields:
    print i,name
    
sqlcolumns = ",".join([fld[0] for fld in fields])
n=1
f=file("sql/entry.sql","w")
for row in r:
    n+=1
    try:
        sqlvalues=",".join([cv(row[i]) for fn,cv,i in fields])
    except ValueError,e:
        print n,row,e
    else:
        #print sqlvalues
        stmt=ENTRY_STMT % (sqlcolumns,sqlvalues)
        #print stmt
        f.write(stmt.encode("utf-8"))
