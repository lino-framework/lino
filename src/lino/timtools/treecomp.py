raise "not used"
"""
treecomp compares two directory trees and provides different actions
based on this analysis.

USAGE :

treecomp [options...] DIR1 DIR2

- DIR1 and DIR2 are two directories to compare

"""

from lino import __version__

import os, sys, time

DIR1 = None
DIR2 = None

def main(dir1,dir2):
   tree = Tree(dir1,dir2)
   tree.compare()
   print tree

def padl(s,width):
   if len(s) <= width:
      return s.ljust(width)
   return s[:width]

def padtime(secs):
   tm = time.gmtime(secs)
   return time.strftime("%y-%m-%d %H:%M",tm)
##    return "%d-%d-%d %d:%d" % (tm.tm_year,tm.tm_mon,tm.tm_mday,
##                               tm.tm_hour,tm.tm_min)
      

   
class Tree:
   def __init__(self,ldir,rdir):
      self.ldir = ldir
      self.rdir = rdir
      self.nodes = []

   def addNode(self,subdir,name):
      self.nodes.append(Node(self,subdir,name))

   def hasNode(self,subdir,name):
      for node in self.nodes:
         if node.subdir == subdir:
            if node.name == name:
               return True
      return False

   def compare(self,subdir="."):
      print "Inspecting %s..." % subdir
      p = os.path.join(self.ldir,subdir)
      if os.path.isdir(p):
         for fn in os.listdir(p):
            pfn = os.path.join(p,fn)
            if os.path.isdir(pfn):
               self.compare(os.path.join(subdir,fn))
            else:
               self.addNode(subdir,fn)
      p = os.path.join(self.rdir,subdir)
      if os.path.isdir(p):
         for fn in os.listdir(p):
            pfn = os.path.join(p,fn)
            if os.path.isdir(pfn):
               self.compare(os.path.join(subdir,fn))
            elif not self.hasNode(subdir,fn):
               self.addNode(subdir,fn)

   def analyse(self):
      self.toUpdate = []
      self.toDelete = []
                      
   def __str__(self):
      s = "%s compared with %s\n" % (self.ldir,self.rdir)
      s += "%d nodes:\n" % len(self.nodes)
      for node in self.nodes:
         if not node.isSame():
            if node.lstat is not None:
               s += " %10d" % node.lstat.st_size
               s += " " + padtime(node.lstat.st_mtime)
            else:
               s += " " * 26
            s += " " + padl(os.path.join(node.subdir,node.name),20)
            if node.rstat is not None:
               s += " %10d" % node.rstat.st_size
               s += " " + padtime(node.rstat.st_mtime)
            s += "\n"
      s += "\n%d nodes" % len(self.nodes)
            
      return s

class Node:
   def __init__(self,tree,subdir,name):
      self.tree = tree
      self.subdir = subdir
      self.name = name
      try:
         self.lstat = os.stat(os.path.join(tree.ldir,subdir,name))
      except OSError,e:
         self.lstat = None
      try:
         self.rstat = os.stat(os.path.join(tree.rdir,subdir,name))
      except OSError,e:
         self.rstat = None

   def isSame(self):
      if self.rstat is None:
         return (self.lstat is None)
      if self.lstat is None:
         return (self.rstat is None)
      if self.lstat.st_size != self.rstat.st_size:
         return False
      if self.lstat.st_mtime != self.rstat.st_mtime:
         return False
      return True
         


   
   
if __name__ == "__main__":
   from lino.misc import gpl
   print "treecomp version " + __version__ \
         + gpl.copyright('2003','Luc Saffre')

   import getopt
   try:
      opts, args = getopt.getopt(sys.argv[1:],
                                 "?:",
                                 ["help"])

   except getopt.GetoptError:
      print __doc__
      sys.exit(-1)

   if len(args) != 2:
      print __doc__
      sys.exit(-1)

   for o, a in opts:
      if o in ("-?", "--help"):
         print __doc__
         sys.exit()

   main(args[0],args[1])

