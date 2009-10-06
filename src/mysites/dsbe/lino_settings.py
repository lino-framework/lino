#coding: utf8
#lino_site.help_url = "http://code.google.com/p/lino/wiki/IgenUserManual"
lino.help_url = "http://lino.saffre-rumma.ee/django/dsbe/userman.html"
lino.title = "dsbe demo"
lino.domain = "dsbe.saffre-rumma.ee"
lino.index_html = u"""
Willkommen auf diesem frühen Prototypen einer Anwendung für den DSBE.
"""

from django.db import models

system = models.get_app('system')
countries = models.get_app('countries')
contacts = models.get_app('contacts')
projects = models.get_app('projects')

from lino.utils import perms

m = lino.add_menu("contacts","~Kontakte")
m.add_action(contacts.Companies())
m.add_action(contacts.Persons())
#m.add_action(contacts.Contacts(),label="~Alle")

m = lino.add_menu("projects","~Projekte")
m.add_action(projects.Projects())

m = lino.add_menu("config","~Konfigurierung",
  can_view=perms.is_staff)
m.add_action(countries.Languages())
#m.add_action(countries.Countries())
m.add_action(contacts.Countries())

#m = lino.add_menu("system","~System")
m.add_action(system.Permissions())
m.add_action(system.Users())
m.add_action(system.Groups())
#m.can_view = perms.is_staff

lino.add_program_menu()

