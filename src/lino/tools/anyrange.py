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


class anyrange:

    def __init__(self, start, stop, step=1):
        self.start = start
        self.stop = stop
        self.step = step
        
    def __contains__(self, obj):
        return self.start <= obj <= self.stop

    def __iter__(self):
        return anyiter(self)

class anyiter:
    def __init__(self,rng):
        self.rng=rng
        self.current=None # rng.start

    def __iter__(self):
        return self
    
    def next(self):
        if self.current is None:
            self.current = self.rng.start
        else:
            self.current += self.rng.step
        if self.current > self.rng.stop:
            raise StopIteration
        return self.current

