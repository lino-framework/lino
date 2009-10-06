import warnings
warnings.filterwarnings("ignore",
                        "DB-API extension",
                        UserWarning,
                        "sqlite")
import sqlite

conn = sqlite.connect("tmp.db")
c = conn.cursor()

c.execute("""\
   create table Partners (
     id int,
     name  char,
     city_id  int,
     nation_id  char
   );
   """)
c.execute("""\
   insert into Partners(id,name,city_id,nation_id)
      values (1,"Luc",1,"ee");
   """)
c.execute("""\
   insert into Partners(id,name,city_id,nation_id)
      values (2,"Paul",2,"be");
   """)
c.execute("""\
   create table Cities (
     id int,
     nation_id  int,
     name char
   );
   """)
c.execute("""\
   insert into Cities (id,nation_id, name)
      values (1,"ee","Tallinn");
   """)
c.execute("""\
   insert into Cities (id,nation_id, name)
   values (2,"be","Eupen");
   """)
c.execute("""\
   create table Nations (
     id char,
     name  char
   );
   """)
c.execute("""\
   insert into Nations (id,name) values ("ee","Eesti");
   """)
c.execute("""\
   insert into Nations (id,name) values  ("be","Belgique");
   """)

c.execute("""
      SELECT Partners.id,
             Partners.name,
             nation.id, 
             city.name,
             nation.name
         FROM Partners
              LEFT JOIN Cities as city on (city.id = Partners.city_id)
              LEFT JOIN Nations as nation on (nation.id = Partners.nation_id)

""")

print c.description
for row in c:
   print row
          
   
