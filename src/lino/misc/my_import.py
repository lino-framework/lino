def my_import(name):
   # python-2.2.1/html/lib/built-in-funcs.html
   mod = __import__(name,globals(),locals(),[])
   components = name.split('.')
   for comp in components[1:]:
      mod = getattr(mod, comp)
      
   return mod

