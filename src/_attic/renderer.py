from lino.dbd.cursor import Row
import lino.type as types

class Section:
   pass
class Sequence:
   pass

class Renderer:
   def __init__(self,writer):
      self.writer = writer
      self.sectionStack = []
      self.sequenceStack = []

   def BeginMarginText(self):
      pass
   def EndMarginText(self):
      pass
   def FlushMargin(self):
      pass
   
   def BeginFootnote(self,label=None):
      pass
   def EndFootnote(self):
      pass
   
   def BeginSection(self,title,num=None):
      pass
   def EndSection(self):
      pass
   
   def BeginSequence(self,format,title=None):
      pass
   def EndSequence(self):
      pass
   
   def BeginItem(self,label=None):
      pass
   def EndItem(self):
      pass

   def BeginDocument(self):
      pass
   def EndDocument(self):
      pass

   def ShowTitle(self,text,level=1,num=None):
      pass
   

   
class HtmlRenderer(Renderer):
##   def __init__(self,writer):
##      Formatter.__init__(self,writer)
##      self.frameStack = []
      
##       self.toUser = HtmlFormatter(BufferWriter())
##       self.toSuperTitle = HtmlFormatter(BufferWriter())
##       self.toMargin = HtmlFormatter(BufferWriter())
##       self.toBody = HtmlFormatter(BufferWriter())
      
##       self.frame = self.toBody

##    def BeginFrame(self,frame):
##       self.frameStack.append(self.frame)
##       self.frame = frame
##    def EndFrame(self):
##       self.frame = self.frameStack.pop()

##    def FlushMargin(self):
##       if len(self.toMargin.writer.buffer) != 0:
##          write = self.toBody.writer.write
##          write('</td><td width="15%" valign="top">')
##          write(self.toMargin.writer.unwrite())
##          write('</td></tr><tr><td>')
      
   def ShowTitle(self,text,level=1,num=None):
      self.writer.write("<H%d>" % level)
      if num != None:
         self.writer.write(num)
      self.writer.write(text)
      self.writer.write("</H%d>" % level)
   
   def BeginDocument(self):
      self.writer.write("""
      <HTML>
      <BODY>
      """)
   def EndDocument(self):
      self.writer.write("""
      </BODY>
      </HTML>
      """)


      
##       write(self.header)
##       write(self.toSuperTitle.writer.unwrite())
##       write(self.toBody.writer.unwrite())
##       write(self.toMargin.writer.unwrite())
##       write(self.toUser.writer.unwrite())
##       write(self.footer)

   def ShowQueryRef(self,cursor,label=None):
      if label is None:
         label = cursor.GetLabel()
      self.writer.write('<a href="TODO">%s</a>' % label)

   def ShowQuery(self,cursor):
      query = cursor.query
      if query.depth == Query.DEPTH_REF:
         self.ShowQueryRef(cursor)
         return
      self.writer.write(repr(query.depth))
      #cursor = query.cursor()
      cursor.executeSelect()
      row = cursor.fetchone()
      self.ShowQueryHeader(cursor)
      while row:
         self.ShowCursorRow(cursor,row)
         row = cursor.fetchone()
      self.ShowQueryFooter(cursor)

   def ShowQueryHeader(self,cursor) :
      echo = self.writer.write
      query = cursor.query
    
