raise "NOT YET CONVERTED"

from lino import adamo
from lino.adamo.table import MemoTable,Table,TreeTable,LinkTable
from lino.adamo.datatypes import *

from lino.sprl.plugins.addrbook import PERSONS

class TOPICS(Table):
   def init(self):
      self.id = Field( IntType())
      self.name_en = Field( StringType())
      # self.addDetail('parents',"TOPIC2TOPIC",True)
      
## class TOPIC2TOPIC(LinkTable):
##    def __init__(self):
##       self.__init__(self,"TOPIC","TOPIC")
##    def init(self):
##       self.p_id = Field( IntType())

class DBITEMS(MemoTable,TreeTable):
   def init(self):
      TreeTable.init(self)
      MemoTable.init(self)
      #self.super_id = Field(StringType()).setSticky()
      self.id = Field(StringType())

class FILES(MemoTable):
   def init(self):
      MemoTable.init(self)
      self.id = Field(StringType())

class CLASSES(MemoTable,TreeTable):
   def init(self):
      TreeTable.init(self)
      MemoTable.init(self)
      self.id = Field(StringType())
      # self.file_id = Field(StringType()).setSticky()
      #self.super_id = Field(StringType())
      
   def link(self,db):
      TreeTable.link(self,db)
      MemoTable.link(self,db)
      self.file = Pointer(db.FILES,"classes")
      
class METHODS(MemoTable):
   def init(self):
      MemoTable.init(self)
      self.name = Field(StringType())
      #self.class_id = Field(StringType()).setSticky()
   def link(self,db):
      self.addPointer("class",db.CLASSES,"methods")
      self.setPrimaryKey("name class")

class CHANGES(MemoTable):
   def init(self):
      MemoTable.init(self)
      self.date = Field(DateType()).setSticky()
      self.id = Field(AutoType())

   def link(self,db):
      self.addPointer("version",VERSIONS,"changes")
      self.addPointer("author",PERSONS,"changes")
      

class VERSIONS(Table):
   def init(self):
      self.major = Field( IntType()).setSticky()
      self.minor = Field( IntType()).setSticky()
      self.release = Field( IntType())
      #self.title = Field(StringType())
      self.date = Field(DateType())
      self.setPrimaryKey('major minor release')
      
METHODS =  METHODS()
CLASSES= CLASSES()
FILES =  FILES()
VERSIONS =  VERSIONS()
CHANGES = CHANGES()
FILES2CHANGES = LinkTable(FILES,"changes", CHANGES,"files")

      
DBITEMS = DBITEMS()
TOPICS  = TOPICS()
TOPIC2TOPIC = LinkTable(TOPICS,"parents", TOPICS,"childTopics")
   
