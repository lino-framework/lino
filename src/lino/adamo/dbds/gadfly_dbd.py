import gadfly

from gandalf import sql_dbd
      
class Cursor(sql_dbd.Cursor):
   def execute(self,query):
      "modified from DBAPI"
      raise MustOverride()
               
      #self.result = ds.GetResult(self)

    
  

   def fetchone(self):
      values = mysql_fetch_row(query.result.handle)
      if values == None: return None
      self.rownumber += 1
      i = 0
    query.row = array()
    query.row['_new'] = FALSE
    for field in query.leadTable.fields:
      query.row[field.name] = row[i]
      i++
    
    for join in query.leadTable.joins :
      joinRow = array()
      empty = TRUE
      for field in join.toTable.fields:
        value = field.type.str2value(row[i])
        joinRow[field.name] = value
        i++
        if value != None: empty = FALSE
      
      if empty : joinRow = NULL
      query.row[join.alias] = joinRow
    
    return TRUE
  

   def fetchone(self):
      if self.rowcount == -1:
         raise "there are no rows"
      if self.rownumber == self.rowcount:
         return None
      self.rownumber += 1
      self.row = ...
      self.trigger("AfterSkip",self.row)
      return 
      

class Connection(dbd_sql.Connection):
   def __init__(self,dbname,dbpath):
      self.dbconn = gadfly.gadfly()
      self.dbconn.startup(dbname,dbpath)
      self.dbcursor = self.dbconn.cursor()

   def sql_exec(self,sql):
      self.dbcursor.execute(sql)

   def commit(self):
      self.dbconn.commit()




## def Peek(table,id,columns='*') :
##     sql = 'SELECT '
##     sep = ''
##     for comp in table.comps:
##       sql = sql + sep
##         + table.name + '.' + comp.name
##       ## + ' AS ' + this.name + '_' + fld.name
##       sep = ','
    
##     sql = sql + ' FROM ' + table.name
##     pkeys = table.GetPrimaryKey()
##     sep = ' WHERE '
##     i = 0
##     for pk in pkeys:
##       type = table.fields[pk].type
##       sql += sep + pk + '=' + type.to_sql(id[i])
##       sep = ' AND '
##       i+=1
    
##     result = self.sql_select(sql)
##     if ( mysql_num_rows(result)!=1 )
##       return NULL
## ##        trigger_error(sql.' returned '
## ##                      .mysql_num_rows(result).' rows',
## ##                      E_USER_ERROR)
##     return mysql_fetch_array(result,MYSQL_ASSOC)
  


  

