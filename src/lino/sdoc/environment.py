import types
import bookland

from lino.misc.etc import isnumber
from lino.misc import debug
from lino.sdoc.memo import parseMemo

# from lino.sdoc import pds

class ParseError(RuntimeError):
   pass



"""

"""

class Writer:
   def __init__(self):
      self._txt = None
      self._autoPara = True
      
   def flush(self):
      if self._txt is not None:
         self.endPara()

   def write(self,txt):
      if self._txt is None:
         self.beginPara()
      self._txt += txt
      if self._autoPara:
         while True:
            i = self._txt.find("\n\n")
            if i == -1:
               break
            suite = self._txt[i+2:]
            self._txt = self._txt[:i]
            self.endPara()
            self.beginPara()
            self._txt = suite

   def beginPara(self,style=None):
      if self._txt is not None:
         self.endPara()
      if style is None:
         style = self.getDefaultParaStyle()
      self._paraStyle = style
      self._txt = ""
      # self._wrap = wrap

   def endPara(self,nextParaStyle=None):
      if self._txt is not None:
         self.p(self._txt, self._paraStyle)
         # self.addElement(elem)
         self._txt = None
         
      if nextParaStyle is not None:
         self._paraStyle = nextParaStyle
      









class BaseEnvironment(Writer):
   # abstract class. Base class for Document and Environment
   """
   maintains the "current paragraph style"
   """
   
   def __init__(self,document,paraStyle):
      # debug.hello(self,"__init__()")
      self.document = document
      self._paraStyle = paraStyle.child()
      self._paraStyle.setName("%s.defaultParaStyle" % \
                              self.__class__.__name__)
      Writer.__init__(self)



   def p(self,txt,style=None):
      assert type(txt) == types.StringType, \
             "%s is not a string" % repr(txt)
      if style is None:
         style = self.getDefaultParaStyle()
      txt = self.document.feeder(txt)
      # self.getRenderer().renderPara(txt, style)
      # print "p() : style is %s" % str(style)
      elem = self.document.renderer.compilePara(txt, style)
      self.toStory(elem)
      
      """ note that the toStory() called from p() is perhaps not the
      one defined above, because TableInstance overrides it.  """

   def memo(self,txt):
      parseMemo(self.document,txt)
      # parseMemo(self.document,txt)


   def h1(self,txt):
      self.p(txt,self.document.stylesheet.Heading1)
      
   def h2(self,txt):
      self.p(txt,self.document.stylesheet.Heading2)
      
   def h3(self,txt):
      self.p(txt,self.document.stylesheet.Heading3)
      
         
   def pre(self,txt,style=None):
      if style is None:
         style = self.document.stylesheet.Code
      self.p(txt,style)

   def img(self,filename,
           width=None,height=None,
           style=None):
      assert self._txt is None
      if style is None:
         style = self.getDefaultParaStyle()
      elem = self.document.renderer.compileImage(filename,
                                                 width,height,
                                                 style)
      self.toStory(elem)

   def barcode(self,txt,coding="EAN13",style=None):
      if style is None:
         style = self.getDefaultParaStyle()
      if coding == 'EAN13':
         barCodeSymbol = bookland.EAN13Symbol(txt)
      else:
         raise coding + " : coding not supported"
      elem = self.document.renderer.compileBarcode(barCodeSymbol,
                                                   style)
      self.toStory(elem)


   def addBackgroundPainter(self,func):
      assert self._txt is None
      elem = self.document.renderer.compileBackgroundPainter(func)
      self.toStory(elem)

      


##    def getenv(self):
##       if self._currentEnv is None:
##          return self
##       assert self._currentEnv is not self
##       return self._currentEnv.getenv()

##    """ during compileBeginEnvironment the current environment is still
##    the old one.  These elements will be added to the story of current
##    environment where they introduce the new environment."""
      


##    def toStory(self,elems):
##       if self._currentEnv is None:
##          print "Rendering %d elements..." % len(elems)
##          self._renderer.render(elems)
##       else:
##          self._currentEnv.toStory(elems)


      


   def getDefaultParaStyle(self):
      return self._paraStyle
   
