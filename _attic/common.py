class SimpleTool:
   VERSION = "0.2.0"
   AUTHOR = "Luc Saffre"
   EMAIL = "luc.saffre@gmx.net"
   NAME = ""
   USAGE = ""
   SUMMARY = ""

   COPYRIGHT = """\
%(NAME)s version %(VERSION)s
Copyright 2002 %(AUTHOR)s <%(EMAIL)s>
This software is part of TIM Tools.
Distributed under the terms of the GNU General Public License.
See file COPYING for more information.
"""
   def __init__(self):
      print self.COPYRIGHT % self.__class__.__dict__
      self.main()

   def main(self):
      raise "must override"

   def usage(self):
      print self.SUMMARY 
      print self.USAGE 

