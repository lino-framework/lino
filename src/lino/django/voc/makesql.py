#coding: utf-8
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




UNIT_DATA = (
  ("1", u"Leçon 1"),
  ("2", u"Leçon 2"),
  ("3", u"Leçon 3"),
  ("4", u"Leçon 4"),
  ("5", u"Leçon 5"),
  ("6", u"Leçon 6"),
)
UNIT_STMT = "INSERT INTO voc_unit (name, title) VALUES %s;\n"

#~ ENTRY_DATA = (
  #~ (1, "je", "", "mina" ),
  #~ (1, "tu", "", "sina" ),
  #~ (1, "il", "", "tema" ),
  #~ (1, "pullover", "nm", "kampsun" ),
#~ )

#ENTRY_STMT = "INSERT INTO voc_entry (unit_id, question,question_type,answer) VALUES %s;\n"

ENTRY_STMT = """\
INSERT INTO voc_entry (id, question,answer,unit_id) 
VALUES (%d,"%s","%s",%d);
"""


def assql(x):
  if type(x) == int:
    return str(x)
  if type(x) == tuple:
    return "(" + ",".join([assql(y) for y in x]) + ")"
  return '"' + x.encode('utf-8') + '"' 
  
f=file("sql/unit.sql","w")
for e in UNIT_DATA:
    f.write(UNIT_STMT % assql(e))
f.close()

#~ f=file("sql/entry.sql","w")
#~ for e in ENTRY_DATA:
    #~ f.write(ENTRY_STMT % assql(e))
    
f=file("sql/entry.sql","w")
r = unicode_csv_reader(codecs.open('voc.csv','r',"utf-8"))
titles = r.next()
print titles
for i,q,a,u in r:
    if len(i) and len(u):
        f.write(ENTRY_STMT % (int(i),q.encode('utf-8'),a.encode('utf-8'),int(u)))

    

