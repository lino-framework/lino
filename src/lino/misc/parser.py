#-------------------------------------------------------------------
# parser.py  lino's little parser
#           
#           
# Created:   February 2002
# Author:    Luc Saffre <luc.saffre@gmx.net>
# Copyright: (c) 2002-2004 Luc Saffre
#-------------------------------------------------------------------
#from __future__ import nested_scopes

import re
import lino

from string import replace

def toHTML(s):
    s = replace(s, "&", "&amp;")
    s = replace(s, "<", "&lt;")
    s = replace(s, ">", "&gt;")
    return s

class SimpleParser:
    
    def __init__(self,globals,locals):
        # self.convert = lambda x : x
        self.locals = locals
        self.globals = globals
            
        # print "locals: %s" % repr(self.locals)
        
    def xrepl(self,matchobj):
        # x = matchobj.group(0)
        groups = matchobj.groups()
        assert len(groups) == 1
        x = groups[0]
        a = x.split(" ",1)
        assert len(a) == 2
        # print repr(a)
        # return x
        try:
           res = eval(a[1],self.globals,self.locals)
        except Exception,e:
           return toHTML("%s: %s" % (a[1], e))
        
        if a[0][0] == "%":
           fs = a[0]
           try:
              return fs % res # self.convert(res)
           except Exception,e:
              return toHTML("%s : %s" % (fs,str(e)))
        if a[0][0] == "!":
           return ""


    def parse(self,s1):
        (s2,n) = re.subn(r'\[(.*)\]', self.xrepl, s1)
        # print "%d patterns found." % n
        # print s2
        return s2


class StreamParser:
   def __init__(self,out,globals,locals):
      # self.convert = lambda x : x
      self.out = out
      self.locals = locals
      self.locals["out"] = out
      self.globals = globals
      self.regex  = re.compile(r'\[(.*)\]')
      
   def parse(self,s):
      pos = 0
      match = self.regex.search(s,pos)
      while match != None:

         groups = match.groups()
         assert len(groups) == 1
         cmd = groups[0]

         start = match.start()
         chunk = s[pos:start]
         # print chunk
         self.out.write(chunk)

         # a = cmd.split(" ",1)
         # assert len(a) == 2
         # print repr(a)
         # return x

         if cmd[0] in "%!":
            try:
               res = eval(cmd[2:],self.globals,self.locals)
            except Exception,e:
               self.out.write(toHTML("%s: %s" % (cmd, e)))

            if cmd[0] == "%":
               fs = cmd[0:2]
               try:
                  self.out.write(fs % res)
               except Exception,e:
                  self.out.write(toHTML("%s : %s" % (fs,str(e))))
         else:
            self.out.write("[%s]" % cmd)

         pos = match.end()
         match = self.regex.search(s,pos)
            
      # print s[pos:]
      self.out.write(s[pos:])  
   
