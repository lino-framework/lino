import sys
import string
import fileinput

False = 0
True = 1


class PinboardError:
   def __init__(self,msg):
      self.msg = msg

## class Action:
##    def eval(self,expr):
##       return eval(expr)

class Type:
   def get_default(self):
      return None
   
class TextType(Type):
   def pin2value(self,expr):
      if(len(expr)==0) : return None;
      return expr
   def value2sql(self,value):
      if value == None:
         return "NULL"
      if len(value) == 0:
         return 'NULL'
      return '"' + value.replace('"',r'\"') + '"'

class MemoType(TextType):
   def pin2value(self,expr):
      raise PinboardError("Memo fields cannot be in header")
   def get_default(self):
      return ''

class DateType(Type):
   def pin2value(self,expr):
      if len(expr)==0 : return None
      return expr
   def value2sql(self,value):
      if value == None:
         return "NULL"
      return '"' + value + '"'

class IntType(Type):
   def pin2value(self,expr):
      if len(expr)==0 : return None
      return int(expr)
   def value2sql(self,value):
      if value == None:
         return "NULL"
      return str(value)

class AutoType(Type):
   pass

class BoolType(IntType):
   pass

class Field:
   def name2sql(self,name):
      return name
   def __init__(self,type=None,sticky=False):
      if type == None:
         type = TextType()
      self.sticky = sticky
      self.type = type
      
   def pin2value(self,expr):
      return self.type.pin2value(expr)
   def value2sql(self,value):
      return self.type.value2sql(value)
   def get_default(self):
      return self.type.get_default()


class JoinField(Field):
   def __init__(self,toTableName,sep='.',sticky=False):
      self.toTable = app.tables[toTableName]
      self.sticky = sticky
      self.sep = sep
      # self.fields = {}
      #for name in toTable.GetPrimaryKey():
      #   self.fields[name] = toTable.fields[name]
      
   def get_default(self):
      a = []
      for name in self.toTable.GetPrimaryKey():
         a.append(self.toTable.fields[name].get_default())
      return a
   
   def pin2value(self,expr):
      if len(expr)==0 : return None
      a = []
      # raise str(type(expr))
      aexpr = expr.split(self.sep)
      pk = self.toTable.GetPrimaryKey()
      if len(aexpr) != len(pk):
         raise PinboardError(
            "found %d components instead of %d" % \
            (len(aexpr),len(pk)))
      i = 0
      for name in pk:
      # for (name,field) in self.fields.items():
         a.append(self.toTable.fields[name].pin2value(aexpr[i]))
         i += 1
      return a
   
   def value2sql(self,value):
      s = ''
      sep = ''
      i = 0
      for name in self.toTable.GetPrimaryKey():
      #for (name,field) in self.fields.items():
         s += sep + self.toTable.fields[name].value2sql(value[i])
         i += 1
         sep = ','
      return s
   
   def name2sql(self,name):
      s = ''
      sep = ''
      for fieldname in self.toTable.GetPrimaryKey():
         # for (colname,field) in self.fields.items():
         s += sep + name + '_' \
              + self.toTable.fields[fieldname].name2sql(fieldname)
         sep = ','
      return s
   

## class ReleaseIdField(ComplexField):
##    def __init__(self):
##       ComplexField.__init__(self,{
##          'major' : Field(IntType()),
##          'minor' : Field(IntType()),
##          'release' : Field(IntType())
##          },'.')
      
      

      
class ArrayField:
   def __init__(self,linkTable,parent=True): #,elementType=None):
##       if elementType == None:
##          elementType = IntType()
##       self.elementType = elementType
      # the fields themselves don't yet exist during initialization
      # so we just store the name
      if parent:
         self.joinField = "c"
         #self.joinTable = linkTable.child
      else:
         self.joinField = "p"
         #self.joinTable = linkTable.parent
      self.parent = parent
      # True : i am parent, children are listed
      # False : i am child, parents are listed
      # pk = linkTable.GetPrimaryKey()
      # self.elementType = linkTable.fields[pk].type
      self.linkTable = linkTable
      
   def pin2value(self,expr):
      if len(expr)==0 : return None
      a = []
      aexpr = expr.split() # split using whitespace as separator
      for e in aexpr:
         #try:
            a.append(self.linkTable.fields[self.joinField].pin2value(e))
