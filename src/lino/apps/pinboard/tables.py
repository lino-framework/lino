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

#from lino.adamo.ddl import *

from lino.apps.addrbook.tables import User
from lino.apps.addrbook.tables import Partner, Nation, City, Person

from babel import Language

from web import Page

from events import Event
from events import EventType

from projects import Project
from projects import ProjectStatus

from news import NewsItem
from news import Newsgroup

from quotes import Author
from quotes import AuthorEvent
from quotes import AuthorEventType
from quotes import Topic
from quotes import Publication
from quotes import PubType
from quotes import PubByAuth
from quotes import Quote



TABLES=(
        User,Partner,
        Nation,
        City,
        Language,
        ProjectStatus,Project,
        EventType, Event,
        Page,
        Newsgroup, NewsItem, 
        AuthorEventType,
        AuthorEvent,
        Author,
        Topic, Publication,
        Quote, PubType, PubByAuth)

#__all__ = filter(lambda x: x[0] != "_", dir())

__all__ = [t.__name__ for t in TABLES]
__all__.append('TABLES')
