import types

def issequence(u):
   return type(u) in (types.TupleType,types.ListType)
def isnumber(n):
   return type(n) in (types.IntType,types.FloatType)


class LinoError(Exception):
   def __init__(self,msg):
      self.msg = msg
   def __str__(self):
      return self.msg


class EventManager:
   
   def __init__(self,possibleEvents):
      self._listeners = []
      self._possibleEvents = possibleEvents
      
   def add_listener(self,l):
      for evt in self._possibleEvents:
         if not hasattr(l,evt):
            raise LinoError("%s instance has no method %s" % (
               repr(l),evt))
      self._listeners.append(l)
      
   def remove_listener(self,l):
      self._listeners.remove(l)
      
   def trigger(self,eventName,*args,**kw):
      if not eventName in self._possibleEvents:
         raise LinoError("%s : no such event" % eventName)
      for l in self._listeners:
         event = getattr(l,eventName)
         event(self)
         
class BufferWriter:
   def __init__(self):
      self.buffer = ''

   def write(self,msg):
      self.buffer += msg
      
   def unwrite(self):
      buffer = self.buffer
      self.buffer = ''
      return buffer



class AttribDict:
   def __init__(self,owner,name=None):
      if name is None:
         name = owner.__class__.__name__
      self.__dict__["_name"] = name
      self.__dict__["_owner"] = owner
      self.__dict__["_dict"] = {}

   def items(self):
      return self.__dict__["_dict"].items()
   
      
   def __getattr__(self,name):
      try:
         return self.__dict__["_dict"][name]
      except KeyError,e:
         s = "%s has no attribute '%s'" % (self._name,
                                           name)
         raise AttributeError,s
   
   def __setattr__(self,name,value):
      self.__dict__["_dict"][name] = value



# http://groups.google.com/groups?th=5c326de1818bac39
# From: Scott David Daniels (Scott.Daniels@Acm.Org)
# Subject: Re: dynamically naming fields?
# Newsgroups: comp.lang.python
# Date: 2004-04-28 08:40:01 PST 

"""

This class allows me to see data in the object.  Either printing
the object or viewing it as a value with idle or the interactive
interpreter will now display data added to the object.

sample = Data(version=1)  # illustrating fields built at creation

setattr(sample, 'time', [1,3,5])
setattr(sample, 'counter', [12,55,93])

print sample  # illustrate the __repr__ magic to see the data

"""

class Data(object):
     def __init__(self, **kwargs):
         self.__dict__.update(kwargs)
     def __repr__(self):
         return '%s(%s)' % (self.__class__.__name__, ', '.join(
             ['%s=%r' % keyval for keyval in self.__dict__.items()]))