##          except PinboardError:
##             print self.linkTable.fields[self.joinField].toTable.GetPrimaryKey()
##             raise PinboardError("foo")
      return a
   
   def sql_insert(self,name,tableHandler):
      """
      """
      sql = ""
      if tableHandler.current[name] == None:
         return ''
      for value in tableHandler.current[name]:
         sql += "INSERT INTO "  \
                + self.linkTable.name \
                + " ("
         sep = ""
         for pk in self.linkTable.parent.GetPrimaryKey():
            sql += sep + "p_" + pk
            sep = ','
         for pk in self.linkTable.child.GetPrimaryKey():
            sql += sep + "c_" + pk
            sep = ','
            
         sql += ") VALUES ("
         if self.parent:
            sep = ""
            for pk in self.linkTable.parent.GetPrimaryKey():
               fld = self.linkTable.parent.fields[pk]
               pkvalue = tableHandler.current[pk]
               if pkvalue == None:
                  sql += sep + "LAST_INSERT_ID()"
               else:
                  sql += sep + fld.value2sql(pkvalue)
               sep = ','
            sql += sep + self.linkTable.fields["c"].value2sql(value)
            
         else:
            sql += self.linkTable.fields["c"].value2sql(value)
            sep = ","
            for pk in self.linkTable.child.GetPrimaryKey():
               fld = self.linkTable.child.fields[pk]
               pkvalue = tableHandler.current[pk]
               if pkvalue == None:
                  sql += sep + "LAST_INSERT_ID()"
               else:
                  sql += sep + fld.value2sql(pkvalue)
               sep = ','

         sql += ");\n"
         
      return sql



## def SetProcessor(p):
##    global processor
## ##    processor.process()
##    ## processor.eof = True
##    ## processor.done = True
##    processor = p

## class Processor:
##    def __init__(self,reader=None,writer=None):
##       if reader == None: reader = sys.stdin
##       if writer == None: 
##       self.eof = False
##       self.done = False
##       self.reader = reader
##       self.writer = writer
##       self.headers = {}
##       self.headers["#cmd"] = Action()
##       self.lineNumber = 0
##       self.handler = None
##       # self.line = None
      
##    def next(self):
##       self.line = self.reader.readline()
##       self.line.replace('\r','')
##       if self.line == '':
##          self.eof = True
##          self.done = True
##          return False
##       self.lineNumber += 1
##       if self.line.startswith('----'):
##          self.done = True
##          return # self.next()
##       # return not self.done
      
##    def read(self):
##       self.done = False
##       self.next()
##       self.read_headers()

##    def skipBlankLines(self):
##       while (not self.done) and self.line == '\n' :
##          self.next()

##    def read_headers(self):
##       self.skipBlankLines()
##       while not self.done: 
##          if self.line == '\n' :
##             self.next()
##             return
##          a = self.line.split(':',1)
##          if len(a) != 2:
##             raise "(%d) %s : invalid header line format " % \
##                   (self.lineNumber,self.line);
##          name = a[0].strip()
##          expr = a[1].strip()
##          if name in self.headers:
##             self.headers[name].eval(expr)
##          else:
##             self.unknown_header(name,expr)
##          self.next()
         
##    def unknown_header(self,name,expr):
##       raise name + ": no such header in " + self.name


class Processor:
   def __init__(self):
      self.status = 0
      ## 0 : waiting for headers
      ## 1 : reading headers
      ## 2 : reading content
      self.blankcount = 0
      self.handler = Handler()

   def process_line(self,line):
      line = line.replace('\r','')
      if line == '\n':
         self.blankcount += 1
         if self.blankcount > 1:
            return # consecutive blank lines count only once
         if self.status == 0:
            # ignore blank lines before headers
            return
         elif self.status == 1:
            # a blank line terminates the header lines
            self.status = 2
            return
         else:
            self.handler.process_blank_contentline()
         return
      else:
         self.blankcount = 0
         
      if line.startswith('----'):
         self.handler.stop_processing()
         self.status = 0
         return
      
      if self.status == 0:
         self.handler.start_processing()
         self.status = 1
         
      if self.status == 1:
         ## i'm reading headers, so this must be a header line
         a = line.split(':',1)
         if len(a) != 2:
            raise PinboardError(
               "missing ':' in header line " + repr(line))
         name = a[0].strip()
         expr = a[1].strip()
         if name == 'handler':
            self.handler.stop_processing()
            #self.handler = eval(expr + '()')
            self.handler = TableHandler(app.tables[expr])
            return 
         self.handler.process_headerline(name,expr)
         return
      ## non-empty content line
      self.handler.process_contentline(line)
         
         
   
class Handler:
   "default Handler. Does nothing but ignoring empty lines"
   def start_processing(self):
      pass
   def process_blank_contentline(self):
      pass
   def stop_processing(self):
      pass
   def process_headerline(self,name,expr):
      raise PinboardError("no handler specified")
   def process_contentline(self,line):
      raise PinboardError("no handler specified")

