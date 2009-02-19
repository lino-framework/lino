## Copyright 2003-2005 Luc Saffre

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
import gadfly

from lino.adamo.sql import SqlConnection
from lino.adamo import DatabaseError


# from lino.ui import console
# import console to make sure that sys.setdefaultencoding() is done
# because sqlite.Connection() will use this as default encoding.
        

class Connection(SqlConnection):
    
    def __init__(self,ui,dbname="temp",
                 dbdir=r"c:\temp\gadflydb"):
        SqlConnection.__init__(self,ui)
        #self.dbapi = gadfly
        #self._isTemporary = isTemporary
        self._mtime = 0.0
        self._dbname = dbname
        self._dbdir=dbdir

        try:
            self._dbconn=gadfly.gadfly(dbname,dbdir)
            self._mtime = 0
            self._status = self.CST_OPENED
        except gadfly.Error,e:
            self._dbconn = gadfly.gadfly()
            self._dbconn.startup(dbname,dbdir)


    def sql_exec_really(self,sql):
        csr = self._dbconn.cursor()
        try:
            csr.execute(sql)
            return csr
        except gadfly.Error,e:
            raise DatabaseError(sql + "\n" + str(e))

    def commit(self):
        #print "commit"
        self._dbconn.commit()

    def close(self):
        self._status = self.CST_CLOSING
        self._dbconn.commit()
        self._dbconn.close()
        self._status = self.CST_CLOSED
        #self._dbconn = None
##         if self._isTemporary and self._filename is not None:
##             os.remove(self._filename)

    def getModificationTime(self,table):
        return self._mtime

    def checkTableExist(self,tableName):
        return tableName in self._dbconn.table_names()
    






## from gandalf import sql_dbd
      
## class Cursor(sql_dbd.Cursor):
##    def execute(self,query):
##       "modified from DBAPI"
##       raise MustOverride()
               
##       #self.result = ds.GetResult(self)

    
  

##    def fetchone(self):
##       values = mysql_fetch_row(query.result.handle)
##       if values == None: return None
##       self.rownumber += 1
##       i = 0
##     query.row = array()
##     query.row['_new'] = FALSE
##     for field in query.leadTable.fields:
##       query.row[field.name] = row[i]
##       i++
    
##     for join in query.leadTable.joins :
##       joinRow = array()
##       empty = TRUE
##       for field in join.toTable.fields:
##         value = field.type.str2value(row[i])
##         joinRow[field.name] = value
##         i++
##         if value != None: empty = FALSE
      
##       if empty : joinRow = NULL
##       query.row[join.alias] = joinRow
    
##     return TRUE
  

##    def fetchone(self):
##       if self.rowcount == -1:
##          raise "there are no rows"
##       if self.rownumber == self.rowcount:
##          return None
##       self.rownumber += 1
##       self.row = ...
##       self.trigger("AfterSkip",self.row)
##       return 
      

## class Connection(dbd_sql.Connection):
##    def __init__(self,dbname,dbpath):
##       self.dbconn = gadfly.gadfly()
##       self.dbconn.startup(dbname,dbpath)
##       self.dbcursor = self.dbconn.cursor()

##    def sql_exec(self,sql):
##       self.dbcursor.execute(sql)

##    def commit(self):
##       self.dbconn.commit()




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
  


  

