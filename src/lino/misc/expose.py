
def expose(obj,names=None,cl=None):

   """ Expose the methods of an object to the specified dictionary.
   (I am not sure whether this is exactly compatible to what does the
   interpreter...)

   """
   if names is None:
      names = {}

   if cl is None:
      cl = obj.__class__
      
   for name in cl.__dict__.keys():
      if not hasattr(names,name):
         names[name] = getattr(obj,name)
   
   for base in cl.__bases__:
      names = expose(obj,names,base)

   return names


