import sys
import string
import fileinput

False = 0
True = 1

from tools import *
import babel
#import datadict

# constants for Processor.status
waiting_for_headers = 0
reading_headers = 1
reading_content = 2

class Processor:
   def __init__(self,app):
      self.status = waiting_for_headers
      self.blankcount = 0
      self.handler = Handler()
      self.app = app

   def process_line(self,line):
      line = line.replace('\r','')
      if line == '\n':
         self.blankcount += 1
         if self.blankcount > 1:
            return # consecutive blank lines count only once
         if self.status == waiting_for_headers:
            # ignore blank lines before headers
            return
         elif self.status == reading_headers:
            # a blank line terminates the header lines
            self.status = reading_content
            return
         else:
            self.handler.process_blank_contentline()
         return
      else:
         self.blankcount = 0
         
      if line.startswith('----'):
         self.handler.stop_processing()
         self.status = waiting_for_headers
         return
      
      if self.status == waiting_for_headers:
         self.handler.start_processing()
         self.status = reading_headers
         
      if self.status == reading_headers:
         ## i'm reading headers, so this must be a header line
         a = line.split(':',1)
         if len(a) != 2:
            raise LinoError(
               "missing ':' in header line " + repr(line))
         name = a[0].strip()
         expr = a[1].strip()
         if name == 'handler':
            self.handler.stop_processing()
            #self.handler = eval(expr + '()')
            self.handler = TableHandler(getattr(self.app.tables,expr))
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
      raise LinoError("no handler specified")
   def process_contentline(self,line):
      raise LinoError("no handler specified")

class TableHandler(Handler):
   def __init__(self,table):
      self.cursor = table.cursor() #datadict.Query(table).GetCursor()
      self.fieldCount = 0
      self.isbody = False
      self.cursor.insert_row()
##       for (name,field) in self.table.fields.items():
##          self.current[name] = field.get_default()
##       for (name,type) in self.table.details.items():
##          self.current[name] = []
   
   def start_processing(self):
      self.isbody = False
      self.fieldCount = 0
      #babel.SetUserLang("de")
      self.cursor.insert_row_copy(self.cursor.GetCurrentRow())
            
   def process_headerline(self,name,expr):
      self.fieldCount += 1
      self.cursor.SetCellByExpr(name,expr)
##       except ValueError,e:
##          raise LinoError(\
##                "(header %s.%s) %s" % (self.query.GetName(),name,e))
      
##       print self.table.fields
##       raise LinoError,\
##             "%s : invalid header field in %s" % (name,self.table.name)
      # return False
      
   def GetContentField(self):
      if self.isbody:
         name = "body"
      else:
         name = "abstract"
      if len(babel.langs) > 1:
         name += "_" + babel.userLang
      return name

   def process_blank_contentline(self):
      if self.isbody:
         row = self.cursor.GetCurrentRow()
         if getattr(row,self.GetContentField()) != None:
            setattr(row,
                    self.GetContentField(),
                    getattr(row,self.GetContentField())
                    + "\n<p>")
      else:
         self.isbody = True
   
   def process_contentline(self,line):
      if line[0] == '.':
         if line[1:2] in babel.langs:
            babel.SetUserLang(line[1:2])
            return
      row = self.cursor.GetCurrentRow()
      if getattr(row,self.GetContentField()) == None:
         setattr(row,self.GetContentField(),line)
      else:
         setattr(row,self.GetContentField(),
                 getattr(row,self.GetContentField())
                 +line)
         #row.values[self.GetContentField()] += line 
##       if self.isbody: 
##          self.current['body'] += line 
##       else:
##          self.current['abstract'] += line

   def stop_processing(self):
      if self.fieldCount == 0:
         return
      self.cursor.commit() #self.cursor.GetCurrentRow())
      # columns = self.fields.keys()

  

def parseall(app):

   for table in app.tables.values():
      table.create_table()
            
   # __builtins__['writer'] = sys.stdout

   # p = Processor()
   p = None
   
   for line in fileinput.input():
      if fileinput.isfirstline():
         if p != None:
            p.handler.stop_processing()
         p = Processor(app)
         sys.stderr.write( fileinput.filename() + '...\n')
      try:
         p.process_line(line)
      except LinoError,e:
         sys.stderr.write("%s(%d) %s\n" % (
            fileinput.filename(),
            fileinput.filelineno(),
            e.msg
            ))
         sys.exit(2)
      
   p.handler.stop_processing()


def parsefile(app,name):
   f = file(name) 
   p = Processor(app)
   lineno = 0
   for line in f.readlines():
      try:
         lineno += 1
         p.process_line(line)
      except LinoError,e:
         sys.stderr.write("%s(%d) %s\n" % (
            name,
            lineno,
            e.msg
            ))
         sys.exit(2)

   p.handler.stop_processing()
 
def parsestring(app,input):
   p = Processor(app)
   lineno = 0
   for line in input.split("\n"):
      try:
         lineno += 1
         p.process_line(line+"\n")
      except LinoError,e:
         sys.stderr.write("(line %d) %s\n" % (
            lineno,
            e.msg
            ))
         sys.exit(2)

   p.handler.stop_processing()


if __name__ == "__main__":
   
   import community
   community.init() # community.CommunityApplication())
      
   import dbd
   import mysql_dbd
   app.SetConnection(mysql_dbd.Connection(dbd.ConsoleHost()))

   parseall()
