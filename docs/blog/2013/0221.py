"""
Trying to explain the problem that occured today.

Thanks to http://www.dabeaz.com/python/UnderstandingGIL.pdf

"""

from time import sleep
from threading import Thread

class Lino(object):
    
    done = False
    doing = False
        
    def startup(self):
        if self.done:  return
        if self.doing:
            #~ raise Exception("doing")
            return
        self.doing = True
        
        # simulate a big work to do before the `ui` attribute can be added
        print "Starting up",
        for i in range(3): print '.', ; sleep(0.5)
        print '. done'
        self.ui = "yes"
          
        self.done = True
        self.doing = False
        
# A Django process has one global Lino instance in `settings.LINO`.
LINO = Lino() 

# Parameters to play with:
SINGLE_THREADED = False # multi-threaded, e.g. mod_wsgi
#~ SINGLE_THREADED = True # single threaded, e.g. development server
#~ WAIT_BEFORE_ACCESSING_UI = 0
WAIT_BEFORE_ACCESSING_UI = 2


def main(name):
    print "Incoming %s:" % name
    LINO.startup()
    if WAIT_BEFORE_ACCESSING_UI:
        sleep(WAIT_BEFORE_ACCESSING_UI)
    print LINO.ui
    

if __name__ == '__main__':
    print "SINGLE_THREADED is %s, WAIT_BEFORE_ACCESSING_UI is %s" % (SINGLE_THREADED, WAIT_BEFORE_ACCESSING_UI)
    if SINGLE_THREADED: 
        main('request1')
        main('request2')
    else:
        # We simulate what mod_wsgi does:
        # Each incoming http request starts a new thread.
        t1 = Thread(target=main,args=('request1',))
        t2 = Thread(target=main,args=('request2',))
        t1.start(); t2.start()
        t1.join(); t2.join()
    