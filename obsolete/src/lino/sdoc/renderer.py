import os

class Renderer:

   def open(self,filename):
      (root,ext) = os.path.splitext(filename)
      if ext.lower() != '.'+self.outputExt:
         filename += '.' + self.outputExt
      if os.path.exists(filename):
         os.remove(filename)
      self._filename = filename
      
   def close(self,showOutput=True):
      if showOutput:
         os.system("start %s" % self.getFilename())
         
   def getFilename(self):
      return self._filename

   def getPageNumber(self):
      return 1
   
   def beginDocument(self,document):
      pass

   def endDocument(self):
      pass

   


   def compileBeginEnvironment(self,env):
      
      """returns an element or a list of elements (or None) to be
      added to the current environment before this one becomes the
      current environment"""
      
      raise NotImplementedError
   
   def compileEndEnvironment(self,env):
      
      """returns an element or a list of elements (or None) to be
      added to the current environment after this one stops to be the
      current environment"""
      
      raise NotImplementedError
   
   def compileListItem(self,text,style,bulletText):
      raise NotImplementedError
   
   def compileList(self,listInstance):
      raise NotImplementedError
   
      

