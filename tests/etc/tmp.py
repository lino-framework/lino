"""

"if x == None" raises "'NoneType' object is not callable"

If I define __getattr__() and __setattr__() for a class, then I cannot
test instances of this class for equality with None.

the code example below raises
TypeError: 'NoneType' object is not callable

Strange! Nobody told you to call 'None'!

Python 2.2.1 (#1, Jun 25 2002, 10:55:46)
[GCC 2.95.3-5 (cygwin special)] on cygwin
         
"""

class Row:

   def __init__(self):
      self.__dict__["_values"] = {}

   def __getattr__(self,name):
      try:
         return self._values[name]
      except KeyError,e:
         AttributeError,str(e)
   
   def __setattr__(self,name,value):
      self.__dict__["_values"][name] = value

class Row2:
   def __init__(self):
      self.a = None
   
row = Row2()
if row is None: 
   print "this works"

row = Row()
#row.a = "a" # this works
#print row.a # this works
if row is None: # here it happens.
   print "row instance is None!"

