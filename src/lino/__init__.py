## Copyright 2003-2006 Luc Saffre

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
import ConfigParser


__docformat__ = 'reStructuredText'

__micro__ = 15

__version__ = "0.6.%d" % __micro__

__author__ = "Luc Saffre <luc.saffre@gmx.net>"

__url__ = "http://lino.berlios.de"

__copyright__ = """\
Copyright (c) 2002-2006 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information.""" 


lino_home = os.path.abspath(
    os.path.join( os.path.dirname(__file__),"..",".."))

rtlib_path = os.path.join(lino_home, "rtlib")

defaults={
    'lino_home' : lino_home,
    'rtlib_path' : rtlib_path,
    }
config = ConfigParser.ConfigParser()
config.add_section('forms')
config.set('forms','wishlist','wx tix cherrypy console')

#config.readfp(open('defaults.cfg'))
config.read( [
    os.path.join(lino_home,'lino.cfg'),
    os.path.expanduser('~/.lino.cfg')])