##       if query.IsMainComponent() :
##          if (query.IsSinglePage()) :
##             query.leadTable.OnSinglePage(query)
##          else :
##             ## if (query.IsSection()) 
      self.BeginSection(query.GetLabel(),None)
      
      if (query.IsEditable()) :
         echo ("""
         <form name="edit_%s" action="update.php" method="POST">
         """ % query.leadTable.name)

         echo("\n")
    
      if query.depth == Query.DEPTH_TABLE:
         echo ( '\n<table width="100%" class="list">')
         echo ( "\n<tr>")
         for comp in  query.leadTable.comps:
            width = comp.format[0]
            echo ( """
            <td class="headrow"
            style="width:%dpx">
            """% width * 10)
        
         ## cell.column.ShowColumnLabel(query,i)

         if (comp.canSort(query)):
            self.ShowQueryRef(query,comp.GetLabel(), {
               "sort":comp.name} )
         else :
            echo (comp.GetLabel())
        
          
         echo ( "\n</td>")
         echo ( "\n</tr>")
      elif query.depth == Query.DEPTH_LIST:
         echo ( '<ul>')
         echo ("\n")
  

   def ShowQueryFooter(self,cursor) :
      query = cursor.query
      echo = self.writer.write
      if query.depth == Query.DEPTH_TABLE:
         echo ( "\n</table>")
      elif query.depth == Query.DEPTH_LIST:
         echo ( '</ul>')
      elif query.depth == Query.DEPTH_SHORTLIST:
         #if (query.HasMore() and not query.IsSingleRow()) :
         self.ShowQueryRef(query,'[all]',{
            "depth":Query.DEPTH_LIST,
            "page":0,
            "edit":0
            })
    
      if (query.IsEditable()) :
         echo ( '<input type="submit" value="Update">')
         echo ( '</form>')
    
    
      #if (query.IsMainComponent()) :
      #   if not query.IsSinglePage() :
      self.EndSection()
      
    
  


  
   def ShowCursorRow(self,cursor,row) :
      echo = self.writer.write
      query = cursor.query
      if query.depth == Query.DEPTH_SHORTLIST:
         if (not first): echo ( ', ')
         echo(cursor.query.leadTable.GetRowLabel(row))

      elif query.depth == Query.DEPTH_LIST:
         echo ( '<li>')
         cursor.query.leadTable.ShowInList(query)
         echo ( '</li>')
         echo ("\n")
      elif query.depth == Query.DEPTH_TABLE:
         echo ( '\n<tr>')
         for col in cursor.columns:
            if query.result.recno % 2 == 0:
               rowclass = "evenrow"
            else:
               rowclass = "oddrow"
            echo ( '\n<td class="%s" valign="top">' % rowclass)

            if (query.IsEditable() and col.canEdit(query)) :
               self.ShowEditor(
                  col.GetType(),
                  col.format,
                  col.name+'[]',
                  getattr(row,col.name),
                  col.IsReadOnly(cursor)
                  )
            else :
               value = getattr(row,col.name)
               self.ShowColValue(col, value)
          
            echo ( "\n</td>")
         echo ( '\n</tr>')
      elif query.depth == Query.DEPTH_PAGE:
         self.BeginSection(query.leadTable.GetRowLabel(query.row),
                           str(query.result.recno)+ '.')
      
##          if (query.GetNestingLevel() == 1) :
##             s = 'row '
##             sep = ''
##             for pk in query.leadTable.GetPrimaryKey():
##                s += sep + query.row[pk.name]
##                sep = '.'
        
##             ToMargin('%s in %s' % (s, query.leadTable.GetRef() ))

         if query.IsEditable() :

            echo ( '\n<table width="100%" class="form">')
            for col in cursor.columns:
               echo ( "\n<tr>")
               echo ( "\n<td>%s</td>" % col.GetLabel() )
               echo ( "\n<td>")


               self.ShowEditor(
                  col.GetType(),
                  col.format,
                  col.name+'[]',
                  getattr(row,col.name),
                  col.IsReadOnly(cursor)
                  )
            
               echo ( '</td>')
               echo ( '</tr>')
        
            echo ( "\n</table>")
         else :
            cursor.query.leadTable.ShowInPage(query,first)
      
         self.EndSection()
  
         
         
   def ShowBeginSequence(self,seq) :
      echo = self.writer.write
      if seq.title != None:
         echo('<p><b>%s</b>' % seq.title)
      if seq.format == SEQ_BR:
         ## echo '<p>'
         pass
      elif seq.format == SEQ_UL:
         echo ('<ul>' )
      elif seq.format == SEQ_OL:
         echo('<ol>')
      elif seq.format == SEQ_PARBOX:
         echo('<blockquote>')
      elif seq.format == SEQ_FORM:
         echo( '<table>')
      elif seq.format == SEQ_PAR:
         pass
      elif seq.format == SEQ_SENTENCES:
         pass
      else:
         raise LinoError('bad sequence format')
    
  
  
   def ShowEndSequence(self,seq) :
      echo = self.writer.write
      if seq.format == SEQ_BR:
         ## echo '</p>'
         pass
      elif seq.format == SEQ_UL:
         echo( '</ul>')
      elif seq.format == SEQ_OL:
         echo( '</ol>')
      elif seq.format == SEQ_PARBOX:
         echo('</blockquote>')
      elif seq.format == SEQ_FORM:
         echo('</table>')
      elif seq.format == SEQ_PAR:
         ## echo '</p>'
         pass
      elif seq.format == SEQ_SENTENCES:
         ## echo '</p>'
         pass
      else:
         raise LinoError('bad sequence format')
    
  

   def ShowBeginItem(seq,label=None) :
      echo = self.writer.write
      echo("\n")
      if (seq.format == SEQ_UL):
         echo ('<li>')
      elif (seq.format == SEQ_OL):
         echo ('<li>')
      elif (seq.format == SEQ_PARBOX):
         echo ('<p>')
      elif (seq.format == SEQ_BR):
         echo ('<br>')
      elif (seq.format == SEQ_PAR):
         echo ('<p>')
      elif (seq.format == SEQ_SENTENCES):
         pass
      elif (seq.format == SEQ_FORM):
         echo ('<tr><td valign="top">')
      else:
         raise LinoError('%s : bad format' % seq.format)

      if (seq.showLables) : ##  && !is_null(label)) :
    
         echo (label )
    
         if (seq.format == SEQ_FORM):
            echo ('</td><td valign="top">')
         else:
            echo (' : ')
    
      
  
  
   def ShowEndItem(seq) :
      echo = self.writer.write
      if (seq.format == SEQ_BR):
         echo ('<br>')
      elif (seq.format == SEQ_UL):
         echo ('</li>')
      elif (seq.format == SEQ_OL):
         echo ('</li>')
      elif (seq.format == SEQ_PARBOX):
         echo ('</p>')
      elif (seq.format == SEQ_SENTENCES):
         echo ('. ')
      elif (seq.format == SEQ_PAR):
         echo ('</p>')
      elif (seq.format == SEQ_FORM):
         echo ('</td></tr>')
      else:
         raise 'bad style'
  
  
   def ShowEditor(type,format,name,value,readonly) :
      echo = self.writer.write
      if isinstance(type,types.MemoType):
         echo ( '<textarea cols=%d rows=%d name="%s"' %\
                (format.width,format.height,name))
         if readonly : echo ( ' readonly' ) 
         echo ( '>')
         echo ( value)
         echo ( '</textarea>')
      elif isinstance(type,types.BoolType):
         echo ( '<input type="checkbox"')
         if value: echo ( ' checked')
         if readonly: echo ( ' readonly'    ) 
         echo ( ' name="%s" value="yes">\n' % name)

      elif isinstance(type,types.TextType):

         echo ( '<input type="Text" name="%s"' % name )
         if readonly: echo ( ' readonly') 
         echo ( ' size=%d value="%s"' % (format.width,
                                         htmlspecialchars(value)
                                         ))
         echo ( "\n")
      else:
         raise LinoError('no editor for type %'. get_class(type))
    
  
  
