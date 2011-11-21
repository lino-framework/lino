## Copyright 2005 Luc Saffre 

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

raise "not yet"

class Progresser:
    
    def __init__(self,sess,maxval=0):
        self.session = sess
        assert maxval is not None
        self.maxval = maxval
        self.curval = 0
        self.pc = None
        self._done = False
        self.session.toolkit.onJobInit(self)

    def setMaxValue(self,n):
        self.maxval = n

    def getStatus(self):
        return _("Working")
    
    def getLabel(self):
        raise NotImplementedError
    
    def confirmAbort(self):
        return self.session.confirm("Are you sure you want to abort?")
        
    def increment(self,n=1):
        self.curval += n
        if self._done:
            return
        if self.maxval != 0:
            pc = int(100*self.curval/self.maxval)
            if pc == self.pc:
                return
            self.pc = pc
        #self.ui.onJobIncremented(self)
        self.refresh()

    def refresh(self):
        self.session.toolkit.onJobRefresh(self)
        
    def done(self,msg=None,*args,**kw):
        if self._done: return
        if msg is not None:
            msg = self.session.buildMessage(msg,*args,**kw)
        self._done = True
        #if msg is not None:
        #    self._status = msg
        self.pc = 100
        #self.ui.onJobIncremented(self)
        self.session.toolkit.onJobDone(self,msg)
        #if msg is not None and self._label is not None:
        #    msg = self._label+": "+msg
            
    def summary(self):
        #self.notice("%d increments",self.curval)
        pass

    def abort(self,msg=None):
        if msg is None:
            msg = _("Aborted")
##         if msg is not None:
##             self._status = msg
        if not self._done:
            self._done = True
            self.session.toolkit.onJobAbort(self,msg)
            #self.pc = 100
            #self.onInc()
            #self.onDone(msg)
            
        #raise JobAborted(msg)

