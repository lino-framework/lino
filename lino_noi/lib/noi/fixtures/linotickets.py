# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
#
# This file is part of Lino Noi.
#
# Lino Noi is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Noi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Noi.  If not, see
# <http://www.gnu.org/licenses/>.


from __future__ import print_function
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import datetime

from unipath import Path

from lino.api import rt

TICKETS = """
#1 [closed] : Wrong layout in Chrome and FF when tab gets activated
#2 [closed] : Deleting a NoteType will delete all Notes with that type (oops!)
#3 [closed] : How to replace the content of a rendered component?
#4 : Documenting Django applications with Sphinx
#5 : Grid is rendered but not visible
#6 : igen demo is broken
#7 [closed] : Code of contacts.Person duplicated in dsbe.Person
#8 : dropTarget and notifyDrop don’t get called
#9 [closed] : mod_wsgi restarts Lino on each request
#10 [closed] : Lino doesn’t like multiple processes
#11 : Django problems when using diamond inheritance
#12 : Communicate with Mozilla Calendar, GroupWise or MS-Outlook
#14 : inheriting verbose_name from abstract Model
#15 [closed] : python-uno and logging
#16 : Lino cannot switch to BSD or LGPL
#17 : UnicodeDecodeError
#18 : responding JSON to a form with file uploads
#19 : values_list() fails on queryset ordered by extra column
#20 : memory exhausted by Apache
#21 : LoadMask for Detail windows
#22 : How to implement MTI child/parent conversion
#23 : writable virtual fields
#24 [closed] : Cheetah not telling me what’s wrong
#25 : makedoc command
#26 : Lino erlaubt es, den job_agent zu löschen
#27 : [closed] How to test Ajax PUT calls
#28 [closed] : Automated data migrations
#29 : How to document several Django apps in one Sphinx tree
#30 [closed] : Developing a Qooxdoo application for a Django server
#31 : The lino.modlib.users module
#32 [closed] : loaddata and processing order of fixtures
#33 [closed] : Qooxdoo Table remains empty
#34 : New Syntax for .dtl files
#35 : makeui also for ExtJS
#36 : AssertionError with Qooxdoo source version in Google Chrome
#37 : Get lino.ui.qx running
#38 [closed]: Fields of Slave GridEditor being submitted to master
#39 : user-specific grid configs
#40 [closed] : Learning Comboboxes (quick insert)
#41 : Moving from Ext JS 3 to 4
#42 [closed]: Wysiwyg Editor
#43 : Neue Anwendung für Lucs Eigenbedarf?
#44 [closed] : Displaying text fields in a grid
#45 [closed]: Make the client launch a WebDAV document
#46 [closed] : multiple doctemplates directories
#47 : CalDAV synchronization
#48 [closed] : One table for all contacts
#49 : cannot inject fields on MTI parents
#50 : initdb causes “foreign key constraint fails”
#51 : Lino and Tryton
#52 : Ext.ensible Calendar Panel
#53 : Lino site on a PHP/MySQL-only host?
#54 [closed] : Report Generator
#55 : Printing tables
#56 : Cannot yet handle known_values in action buttons
#57 : Atomizers
#58 : reuseable ExtJS Windows
#59 : split lino.apps.pcsw to a independant project
#60 : What is a Partner?
#61 : Handling long-running processes
#62 : Authentication using BEID card
#63 : Debts mediation
#64 : Application-specific user manual
#65 : Class-based views
#66 : Content Management à la Lino
#67 : Write a jQuery-based GUI
#68 : Automatically update invoice total when item changed
#69 [closed] : Where to store the version number?
#70 : Lino UI together with Django’s permission system
#71 [closed] : How to make Django and Jinja template machines coexist
#72 : Digesting two scoops of Django
#73 : UI concept for handling OneToOne fields
#74 [closed] : A better name than settings.LINO
#75 : Merge Store into LayoutHandle?
#77 : AJAX API for DELETE and other actions
#78 : eidreader says “Error: No card reader found”
#79 : Change Lino license from GPL to LGPL
#80 : Inkasso-Schulden
#81 : Verträge will ich, nicht Klienten
#82 : Signed Applet Blocked by Security Settings
#83 : User-configurable views
#84 : Laufende Anfragen Eiche
#85 : Diverse Anfragen Gerd
#86 : Questions en cours Marc
#87 : Sammelticket Kalendermodul
#88 : How to blog?
#89 : resolve docs interdependences
#90 : automatically install MergeAction
#91 : Miscellaneous copyright issues
#92 : A Sphinx extension for writing language courses
#93 : Sozialsekretariat
#94 : A Logo for Lino
#95 : Laufende Anfragen Andreas
#96 : How to read Belgian eID cards in 2014 and thereafter?
#97 : choosers with GenericForeignKey in context
#98 : permissions configuration
#99 : How can dd.apps differ from settings.SITE.plugins?
#100 : Ce qui reste à faire pour Châtelet
#101 : Upgrade from ExtJS 3 to 5
#102 : More user-friendly file uploading
#103 : User interface for mobile devices
#104 : Aktive Begleitung weitergeben
#105 : dialog actions can’t be in the toolbar
#106 : Signed Applet Blocked by Security Settings
#107 : How to manage code certificates
#108: Internationalize demo fixtures
#109 : Loading city names into a database
#110 : VSEs mit mehr als einem externen Partner
#111: See who’s logged in
#112 [closed] : Change “PCSW” to “PSWC”
#113 [closed]: Creating invoices in cosi
#114 : Inserting items into a sales invoice
#115 : ChangePassword says “Sorry, dialog action without base_params.mk”
#116 : DavLink fails to get permission
#117 : Add Python 3 support
#118: Backup causes computer to hang after hours of work
#119 : Adding records in grid mode
#120 : Multiple migrations can conflict with each other
#121 : Changements Châtelet Août 2014
#122: Endspurt Bescheinigungen
#123 : Lino Faggio August 2014
"""

from django.conf import settings

def objects():

    Project = rt.modules.tickets.Project
    Ticket = rt.modules.tickets.Ticket
    TicketStates = rt.modules.tickets.TicketStates

    prj = Project(name="Lino")
    yield prj

    settings.SITE.loading_from_dump = True

    for ln in TICKETS.splitlines():
        ln = ln.strip()
        if ln:
            a = ln.split(':')
            state = TicketStates.accepted
            a2 = []
            for i in a:
                if '[closed]' in i:
                    state = TicketStates.closed
                i = i.replace('[closed]', '')
                a2.append(i.strip())
            num = a2[0][1:]
            title = a2[1]

            import lino
            fn = Path(lino.__file__).parent.parent.child('docs', 'tickets')
            fn = fn.child(num + '.rst')
            kw = dict()
            kw.update(created=datetime.datetime.fromtimestamp(fn.ctime()))
            kw.update(modified=datetime.datetime.fromtimestamp(fn.mtime()))
            kw.update(id=int(num), summary=title, project=prj, state=state)
            logger.info("%s %s", fn, kw['modified'])
            kw.update(description=fn.read_file())
            # fd = open(fn)
            yield Ticket(**kw)

            
        
