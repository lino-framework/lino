# coding: latin1

## Copyright Luc Saffre 2003-2005

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
"""


import os
from lino import adamo
from lino.schemas.sprl.sprl import makeSchema
from lino.schemas.sprl import tables 


def startup(populate=True,
            filename=None,
            langs=None,
            **kw):
    
    schema = makeSchema(**kw)
    
    sess = schema.quickStartup(populate=populate,
                               langs=langs,
                               filename=filename )
    
    if populate:
        from lino.schemas.sprl.data import demo1
        demo1.populate(sess)
        
    return sess


# deprecated name for beginSession:
# getDemoDB = beginSession

# deprecated name for startup:
beginSession = startup
