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

from lino.adamo import center

class Connection:

    def __init__(self,schema):
        self.schema = schema
        center.addConnection(self)
        

    def onTableSetup(self,table):
        pass
    
    def create_table(self,table):
        pass
    
    def commit(self):
        pass
    
    def close(self):
        pass

    
    def executeCreateTable(self,table):
        pass
    
    def executeSelect(self,query,
                            limit=None,
                            offset=None):
        raise NotImplementedError
        
    def executeCount(self,query):
        raise NotImplementedError
    
    def executeGetLastId(self,table,knownId=()):
        raise NotImplementedError
        
    def executeInsert(self,table,row):
        raise NotImplementedError
    
    def executeUpdate(self,table,row):
        raise NotImplementedError
    
    def executePeek(self,table,id):
        raise NotImplementedError
    

##  def getConnection(self):
##      return self.conn

##  def newCursor(self,query):
##      return self.conn.newCursor(query)

##      def ui_shutdown(self,ui):
##          return ui.confirm("Shutdown",
##                                  "Are you sure?",
##                                  self.shutdown,
##                                  None)


##  def commit_row(self,cursor,row):
##      if row.IsDirty():
##          if row.IsNew():
##              self.executeInsert(cursor,row)
##              row.SetNew(False)
##          else:
##              self.executeUpdate(cursor,row)
##          row.SetDirty(False)
##      #else:
##      #    raise "No changes need to be commited"
##      # self.commit_row(self.row)


        
