from lino.misc.pset import PropertySet
from lino.sdoc.environment import ChildEnvironment

## class ListItem(ChildEnvironment,ElementContainer):
##    def __init__(self,parent,bulletText,txt):
##       ChildEnvironment.__init__(self,parent,None,None)
##       ElementContainer.__init__(self)
##       self.bulletText = bulletText
##       self.text = txt

class ListStyle(PropertySet):
   defaults = {
      'bulletWidth' : 12,
      'bulletText' : '-'
      }
   def getBulletText(self,listInstance):
      return self.bulletText
      
class NumberedListStyle(ListStyle):
   defaults =  {
      'bulletWidth' : 12,
      'bulletText' : '-',
      'showParent' : False
      }
##    def __init__(self,bulletWidth,showParent=False):
##       ListStyle.__init__(self,bulletWidth)
##       self.showParent = showParent
      
   def getBulletText(self,listInstance):
      text = str(listInstance.itemCount)+'.'
      if self.showParent:
         parent = listInstance.getParent()
         if parent is not None:
            text = parent.getBulletText() + text
      return text

         

class ListInstance(ChildEnvironment):
   def __init__(self,doc,
                parent,width,listStyle,itemStyle):
      
      ChildEnvironment.__init__(self,doc,parent,width,itemStyle)
      #self._currentItem = None
      self.itemCount = 0
      self.listStyle = listStyle
      #self._items = []

      # dynamically create ParagraphStyle with the indentation
      # depending on the nesting level of the list:
      # TODO : manage _paraStyle for ListItem
      level = self.getListLevel()
      self._paraStyle = self._paraStyle.child(
         leftIndent=level * listStyle.bulletWidth,
         bulletIndent=(level-1)* listStyle.bulletWidth)
      

   def getListLevel(self):
      lvl = 1
      parent = self
      while True:
         parent = parent.getParent()
         if parent is None:
            return lvl
         elif parent.__class__ == self.__class__:
            lvl += 1


##    def addElement(self,elem):
##       "overrides FlowingEnvironment.addElement()"
##       if elem is None:
##          return

##       if type(elem) is types.ListType:
##          self._items += elem
##       else:
##          self._items.append(elem)
         
##    def getItems(self):
##       return self._items


##    def beginListItem(self,i):
##       self._currentItem = i

##    def endListItem(self):
##       if self._currentItem is not None:
##          self.getRenderer().renderListItem(self._currentItem)
##       self._currentItem = None

   def getBulletText(self):
      return self.listStyle.getBulletText(self)
      
   def li(self,txt):
      txt = self.document.feeder(txt)
      #if self._currentItem is not None:
      #   self.endListItem()
      self.itemCount += 1
      bulletText = self.getBulletText()
      # self.beginListItem(ListItem(self,bulletText,txt))
      # self.getRenderer().renderListItem()
      elem = self.document.renderer.compileListItem(
         txt,
         self._paraStyle,
         bulletText)
      #elem = self.getRenderer().compilePara(txt, self._paraStyle)
      #elem = ListItem(bulletText)
      self.toStory(elem)

##    def onBegin(self):
##       pass
##       #return self.getRenderer().compileBeginList(self)
   
##    def onEnd(self):
##       pass
##       #return self.getRenderer().compileEndList(self)


class ListsMixin:
   "mix-in class for Document"

##    def __init__(self):
##       self.declareCommands(
##          'beginList','endList','li',
##          )      

   def setupStyleSheet(self,sheet):
      # print sheet
      sheet.define('UL', ListStyle(bulletWidth=12))
      sheet.define('OL', NumberedListStyle(bulletWidth=12))

   
   def getDefaultListStyle(self):
      return self.stylesheet.UL
   
   def beginList(self,listStyle=None,paraStyle=None):
      if listStyle is None:
         listStyle = self.getDefaultListStyle()
      if paraStyle is None:
         paraStyle = self.getDefaultParaStyle()
         
      lst = ListInstance(self,
                         self.getenv(),
                         self.getTextWidth(),
                         listStyle,
                         paraStyle)
      self.beginEnvironment(lst)
      # self._currentEnv.append(elem)
      return True

   def endList(self):
      self.endEnvironment(ListInstance)


##    def li(self,txt):
##       """inserts txt as a list item.
##       """
##       txt = self.feeder(txt)
##       lst = self.getEnvironment(ListInstance)
##       assert lst,\
##             "li() not allowed outside list environment"
##       lst.li(txt)