#   def getRenderer(self):
#      raise NotImplementedError


   def formatParagraph(self,**kw):
      # parent paragraph styles don't get updated by manual
      # formattings
      #self._paraStyle = self._paraStyle.child(**kw)
      s = self.getDefaultParaStyle()

      # print s
      
      # s is now usually equal to self._paraStyle, but not for example
      # in a TableRow where it could be the column's style
      
      for k,v in kw.items():
         setattr(s,k,v)

   #def getTextWidth(self):
   #   raise NotImplementedError


      
   def onBegin(self):
      return None
   
   def onEnd(self):
      
      # print 'onEnd() : ' + str(self)
      return None



##    def append(self,elem):
##       parent = self
##       while True:
##          if parent is None:
##             raise "No story"
##          if isinstance(parent,ElementContainer):
##             parent.addElement(elem)
##             return
##          parent = parent._parent
      

         
class ChildEnvironment(BaseEnvironment):
   def __init__(self,
                doc,
                parent,
                width=None,
                flowStyle=None,
                paraStyle=None):
      """

      - parent : the environment to which this environment belongs

      - width : the outer width of this environment as a flowable.
      
      - flowStyle (or outer style) is the paragraph style of this
        Environment as a flowable inside its parent.
      
      - paraStyle (or inner style) is the default paragraph style for
        elements in this environment. Forwarded to BaseEnvironment.

      A ChildEnvironment dynamically inherits attributs from its
      parent. If somebody asks for some attribute from a
      ChildEnvironment, and if the ChildEnvironment does not have this
      attribut, then it will forward this request to its parent.
      
      """
      if paraStyle is None:
         paraStyle = parent.getDefaultParaStyle()
      BaseEnvironment.__init__(self,doc,paraStyle)
      
      self._parent = parent
      
      if flowStyle is None:
         flowStyle = parent.getDefaultParaStyle()
      self._flowStyle = flowStyle.child()
      self._flowStyle.setName("%s.flowStyle" % \
                              self.__class__.__name__)
      
      if width is None:
         width = parent.getTextWidth() \
                 - self._flowStyle.leftIndent \
                 - self._flowStyle.rightIndent # 20030417 - 20
      assert isnumber(width) 
      self.width = width

   
   def getFlowStyle(self):
      return self._flowStyle

   def getTextWidth(self):
      return self.width 
##       return self.width \
##              - self._flowStyle.leftIndent \
##              - self._flowStyle.rightIndent

#   def getRenderer(self):
#      # overridden by Story
#      return self._parent.getRenderer()


   def getParent(self):
      return self._parent
##       parent = self._parent
##       while True:
##          if parent is None or parent.__class__ == self.__class__:
##             return parent
##          parent = parent.getParent()

   def __getattr__(self,name):
      return getattr(self._parent,name)
   

   
class Body(BaseEnvironment):
   """
   Body is the main environment of a Document
   """
   
   def __init__(self,doc):
      BaseEnvironment.__init__(self, doc, doc.stylesheet.Normal)
      
   def close(self):
      pass

   def getParent(self):
      return None
      
   def getTextWidth(self):
      return self.document.getDocumentWidth()
   
   def toStory(self,elem):
      self.document.renderer.render(elem)
      


         
   
class ElementContainer:
	"""
	a Mixin for Environment
	Collects elements of a "story". Each element is a Flowable.
	"""
	def __init__(self):
		self._elements = []

	def __str__(self):
		s = self.__class__.__name__
		s += '(elements=%s)' % str(self._elements)
		return s
	
	def getStory(self,flush=True):
		elems = self._elements
		if flush:
			self._elements = []
		return elems

	def getElemCount(self):
		return len(self._elements)
	
	def toStory(self,elem):
		# debug.hello(self,'toStory(%s)' % str(elem))
		# print "ElementContainer.toStory()"
		if elem is None:
			return
		# print '%s.toStory(%s)' % (self.__class__.__name__,str(elem))
		if type(elem) is types.ListType:
			self._elements += elem
		else:
			self._elements.append(elem)
			








class Story(BaseEnvironment,ElementContainer):
	
   def __init__(self,doc,textWidth):
      BaseEnvironment.__init__(self, doc, doc.stylesheet.Normal)
      ElementContainer.__init__(self)
      self._textWidth = textWidth
   
   def getTextWidth(self):
      return self._textWidth
   
   def getParent(self):
      return None



## ##    def formatParagraph(self,**kw):
## ##       return self._currentEnv.formatParagraph(**kw)
      
## ##    def getDefaultParaStyle(self):
## ##       return self._doc.getDefaultParaStyle()

##    def onEnd(self):
##       raise """don't call onEnd() replace by getElements?"""
   
   
      
