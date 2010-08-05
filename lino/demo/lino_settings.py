#coding: UTF-8
from django.utils.translation import ugettext_lazy as _

#lino_site.help_url = "http://code.google.com/p/lino/wiki/IgenUserManual"
lino.help_url = "http://lino.saffre-rumma.ee"
lino.title = "lino.demo"
lino.domain = "lino-demo.saffre-rumma.ee"
lino.index_html = u"""
Willkommen auf dem ersten Prototypen von Lino-DSBE.
"""

lino.index_html += """<ul>"""
#~ lino.index_html += """<li><a href="#" onclick="Lino.goto_permalink()">permalink with open windows</a></li>"""
lino.index_html += """<li><a href="%s">User manual</a></li>""" % lino.help_url
lino.index_html += """</ul>"""

#~ from django.db import models
from lino.utils import perms

from lino.modlib.system import models as system
#~ system = models.get_app('system')

m = lino.add_menu("contacts",_("~Contacts"))
m.add_action('contacts.Companies')
m.add_action('contacts.Persons')

m = lino.add_menu("projects",_("~Projects"),can_view=perms.is_authenticated)
m.add_action('projects.Projects')
m.add_action('notes.MyNotes')

m = lino.add_menu("config",_("~Configure"),
  can_view=perms.is_staff)
m.add_action('projects.ProjectTypes')
m.add_action('notes.NoteTypes')
#~ m.add_action('properties.Properties')
m.add_action('countries.Languages')
m.add_action('countries.Countries')
m.add_action('countries.Cities')
m.add_action('auth.Permissions')
m.add_action('auth.Users')
m.add_action('auth.Groups')

m = lino.add_menu("explorer",_("E~xplorer"),
  can_view=perms.is_staff)
#m.add_action('properties.PropChoices')
m.add_action('properties.PropValues')
m.add_action('notes.Notes')
#~ m.add_action('links.Links')
m.add_action('contenttypes.ContentTypes')
m.add_action('system.ReportConfigs')

system.add_system_menu(lino)

