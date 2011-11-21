## Copyright 2005-2006 Luc Saffre 

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

from lino.console import syscon

STEPS = 2

def work(task):
    sess=task.session
    sess.status("Working hard")
    for n in range(1,STEPS+1):
        sess.error('error message %d',n)
        for h in range(1,STEPS+1):
            sess.warning('warning message %d.%d',n,h)
            for i in range(1,STEPS+1):
                sess.notice('notice message %d.%d.%d',n,h,i)
                for j in range(1,STEPS+1):
                    sess.verbose(
                        'verbose message %d.%d.%d.%d',n,h,i,j)
                    for k in range(1,STEPS+1):
                        sess.debug(
                            'debug message %d.%d.%d.%d.%d',n,h,i,j,k)
                        task.increment()
                        sleep(0.05)
        


if __name__ == "__main__":
    syscon.parse_args()
    syscon.loop(work,"loop() with known maxval",pow(STEPS,5))
    syscon.loop(work,"loop() without known maxval")

    
    
