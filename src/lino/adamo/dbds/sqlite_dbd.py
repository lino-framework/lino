## Copyright Luc Saffre 2003-2005

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
#import time
import warnings
warnings.filterwarnings("ignore",
                        "DB-API extension",
                        UserWarning,
                        "sqlite")

import sqlite
from types import TupleType

from lino.adamo.sql import SqlConnection
from lino.adamo import DatabaseError


from lino.ui import console

# import console to make sure that sys.setdefaultencoding() is done
# because sqlite.Connection() will use this as default encoding.
        

class Connection(SqlConnection):
    
    def __init__(self,schema,filename=None):
        SqlConnection.__init__(self,schema)
        self.dbapi = sqlite
        #self._isTemporary = isTemporary
        self._mtime = 0.0
        self._filename = filename
        if filename is None:
            # assert isTemporary
            filename=":memory:"
        elif os.path.exists(filename):
            self._mtime = os.stat(filename).st_mtime
            self._status = self.CST_OPENED
            
        try:
            self._dbconn = sqlite.connect(filename)
                                          #client_encoding='latin1')
        except sqlite.DatabaseError,e:
            raise DatabaseError(filename + ":" +str(e))


    def __str__(self):
        filename = self._filename
        if filename is None:
            filename = '(stdout)'
        return "%s (SQLite)" % filename
        
        
        #print "SQLite database : " + os.path.abspath(filename)
        # self._dbcursor = self._dbconn.cursor()

##     def isVirtual(self):
##         return self._filename is None

    def sql_exec_really(self,sql):
##         if self._filename is None:
##             print sql+";"
##             return
        csr = sqlite.Cursor(self._dbconn,TupleType)
        # print "sqlite_dbd.py:" + sql
        try:
##              if "PARTNERS" in sql:
##                  print "sqlite_dbd.py:" + sql
            csr.execute(sql)
            return csr
        except sqlite.DatabaseError,e:
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
        sql = """SELECT rootpage
        FROM sqlite_master
        where tbl_name='%s' AND type='table';""" % tableName
        csr = self.sql_exec(sql)
        if csr is None:
            return False
        if csr.rowcount == 0:
            return False
        if csr.rowcount == 1:
            return True
        raise DatabaseError('"%s" returned %d' % (sql,csr.rowcount))
    

  

##  def executeCreateTable(self,table):
        
##      try:
##          self.sql_exec("DROP TABLE %s" % table.getName())
##      except sqlite.DatabaseError:
##          pass
##      SqlConnection.executeCreateTable(self,table)


    def checkDatabaseSchema(self,db):
        # not yet usable
        csr = self.sql_exec("""\
        SELECT * FROM sqlite_master
            WHERE type='table'
        UNION ALL
        SELECT * FROM sqlite_temp_master
        WHERE type='table' '
        ORDER BY name;
        """)
        print csr
