## Copyright Luc Saffre 2003-2004.

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import os
import anygui as gui

from lino.ui import console

class Skipper:
   def __init__(self,dir='.'):
      self._data = os.listdir(dir)
      self.rowcount = len(self._data)
      assert self.rowcount > 0
      self.top()
      
   def eof(self):
      return self.recno > -1

   def top(self):
      if self.rowcount > 0:
         self.recno = 0
      else:
         self.recno = -1

   def bottom(self):
      self.recno = self.rowcount - 1

   def skip(self,n=1):
      newRecno = self.recno + n 
      if newRecno >= self.rowcount:
         return False
      if newRecno < 0:
         return False
      self.recno = newRecno
      return True
         

   def row(self):
      return self._data[self.recno]
      
   


class MainForm:
   
   def __init__(self,skipper):
      self.skipper = skipper

   def build(self,win):

      self.filename = gui.TextField()
      win.add(self.filename, top=5, left=5, hstretch=1)

      self.prevButton = gui.Button(text='Prev <<', height=25)
      win.add(self.prevButton,
              left=(self.filename,5),
              top=5,
              hmove=1)

      self.nextButton = gui.Button(text='>> Next', height=25)
      win.add(self.nextButton,
              left=(self.prevButton, 5),
              right=5,
              top=5, hmove=1)


##       grp = gui.RadioGroup(height=25)
##       self.rbn1 = gui.RadioButton(group=grp,text="A")
##       self.rbn2 = gui.RadioButton(group=grp,text="B")
##       self.rbn3 = gui.RadioButton(group=grp,text="C")
##       win.add((self.rbn1,self.rbn2,self.rbn3),
##               top=(self.contents,5),left=5,bottom=5,
##               direction='right',space=10)

      self.statusbar = gui.Label()
      win.add(self.statusbar,
              # top=(self.messages,5),
              bottom=5,
              left=5,right=5, # height=10,
              vstrech=0,
              hstretch=1
              )
      
      self.messages = gui.Label()
      win.add(self.messages,
              # top=(self.contents,5),
              bottom=(self.statusbar,5),
              left=5,right=5, # height=20,
              vstrech=0,
              hstretch=1)
              
      self.contents = gui.TextArea()
      win.add(self.contents,
              top=(self.filename, 5),
              bottom=(self.messages,5),
              left=5, right=5,
              hstretch=1, vstretch=1)




      # filename.text = "readme.txt"


      gui.link(self.nextButton, 'click', self.next)
      gui.link(self.prevButton, 'click', self.prev)
      console.notifier = self.notify
      self.read()

   def notify(self,msg):
      self.messages.text = msg

   def read(self):
      row = self.skipper.row()
      self.filename.text = row
      self.contents.text = file(row).read()
      self.statusbar.text = "row %d of %d" % (self.skipper.recno+1,\
                                              self.skipper.rowcount)
      self.notify("File %s has been read." % row)

   def write(self):
      file(self.filename.text,'w').write(self.contents.text)
   
   def next(self,event):
      if self.skipper.skip(1):
         self.read()
      else:
         console.notify("cannot skip beyond last row")

   def prev(self,event):
      if self.skipper.skip(-1):
         self.read()
      else:
         console.notify("cannot skip beyond first row")

def main():
   skipper = Skipper('.')
   ctrl = MainForm(skipper)
   
   app = gui.Application()
   win = gui.Window(size=(300,200))
   ctrl.build(win)
   app.add(win)
   app.run()


if __name__ == '__main__':

   main()
