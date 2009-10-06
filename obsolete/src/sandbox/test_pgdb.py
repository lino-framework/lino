import pgdb
conn = pgdb.connect("localhost:unittest_data:luc")

cursor = conn.cursor()
cursor.execute("""CREATE TABLE TEST (
  id int,
  name varchar(80),
  date date)
""")
cursor.execute("""INSERT INTO TEST VALUES (
1,
"the first",
"2002-08-20")
""")

conn.close()



