#coding: latin1
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

from lino.adamo.ddl import *

from lino.schemas.sprl.addrbook import Users
from lino.schemas.sprl.addrbook import Partners
from lino.schemas.sprl.addrbook import Nations
from lino.schemas.sprl.addrbook import Cities
from lino.schemas.sprl.addrbook import Persons

from babel import Languages

from web import Pages

from events import Events
from events import EventTypes

from projects import Projects
from projects import ProjectStati

from news import News
from news import Newsgroups

from quotes import Authors
from quotes import AuthorEvents
from quotes import AuthorEventTypes
from quotes import Topics
from quotes import Publications
from quotes import PubTypes
from quotes import PubByAuth
from quotes import Quotes



TABLES=(
        Users,Partners,
        Nations,
        Cities,
        Languages,
        ProjectStati,Projects,
        EventTypes, Events,
        Pages,
        Newsgroups, News, 
        AuthorEventTypes,
        AuthorEvents,
        Authors,
        Topics, Publications,
        Quotes, PubTypes, PubByAuth)

__all__ = filter(lambda x: x[0] != "_", dir())
