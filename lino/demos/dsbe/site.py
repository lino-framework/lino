## Copyright 2009-2011 Luc Saffre
## This file is part of the TimTools project.
## TimTools is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## TimTools is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with TimTools; if not, see <http://www.gnu.org/licenses/>.

from lino import Site as Base

class Site(Base):
  
    title = "Another Lino/DSBE site"
    domain = "dsbe.saffre-rumma.net"
    help_url = "http://lino.saffre-rumma.net/dsbe/index.html"
    
    residence_permit_upload_type = None
    work_permit_upload_type = None
    driving_licence_upload_type = None 
    
    def init_site_config(self,sc):
        #~ print 20100908, "lino_settings.py init_site_config"
        sc.next_partner_id = 200000

    def setup_main_menu(self):
  
        from django.utils.translation import ugettext_lazy as _
        from lino.utils import perms

        from lino import models as system
        from lino.modlib.dsbe import models as dsbe
        
        self.index_html = u"""
        Willkommen auf dem ersten Prototypen von Lino-DSBE.
        """

        self.index_html += """<ul>"""
        #~ lino.index_html += """<li><a href="#" onclick="Lino.goto_permalink()">permalink with open windows</a></li>"""
        self.index_html += """<li><a href="%s">User manual</a></li>""" % self.help_url
        self.index_html += """</ul>"""

        m = self.add_menu("contacts",_("~Contacts"))
        m.add_action('contacts.Companies')
        m.add_action('contacts.Persons')
        m.add_action('dsbe.PersonSearches')

        m = self.add_menu("my",_("~My menu"),can_view=perms.is_authenticated)
        #~ m.add_action('projects.Projects')
        m.add_action('notes.MyNotes')
        m.add_action('uploads.MyUploads')
        m.add_action('dsbe.MyContracts')
        m.add_action('contacts.MyPersons')
        for pg in dsbe.PersonGroup.objects.all():
            m.add_action('contacts.MyPersonsByGroup',label=pg.name,
            params=dict(master_id=pg.pk))

        m = self.add_menu("courses",_("~Courses"),can_view=perms.is_authenticated)
        m.add_action('dsbe.Courses')
        m.add_action('contacts.CourseProviders')
        m.add_action('dsbe.CourseContents')
        m.add_action('dsbe.CourseEndings')
        
        m = self.add_menu("config",_("~Configure"),
          can_view=perms.is_staff)
        #~ m.add_action('projects.ProjectTypes')
        m.add_action('notes.NoteTypes')
        m.add_action('dsbe.ContractTypes')
        m.add_action('dsbe.PersonGroups')
        m.add_action('contacts.CompanyTypes')
        m.add_action('contacts.ContactTypes')
        m.add_action('dsbe.Skills1')
        m.add_action('dsbe.Skills2')
        m.add_action('dsbe.Skills3')
        #~ m.add_action('dsbe.Skills',known_values=dict(type=1))
        #~ m.add_action('dsbe.Skills',known_values=dict(type=2))
        #~ m.add_action('dsbe.Skills',known_values=dict(type=3))
        #~ m.add_action('properties.Properties')
        m.add_action('countries.Languages')
        m.add_action('countries.Countries')
        m.add_action('countries.Cities')
        m.add_action('auth.Permissions')
        m.add_action('auth.Users')
        m.add_action('auth.Groups')
        #~ m.add_action('dsbe.DrivingLicenses')
        m.add_action('dsbe.StudyTypes')
        #~ m.add_action('dsbe.StudyContents')
        m.add_action('dsbe.Activities')
        m.add_action('dsbe.ExclusionTypes')
        m.add_action('dsbe.AidTypes')
        m.add_action('dsbe.ContractEndings')
        #~ m.add_action('dsbe.JobTypes')
        m.add_action('dsbe.ExamPolicies')
        #~ m.add_action('dsbe.CoachingTypes')
        m.add_action('links.LinkTypes')
        m.add_action('uploads.UploadTypes')

        m = self.add_menu("explorer",_("E~xplorer"),
          can_view=perms.is_staff)
        #m.add_action('properties.PropChoices')
        #~ m.add_action('properties.PropValues')
        m.add_action('notes.Notes')
        m.add_action('links.Links')
        m.add_action('dsbe.Exclusions')
        m.add_action('dsbe.Contracts')
        m.add_action('uploads.Uploads')
        m.add_action('dsbe.CourseRequests')
        m.add_action('contenttypes.ContentTypes')

        system.add_site_menu(self)
        

