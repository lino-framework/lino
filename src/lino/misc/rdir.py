import os

def show(x):
   print x
   
def rdir(rootPath='.',func=show,filter=None,subpath=None):
   path = rootPath
   if subpath is not None:
      path = os.path.join(rootPath,subpath)
   for fn in os.listdir(path):
      pfn = fn
      if subpath is not None:
         pfn = os.path.join(subpath,fn)
      rpfn = os.path.join(rootPath,pfn)
      if os.path.isdir(rpfn):
         rdir(rootPath,func,filter,pfn)
      else:
         if filter is None or filter(pfn):
            func(pfn)

def rdirlist(path='.',filter=None):
   l = []
   rdir(path,lambda x : l.append(x),filter)
   return l
   

if __name__ == "__main__":
   import sys
   if len(sys.argv) > 1:
      rdir(sys.argv[1])
   else:
      rdir()
