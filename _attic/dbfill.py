def insert():
   print """
   INSERT INTO PROJECTS VALUES (NULL,1,
   %(date)s,
   "%(title)s",
   "%(abstract)s",
   "%(body)s",
   %(stopDate)s
   );
   """ % globals()


   
stopDate="NULL"

date="2002-05-31"
title=""
abstract="""
"""
body="""
"""

   
insert()
