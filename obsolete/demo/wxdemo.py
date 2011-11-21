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

"""
starts a GUI application with an adamo database.
Just a proof of concept, far from being usable.
"""

import sys

from lino.ui import console
from lino.schemas.sprl import demo
from lino.ui.wxwindows import run

if __name__ == "__main__":
    console.parse_args(sys.argv)
    sess = demo.beginSession()
    run(sess)
    
