import warnings
warnings.filterwarnings("ignore",
                        "DB-API extension",
                        UserWarning,
                        "sqlite")
import os
import sqlite


testdata = [
   (1, "the first",  "2002-08-20"),
   (2, "the second", "2002-08-30"),
   (2, "the third",  "2003-04-03"),
]

filename = "tmp.db"
conn = sqlite.connect(filename)


cursor = conn.cursor()
cursor.execute("""CREATE TABLE TEST (
  id int,
  name varchar(80),
  date date)
""")
for row in testdata:
   cursor.execute("""INSERT INTO TEST VALUES (
   %d, "%s", "%s")""" % row)

cursor.close()
conn.commit()

cursor = conn.cursor()
cursor.execute("SELECT * FROM TEST")
for row in cursor:
   print row


cursor = conn.cursor()
cursor.execute("""SELECT * FROM sqlite_master WHERE type='table' 
UNION ALL SELECT * FROM sqlite_temp_master WHERE type='table'
ORDER BY name;
""")
print "\t".join([x[0] for x in cursor.description])
for row in cursor:
   print "\t".join([repr(x) for x in row])



conn.close()
os.remove(filename)