class TableHandler(Handler):
   def __init__(self,table):
      self.table = table
      self.fieldCount = 0
      self.isbody = False
      self.current = {}
      for (n,field) in self.table.fields.items():
         self.current[n] = field.get_default()
      for (n,type) in self.table.arrays.items():
         self.current[n] = []
   
   def start_processing(self):
      self.isbody = False
      self.fieldCount = 0
      for (name,field) in self.table.fields.items():
         if not field.sticky:
            self.current[name] = field.get_default()
            
   def process_headerline(self,name,expr):
      #if Handler.process_headerline(self,name,expr):
      #   return True
      self.fieldCount += 1
      if name in self.table.fields:
         fld = self.table.fields[name]
         self.current[name] = fld.pin2value(expr)
         return True
      if name in self.table.arrays:
         fld = self.table.arrays[name]
         self.current[name] = fld.pin2value(expr)
         return True
      raise PinboardError(
         name + ": invalid header field in " + self.table.name)
      # return False

##    def process_blank_contentline(self):
##       self.table.process_blank_contentline():
   
##    def process_contentline(self,line):
##       self.table.process_contentline(line)
   
   def process_blank_contentline(self):
      if self.isbody: 
         self.current['body'] += '\n<p>'
      else:
         self.isbody = True
   
   def process_contentline(self,line):
      if self.isbody: 
         self.current['body'] += line 
      else:
         self.current['abstract'] += line

   def stop_processing(self):
      if self.fieldCount == 0:
         return
      # columns = self.fields.keys()
      sql = "INSERT INTO %s (" % self.table.name
      sep = ""
      for (name,field) in self.table.fields.items():
         sql += sep + field.name2sql(name)
         sep = ", "
      sql += ") VALUES ("
      sep = ""
      # writer.write(sql)
      for (name,field) in self.table.fields.items():
         if self.current[name] == None:
            sql += sep + "NULL"
         else:
            sql += sep + field.value2sql(self.current[name])
         sep = ", "
      sql += ");\n"
      writer.write(sql)
      for (name,a) in self.table.arrays.items():
         sql = a.type.sql_insert(name,self)
         writer.write(sql)

class Table:
   def __init__(self):
      self.fields = {}
      self.arrays = {}
      #self.joins = {}
      #self.details = {}

   def Declare(self,name):
      self.name = name # self.__class__.__name__
         
   def init(self):
      pass
   
   def AddField(self,name,type=None,sticky=False):
      self.fields[name] = Field(type,sticky)
      
   def AddJoin(self,name,toTableName,sep='.',sticky=False):
      self.fields[name] = JoinField(toTableName,sep,sticky)
      
   def AddArray(self,name,linkTableName,parent,sticky=False):
      linkTable = app.tables[linkTableName]
      self.arrays[name] = Field(ArrayField(linkTable,parent),sticky)

   def GetPrimaryKey(self):
      return ('id',)
   
##    def process_contentline(self,line):
##       raise PinboardError(self.name + ' : no body lines allowed')
   
##    def process_blank_contentline(self):
##       pass


class LinkTable(Table):
   def __init__(self,parentName,childName):
      Table.__init__(self)
      self.parent = app.tables[parentName]
      self.child = app.tables[childName]
      
   def init(self):
      self.AddJoin("p",self.parent.name,".")
      self.AddJoin("c",self.child.name,".")

class MemoTable(Table):
   def __init__(self):
      Table.__init__(self)
      self.isbody = False
      
   def init(self):
      self.AddField("title")
      self.AddField("abstract",MemoType())
      self.AddField("body",MemoType())
      
##    def start_processing(self):
##       Table.start_processing(self)
##       self.isbody = False
      
      
class NEWS(MemoTable):
   def init(self):
      MemoTable.init(self)
      self.AddField("author_id",IntType(),True)
      self.AddField("project_id",IntType(),True)
      self.AddField("date",DateType(),True)
      self.AddField("id",IntType())
      self.AddField("lang_id",TextType(),True)
      self.AddArray("groups",'NEWS2NEWSGROUPS',True)

class NEWSGROUPS(Table):
   def init(self):
      self.AddField("id",TextType())

class PROJECTS(MemoTable):
   def init(self):
      MemoTable.init(self)
      self.AddField("id",IntType())
      self.AddField("sponsor_id",IntType())
      # self.AddField("super_id",IntType())
      self.AddField("responsible_id",IntType())
      self.AddField("date",DateType())
      self.AddField("stopDate",DateType())
      self.AddArray("parentProjects","PRJ2PRJ",False)
      self.AddJoin("version","VERSIONS")


