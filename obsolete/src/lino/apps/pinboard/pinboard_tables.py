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

from lino.adamo.ddl import Schema
from lino.adamo.ddl import DbMainForm

from lino.apps.contacts.contacts_tables import User
from lino.apps.contacts.contacts_tables import Contact
from lino.apps.contacts.contacts_tables import Nation, City
from lino.apps.contacts.contacts_tables import Language

from lino.apps.pinboard.web import Node

from lino.apps.pinboard.events import Event
from lino.apps.pinboard.events import EventType

from lino.apps.pinboard.projects import Project
from lino.apps.pinboard.projects import ProjectStatus

from lino.apps.pinboard.news import NewsItem, NewsItemsReport
from lino.apps.pinboard.news import Newsgroup, NewsgroupsReport

from lino.apps.pinboard.quotes import Author, \
     AuthorEvent, \
     AuthorEventType, \
     Topic, \
     Publication, \
     PubType, \
     PubAuthor, \
     Quote,\
     AuthorsReport,\
     QuotesReport


## from lino.apps.pinboard import babel, web, events, \
##      projects, news, quotes


class PinboardSchema(Schema):
    tableClasses = (
        User,
        Contact,
        Nation,
        City,
        Language,
        ProjectStatus, Project,
        EventType, Event,
        Node,
        Newsgroup, NewsItem, 
        AuthorEventType,
        AuthorEvent,
        Author,
        Topic,
        Publication,
        Quote,
        PubType,
        PubAuthor)



class PinboardMainForm(DbMainForm):
    schemaClass=PinboardSchema
    
    def setupMenu(self):
        m = self.addMenu("pinboard","&Pinboard")
        
        self.addReportItem(m,"authors",tables.AuthorsReport,
                        label="&Authors")
        self.addReportItem(m,"publications",tables.PublicationsReport,
                        label="&Publications")
        self.addReportItem(m,"nodes",tables.NodesReport,
                        label="&Nodes")
        self.addReportItem(m,"news",tables.NewsItemsReport,
                        label="&News")
        self.addReportItem(m,"newsgroups",tables.NewsgroupsReport,
                        label="&Newsgroups")
        
##         m = frm.addMenu("reports","&Reports")
##         m.addItem("s",label="&Static HTML").setHandler(
##             self.writeStaticSite,sess)
        
        self.addProgramMenu()




__all__ = [t.__name__ for t in PinboardSchema.tableClasses]

__all__.append('PinboardSchema')
#__all__.append('Pinboard')
