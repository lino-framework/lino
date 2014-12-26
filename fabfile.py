from atelier.fablib import *
setup_from_fabfile(globals(), 'lino_noi', 'lino_noi.settings.demo')

env.revision_control_system = 'git'