class CHANGES(MemoTable):
   def init(self):
      MemoTable.init(self)
      self.AddField("author_id",IntType(),True)
      self.AddJoin("version","VERSIONS",'.',True)
      self.AddField("date",DateType(),True)
      self.AddField("id",IntType())
      self.AddArray("files","FILES2CHANGES",False)
      #self.AddField("salesVisible",BoolType())
      #self.AddField("userVisible",BoolType())
      #self.AddField("adminVisible",BoolType())

class VERSIONS(Table):
   def init(self):
      self.AddField('major', IntType(),True)
      self.AddField('minor', IntType(),True)
      self.AddField('release', IntType())
      #self.AddField("title",TextType())
      self.AddField("date",DateType())
      
   def GetPrimaryKey(self):
      return ('major', 'minor', 'release')
      
class TOPICS(Table):
   def init(self):
      self.AddField('id', IntType())
      self.AddField('name_en', TextType())
      self.AddArray('parents',"TOPIC2TOPIC",True)

## class TOPIC2TOPIC(LinkTable):
##    def __init__(self):
##       self.__init__(self,"TOPIC","TOPIC")
##    def init(self):
##       self.AddField('p_id', IntType())

class DBITEMS(MemoTable):
   def init(self):
      MemoTable.init(self)
      self.AddField("super_id",TextType(),True)
      self.AddField("id",TextType())

class FILES(MemoTable):
   def init(self):
      MemoTable.init(self)
      self.AddField("id",TextType())

class CLASSES(MemoTable):
   def init(self):
      MemoTable.init(self)
      self.AddField("id",TextType())
      self.AddField("file_id",TextType(),True)
      self.AddField("super_id",TextType())
      
class METHODS(MemoTable):
   def init(self):
      MemoTable.init(self)
      self.AddField("name",TextType())
      self.AddField("class_id",TextType(),True)
      
## class MEETINGS(MemoTable):
##    def init(self):
##       MemoTable.init(self)
##       self.AddField("date",DateType())
##       self.AddField("time",TextType())


## def AddLink(fromTable, toTable,
##             joinName,joinLabel,
##             detailName=None,detailLabel=None):
##    fromTable.AddJoin(joinName,joinLabel,toTable)
##    if detailName != None:
##       toTable.AddDetail(fromTable,joinName,
##                         detailName,detailLabel)


class Application:
   def __init__(self):
      self.tables = {}

   def DeclareTable(self,name,table):
      table.Declare(name)
      self.tables[name] = table

   def InstanciateTables(self):
      self.DeclareTable('METHODS' , METHODS())
      self.DeclareTable('CLASSES' , CLASSES())
      self.DeclareTable('FILES' , FILES())
      self.DeclareTable('DBITEMS' , DBITEMS())
      self.DeclareTable('TOPICS' , TOPICS())
      self.DeclareTable('PROJECTS' , PROJECTS())
      self.DeclareTable('VERSIONS' , VERSIONS())
      self.DeclareTable('CHANGES' , CHANGES())
      self.DeclareTable('NEWS' , NEWS())
      self.DeclareTable('NEWSGROUPS' , NEWSGROUPS())
      
      # self.DeclareTable('ARTWORKS' , ARTWORKS())
      
      self.DeclareTable('NEWS2NEWSGROUPS' ,
                        LinkTable("NEWS","NEWSGROUPS"))
      self.DeclareTable('TOPIC2TOPIC' ,
                        LinkTable("TOPICS","TOPICS"))
      self.DeclareTable('PRJ2PRJ' ,
                        LinkTable("PROJECTS","PROJECTS"))
      self.DeclareTable('FILES2CHANGES' ,
                        LinkTable("FILES","CHANGES"))

   def InitializeTables(self):
      for table in self.tables.values():
         table.init()
      
            
writer = sys.stdout

app = Application()
app.InstanciateTables()
app.InitializeTables()

p = Processor()
   
for line in fileinput.input():
   if fileinput.isfirstline():
      sys.stderr.write( fileinput.filename() + '...\n')
   try:
      p.process_line(line)
   except PinboardError,e:
      sys.stderr.write("%s(%d) %s\n" % (
         fileinput.filename(),
         fileinput.filelineno(),
         e.msg
         ))
      sys.exit(2)
      
p.handler.stop_processing()


## for f in sys.argv[1:]:
##    print f
## exit   
## processor = Processor()
## while not processor.eof:
##    processor.read()


 
