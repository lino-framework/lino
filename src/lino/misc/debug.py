debugStack = []
sep = "  "

if True:

   def hello(o,meth):
      pass
   def begin(o,meth):
      pass
   def end():
      pass

else:
   
   def hello(o,meth):
      name = "%s.%s" % (o.__class__.__name__,meth)
      print sep * len(debugStack) + "- " + name

   def begin(o,meth):
      name = "%s.%s" % (o.__class__.__name__,meth)
      print sep * len(debugStack) + "- " + name + ":"
      debugStack.append(name)

   def end():
      name = debugStack.pop()
      print sep * (len(debugStack)+1) + "[end %s]" % name

