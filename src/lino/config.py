## Copyright 2006 Luc Saffre

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
from ConfigParser import ConfigParser, DEFAULTSECT


lino_home = os.path.abspath(
    os.path.join( os.path.dirname(__file__),"..",".."))

rtlib_path = os.path.join(lino_home, "rtlib")

defaults={
    'lino_home' : lino_home,
    'rtlib_path' : rtlib_path,
    }
config = ConfigParser(defaults)
#config.add_section('forms')
#config.set('forms','wishlist','wx tix cherrypy console')

#config.readfp(open('defaults.cfg'))
config.read( [
    os.path.join(lino_home,'lino.cfg'),
    os.path.expanduser('~/.lino.cfg')])

get=config.get
