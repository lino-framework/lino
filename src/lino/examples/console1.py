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

from time import sleep

from lino.ui import console

def f(maxval):
    
    #p = console.progressbar("Gonna do it", maxval=maxval*3)
    p = console.progress("Gonna do it")
    
    p.title("First part")
    for i in range(maxval):
        console.debug('foo')
        sleep(0.5)
        p.inc()
        sleep(0.5)
        
    p.title("Second part (with longer title)")
    for i in range(maxval):
        sleep(0.5)
        p.inc()
        sleep(0.5)
        
    p.title("Last part")
    for i in range(maxval):
        sleep(0.5)
        p.inc()
        sleep(0.5)
        
    p.done()


if __name__ == "__main__":
    console.parse_args()
    f(3)
