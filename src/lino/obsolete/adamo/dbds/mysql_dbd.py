from lino.adamo.dbds import sql_dbd
      
class Cursor(sql_dbd.Cursor):

   def executeSelect(self) :
      sql = self.conn.GetSqlSelect(query)
      self.conn.sql_exec(sql)
      #self.dbcursor = self.dbconn.cursor()
      #self.dbcursor.execute(sql)
      

class Connection(sql_dbd.Connection):
   
##    def __init__(self,dbname,dbpath):
##       self.dbconn = gadfly.gadfly()
##       self.dbconn.startup(dbname,dbpath)
##       self.dbcursor = self.dbconn.cursor()
      
#   def __init__(self,host):
#      self.host = host
      
   def sql_exec(self,sql):
      self.host.write(sql)
      
   def cursor(self,query):
      return Cursor(self,query)