##    def ShowTextInput(name,value,width,readonly) :
##       echo ( '<input type="Text" name="' . name . '"')
##       if (readonly) echo ( ' readonly'    ) 
##       echo ( ' size=' . width
##         . ' value="' . htmlspecialchars(value)
##         . '">')
##       echo ( "\n")
##    
  
##    def ShowBoolInput(name,value,readonly) :
##      echo ( '<input type="checkbox"')
##      if (value) echo ( ' checked')
##      if (readonly) echo ( ' readonly'    ) 
##      echo ( ' name="' . name
##        . '" value="yes">')
##      echo ( "\n")
##    
  
##    def ShowMemoInput(name,value,width,height,readonly) :
##      echo ( '<textarea cols=' . width
##        .' rows=' . height
##        .' name="' . name . '"')
##      if (readonly) echo ( ' readonly' ) 
##      echo ( '>')
##      echo ( value)
##      echo ( '</textarea>')
##    
  
   def ShowColValue(col,value,format=None) :
      echo = self.writer.write
      type = col.GetType()
      if isinstance(type,Query):
         if format != None: value.SetDepth(format)
         value.Render()
      elif isinstance(type,Row):
         if value != None:
            echo('NULL')
            return
      
         echo ( col.join.toTable.GetPeekRef(value))
         
      elif isinstance(type,types.MemoType):

         """
         QuickTags
      
         - a litteral '[ref' (or '[url', or...)

         - followed by at least one whitespace
      
         - followed by a word (a greedy sequence of at least one
         character which is neither ']' nor whitespace). This will be 1
         in replPattern
         
         - followed optionally by more whitespace and a sequence of any
         characters (including whitespace), but except ']' because this
         is the terminator.
         
         Note: currently it is not possible for this label string to
         contain a ']'
      
         if a quantifier is followed  by  a  question  mark,
         then it ceases to be greedy...
         http://ee.php.net/manual/en/pcre.pattern.syntax.php

         """
    
         # findPattern = '/^\\\[url\w+(^\w+)\w+(.*)\]/e'
         findPattern = r'/\[url\s+([^\]\s]+)\s*(.*)\]/e'
         replPattern = r'urlref(\'1\',\'2\')'
         value = preg_replace(findPattern,replPattern,value)
    
         findPattern = r'/\[ref\s+([^\]\s]+)\s*?(.*?)\]/e'
         # findPattern = '/\[ref\s+(\w+)\s*?(.*?)\]/e'
         replPattern = r'ref(\'1\',\'2\')'
         value = preg_replace(findPattern,replPattern,value)
    
         # findPattern = '/\[srcref\s+(\S+)\s*(.*)\]/e'
         # replPattern = 'srcref(\'1\',\'2\')'
         findPattern = r'/\[srcref\s+([^\]\s]+)\s*?(.*?)\]/e'
         # findPattern = '/\[srcref\s+(\S+)\]/e'
         replPattern = r'srcref(\'1\')'
         value = preg_replace(findPattern,replPattern,value)
         echo (value)
      elif isinstance(type,types.BoolType):
         if (value):
            echo ('yes')
         else:
            echo ('no')
      else:
         echo (value)
    
  









