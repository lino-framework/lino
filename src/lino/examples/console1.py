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

STEPS = 3

def f(withMaxVal):
        
    job = console.job("Demonstrating console.job()")
    
    if withMaxVal:
        job.setMaxValue(pow(STEPS,5))
    
    job.status("Working hard")
    for n in range(STEPS):
        console.error('error message %d',n)
        for h in range(STEPS):
            console.warning('warning message %d.%d',n,h)
            for i in range(STEPS):
                console.notice('notice message %d.%d.%d',n,h,i)
                for j in range(STEPS):
                    console.verbose(
                        'verbose message %d.%d.%d.%d',n,h,i,j)
                    for k in range(STEPS):
                        console.debug(
                            'debug message %d.%d.%d.%d.%d',n,h,i,j,k)
                        job.increment()
                        sleep(0.1)
        
    job.done()


if __name__ == "__main__":
    console.parse_args()
    f(True)
    f(False)
