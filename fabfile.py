from atelier.fablib import *
setup_from_fabfile(globals(), 'lino_noi')

# caution: ``bs3`` uses the same database file as the first. And then,
# bs3 has :attr:`default_user<lino.core.site.Site.default_user>` set
# to 'anonymous'. Which causes it to deactivate both authentication
# and sessions.
add_demo_project('lino_noi.projects.team.settings.demo')
add_demo_project('lino_noi.projects.bs3.settings.demo')
add_demo_project('lino_noi.projects.care.settings.demo')
# no longer used:
# add_demo_project('lino_noi.projects.public.settings.demo')

env.revision_control_system = 'git'
env.cleanable_files = ['docs/api/lino_noi.*']

env.locale_dir = 'lino_noi/lib/noi/locale'
env.languages = "en de fr et".split()

