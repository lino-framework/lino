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


from lino.apps.addrbook.tables import User
from lino.apps.addrbook.tables import Nation, City, Person

from lino.apps.spz.akten import PRB, DLA, Partner, DLS

TABLES=(
        User,Partner,
        PRB, DLA, DLS,
        Nation,
        City)
        
__all__ = [t.__name__ for t in TABLES]
__all__.append('TABLES')
