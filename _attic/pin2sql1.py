__doc__ = """
this is the first running version of pin2sql.py
just for historical reasons...
Luc Saffre, June 2002
"""
import sys
import string

sql = """INSERT INTO NEWS VALUES (NULL,
   %(author)s,
   "%(date)s",
   "%(title)s",
   "%(abstract)s",
   "%(body)s"
   );""" 

def error(msg):
   sys.stderr.write(msg)
   sys.exit()

def read_entry():
   d = {}
   d['abstract'] = ""
   d['body'] = ""
   d['title'] = "NULL"
   d['date'] = "NULL"
   d['author'] = "1"
   okay = 0
   while 1:
      line = sys.stdin.readline()
      if line == '' : break
      if line == '\n' : break
      a = line.split(':',1)
      if len(a) != 2:
         error("invalid header line");
      d[a[0]] = a[1]
      okay = 1
      
   abstract = 1
   # whether we are reading the abstract or (if not) the body
   
   while 1:
      line = sys.stdin.readline()
      if line == '' : break
      if line.startswith('----'): break
      if abstract:
         if line == '\n':
            abstract = 0
         else:
            d['abstract'] += line
      else:
         if line == '\n':
            d['body'] += '<p>'
         d['body'] += line

   if okay:
      d['title'] = d['title'].replace('"',r'\"')
      d['body'] = d['body'].replace('"',r'\"')
      d['abstract'] = d['abstract'].replace('"',r'\"')
      print sql % d
   else:
      sys.exit()
         
         
   
   
while 1:
   read_entry()

 
