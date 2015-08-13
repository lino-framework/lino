from atelier.fablib import *
setup_from_fabfile(globals(), 'lino_noi')
add_demo_project('lino_noi.projects.team.settings.demo')
# add_demo_project('lino_noi.projects.teamadm.settings')

env.revision_control_system = 'git'
env.cleanable_files = ['docs/api/lino_noi.*']

